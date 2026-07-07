import subprocess
from pathlib import Path

import pytest

import commons.runtime_ollama as ollama_module
from commons.runtime_errors import CmocError


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

    def fake_run_ollama(
        executable: Path, args: list[str]
    ) -> subprocess.CompletedProcess[str]:
        commands.append(args)
        returncode = next(show_iter) if args[0] == "show" else 0
        return subprocess.CompletedProcess([str(executable), *args], returncode, "", "")

    monkeypatch.setattr(ollama_module, "_run_ollama", fake_run_ollama)
    monkeypatch.setattr(ollama_module, "_load_ollama_model", loaded.append)

    ollama_module._ensure_ollama_model(Path("ollama"), "model")

    assert commands == expected_commands
    assert loaded == ["model"]
