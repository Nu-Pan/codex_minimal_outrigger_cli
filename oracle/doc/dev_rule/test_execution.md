# cmoc の test・品質検査実行手順

## 責務境界

- この文書は、構築済みの cmoc 開発環境で test と品質検査を選択、実行、完了判定、および報告する手順を定める。
- realization test が満たすべき意味上の要件は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` を正本とする。
- Python 環境の新規構築、依存関係の追加、および pip 操作は、`{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` を正本とする。
- この手順の実行中に環境を新規構築したり、依存関係を追加したり、pip を実行したりしてはいけない。
- この手順を根拠に、agent call の file access mode、作業範囲、または sandbox の書き込み先を広げてはいけない。

## repository root と Python interpreter を決定する

現在の worktree を検査対象とし、Python interpreter は現在の worktree、main worktree の順に構築済み環境から選択する。

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

- linked worktree に `.venv` がない場合は、main worktree の `.venv` を使用してよい。
- main worktree の interpreter を使用する場合も、command の cwd と検査対象は現在の worktree とする。
- システム Python または別 repository の仮想環境へ fallback してはいけない。

## 構築済み環境を preflight する

検査開始前に、現在の worktree に次の path が存在することを確認する。

- `pyproject.toml`
- `src`
- `oracle/src`
- `test`
- `test/_ollama_support.py`

Python version、依存関係、pytest marker、timeout、Ruff、および mypy の機械可読な設定値は `pyproject.toml` を正本とする。選択した interpreter で次の command を実行する。

```bash
"$cmoc_python" -c 'import sys, tomllib; from pathlib import Path; config = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8")); print(sys.version.split()[0], config["project"]["requires-python"])'
"$cmoc_python" -m pytest --version
"$cmoc_python" -m ruff --version
"$cmoc_python" -m mypy --version
```

- 表示された Python version が `project.requires-python` を満たすことを確認する。
- path、version、または module が不足している場合は検査を開始しない。
- 不足している前提を具体的に報告し、環境構築が必要な未完了状態として停止する。
- preflight の失敗を回避するために、その場で package を導入してはいけない。

## focused test と検査対象を選択する

変更中の検査対象は、変更した外部挙動または制御ロジックを直接検証する最小範囲から選ぶ。

- 明示された test failure を再現する場合は、その node ID を focused test とする。
- repository local skill の metadata を変更した場合は、`test/test_skill_metadata.py` を focused test とする。
- implementation の変更では、`test/INDEX.md` の routing 情報と `rg` による import・symbol の参照検索から、対応する test file または node ID を選ぶ。
- test helper の変更では、helper を直接検証する test と、変更した interface の主要な利用側を選ぶ。
- test file に GPU test と非 GPU test が混在する場合は、`gpu_integration` marker で別 command に分ける。
- Ruff の first-party 対象は `src`、`oracle/src`、`test` とし、変更中は変更 path に絞ってよい。
- mypy の対象は `src` と `oracle/src` とし、`test` を追加しない。
- 文書だけを変更した場合は、参照、用語、path、command、および project 設定との整合性を検査する。

## repository local pytest runner を使用する

cmoc の pytest は、focused test と full test、GPU test と非 GPU test のいずれでも、選択した Python から次の interface を使用して起動する。

```bash
"$cmoc_python" test/_ollama_support.py run-pytest <pytest arguments>
```

- `python -m pytest` または `pytest` を直接使用して、この runner を迂回してはいけない。
- pytest の隔離だけを理由として run 固有の `TMPDIR` を設定してはいけない。
- `TMPDIR`、`TMP`、または `TEMP` が設定済みの場合も runner を使用する。
- cache の環境変数名、schema version、OS user namespacing、または root path を呼び出し側で組み立ててはいけない。
- archive、binary、model の配置、cache hit、cache miss、materialize、および publish は test helper に任せる。
- cache 状態、GPU 可視性、または既存 Ollama service を pytest command より前に独自判定してはいけない。

## Python development mode と ResourceWarning 検査を適用する

focused test と full test の全 pytest command で、runner が起動する Python process に development mode と `ResourceWarning` のエラー化を適用する。

```bash
PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
    "$cmoc_python" test/_ollama_support.py run-pytest <pytest arguments>
```

- `ResourceWarning` 以外の全 warning を、この手順だけを根拠に一律でエラー化してはいけない。
- 第三者 library の warning を除外する場合は、実際の出力を根拠に category、module、message の最小範囲へ限定し、理由を記録する。
- project code の resource leak を warning filter、広範な pytest 設定、または環境変数の解除で隠してはいけない。

## 変更中の検査を実行する

変更中は、非 GPU の focused test を repository 所定の sandbox 内で実行する。

```bash
PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
    "$cmoc_python" test/_ollama_support.py run-pytest \
    <test paths or node IDs> -ra -m "not gpu_integration"
```

- GPU の focused test は、後述する command 単位 sandbox escalation で別に実行する。
- 変更した first-party path に Ruff check と Ruff format check を実行する。
- `src` または `oracle/src` の変更には、変更 module と主要な利用側に mypy を実行する。
- failure は、実行環境、外部 executable、timeout、cache または helper、test assertion のどこで発生したかを分類する。

## fresh な完了ゲートを実行する

`src`、`oracle/src`、または `test` の Python code を変更した場合は、最後の変更後に次の全 command を現在の worktree で fresh に実行する。

```bash
"$cmoc_python" -m ruff check src oracle/src test
"$cmoc_python" -m ruff format --check src oracle/src test
"$cmoc_python" -m mypy src oracle/src
PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
    "$cmoc_python" test/_ollama_support.py run-pytest \
    test -ra -m "not gpu_integration"
PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
    "$cmoc_python" test/_ollama_support.py run-pytest \
    test -ra -m gpu_integration
```

- 過去の実行結果、focused test、または一部 command の成功だけで完了扱いにしてはいけない。
- full test は、非 GPU full pytest と GPU full pytest の和集合とする。
- Ruff check、Ruff format check、mypy、および非 GPU full pytest は repository 所定の sandbox 内で実行する。
- 最後の GPU full pytest だけを command 単位 sandbox escalation の対象とする。

## GPU test だけを command 単位で sandbox escalation する

- `gpu_integration` を選択する pytest runner command とその descendant process だけに command 単位 sandbox escalation を要求してよい。
- test-local Ollama が host の GPU device と実推論を使用するための例外とし、sandbox 内での事前失敗を要求しない。
- GPU command は最初の実行から escalation を要求し、同じ command を先に sandbox 内で実行してはいけない。
- escalation の理由には、test-local Ollama が host の GPU device を使用する必要があることを明記する。
- Ruff、mypy、または `gpu_integration` 以外の pytest を sandbox 外で実行してはいけない。
- agent call 全体へ `danger-full-access` を指定してはいけない。
- GPU test のための prefix allow rule を作成または永続化してはいけない。
- cache の利用、再構築、または永続化を理由に escalation の範囲を広げてはいけない。
- escalated command が作成した test-local の一時 file と cache、および GPU device 以外の host resource を探索または操作してはいけない。

escalation が利用不能、拒否、または review failure になった場合は、その時点で停止する。

- 同じ GPU test を sandbox 内で再実行してはいけない。
- GPU test と full test を未完了として報告する。
- sandbox 外の GPU test が GPU 利用不能を理由に skip した場合も、GPU test と full test を未完了として扱う。
- skip reason をそのまま報告する。

## 完了を判定する

Python code 変更の完了には、fresh な完了ゲートの全 command が成功し、必要な外部経路が実際に検証されていることを要求する。

- GPU test の未実行、失敗、または GPU 利用不能による skip がある場合は full test 未完了とする。
- Real Codex CLI を必要とする test が環境不足で skip され、必要な実経路を検証できなかった場合は full test 未完了とする。
- その他の skip は reason と対象を確認し、今回必要な検証を欠く場合は未完了とする。
- test または品質検査の失敗を残したまま完了扱いにしてはいけない。
- development mode と `ResourceWarning` 検査だけですべての resource leak を検出できるとは保証しない。

## 実行結果を報告する

結果では、次の情報を区別して報告する。

- 使用した worktree root と Python interpreter
- preflight の結果
- 実行した command と各終了状態
- Ruff check、Ruff format check、および mypy の結果
- sandbox 内の focused test と非 GPU full pytest の結果
- escalated GPU focused test と GPU full pytest の結果
- test 数、skip 数、および skip reason
- Real Codex CLI を使う test の実行または skip
- cache hit または cache miss など、出力から確認できた実行上の原因
- full test が fresh に完了したか、未完了ならその理由

失敗した期待値を変更すべきかという意味上の判断は、実行上の原因分類と同じ作業として扱わない。必要な場合は、別の仕様調査として明示する。
