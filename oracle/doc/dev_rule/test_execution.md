# cmoc の test・品質検査実行手順

## 責務境界

この文書は、構築済みの cmoc 開発環境における test と品質検査の選択・実行・完了判定・報告を定める。関連する要件は、次の正本に従う。

- realization test が満たすべき意味上の要件は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「cmoc テスト実装規約」を正本とする。
- 型注釈と docstring の意味上の品質要件は、`{{cmoc-root}}/oracle/doc/dev_rule/coding_rule.md` の「型ヒント」と「docstring」が所有する。
- Python 環境の新規構築、依存関係の追加、および pip 操作は、`{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` の「cmoc 開発環境」を正本とする。

この手順の実行中に環境を新規構築したり、依存関係を追加したり、pip を実行したりしてはいけない。また、この手順を根拠に、agent call の file access mode、作業範囲、または sandbox の書き込み先を広げてはいけない。

## 通常検証と追加検証を選択する

この選択方針は、agent による開発時の focused test、全件検証、および fresh な完了ゲートに適用する。製品の通常機能としての Codex CLI 呼び出しは対象としない。

通常検証は、Real Codex CLI を使わない test と所定の品質検査から成る。Codex CLI 呼び出しを伴う制御の検証には Fake Codex CLI を使用する。通常検証に属する test の全件検証を、本書では full test と呼ぶ。

実経路統合テストを含む Real Codex CLI を使う test は、その実行をユーザーが明示的に指示した場合に限り、通常検証へ追加する。一般的なテスト・検証の依頼や agent 独自の判断は、この明示指示に含めない。通常検証の失敗や Codex CLI の更新を理由に、自動で Real Codex CLI を使う test を実行してはいけない。

## repository root と Python interpreter を決定する

検査対象は現在の worktree とする。Python interpreter は、現在の worktree、main worktree の順に、構築済み環境から選択する。

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

`pyproject.toml` は、現在の検査に使用する機械可読な realization 設定とする。選択した interpreter で次の command を実行する。

```bash
"$cmoc_python" -c 'import sys, tomllib; from pathlib import Path; config = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8")); print(sys.version.split()[0], config["project"]["requires-python"])'
"$cmoc_python" -m pytest --version
"$cmoc_python" -m ruff --version
"$cmoc_python" -m mypy --version
```

表示された Python version が `project.requires-python` を満たすことを確認する。必要な path、version、または module が揃わない場合は、環境構築が必要な未完了状態として検査を開始せず、不足している前提を具体的に報告する。

## focused test と検査対象を選択する

変更中の検査対象は、本書の「通常検証と追加検証を選択する」で定める実行対象の中から、変更した外部挙動または制御ロジックを直接検証する最小範囲を選ぶ。

- 明示された test failure を再現する場合は、その node ID を focused test とする。
- repository local skill の metadata を変更した場合は、`test/test_skill_metadata.py` を focused test とする。
- implementation の変更では、`rg` による import・symbol の参照検索と test 本文から、対応する test file または node ID を選ぶ。
- test helper の変更では、helper を直接検証する test と、変更した interface の主要な利用側を選ぶ。
- test file に実経路統合テストとそれ以外の test が混在する場合は、`real_path_integration` marker で別 command に分ける。
- 以下の pytest command で、marker だけでは Real Codex CLI を使う test を通常検証から除外できない場合は、test paths または node ID で対象を調整する。full test では、通常検証に属する test を全件含める。
- Ruff の first-party 対象は `src`、`oracle/src`、`test` とし、変更中は変更 path に絞ってよい。
- mypy の対象は `src` と `oracle/src` とし、`test` を追加しない。
- 文書だけを変更した場合は、参照、用語、path、command、および project 設定との整合性を検査する。

## 選択した Python interpreter で pytest を実行する

cmoc の pytest は、focused test と full test、実経路統合テストとそれ以外の test のいずれでも、選択した Python から起動する。

```bash
"$cmoc_python" -m pytest <pytest arguments>
```

- `pytest` executable を直接起動して、選択した interpreter を迂回してはいけない。
- pytest の隔離だけを理由として run 固有の `TMPDIR` を設定してはいけない。
- `TMPDIR`、`TMP`、または `TEMP` が設定済みの場合も、選択した interpreter から pytest を起動する。

## Python development mode と ResourceWarning 検査を適用する

通常検証と追加検証の全 pytest command で、pytest を実行する Python process に development mode と `ResourceWarning` のエラー化を適用する。

```bash
PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
    "$cmoc_python" -m pytest <pytest arguments>
```

- `ResourceWarning` 以外の全 warning を、この手順だけを根拠に一律でエラー化してはいけない。
- 第三者 library の warning を除外する場合は、実際の出力を根拠に category、module、message の最小範囲へ限定し、理由を記録する。
- project code の resource leak を warning filter、広範な pytest 設定、または環境変数の解除で隠してはいけない。

## 変更中の検査を実行する

変更中は、通常検証の focused test を repository 所定の sandbox 内で実行する。

```bash
PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
    "$cmoc_python" -m pytest \
    <test paths or node IDs> -ra -m "not real_path_integration"
```

- 追加検証の対象に選ばれた実経路統合テストは、本書の「実経路統合テストを実行する」に従って別 command で実行する。
- 変更した first-party path に Ruff check と Ruff format check を実行する。
- `src` または `oracle/src` の変更には、変更 module と主要な利用側に mypy を実行する。
- failure は、実行環境、外部 executable、model provider、quota、timeout、helper、または test assertion のどこで発生したかを分類する。

## fresh な完了ゲートを実行する

`src`、`oracle/src`、`test` の Python code、Ruff・mypy・pytest の設定、または開発依存関係を変更した場合は、最後の変更後に次の通常検証の全 command を現在の worktree で fresh に実行する。

```bash
"$cmoc_python" -m ruff check src oracle/src test
"$cmoc_python" -m ruff format --check src oracle/src test
"$cmoc_python" -m mypy src oracle/src
PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
    "$cmoc_python" -m pytest \
    test -ra -m "not real_path_integration"
```

- 過去の実行結果、focused test、または一部 command の成功だけで完了扱いにしてはいけない。
- 追加検証を指示されている場合は、その検証も最後の変更後に fresh に実行する。
- Ruff check、Ruff format check、mypy、および全 pytest command は repository 所定の sandbox 内で実行する。

## 実経路統合テストを実行する

本書の「通常検証と追加検証を選択する」に従って追加検証の対象となった実経路統合テストを、次の別 command で実行する。変更中の focused test では `test` を対応する test paths または node ID に置き換え、fresh な完了ゲートでは実経路統合テストの全件を対象とする。

```bash
PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
    "$cmoc_python" -m pytest \
    test -ra -m real_path_integration
```

- 実経路統合テストの成立条件、専用のモデル設定、quota、および model provider の扱いは、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「実経路統合テスト」を正本とする。
- pytest command から具体的な model provider またはモデル名を上書きしてはならない。

## 完了を判定する

fresh な完了ゲートの対象となる変更は、通常検証の全 command が成功し、明示指示による追加検証がある場合はその検証も成功した場合に限り完了とする。実経路統合テストを追加した場合は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「実経路統合テスト」が定める検証要件も満たす必要がある。

- 明示指示がなく Real Codex CLI を使う test が実行対象外の場合、その未実行は通常検証や作業の未完了理由にしない。
- 指示された追加検証に未実行、失敗、または環境不足による skip がある場合は、追加検証と作業を未完了とする。通常検証の成功で代替してはいけない。
- その他の skip は reason と対象を確認し、今回必要な検証を欠く場合は未完了とする。
- test または品質検査の失敗を残したまま完了扱いにしてはいけない。
- development mode と `ResourceWarning` 検査だけで、すべての resource leak を検出できる保証はない。

## 実行結果を報告する

結果では、次の情報を区別して報告する。

- 使用した worktree root と Python interpreter
- preflight の結果
- 実行した command と各終了状態
- Ruff check、Ruff format check、および mypy の結果
- 通常検証の focused test と full test の結果
- Real Codex CLI を使う test に対する明示指示の有無と、指示された追加検証の範囲
- 追加検証の実行有無と結果。実経路統合テストでは focused test と full pytest の結果を区別する
- test 数、skip 数、および skip reason
- model provider、quota、timeout など、出力から確認できた実行上の原因
- 通常検証と追加検証それぞれが fresh に完了したか、および作業の完了判定。未完了ならその理由

明示指示がない場合、Real Codex CLI を使う test は「実行対象外（明示指示なし）」と報告し、実行成功や環境不足による skip と区別する。指示された追加検証は、成功、失敗、未実行、または環境不足による skip とその理由を報告する。Fake Codex CLI だけによる成功を、Real Codex CLI との互換性や実経路の検証済みという結果として報告してはいけない。

test が失敗したとき、期待値を変更すべきかという意味上の判断は、実行上の原因分類とは別に扱う。この判断が必要な場合は、別の仕様調査であることを明示する。
