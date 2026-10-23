# decision / reference / spec / realization への移行手順

各工程の **「簡潔にまとめた手順」** を順に進める。背景・注意点・例外は、折りたたんだ **「詳しい説明」** を必要に応じて開いて確認する。

**この手順書とスクリプトの追加だけでは、移行は実行されていない。** 全コマンドは repository root で実行する。`$cmoc_python` は工程 0 で設定する。

## 全体の流れ

| 工程 | 主な担当 |
|---|---|
| 0. 作業環境と基準の記録 | 人間 |
| 1. 初期材料と変更範囲の確認 | 人間とエージェント |
| 2. 配置の機械的な移設とパス更新 | 人間がスクリプト実行 |
| 3. reference の改訂 | 人間 |
| 4. 既存事項の抽出と新仕様の decision 化 | 人間（エージェントは候補を提示） |
| 5. spec の初回同期 | エージェント |
| 6. 製品コードの追従 | エージェント |
| 7. 検証・運用切替 | 人間とエージェント |
| 8. 後始末 | 人間 |

各工程の判断・未完了事項・検証結果は `transition/work/` に記録する。

## 採用済みの方針

<details>
<summary>共通方針と、この手順書の位置付け</summary>

この手順書は、cmoc 自身を新しい所有区分と開発フローへ移すための作業記録・実行手順である。製品仕様の正本にはしない。最終的な人間の決定は `decision`、人間が保守する資料・コードは `reference`、生成する仕様は `spec` に置く。

- メモ `transition/rethinking_oracle_and_realization.md` の方向に沿い、人間が `decision`・`reference`、エージェントが `spec`・`realization` を編集する。
- **`oracle/src` は全体を `reference/src` に移す。** プロンプトに埋め込む文言、その組合せを示すプログラム、schema、設定等を仕分けして realization へ移さない。
- 人間がプロンプト文言と構築方法を保守する。reference のコードを直接利用し、realization 側に同内容を複製しない。
- `cmoc decision plan` は調査・プラン提示、`cmoc decision apply` は spec 同期と realization 追従を担う。既存の `oracle investigation`、`oracle edit`、`realization apply` を置き換える。
- 移行専用のプログラム、検査、作業記録は `transition` に集める。cmoc 本体には移行サブコマンド、旧配置への fallback、移行中だけの分岐を追加しない。製品コードには新仕様の通常動作を実装する。
- **機械的な配置移設、reference の改訂、decision の抽出、spec の初回同期、製品コードの追従の順に進める。** decision は開始時点で空でもよく、改訂済みの reference と移設した spec を材料に、初回同期の前に人間が必要な内容を選ぶ。

`reference/src/oracle` の `oracle` は、移設時点での Python package 名である。分類上の oracle を残す意味ではない。まず package の相対構成を維持し、人間が所有するコードの一括 rename・文言置換を移設と混ぜない。

`migrate.py` は配置移設・ファイル内のパス更新・ID 採番・文書参照検査を補助する。人間の意図の抽出、新しいプロンプトの作成、spec の意味上の改訂、新コマンドの実装を自動完了させるプログラムではない。

`transition/work/` は Git ignore 対象であり、履歴やバックアップの代わりにはならない。工程 4 で人間が固定すると選んだ判断は decision に、共有する移行記録は `transition` 直下の別ファイル等に人間が保存する。

</details>

## 0. 作業環境と基準を記録する

### 簡潔にまとめた手順

1. 旧版の未完了 run・会話・TUI を整理し、移行中に使う作業環境を用意する。
2. 以下で構築済みの Python 環境を選び、移行専用テストを実行する。

    ```bash
    cmoc_work_root="$(git rev-parse --show-toplevel)"
    cmoc_common_git_dir="$(git rev-parse --path-format=absolute --git-common-dir)"
    cmoc_main_root="$(dirname "$cmoc_common_git_dir")"
    if [ -x "$cmoc_work_root/.venv/bin/python" ]; then
        cmoc_python="$cmoc_work_root/.venv/bin/python"
    elif [ -x "$cmoc_main_root/.venv/bin/python" ]; then
        cmoc_python="$cmoc_main_root/.venv/bin/python"
    else
        echo "構築済みの Python 環境が必要です" >&2
        exit 1
    fi
    cd "$cmoc_work_root"
    "$cmoc_python" -m pytest --version
    "$cmoc_python" -c 'import markdown_it; print("Markdown parser available")'
    ```

    ```bash
    PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
        "$cmoc_python" -m pytest transition/test_migrate.py -ra
    ```

3. 既存の変更を確認して人間が移行前の状態を commit し、その commit と移設計画を記録する。

    ```bash
    git status --short
    mkdir -p transition/work
    git rev-parse HEAD > transition/work/before_commit.txt
    "$cmoc_python" transition/migrate.py plan
    ```

**次へ進む条件：** 未完了 run・会話と既存変更を整理し、戻る基準を記録した。

<details>
<summary>詳しい説明</summary>

Python は構築済みのプロジェクト環境を使う。linked worktree に環境がなければ main worktree の環境を使用できる。移行専用テストは一時ディレクトリ内の模擬 tree を使い、この repository の移設や Real Codex CLI の起動を行わない。

Git 操作は人間が行い、スクリプトは commit、stash、branch 切替を行わない。

移設前に旧版の編集 run、join/recovery、TUI 等を終了・整理する。人間の入力を待つ会話も、新版の編集に再利用しない。移行の途中で旧版 cmoc の apply/refactor/doctor 等を動かすと、旧分類で新しい配置を扱うことになる。

移行中の編集には、配置変更で動作を変えない作業環境を用意する。現在の checkout の `bin/cmoc` は現在のコードを直接使うので、旧版の固定環境とはみなさない。スクリプト自体は cmoc を import・起動せず、移設後も同じ Python から実行できる。

</details>

## 1. 引き継ぐ初期材料と変更範囲を確認する

### 簡潔にまとめた手順

1. [新仕様の入力](rethinking_oracle_and_realization.md) と上の「採用済みの方針」を読み、今回変える範囲が意図と合っていることを確認する。変更対象以外の既存要求は引き継ぐ。
2. 空の decision ディレクトリを用意する。決定の記述は工程 4 で行う。

    ```bash
    mkdir -p decision
    ```

3. 工程 3〜5 の作業依頼には、対象工程と、新仕様の入力・採用済みの方針を明示する。

**次へ進む条件：** 移行方針と変更範囲に意図とのずれがない。細部の判断は後続工程で順次行う。

<details>
<summary>詳しい説明</summary>

今回適用する新仕様の入力は [rethinking_oracle_and_realization.md](rethinking_oracle_and_realization.md) と、この手順書の「採用済みの方針」に記録した追加方針である。移行スクリプトによる自動注入は行わず、以下の工程で人間とエージェントが成果物へ反映する。

| 工程 | 新仕様の反映先 | 行うこと |
|---|---|---|
| 3. reference の改訂 | `reference/src` のプロンプト文言・builder・schema 等 | 新しい責務や読み書きの境界を、agent に渡す自己完結した指示とその構築処理へ反映する |
| 4. decision の記述 | `decision/**/*.md` | 新しい区分・編集者・参照方式・ワークフロー等の採用済み決定を、人間が短い記述として追加する |
| 5. spec の初回同期 | `spec/**/*.md` | decision と reference を根拠に、旧モデルの規定を新モデルの仕様へ更新する |
| 6. 製品コードの追従 | realization の実装・テスト等 | 同期した spec に従って新しい動作を実装する |

移設と reference の改訂では、この新仕様の入力を適用し、明示的に変更する事項以外の既存要求は引き継ぐ。decision が空であることを理由に既存要求を削除・弱化しない。これは移行中の作業基準であり、cmoc 本体に一時的な判定分岐を実装する指示ではない。開始時点でダミーの決定を用意する必要もない。

機械的な移設では、配置と対応が明確なパス表記を更新し、旧 oracle 文書の仕様上の意味は保持する。その spec を decision の抽出材料にし、意味上の初回同期は工程 5 で行う。移設しただけでは、その全内容を新たな人間の決定として採用したことにはならない。

次は作業中に順次確認する事項であり、開始前にすべてを決定する条件にはしない。後続工程で判断が必要になった時点で具体的な文書・変更案を示し、その工程に必要な範囲で解決する。この一覧だけで採用済み仕様にはしない。

- `reference` の読み取り範囲と、decision が参照した資料の拘束範囲。reference 全体の編集者が人間であることは確定済み。
- `decision plan` と apply の各段階の読み書き範囲、および汎用 TUI・join・feedback 等の権限。
- 任意のプランを apply へ渡す方法。プランなし・古いプランと現在の decision が食い違う場合の扱い。
- spec 同期と realization 追従の入力 commit、初回適用、途中失敗、再実行、join、適用済み基点の更新条件。
- ID の書式・一意性・移動時の保持・削除時の参照の扱い。以下の採番器は移行用の補助であり、製品の ID 仕様の正本ではない。
- 旧 session・設定・保存データをどう扱うか。引き継いだ既存要求と、工程 4 で抽出する decision に対する整合を確認する範囲、新しい差分追従の基点。

各工程の依頼には判断根拠を明記する。抽出前に必要になった判断は移行記録に残し、工程 4 の候補に含める。エージェントの補完を人間の決定とみなしたり、自動で decision に書き込んだりしない。

</details>

## 2. 配置を機械的に移設し、ファイル内のパスを更新する

### 簡潔にまとめた手順

1. 他の編集処理を止め、移設と内容一致の検査を行う。**`verify-move` はパス更新前に実行する。**

    ```bash
    "$cmoc_python" transition/migrate.py plan
    "$cmoc_python" transition/migrate.py move
    "$cmoc_python" transition/migrate.py verify-move
    ```

2. パス更新の差分を出し、`path-plan.txt` を読む。`REVIEW` は要確認箇所、`SKIP` は対象外になったファイルを示す。

    ```bash
    "$cmoc_python" transition/migrate.py plan-paths > transition/work/path-plan.txt
    ```

3. 差分を確認したら適用し、`path-result.txt` と `path-check.txt` で結果・残りの候補を確認する。

    ```bash
    "$cmoc_python" transition/migrate.py rewrite-paths > transition/work/path-result.txt
    "$cmoc_python" transition/migrate.py plan-paths > transition/work/path-check.txt
    git diff --stat
    git status --short
    ```

**次へ進む条件：** `verify-move` が成功し、パス更新の差分と確認候補を確認した。

<details>
<summary>詳しい説明</summary>

まず内容を変えずに配置を移し、移設前との一致を確認する。その後、同じ工程内でファイル中のパスを更新する。

| 移設元 | 移設先 | 本文のパス更新前の状態 |
|---|---|---|
| `oracle/doc/**` | `spec/**` | 内容・相対構成・permission を変えずに移設する。decision 抽出前の初期材料であり、新仕様への同期は後で行う |
| `oracle/src/**` | `reference/src/**` | 全体を内容・相対構成・permission を変えずに移設する |

`move` は directory の rename を行う。既存の移設先を上書き・merge せず、全組合せを確認してから開始する。移設前の fingerprint を `transition/work/move.json` に保存し、内容、path、permission、空 directory の一致を確認する。移設元に含まれる通常ファイルは ignored なものも保持する。

symlink、特殊ファイル、Git metadata 等の保護対象が tree にあれば停止する。`oracle/test` は空の場合だけ除去できる。内容がある場合や oracle 直下に他の材料がある場合は、人間が行き先を決め、スクリプトと手順を更新してから進める。

`move` は一つずつ rename するため、複数 tree 全体を一括で原子的に切り替える処理ではない。中断した場合はファイルを編集せず、同じ `move` を再実行する。receipt と一致する移設済み部分を認識し、残りだけ進める。receipt の破損、両側にファイルがある状態、移設開始後の内容変更は停止理由になる。receipt を削除して無理にやり直さない。

機械的なパス更新と、以後の正常な編集によって fingerprint は変わる。`verify-move` は後工程の完了判定には使用しない。

パス更新の対象は `spec`、`reference`、`decision`、`src`、`test`、`bin` の各 tree と、root の `README.md`、`pyproject.toml`、`.gitignore`、`codex_minimal_outrigger_cli.code-workspace` とする。存在する UTF-8 テキストだけを扱い、改行と permission を保持する。`transition`、`memo`、`AGENTS.md`、Git metadata・管理領域、仮想環境・依存物・キャッシュは走査対象から外す。バイナリと UTF-8 以外のファイルは変更せず報告する。

自動更新するのは次の範囲である。

- 独立したパス接頭辞として現れる `oracle/doc` → `spec`、`oracle/src` → `reference/src`。root 相対、`./`、`{{work-root}}`・`{{cmoc-root}}`・`{{repo-root}}`、この checkout の絶対 path に対応する。本文、コメント、文字列、設定、コード例も対象になる。
- Markdown の通常の inline link と参照定義にある相対 path。移設前の参照元から行き先を求め、移設後の参照元・先に合わせて書き換える。行き先を root 内で確認でき、現在の表記では別の既存対象へ到達しない場合に限る。query と anchor は保持する。

Python package 名の `oracle`、外部 URL、別 repository の絶対 path、行き先が決まっていない `oracle/test` は一括 rename しない。`root / "oracle" / "src"` のような分割した表記、backslash 表記、解決できない相対リンクなどは確認候補として残す。動的なパス構築や特殊な Markdown 構文の全件検出は保証しない。

本文にある path が現在の参照なのか、意図的な旧入力・履歴なのかは、差分の内容確認で判断する。必要な旧表記はその確認で残し、仕様の意味や実行動作に関わる修正は工程 3 以降で行う。パス更新だけで新仕様への適合やリンク先の意味まで確認できたとは扱わない。

パス更新はファイルごとに原子的に置換する。途中で失敗した場合は人手による後続編集を始めず、同じ `rewrite-paths` を再実行する。更新済みのパスは重ねて変換しない。移設の receipt を書き換えたり、`verify-move` を通すために変更を戻したりしない。

`transition` 内の移設元 mapping、テストの移設前入力、手順書の旧パスは、移設後もそのまま保持する。エディタ等でこれらまで一括置換すると receipt の検証や旧パスの解釈が壊れるため、パス更新の対象に含めない。

この時点から工程 6 の完了までは、旧 import path 等により cmoc が動作しない期間があり得る。配置移設成功を、製品の新仕様対応完了として記録しない。

</details>

## 3. 人間が reference のコード・文言を改訂する

### 簡潔にまとめた手順

1. 新仕様の入力に従い、人間が `reference/src` のプロンプト文言・builder・schema・設定を改訂する。
2. 工程 2 のパス更新で残った確認候補を扱う。
3. 最終的に生成されるプロンプトを読み、agent が内部仕様を読まずに目的・制限・入力・完了条件を理解できることを確認する。

**次へ進む条件：** reference が新仕様と引き継ぐ既存要求に合っている。decision はまだ空でもよい。

<details>
<summary>詳しい説明</summary>

人間が工程 1 で示した新仕様の入力に従って `reference/src` を編集し、新しい責務と引き継ぐ既存要求に対応する正確な定義を用意する。エージェントは変更候補や不整合を提示できるが、人間が保守する内容を独断で realization へ移したり複製したりしない。

確認対象には次を含める。path は `reference/src` からの相対 path である。

- `oracle/prompt_builder/parts` と `policy`：四区分、権限、判断基準、検索、feedback、handoff の文言。
- `oracle/acp_builder/basic.py` と各 builder：file access mode、decision plan、apply の各段階、TUI、join、report 等への prompt part の組込み。
- `oracle/other/cmoc_config.py`：新しい call に対応する設定の定義。
- schema、文書参照の表現、機械的なパス更新で残った確認候補。

</details>

## 4. 人間が既存事項を抽出し、新仕様の決定を decision に加える

### 簡潔にまとめた手順

1. 候補を SPEC ID で指せるよう、移設した spec の見出しを採番する。

    ```bash
    "$cmoc_python" transition/migrate.py number-specs
    ```

2. エージェントに「旧 spec から残す決定」と「新仕様の入力から追加する決定」の候補を提示させる。
3. 人間が採否・表現を決め、`decision/**/*.md` に `[DECI-...]` 付きで記述する。
4. decision と reference の不整合を人間が調整する。

**次へ進む条件：** 今回残す・追加する決定を記述し、reference と整合した。既存事項を網羅する必要はない。

<details>
<summary>詳しい説明</summary>

ここでは二つの入力から decision を記述する。機械的に移設した spec からは、人間が今後も固定したい既存事項を抽出する。工程 1 で示した新仕様の入力からは、今回導入する新しい区分・編集者、ID と参照方式、`decision plan/apply` のワークフロー等、採用済みの決定を追加する。新しい決定は旧 spec に存在することを前提にしない。

この時点の spec はまだ旧仕様を含むため、新仕様の入力と改訂済みの reference を踏まえて候補を整理する。見出しの採番は本文の意味を変えない準備作業であり、spec 全体を新仕様へ同期するのは次の工程である。

採番器は、現在の spec 全体で未使用の `[SPEC-000000]` からの数値 ID を付け、既存 ID は保持する。decision と reference は編集しない。コード例の見出しは採番しない。ネストした見出しや複数行 setext 見出しは、無理に書き換えず停止するので手で ID を付ける。採番処理が中断した場合も既存 ID を保持して再実行できる。削除済み ID の履歴管理は行わない。

エージェントは候補ごとに、出典、内容の短い要約、固定する理由・守りたい境界を提示する。出典は、既存事項なら元の SPEC ID、新しい決定なら新仕様の入力文書の見出しと対応する内容で示す。関連する reference があれば、その対応箇所も示す。候補には目的・非目的、所有区分、実行権限、失敗時に守る条件、reference に委ねる正確な詳細などが考えられる。

人間が採用した内容だけを decision に記述し、見出しには重複しない ID を付ける。reference の内容を固定する場合は、`reference/src/...` と対象の関数・定義等、固定する内容を特定する。

spec の全文コピーや、スクリプトによる自動昇格は行わない。旧 oracle 文書の内容を、新仕様でもそのまま人間が固定したいとは限らない。抽出しなかった spec の記述は、それだけを理由に削除しない。すべての判断をここで確定する必要はなく、運用後も必要に応じて decision を追加できる。

</details>

## 5. decision・reference から spec を初回同期する

### 簡潔にまとめた手順

1. エージェントに、decision・reference を根拠とした spec の初回同期を依頼する。今回の変更対象以外の既存要求は保持する。
2. 文書間の参照を「短い説明＋参照先 ID」に揃える。decision に抽出した内容は DECI ID で参照する。
3. 不足 ID の採番と文書検査を実行する。

    ```bash
    "$cmoc_python" transition/migrate.py number-specs
    "$cmoc_python" transition/migrate.py check-docs
    ```

**次へ進む条件：** decision・reference と spec が整合し、引き継ぐ要求、ID と参照を確認した。

<details>
<summary>詳しい説明</summary>

工程 4 で人間が記述した decision と改訂済みの reference を根拠に、新しい区分・責務・ワークフローの決定を使って旧モデルの規定を更新する。仕様を実装から逆算する作業にしない。

decision へ抽出しなかった詳細も含めて spec を整合させる。同期中に decision や reference の不整合が分かった場合は、人間が調整した結果を反映する。

仕様書の文章品質について旧 oracle と同じ細かな編集規定を自動継承しない。引き継いだ要求、今回明示された変更、エージェントが補った記述の根拠を追えるようにする。

採番器は旧 path・見出しから意味上の参照先を推測して変換しない。同期で見出しが増えた場合の不足 ID は、再実行で採番できる。

文書検査は、decision/spec の見出し先頭の ID、区分、重複、本文中の参照先の存在を確認する。移設直後にも使えるよう、検査自体は decision の未作成・空ディレクトリ・空白だけの Markdown 文書を許容する。spec 文書は必要であり、存在しない `[DECI-...]` への参照は decision が空でもエラーにする。コードブロック・inline code の例は対象外。ID suffix の最終的な文字種・桁数、reference 内の locator、仕様の意味上の整合性は別に確認する。

</details>

## 6. 製品コードを新仕様へ追従させる

### 簡潔にまとめた手順

1. エージェントに、同期済み spec に従って realization の実装・テスト・利用手順を更新させる。
2. reference の直接利用、新しい分類・検索、`decision plan/apply`、全 call の権限を確認する。
3. 旧前提の残りを検索し、ヒットごとに必要な修正を判断する。

    ```bash
    rg -n 'oracle/(doc|src|test)|PURE_ORACLE|oracle investigation|oracle edit|realization apply' \
        src test reference decision spec bin README.md pyproject.toml
    ```

**次へ進む条件：** 新しい通常動作を実装し、旧モデルへの不要な実行依存を整理した。

<details>
<summary>詳しい説明</summary>

変更するのは新仕様の通常実装であり、移行専用処理は引き続き `transition` に置く。

| 変更単位 | 主な確認対象 |
|---|---|
| 実行可能な reference の利用 | `src/oracle.py`、`pyproject.toml`、起動・配布・schema 読み込み。新配置のコードを直接使い、旧配置への fallback を残さない |
| 分類と配置 | `runtime_git.py`、doctor、refactor の対象集合。管理領域・Git ignore 等の既存境界も保つ |
| 検索と参照 | 新しい検索対象、ID から原文への到達、索引更新。旧本文を検索結果に残さない |
| decision plan/apply | CLI、設定、builder 呼出し、入力、各段階の権限、差分、失敗、join、適用基点 |
| 全 call の整合 | TUI/resume、run/session join、feedback、report、handoff。別経路から人間所有の内容を編集する経路を残さない |
| 利用・検証手順 | help、補完、README、fixture、通常テスト、配布テスト、品質検査の対象 path |

Python package 名 `oracle` は引き続き reference のコードを指し得るため、単語全体の機械置換はしない。検索ヒットは移行候補の位置情報であり、意図的な履歴・旧入力を検査する fixture 等まで無条件に削除しない。検索ゼロ件だけで適合性の確認を終えない。

旧設定や管理 state に変換が必要と分かった場合は、対象・変換内容・保持する情報を確定してから `transition` に専用処理を追加し、この手順に実行コマンドを追記する。現在のスクリプトは `.cmoc` の変更・削除、旧履歴の破棄、設定の自動再生成を行わない。具体的な schema 変更が未確定のまま汎用変換を作らない。

</details>

## 7. 検証して運用を切り替える

### 簡潔にまとめた手順

1. 移行用スクリプトと文書の検査を実行する。

    ```bash
    "$cmoc_python" -m ruff check transition
    "$cmoc_python" -m ruff format --check transition
    "$cmoc_python" -m mypy transition/migrate.py
    PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
        "$cmoc_python" -m pytest transition/test_migrate.py -ra
    "$cmoc_python" transition/migrate.py check-docs
    ```

2. テスト・package・mypy・fixture が新配置に対応済みであることを確認し、更新後の通常検証を実行する。以下は移設後のコマンド例である。**Real Codex CLI を使うテストは、明示的な実行指示がある場合だけ行う。**

    ```bash
    "$cmoc_python" -m ruff check src reference/src test
    "$cmoc_python" -m ruff format --check src reference/src test
    "$cmoc_python" -m mypy src reference/src
    PYTHONDEVMODE=1 PYTHONWARNINGS="error::ResourceWarning" \
        "$cmoc_python" -m pytest test -ra -m "not real_path_integration"
    ```

3. 下の「切替の確認事項」に沿って内容を確認し、検証結果を記録して、人間が移行済みの基準 commit を確定する。
4. 新しい session で、小さな decision 変更 → plan → apply → 結果確認を一巡する。

**次へ進む条件：** 通常検証と人間による内容確認を終え、新フローを使えることを確認した。

<details>
<summary>詳しい説明</summary>

移行用テストは `transition` 内に置き、通常の製品テストとは明示的に分けて起動する。製品の最終検証は、工程 5・6 で更新したテスト実行手順を確認して行う。上の通常検証コマンドを実行する前に、pytest の pythonpath、package 設定、mypy path と fixture が新配置に対応していることを確認する。

Fake Codex CLI で二段階の順序、入力、権限、失敗・再実行、join、適用基点を検証する。Real Codex CLI を使うテストは人間が実行を明示した場合だけ別途追加し、Fake の成功を実経路の検証済みとは扱わない。

切替の確認事項は以下のとおり。

- 全体を reference へ移したコードを実行時に直接利用できる。製品の import・起動・配布・テストが `transition` に依存しない。
- 移行で引き継いだ既存要求と、工程 4 で抽出した decision に対する spec・realization の整合を確認した。decision が当初空だったことや差分ゼロだけを理由に確認を省略していない。
- 人間所有の decision/reference、生成する spec/realization の境界が全 call に反映され、生成後のプロンプトも確認した。
- 新コマンドの通常動作を確認し、旧コマンドと旧分類への不要な依存を整理した。
- 移行前の未完了 run・旧設定・保存データの扱いが確定している。移行前の apply 基点や会話を暗黙に流用していない。
- 通常検証の結果と人間による確認結果を記録し、移行済みの基準 commit を人間が確定した。

切替後の一巡では、人間が小さな decision 変更を行い、結果が意図に合うことを確認する。これは運用上の確認であり、テストの成功だけで意味上の成功を保証したことにはしない。

</details>

## 8. 失敗時の扱いと後始末

### 簡潔にまとめた手順

1. 途中で失敗した場合は現在の工程に留まり、下の対処表に従う。後始末は運用切替後に行う。
2. 残す移行記録を保存し、新仕様の反映漏れと製品の `transition` 依存がないことを確認する。
3. 人間が `transition` を削除する。

**完了条件：** 必要な記録を保存し、`transition` を外しても製品が動作する。

<details>
<summary>詳しい説明</summary>

| 状況 | 行うこと |
|---|---|
| `plan` / 移設前検査の失敗 | 指摘された既存配置や未割当材料を確認する。移設先を削除して上書きしようとしない |
| rename 途中で中断 | 他の編集をせず、receipt を保持して同じ `move` を再実行する |
| パス更新の途中で中断 | 後続の人手編集を始めず、同じ `rewrite-paths` を再実行する |
| 移設後に内容を変更済み | `verify-move` を再度成功させるために編集を戻さない。後工程の差分・検証で確認する |
| 新版の実装・検証に失敗 | 現在の工程に留まり、旧 cmoc を新配置へ向けて通常運用しない |
| 移行全体を取り消す | 人間が移行前 commit と後続差分を照合し、新しい人間の編集・作業記録を保持してコードと配置をまとめて戻す。管理 state は Git の復元だけで戻ると仮定しない |

スクリプトに自動 rollback や一括削除は設けていない。元の内容は rename で保持され、移行後に人間が編集した内容も破棄しない。Git 未追跡・ignored な情報は基準 commit から復元できないので、必要な保存は人間が別途行う。

採用済みの新仕様が `transition` にしか残っておらず、decision・reference・spec への反映から漏れている状態がないことを確認する。未完了の移行で `work/move.json` を失うと、中断した移設の自動再開に使えなくなるため、後始末は最後に行う。

</details>
