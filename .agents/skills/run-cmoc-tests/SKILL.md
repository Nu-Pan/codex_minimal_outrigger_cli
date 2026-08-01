---
name: run-cmoc-tests
description: cmoc リポジトリで、既存の Python 環境と test helper を使って focused test、full pytest、Ruff、mypy を選択・実行・報告する。cmoc の implementation・test 変更後、品質検査、test failure の再現、または test-local Ollama cache を維持した実行に使用する。通常の検査は sandbox 内、GPU integration test だけは限定した command 単位 sandbox escalation で実行する。
---

# cmoc のテストと品質検査を実行する

## 責務を限定する

- この skill は、構築済みのサポート対象開発環境で検査対象を選択し、command を実行して結果を報告する。
- Python 共通の品質ゲートには `python-dev-skill` を併用する。この skill に共通規則を複製しない。
- 通常の検査実行では oracle file を事前に読まず、その内容を実行時に解釈しない。
- test の期待値が仕様上正しいかを判断する意味論的調査は、通常の検査実行と分離する。
- 環境の新規構築、依存関係の追加、または pip の操作は行わない。
- この skill を根拠として、現在の file access mode、作業範囲、または sandbox の書き込み先を広げない。

## repository root と Python を決定する

次の手順で、現在の worktree と main worktree のどちらからも構築済み環境を選択できるようにする。

```bash
cmoc_work_root="$(git rev-parse --show-toplevel)"
cmoc_common_git_dir="$(git -C "$cmoc_work_root" rev-parse --path-format=absolute --git-common-dir)"
cmoc_main_root="$(dirname "$cmoc_common_git_dir")"

if [[ -x "$cmoc_work_root/.venv/bin/python" ]]; then
    cmoc_python="$cmoc_work_root/.venv/bin/python"
elif [[ -x "$cmoc_main_root/.venv/bin/python" ]]; then
    cmoc_python="$cmoc_main_root/.venv/bin/python"
else
    echo "cmoc Python environment is not built" >&2
    exit 1
fi

cd "$cmoc_work_root"
```

`pyproject.toml`、`src`、`oracle/src`、`test`、`test/_ollama_support.py` が worktree root に存在することを確認する。Python version、依存関係、pytest marker、timeout、Ruff、および mypy の機械可読な値は `pyproject.toml` を正本とし、この skill に転記しない。

選択した Python で次の command を実行する。表示された Python version が `project.requires-python` を満たすことと、検査用 module が利用可能なことを確認する。

```bash
"$cmoc_python" -c 'import sys, tomllib; from pathlib import Path; config = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8")); print(sys.version.split()[0], config["project"]["requires-python"])'
"$cmoc_python" -m pytest --version
"$cmoc_python" -m ruff --version
"$cmoc_python" -m mypy --version
```

前提を満たさない場合は検査を開始しない。欠けている path、version、または module を報告し、環境構築が必要な未完了状態として停止する。

## 検査対象を選ぶ

- 明示された test failure の再現では、その node ID を focused test とする。
- implementation の変更では、`test/INDEX.md` の Summary と `rg` による import・symbol の参照検索から、変更した外部挙動または制御ロジックを検証する test file または node ID を選ぶ。
- test helper の変更では、その helper を直接検証する test と、変更した interface の主要な利用側を選ぶ。
- test file に GPU test と非 GPU test が混在する場合は、`gpu_integration` marker で focused test も 2 command に分割する。
- Ruff の first-party 対象は `src`、`oracle/src`、`test` とする。変更中は、この中の変更 path を focused 対象にしてよい。
- mypy の対象は `src`、`oracle/src` とする。`test` は追加しない。

## pytest runner で一時領域と cache を分離する

pytest は、選択した Python から次の repository local interface を使って起動する。

```bash
"$cmoc_python" test/_ollama_support.py run-pytest <pytest arguments>
```

- pytest の隔離だけを理由として run 固有の `TMPDIR` を設定せず、pytest の case/session 用一時領域を使う。
- `TMPDIR`、`TMP`、または `TEMP` が既に設定されている場合も、この runner を使う。runner は pytest の一時領域を保ったまま、test-local Ollama cache を run 固有の一時 path から分離する。
- cache の環境変数名、schema version、OS user namespacing、root path を skill 内で組み立てない。
- archive、binary、model を手動配置せず、cache hit、cache miss、materialize、および publish を test helper に任せる。
- cache 状態、GPU 可視性、または既存 Ollama service を事前判定しない。選択した pytest command から helper を起動する。

## 変更中の検査を実行する

1. 非 GPU の focused test を repository 所定の sandbox 内で実行する。
2. GPU の focused test は、後述する command 単位 sandbox escalation で実行する。
3. 変更した first-party path に対して、`python-dev-skill` に従う Ruff check、Ruff format check、および必要な mypy を実行する。
4. failure を再現する場合は、最小の node ID から始め、実行環境、外部 executable、timeout、cache/helper、test assertion のどこで失敗したかを分類する。

非 GPU focused test の基本形を次に示す。

```bash
"$cmoc_python" test/_ollama_support.py run-pytest <test paths or node IDs> -ra -m "not gpu_integration"
```

## fresh な完了ゲートを実行する

realization implementation または realization test を変更した場合は、最後の変更後に次の全 command を fresh に実行する。過去の実行結果や focused test だけで完了扱いにしない。

```bash
"$cmoc_python" -m ruff check src oracle/src test
"$cmoc_python" -m ruff format --check src oracle/src test
"$cmoc_python" -m mypy src oracle/src
"$cmoc_python" test/_ollama_support.py run-pytest test -ra -m "not gpu_integration"
"$cmoc_python" test/_ollama_support.py run-pytest test -ra -m gpu_integration
```

pytest command には、`python-dev-skill` が定める Python development mode と `ResourceWarning` 検査を適用する。上から 4 番目までは repository 所定の sandbox 内で実行し、最後の GPU command だけを sandbox escalation の対象とする。

文書と skill だけを変更した場合は、変更箇所の参照、用語、path、command、および project 設定との整合性を検査する。Python helper または test を変更した場合は、focused test と上記の完了ゲートを実行する。

## GPU integration test だけを sandbox 外で実行する

- `gpu_integration` を選択する pytest command は sandbox 内で試行せず、最初の実行から command 単位 sandbox escalation を要求する。
- Codex の unified exec tool では、その command にだけ `sandbox_permissions=require_escalated` を指定する。
- justification には、test-local Ollama が WSL host の GPU device を使用するために必要であることを明記する。
- escalation は pytest runner command と descendant process に限定する。agent call 全体へ `danger-full-access` を指定せず、prefix allow rule の作成または永続化を要求しない。
- escalation が利用不能、拒否、または review failure になった場合は停止する。同じ test を sandbox 内で実行せず、GPU test と full test を未完了として報告する。
- sandbox 外の test が GPU 利用不能を理由に skip した場合は、skip reason を報告し、GPU test と full test を未完了として扱う。
- escalated test が作成した case-local 一時ファイル、cache、および GPU device 以外の host resource を探索または操作しない。

## 結果を報告する

結果では、次の情報を区別して報告する。

- 実行した command と終了状態
- Ruff check、Ruff format check、mypy の結果
- sandbox 内の focused test と非 GPU full pytest の結果
- escalated GPU focused test と GPU full pytest の結果
- test 数、skip 数、および skip reason
- Real Codex CLI を使う test の実行または skip
- cache hit/miss など、出力から確認できた実行上の原因
- full test が fresh に完了したか、未完了ならその理由

失敗した期待値を変更すべきかという意味論的判断は、実行上の原因分類と同じ作業として扱わない。必要な場合は別の仕様調査として明示する。
