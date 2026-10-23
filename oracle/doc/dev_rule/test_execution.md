# cmoc の test・品質検査実行手順

## 責務境界

この文書は、構築済みの cmoc 開発環境における test と品質検査の選択・起動場所・実行・完了判定・報告を定める。VS Code のテストタブ用の pytest 連携設定と操作手順も本書で扱う。関連する要件は、次の正本に従う。

- realization test が満たすべき意味上の要件は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「cmoc テスト実装規約」を正本とする。
- Codex CLI の sandbox・承認設定と command 単位 sandbox escalation の共通契約は、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「Codex CLI 引数による設定上書き」「Codex CLI sandbox」「command 単位の sandbox 外実行」を正本とする。
- 型注釈と docstring の意味上の品質要件は、`{{cmoc-root}}/oracle/doc/dev_rule/coding_rule.md` の「型ヒント」と「docstring」が所有する。
- Python 環境の新規構築、依存関係の追加、および pip 操作は、`{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` の「cmoc 開発環境」を正本とする。

この手順の実行中に環境を新規構築したり、依存関係を追加したり、pip を実行したりしてはいけない。また、この手順を根拠に、agent call の file access mode、作業範囲、または既定 sandbox の書き込み先を広げてはいけない。追加検証の command の起動場所に限り、本書の「Real Codex CLI を使う追加検証を起動する」で定める例外を適用する。

## 通常検証と追加検証を選択する

この選択方針は、agent による開発時の focused test、全件検証、および fresh な完了ゲートに適用する。製品の通常機能としての Codex CLI 呼び出しは対象としない。

通常検証は、Real Codex CLI を使わない test と所定の品質検査から成る。Codex CLI 呼び出しを伴う制御の検証には Fake Codex CLI を使用する。通常検証に属する test の全件検証を、本書では full test と呼ぶ。

実経路統合テストを含む Real Codex CLI を使う test は、その実行をユーザーが明示的に指示した場合に限り、通常検証へ追加する。一般的なテスト・検証の依頼や agent 独自の判断は、この明示指示に含めない。通常検証の失敗や Codex CLI の更新を理由に、自動で Real Codex CLI を使う test を実行してはいけない。

選択した追加検証は通常検証と別 command に分け、本書の「Real Codex CLI を使う追加検証を起動する」に従う。

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

## VS Code のテストタブから実行する

WSL 上の既存ワークスペースで Microsoft の Python 拡張を使い、テストタブから pytest の探索、個別・ファイル単位・全件の実行、および失敗箇所の確認ができる構成にする。既定の実行対象は、本書の「通常検証と追加検証を選択する」が定める通常検証に属する test（以下、この節では通常テスト）とする。

pytest とテスト配置の根拠は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「基本」、実経路統合テストの意味と marker の根拠は、同文書の「実経路統合テスト」「用語と選択」を参照する。

### ワークスペースと Python interpreter を確認する

1. `{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` の「基本環境」に定める既存の `codex_minimal_outrigger_cli.code-workspace` を WSL 接続で開く。拡張機能ビューの WSL 側で Python 拡張が有効であることを確認する。
2. 対象の workspace folder が現在の worktree root を指し、`${workspaceFolder}` がその path に解決されることを確認する。
3. 本書の「repository root と Python interpreter を決定する」に従って interpreter を決め、コマンドパレットの `Python: Select Interpreter` でその path を選択して確認する。現在の worktree と main worktree の選択条件、cwd、および検査対象は同節に従う。`python.defaultInterpreterPath` の設定変更だけで、既に選択済みの interpreter が切り替わるとは扱わない。
4. 選択した Python で pytest が動作することを、本書の「構築済み環境を preflight する」に従って確認する。

環境の新規構築や依存関係の準備が必要な場合は、この実行手順を始める前に、`{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` の「Python 実行環境」「仮想環境の管理」に従って準備する。

### pytest 連携と環境変数を設定する

既存ワークスペースに Python 拡張の pytest 連携を設定する。次は、後続実装で既存設定との整合性を確認するための了承済み設定案であり、現状の設定値を示すものではない。

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.cwd": "${workspaceFolder}",
  "python.testing.pytestArgs": ["test", "-ra", "-m", "not real_path_integration"]
}
```

後続実装では、既存の `.code-workspace` と `pyproject.toml` などの設定を確認して統合する。設定ファイルの配置や分割は固定しない。marker だけでは対象を分離できない場合の調整は、本書の「focused test と検査対象を選択する」に従う。

環境変数の意味上の要件と適用範囲は、本書の「Python development mode と ResourceWarning 検査を適用する」を正本とする。同節の実行設定を、`python.envFile` で指定する環境変数ファイルから Python 拡張へ渡す。環境変数ファイルへの記述例は次のとおりとする。

```dotenv
PYTHONDEVMODE=1
PYTHONWARNINGS=error::ResourceWarning
```

環境変数ファイルの具体的な配置先は、既存のファイルと設定を後続実装で確認して決定する。設定後にテストを再探索し、pytest を実行する Python process に両変数が適用されることを確認する。統合ターミナルだけで環境変数を設定したことを、この確認の代わりにしてはいけない。

### 通常テストを探索して実行する

1. テストと設定を保存し、テストタブの更新操作、または `Test: Refresh Tests` で再探索する。探索に失敗した場合は、表示されたエラーと Python の出力を確認する。
2. 探索された個々の test の実行ボタンで個別実行し、ファイルの実行ボタンでそのファイル内の対象 test を実行する。
3. テストタブの「すべて実行」で、探索された通常テストを全件実行する。
4. 結果をテストタブで確認する。失敗した test は、結果とエディターの失敗表示から該当箇所とエラー内容を確認する。

### 人間が実経路統合テストへ切り替える

以下は、人間が実経路統合テストを UI から実行する場合の手順である。テスト自体の実行条件は、本書の「実経路統合テストを実行する」を参照する。

1. `python.testing.pytestArgs` を `["test", "-ra", "-m", "real_path_integration"]` に切り替える。
2. `Test: Refresh Tests` で再探索し、実経路統合テストが対象になっていることを確認してから、個別・ファイル単位・全件のいずれかで実行する。
3. 実行後は、後続実装で確定した通常テスト用の引数へ戻して再探索し、通常テストが既定対象に戻ったことを確認する。

agent による Real Codex CLI 使用テストの選択は、本書の「通常検証と追加検証を選択する」に従う。設定追加や UI 手順整備の依頼を、追加検証の実行に対する明示指示とみなしてはいけない。agent の sandbox と command の起動場所には、引き続き本書の「変更中の検査を実行する」「fresh な完了ゲートを実行する」「Real Codex CLI を使う追加検証を起動する」を適用する。

### 後続実装の受入条件

設定実装後、VS Code 上で次を確認する。

- テストの探索、個別実行、ファイル単位実行、通常テスト全件実行、および失敗箇所とエラー内容の表示が、上記の操作でできる。
- Python 拡張が選択した Python で pytest を起動し、cwd と検査対象が現在の worktree になっている。main worktree の interpreter を使う場合も同じ条件を満たす。
- pytest を実行する Python process に、本書の「Python development mode と ResourceWarning 検査を適用する」の設定が適用されている。
- UI と本書の CLI 手順で実行対象が一致し、既定の「すべて実行」が通常テストを欠落なく含み、Real Codex CLI を使う test を含まない。`real_path_integration` marker だけで分離できないケースがある場合も、この条件を満たす。分離のためのテスト変更は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「テストの削除・統合」に従う。
- 人間による実経路統合テストへの切り替えと通常テストへの復帰が、再探索後の対象に反映される。agent による Real Codex CLI 使用テストの実行を伴う確認には、本書の「通常検証と追加検証を選択する」の条件を適用する。

pytest 設定などの変更後の品質検査は、本書の「fresh な完了ゲートを実行する」「完了を判定する」に従う。UI の受入確認で完了ゲートを代替しない。

既存設定との統合方法、環境変数ファイルの配置先、および marker による分離の十分性は、後続実装で確定する。仕様編集の完了は、設定実装、VS Code 上の動作確認、またはテスト実行の完了を意味しない。

VS Code の機能については、Microsoft の [Python testing](https://code.visualstudio.com/docs/python/testing)、[Python settings reference](https://code.visualstudio.com/docs/python/settings-reference)、[Python environments](https://code.visualstudio.com/docs/python/environments) を技術参考とする。cmoc の意味仕様は、本書と参照先の oracle を正本とする。

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
- 追加検証を指示されている場合は、その検証も最後の変更後に、本書の「Real Codex CLI を使う追加検証を起動する」に従って fresh に実行する。
- Ruff check、Ruff format check、mypy、および通常検証の全 pytest command は repository 所定の sandbox 内で実行する。

realization refactor で変更を確定する時点は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「確定前の検証」に従う。反復する workload であることを理由に、本節の完了ゲートを複数の変更単位や一巡の終了まで先送りしない。停止要求で検査を打ち切った場合は、その結果を未完了とし、停止・rollback のためにゲートを追加実行しない。

## Real Codex CLI を使う追加検証を起動する

本書で親 sandbox は開発作業を行う agent の shell command を囲む境界、子 sandbox は被テスト cmoc が起動する Codex の shell command を囲む境界を指す。

本書の「通常検証と追加検証を選択する」に従って選択された追加検証では、テスト runner を起動する command を親 sandbox 外で実行することを必要条件とする。これは、固定 socket path の保護と内側の Codex による directory 検査が衝突する、入れ子の sandbox 構成を避けるための条件である。

1. 選択した追加検証だけを起動する command を用意する。cwd と Python interpreter は本書の「repository root と Python interpreter を決定する」に従う。Python の実行設定には、本書の「Python development mode と ResourceWarning 検査を適用する」を適用する。
2. 対象 command と入れ子を避ける理由を限定して、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「command 単位の sandbox 外実行」に従う escalation を要求する。承認された command を親 sandbox 外で実行する。
3. 承認が得られない場合は追加検証を未実行とし、本書の「完了を判定する」「実行結果を報告する」に従う。

被テスト cmoc の隔離は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「基本」に従う。子 Codex には、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「Codex CLI 引数による設定上書き」「Codex CLI sandbox」が定める通常の呼び出し規約を適用する。

承認が得られない場合も含め、この回避手順を `TMPDIR` の変更、予約 socket directory などの保護ディレクトリの権限変更、子 sandbox の無効化、または CLI の旧 sandbox への切り替えで代替してはいけない。

### 未実測事項

親 sandbox 外での起動方針は採用済みだが、2026-10-07 時点では、その環境で子 Codex の shell が正常に動作することは未実測である。後続の明示指示による検証で子 shell の実行結果まで確認し、Codex CLI 自体の終了コード 0 だけで正常動作と判定してはいけない。仕様変更だけを、issue 解消や性能改善の実証として扱わない。

## 実経路統合テストを実行する

本書の「通常検証と追加検証を選択する」に従って追加検証の対象となった実経路統合テストには、次の command を用意し、「Real Codex CLI を使う追加検証を起動する」の手順を適用する。変更中の focused test では `test` を対応する test paths または node ID に置き換え、fresh な完了ゲートでは実経路統合テストの全件を対象とする。

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
- 追加検証の実行有無と結果、親 sandbox 外での command 実行の承認状況、および実際の起動場所。実経路統合テストでは focused test と full pytest の結果を区別する
- test 数、skip 数、および skip reason
- model provider、quota、timeout など、出力から確認できた実行上の原因
- 通常検証と追加検証それぞれが fresh に完了したか、および作業の完了判定。未完了ならその理由

明示指示がない場合、Real Codex CLI を使う test は「実行対象外（明示指示なし）」と報告し、実行成功や環境不足による skip と区別する。指示された追加検証は、成功、失敗、未実行、または環境不足による skip とその理由を報告する。Fake Codex CLI だけによる成功を、Real Codex CLI との互換性や実経路の検証済みという結果として報告してはいけない。

test が失敗したとき、期待値を変更すべきかという意味上の判断は、実行上の原因分類とは別に扱う。この判断が必要な場合は、別の仕様調査であることを明示する。
