# Doctor Preprocess

## 概要

doctor preprocess は、各サブコマンドに共通する実行環境・設定・管理状態・必須の検索用コンポーネントの検証と文書検索索引の同期を担い、本命処理・agent 起動前に必ず実行する。明示的な `cmoc doctor` は、この共通処理を準備・修復の入口として使用する。CLI 自動補完用プローブには、`{{cmoc-root}}/oracle/doc/app_spec/cli_auto_completion.md` の「CLI 自動補完規則」が定める境界を適用する。

## 成功条件と保証範囲

正常終了は、対象の repo-root・work-root で使用する共通実行環境・保存設定・管理状態と、使用する cmoc-root の必須のコンポーネントが、本書の検証をすべて満たし、検査時点で利用可能であることを表す。本書の「作業用配置先の存在保証」の成立と「検索索引の同期」の完了も含む。必須の依存・コンポーネントが不足、不一致、未検証、または利用不能のまま、正常終了してはならない。

各サブコマンド固有の branch、session/run state、git working tree・staging area の clean 状態などの操作条件は、この保証に含めず、doctor preprocess の正常終了後に個別仕様に従って検証する。任意の入力での推論成功や、検査後の文書・設定・環境変化に対する成功も保証しない。model provider の稼働・認証などの保証範囲は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` の「cmoc の責務境界」を維持する。

検証・必要な修復・索引同期を完了できない場合は、本命処理・agent 起動へ進まずエラー終了する。診断には、問題のある依存・設定・作業用配置先・コンポーネントまたは索引同期の処理、対象 root または path、理由、および実際に取り得る修復方法を含める。ただし、本書の「feedback MCP reporter/client の事前検証」が定める degraded warning と、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「Windows toast transport」が定める非必須機能の失敗契約は維持する。これらの例外を作業用配置先の存在保証、必須の検索用コンポーネント、または索引同期へ適用してはならない。

## 共通実行環境の検証

cmoc の Python 実行環境と必須依存、Git、および Codex CLI が利用できることを検証する。検索用コンポーネントとして準備する依存は、本書の「検索用コンポーネントの準備と検査」の経路で扱う。Python 環境の前提は、`{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` の「Python 実行環境」「仮想環境の管理」に従う。Codex CLI に渡す環境については、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「環境変数 `$CODEX_HOME`」「preflight validation」に従う。

cmoc 本体と doctor を起動するための Python 環境・起動用依存は事前導入の範囲とする。検索用 runtime・モデル等の未準備を、doctor 自身を起動できない理由にしてはならない。doctor は OS、Git、Codex CLI、または model provider の導入・修復を担わず、自動修復しない必須依存の不足も診断してエラーとする。

保存設定は、検索設定に加え、既存の agent call 種別に必要な設定の存在・構造と provider 定義への参照整合性を検証する。設定の正確な構造は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CmocConfig`、検証の意味と限界は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` の「agent call ごとの直接設定」「provider 定義」に従う。検索以外の既存設定を自動で置換せず、不備には手動修正を案内する。provider 固有の認証・疎通や Model の互換性検査を追加しない。

## 実行手順

通常のサブコマンドと明示的な `cmoc doctor` は、検索設定・検索用コンポーネントに対して異なる経路を使う。設定は本書の「検索設定の検証と補完」、コンポーネントは「検索用コンポーネントの準備と検査」に従う。明示 doctor の入口で通常起動用の不足検査を先に行い、準備・修復へ到達する前に停止させてはならない。

1. 起動基盤と検索用コンポーネント以外の共通依存を検証し、コンポーネントを所有する cmoc-root と、処理対象の repo-root・各 work-root を確定する
2. 本書の「作業用配置先の存在保証」に従って、処理に使用する各 work-root の配置先を補完・検証する
3. 本書の「管理領域の非追跡保証」に従って、それぞれの root の `.cmoc/gu` が git 追跡対象外であることを保証する
4. `{{work-root}}/.agents` が git 追跡対象であることを保証する
5. 処理に使用する各 work-root の `{{work-root}}/.cmoc/gt/config.json` に対し、入口に応じた検索設定の検証・補完、共通設定の検証、および追跡保証を行う
6. `{{work-root}}/.cmoc/gt/realization/refactor/state.json` が git 追跡対象であり、schema を満たし、entry 集合と調査要求が同期済みであることを保証する
7. 入口に応じた検索用コンポーネントの準備・検査を行う
8. 本書の「検索索引の同期」に従って、処理対象の各 work-root の索引を同期する
9. cmoc が管理する local stdio MCP reporter/client の利用可能性と collector との protocol compatibility を事前検証する
10. ここまでの作業で発生した tracked 差分を、それぞれの修復対象 root の owning repository・worktree で git commit する。検索設定の補完差分も含め、差分がなければ commit を作らない

通常起動でも、検索設定・検索用コンポーネント以外の既存の管理ファイルの修復・同期と、それに伴う commit は本書の各規則に従って行う。検索用コンポーネントの準備を明示 doctor に集約することを理由に、これらの管理責務を省略しない。

## 作業用配置先の存在保証

cmoc が固定の作業用配置先として案内するディレクトリを、空でも利用できるようにする。存在保証の対象集合は次の五つとし、配置先の意味は `{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle doc と oracle src の正本責務」「realization file の責務」に従う。

- `{{work-root}}/oracle/doc`
- `{{work-root}}/oracle/src`
- `{{work-root}}/oracle/test`
- `{{work-root}}/src`
- `{{work-root}}/test`

この集合は、その回の prompt の組込み選択や path 文字列の出現に依存しない。prompt 本文やコマンドに現れる全 path の自動作成へ一般化しない。

### 対象 root と成立時点

処理に使用する各 `{{work-root}}` に適用する。agent call では、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「agent call の path context」が定める cwd 起点の worktree root を対象とし、repo-root や cmoc-root で代替しない。管理領域のためだけに扱う cmoc-root や、処理に使用しない worktree へ適用範囲を広げない。

通常サブコマンドと明示的な `cmoc doctor` の双方で、不足する対象と必要な親ディレクトリを作成し、正常終了を判定する検証時点で対象のすべてがディレクトリとして存在することを保証する。作成・検証は、その work-root の前処理で対象を使うファイル列挙・索引同期より前に完了する。

doctor preprocess の後に作成する run worktree にも、その worktree の初回利用・agent 起動前に同じ保証を成立させる。main worktree での前処理成功だけで代替しない。この適用のために doctor preprocess 全体を再実行する方式は要求しない。

検証後の checkout・merge 等による変化への継続保証は、本節では定めない。merge 中の doctor 修復・commit の制限は、本書の「管理領域の非追跡保証」「editing run の join での同期時点」に従う。

### 補完・検証と失敗時の扱い

空のディレクトリも保証を満たす。既存のディレクトリと内容を保持し、同じ状態への再実行で不要な変更を生じさせない。この保証のために `.gitkeep` 等のファイルを追加したり、Git 追跡を要求したりしない。本書が別に定める `.agents`・設定・refactor state の追跡保証、`.cmoc/gu` の非追跡保証、および tracked 差分の commit 責務は維持する。

対象または必要な親ディレクトリに同名ファイルその他の衝突がある場合、自動で置換・削除しない。必要な作成・検証を完了できなければ、対象 work-root と path、理由、および実際に取り得る修復方法を示し、本書の「成功条件と保証範囲」の失敗契約に従う。

ディレクトリの存在とファイル列挙の成功は別に判定し、内部のファイル件数・検索ヒット件数や、任意の検索コマンドの終了コード 0 は保証しない。正常に列挙・確認できた空集合と検索失敗の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「検索と routing」「逐次反映と同期完了」に従う。

## 管理領域の非追跡保証

doctor は repo-root と処理対象 work-root に適用する。加えて、共有コンポーネントを所有する cmoc-root の管理領域にも、コンポーネントの初回書込みより前に同じ非追跡保証を適用する。共有コンポーネントのためだけに扱う cmoc-root の不足は明示 doctor が修復し、通常起動で検出した場合は `cmoc doctor` による修復を案内してエラー終了する。

同じ root は重複処理しない。linked worktree も、それ自身の owning repository・index・ignore source で検証し、main worktree の検証成功だけで代替しない。後から作成する run worktree も、管理領域の初回使用前に確認する。merge 中へ doctor の修復・commit を割り込ませず、検証を満たさなければ当該管理処理を失敗させる。

以下の `<対象root>` は、検証・修復する root を表す。共有コンポーネントのために cmoc-root を扱う場合、repo-root・work-root の設定や refactor state の修復まで cmoc-root へ適用範囲を広げない。cmoc-root 自身が処理対象 work-root でもある場合は、その役割に従う。

### 検証

非追跡保証は、`<対象root>/.cmoc/gu` ツリー全体と、将来作成される全 descendant に適用する。feedback の pending observation、active state、report cut、checkpoint、Markdown report、および検索の索引・cache・lock・コンポーネント・常駐枠の調停情報も含む。

完了判定では、次の両方を満たすことを確認する。

- `git -C <対象root> ls-files -- .cmoc/gu` の出力が空である。
- `git -C <対象root> check-ignore -q .cmoc/gu/.__cmoc_ignore_probe__` が成功する。

後者の probe path は、将来作成されるファイルが git ignore 対象になることを確認するために使う。この probe のために実ファイルを作成する必要はない。

### 修復

- `<対象root>/.gitignore` が存在しなければ作成する
- `<対象root>/.gitignore` に `/.cmoc/gu/` が無ければ追加する
- `<対象root>/.cmoc/gu` ツリー内に tracked file があれば、working tree 上の実ファイルを残したまま対応する git index から除外する
- 修復後も完了判定を満たさない場合はエラー終了する

## `{{work-root}}/.agents` の追跡保証

agent が書き込めない `.agents` は、doctor preprocess があらかじめ用意する。

### 検証

- `{{work-root}}/.agents` が存在すること
- `{{work-root}}/.agents` ツリー内に git 追跡対象 file が 1 件以上あること

### 修復

- `{{work-root}}/.agents` が存在しなければ作成する
- `{{work-root}}/.agents` ツリー内に tracked file がない場合は `{{work-root}}/.agents/.gitkeep` を用意し、git index に追加する
- 修復後も `{{work-root}}/.agents` ツリー内に tracked file がない場合はエラー終了する

## `{{work-root}}/.cmoc/gt/config.json` の追跡保証

本書の「検索設定の検証と補完」に従って検証・必要時の保存を終えた設定ファイルが、git 追跡対象であることを保証する。未追跡なら git 追跡対象に追加し、追跡を保証できなければエラー終了する。

## 検索設定の検証と補完

検索設定は、処理対象 work-root の `.cmoc/gt/config.json` の `document_search` に保存する。通常起動で設定不備を早期に検出し、明示的な doctor で不足を補えることを目的とする。本節の設定検証と、本書の「検索用コンポーネントの準備と検査」の両方を完了させる。

正確な field、型、数値制約、項目間制約、および補完に使う暫定既定値は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `DocumentSearchConfig` へ委譲する。新規ファイル全体の設定構造と既定状態は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CmocConfig` へ委譲する。これらの既定値を使う新規生成・明示補完と、保存済み設定の検証を区別する。

MCP 検索要求用の四種類の期限設定も、以下の必須項目の検証と不足補完に含める。既存の `request_timeout_seconds` が保存されていても、追加された項目が存在することの代わりにはせず、その値から新しい項目を推定しない。各設定の適用先は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「設定と未確定事項」に従う。

### 共通の検証

- 既存の設定ファイルが読み取れ、正しい JSON の object であることを検証する。通常起動でファイルが存在しない場合は、未設定として扱う。
- `document_search` が object であり、必要なすべての項目を持つことを検証する。欠落と旧 `document_search: null` は未設定とし、個々の tuning 項目の `null` は不正な明示値として扱う。
- 明示された値の型・値域と、設定値だけで判定できる項目間制約を検証する。暗黙の型変換、丸め、既定値への置換によって不正値を受理しない。
- 廃止項目 `reranker_context_tokens` が残る設定は不正とし、黙って無視しない。
- 通常起動では保存された内容そのものを検証する。デシリアライズ時のメモリ内既定値で不足を埋めて、検証成功としてはならない。
- 不足または不正があれば、本命処理・agent 起動へ進まず、本書の「設定不備の診断」に従ってエラー終了する。明示的な doctor では、次節の補完候補をこの検証へ渡す。

### 明示的な doctor での補完

確認入力を求めず、次のように補完候補を作る。

- ファイルが存在しない場合は、`CmocConfig` の既定状態から新規ファイルの候補を作る。
- `document_search` が欠落または `null` の場合は、`DocumentSearchConfig` のすべての暫定既定値を補う。
- `document_search` が部分的な object の場合は、欠落項目だけに対応する暫定既定値を補う。

既存の明示値と検索以外の既存設定は保持する。不正な JSON、object 以外の構造、不正な型・値域は不足として扱わず診断する。既存値を暫定既定値へ置換したり、既存値に合わせて補完値を調整したりしない。

補完候補全体を共通の検証にかけ、既存値と補完値の組合せも含めて成功した場合だけ保存する。補完後も不整合ならエラー終了し、その候補や部分的な補完を設定ファイルへ保存しない。補完が不要ならファイルを書き換えず、同じ状態への再実行で設定の不要な差分を生まない。保存した補完差分の追跡・commit は、本書の「実行手順」に含める。

### 設定不備の診断

診断には、対象設定ファイルの path、該当項目、理由、および修復方法を含める。JSON の構文不正など項目を特定できない場合は、ファイル全体の問題として分かる位置情報や理由を示す。不足には対象 work-root での `cmoc doctor`、不正な明示値には該当項目の手動修正を案内する。補完後の不整合では、衝突する既存項目と補完候補の値が分かるようにする。

旧設定の `candidate_count: 8` など、委譲先の範囲外の明示値には、許容する整数の範囲を示して手動修正を案内する。廃止項目 `reranker_context_tokens` には手動での除去を案内し、明示 doctor でも自動削除しない。`candidate_count` の欠落は、旧値が明示されている場合と区別し、上記の不足補完で扱う。

これらは handled failure とし、終了処理と表示には `{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラー終了の確定」「handled failure の表示」を適用する。

### 検査範囲の境界

本節は保存設定の検査・補完を扱い、コンポーネントの利用可能性は次節で検証する。call 接続は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。

起動後の設定変更、コンポーネントの不足・不一致、入力に依存する context 超過、推論失敗の検出は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「設定と未確定事項」「検索用コンポーネントの検証契約」「初期方式と推論の失敗」に従い、検索・索引同期の必要な操作時に引き続き行う。

## 検索用コンポーネントの準備と検査

コンポーネントの配置と共有単位は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「identity と保存先」に従う。使用する cmoc installation の共有コンポーネントを扱い、処理対象 repository・worktree ごとに別のコンポーネントを準備しない。

明示 doctor は、同文書の「初期方式と推論の失敗」の委譲先が定める推論 runtime、ベクトル演算依存、embedding 用モデル・tokenizer、およびその推移的依存を照合し、不足・破損・不一致・利用不能があれば取得・必要な構築・修復を行う。正常な準備済みのコンポーネントは再利用し、再実行だけを理由に再取得・再構築しない。そのうえで、再利用時も含め、同文書の「検索用コンポーネントの検証契約」に従う実モデルの検証を完了させる。検証には今回使用する各 work-root の検索設定を用い、同じ適合条件の検証は共有してよい。

通常起動では、保存済み検索設定と共有コンポーネントを変更せず、コンポーネントの照合と、明示 doctor で完了した検証が現在のコンポーネント・runtime・実行環境・設定条件にも適用できることを確認する。コンポーネントの取得・構築・置換や実モデルの検証を通常起動の修復として実施しない。コンポーネントの不足・不一致、検証未完了、または検証結果を現在の条件へ適用できない場合は、理由と処理対象 work-root での `cmoc doctor` を案内して、本命処理の前にエラー終了する。

明示 doctor が準備・検証を完了できない場合も、必要条件が整ったとは扱わない。取得・構築・照合・互換検査・推論のどこで失敗したかと修復方法を示す。権限や外部依存などに手動対処が必要なら、その対処と doctor の再実行を案内する。これらの想定済み失敗は、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラー終了の確定」「handled failure の表示」に従う。

準備・検証の途中状態の扱い、使用中のコンポーネントの保護、および検証 process の停止・解放は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「排他、期限、終了」に従う。

## 検索索引の同期

通常起動・明示 doctor のどちらも、検索設定とコンポーネントの検証後に、処理対象の各 work-root の索引を同期する。

対象・逐次反映と再利用・期限・資源管理は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「対象と信頼境界」「同期と cache」「identity と保存先」「排他、期限、終了」を正本とする。ここで準備した索引を別の worktree の索引と取り違えず、後続の検索要求でも同文書に従って現在の検索対象と本文を確認する。

索引同期の開始・終端と、所要時間・結果・処理量・資源待ちの記録は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「索引同期の診断記録」に従う。

## refactor state の追跡保証と同期

### 検証

- `{{work-root}}/.cmoc/gt/realization/refactor/state.json` が存在していること
- 同 file が git 追跡対象であること
- 同 file が `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「保存先と JSON schema」を満たすこと
- entry 集合と調査要求が、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「entry 集合の同期」が定める同期完了時点の条件を満たすこと

### 修復

- file が存在しなければ、空の object `{}` を保存する
- file を git 追跡対象に追加する
- 同文書の「entry 集合の同期」に従って entry 集合と調査要求を同期する
- file が存在するものの schema を満たさない場合は、既存の調査履歴を破棄せずエラー終了する

### editing run の join での同期時点

active run の kind が `realization_refactor` または `feedback_report` の場合、merge 前の doctor preprocess では追跡状態と schema だけを検証し、entry 集合の同期を merge 後まで遅延する。これは、session branch と run branch が同じ refactor state を独立に更新して merge conflict を起こすことを避けるためである。

merge 後は kind にかかわらず、競合解消の付随編集も反映した最終的な session tree に対して entry 集合を同期する。merge 進行中に doctor preprocess を再実行して同期・commit を割り込ませない。競合中の管理物の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/merge_conflict_resolution.md` の「agent と cmoc の責務」に従う。

## feedback MCP reporter/client の事前検証

- reporter の agent-facing interface と期待する protocol は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「MCP interface」と「collector と transport」を正本とする。
- doctor preprocess の検査は、次の事前判定に必要な範囲に限る。
    - cmoc が管理する local stdio MCP reporter/client を call 開始時に起動できること
    - 同 reporter/client と collector の protocol に互換性があること
- doctor preprocess は repo-local reporter executable を作成、copy、配置、修復、または version command で検証してはならない。
- reporter の利用不能または protocol 不一致を検出した場合は、`feedback.reporter_unavailable` の構造化 event と warning を記録する。その invocation の agent 自己申告を degraded として、本命処理を続ける。
- reporter の利用不能を理由に sandbox、file access mode、Structured Output schema、個別 agent call の完了条件、または Codex workload の retry 判定を変更してはならない。
