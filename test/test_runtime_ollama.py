import subprocess
from pathlib import Path

import pytest

import commons.runtime_ollama as ollama_module
from commons.runtime_errors import CmocError


class _Response:
    def __init__(self, body: bytes, status: int = 200) -> None:
        self.body = body
        self.status = status

    def read(self) -> bytes:
        return self.body

    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *_args: object) -> None:
        return None


# {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
@pytest.mark.parametrize(
    ("service_changed", "process_matches", "restart_expected"),
    [(True, True, True), (False, False, True), (False, True, False)],
)
def test_ensure_ollama_service_restarts_only_when_active_service_needs_repair(
    monkeypatch: pytest.MonkeyPatch,
    service_changed: bool,
    process_matches: bool,
    restart_expected: bool,
) -> None:
    calls: list[list[str]] = []
    executable = Path("/home/user/.cmoc/ollama/bin/ollama")

    def fake_systemctl(args: list[str]) -> subprocess.CompletedProcess[str]:
        calls.append(args)
        return subprocess.CompletedProcess(["systemctl", *args], 0, "", "")

    monkeypatch.setattr(
        ollama_module, "_write_ollama_service_file", lambda path: service_changed
    )
    monkeypatch.setattr(ollama_module, "_run_systemctl", fake_systemctl)
    monkeypatch.setattr(ollama_module, "_service_active", lambda: True)
    monkeypatch.setattr(
        ollama_module, "_service_process_matches", lambda path: process_matches
    )

    ollama_module._ensure_ollama_service(executable)

    expected = [["daemon-reload"], ["enable", "--now", "cmoc-ollama"]]
    if restart_expected:
        expected.append(["restart", "cmoc-ollama"])
    assert calls == expected


def test_write_ollama_service_uses_home_specifier_for_executable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home with spaces"
    executable = home / ".cmoc" / "ollama" / "bin" / "ollama"
    service = home / ".config" / "systemd" / "user" / "cmoc-ollama.service"
    monkeypatch.setattr(ollama_module, "_ollama_service_file", lambda: service)

    assert ollama_module._write_ollama_service_file(executable)

    assert "ExecStart=%h/.cmoc/ollama/bin/ollama serve" in service.read_text()


def test_verify_ollama_service_rejects_missing_main_pid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    executable = Path("/home/user/.cmoc/ollama/bin/ollama")

    monkeypatch.setattr(ollama_module, "_service_active", lambda: True)
    monkeypatch.setattr(ollama_module, "_service_main_pid", lambda: None)

    with pytest.raises(CmocError):
        ollama_module._verify_ollama_service(executable)


@pytest.mark.parametrize("status", [400, 404, 500])
def test_verify_ollama_service_rejects_non_2xx_http_status(
    monkeypatch: pytest.MonkeyPatch, status: int
) -> None:
    executable = Path("/home/user/.cmoc/ollama/bin/ollama")

    class Response:
        def __enter__(self) -> "Response":
            self.status = status
            return self

        def __exit__(self, *args: object) -> None:
            return None

    clock = iter([0.0, 0.0, 2.0])
    monkeypatch.setattr(ollama_module, "_service_active", lambda: True)
    monkeypatch.setattr(ollama_module, "_service_main_pid", lambda: 10)
    monkeypatch.setattr(
        ollama_module, "_process_argv_uses_executable", lambda pid, path: True
    )
    monkeypatch.setattr(
        ollama_module, "_listener_matches_service", lambda pid, path: True
    )
    monkeypatch.setattr(
        ollama_module.urllib.request, "urlopen", lambda *args, **kwargs: Response()
    )
    monkeypatch.setattr(ollama_module.time, "monotonic", lambda: next(clock))
    monkeypatch.setattr(ollama_module.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(ollama_module, "_OLLAMA_START_TIMEOUT_SEC", 1.0)

    with pytest.raises(CmocError, match="接続できませんでした"):
        ollama_module._verify_ollama_service(executable)


def test_ollama_listener_must_be_expected_service_process(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    executable = Path("/home/user/.cmoc/ollama/bin/ollama")

    monkeypatch.setattr(ollama_module, "_ollama_listener_process_ids", lambda: {20, 30})
    monkeypatch.setattr(
        ollama_module, "_process_is_descendant", lambda pid, main: pid == 20
    )
    monkeypatch.setattr(
        ollama_module,
        "_process_argv_uses_executable",
        lambda pid, path: path == executable and pid == 30,
    )

    assert not ollama_module._listener_matches_service(10, executable)

    monkeypatch.setattr(
        ollama_module,
        "_process_argv_uses_executable",
        lambda pid, path: path == executable and pid == 20,
    )

    assert ollama_module._listener_matches_service(10, executable)


@pytest.mark.parametrize(
    ("show_codes", "expected_commands"),
    [
        ([0], [["show", "model"]]),
        ([1, 0], [["show", "model"], ["pull", "model"], ["show", "model"]]),
    ],
)
def test_ensure_ollama_model_loads_after_store_is_ready(
    monkeypatch: pytest.MonkeyPatch,
    show_codes: list[int],
    expected_commands: list[list[str]],
) -> None:
    commands: list[list[str]] = []
    show_iter = iter(show_codes)
    loaded: list[str] = []
    verified: list[str] = []

    def fake_run_ollama(
        executable: Path, args: list[str]
    ) -> subprocess.CompletedProcess[str]:
        commands.append(args)
        returncode = next(show_iter) if args[0] == "show" else 0
        return subprocess.CompletedProcess([str(executable), *args], returncode, "", "")

    monkeypatch.setattr(ollama_module, "_run_ollama", fake_run_ollama)
    monkeypatch.setattr(ollama_module, "_verify_ollama_gpu", verified.append)
    monkeypatch.setattr(ollama_module, "_load_ollama_model", loaded.append)

    ollama_module._ensure_ollama_model(Path("ollama"), "model")

    assert commands == expected_commands
    assert loaded == ["model"]
    assert verified == ["model"]


def test_verify_ollama_gpu_accepts_runtime_vram(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = _Response(b'{"models":[{"name":"model","size_vram":1}]}')
    monkeypatch.setattr(
        ollama_module.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: response,
    )
    ollama_module._verify_ollama_gpu("model")


@pytest.mark.parametrize(
    "body", [b'{"models":[]}', b'{"models":[{"name":"model","size_vram":0}]}']
)
def test_verify_ollama_gpu_rejects_unconfirmed_runtime(
    monkeypatch: pytest.MonkeyPatch, body: bytes
) -> None:
    response = _Response(body)
    monkeypatch.setattr(
        ollama_module.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: response,
    )
    with pytest.raises(CmocError, match="GPU 推論を確認できませんでした"):
        ollama_module._verify_ollama_gpu("model")
