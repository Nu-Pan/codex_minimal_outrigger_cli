# cmoc 専用文書検索

## 目的と責務

agent が必要な正本の原文へ到達するため、cmoc は日本語を含む embedding による意味検索を提供する。待ち時間と応答量を抑えるため、再ランキングは行わず、候補位置をまとめて返す。部分編集に伴う再推論を抑えながら、保存済み編集を反映し、現在の検索対象の原文と正しい位置へ対応付ける。原文の選択・確認と判断は agent が担う。

本書は検索の意味仕様を所有する。本書と参照先で定める契約を満たす範囲で、内部構成と処理方式は実装に委ねる。QMD 本体・SDK・CLI・QMD MCP は実行時依存に含めない。HTTP 待受、共有推論サーバー、独立した query expansion model、QMD 全機能との互換性、推論エンジンやベクトル演算の自作、および既存のキーワード検索の再実装は目的に含めない。

## 対象と信頼境界

検索対象は、call の `{{work-root}}/oracle/doc` 内の Markdown（拡張子 `.md`）のうち、oracle file と分類される文書に限る。分類・安全な列挙・性能条件は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md` の「分類結果」「traversal と事前 pruning」「Git ignore 判定の性能不変条件」に従う。

work-root は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「agent call の path context」に従って接続ごとに固定し、MCP 引数から root、任意 path、索引 identity を指定・変更させない。本文を読む際も、symlink 等への差替えを含めて検索対象の regular file であることを確認し、確認できなければ失敗させる。対象外の本文を推論・保存・cache・結果へ流入させない。検索の提供によって agent のファイルアクセス権限を拡張しない。

## 検索と routing

agent が oracle doc の仕様文章を検索するときは、キーワード検索と文書検索 MCP を併用する。検索結果にもファイルアクセス制限を適用し、返された位置を手掛かりに現在の原文を読んで判断する。検索失敗と成功ゼロ件を区別し、ゼロ件だけを根拠に仕様の不存在や調査完了と判断してはならない。検索が無効な call、または検索に失敗した場合は、許可された手段で調査を続けてよい。

候補箇所の採用上限は、設定 `candidate_count` と MCP 引数 `limit` の小さい方とし、`limit` の省略時は `candidate_count` を使う。件数はファイル集約・行範囲統合前の候補箇所数で数え、候補不足なら指定可能な件数の下限未満でも返す。値の範囲は本書の「設定と未確定事項」、入出力の正確な定義は「stdio MCP と失敗の公開」の委譲先に従う。

採用した候補を同一ファイルごとに集約し、work-root 相対 path と行範囲だけを返す。同一パスは一度だけ掲載し、重複・重なりのある行範囲は統合する。本文・抜粋・見出し文・スコアは返さない。

agent の検索・原文確認・判断規則を伝える routing policy の正確な文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/routing.py` の `build_routing_policy` へ委譲する。完全 prompt への組込みは、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲し、検索の有効状態を実際の call と一致させる。tool の使い方は公開 tool 定義で伝え、routing policy へ重複させない。

## 同期と cache

検索要求ごとに現在の検索対象と本文を確認し、追加・変更・移動・削除・空白化を索引へ反映してから検索する。未作成なら構築し、検索対象から外れた旧箇所は使用しない。同じ process の次の検索にも保存済み編集を反映する。本節は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「検索索引の同期」にも適用する。

Markdown の構造を利用して本文を自動分割し、部分編集の影響を局所化する。手動の境界マーカーを要求せず、本文を切り捨てずに、分割した単位（chunk）と原文位置の対応を保つ。

同じ索引 identity 内で、完全なモデル入力と互換条件が一致し、現在の検索対象へ対応付けられる保存済み embedding は再利用する。変更文書内や移動後の chunk も対象とし、path・行番号・出現順の変化だけで再推論しない。索引 identity の意味は、本書の「identity と保存先」に従う。

同期全体の完了を待たずに、検証済みの中間結果を永続化する。失敗・取消・期限超過でも保存済みの有効な結果を保持し、次回は現在の本文と互換条件を確認して再利用する。同期未完了の一部や旧結果を正常な検索結果として返してはならない。正常に列挙・確認できた空集合や、全対象が空白である状態は成功ゼロ件とする。

返却前に候補位置と現在原文の対応を確認し、不一致なら期限内に再同期するか変更競合として失敗させる。file tree 全体の原子的 snapshot や編集 workload 全体の排他は要求しない。

診断記録は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「索引同期の診断記録」に従う。

## 初期方式と推論の失敗

候補は文書と query の embedding の類似度に基づいて選ぶ。初期採用するコンポーネントの正確な識別情報とモデル入力条件は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `INITIAL_SEARCH_MATERIALS`、`EMBEDDING_QUERY_TEMPLATE` へ委譲する。これらを repository 設定や MCP 引数で差し替えない。推論専用 worker には確認済みの対象本文だけを渡し、検索対象の決定や repository の走査を担わせない。

入力の context 制約と、embedding の存在・次元・有限性・非ゼロを検査する。入力の切捨て、不正な推論結果、モデルや worker の失敗を、成功ゼロ件や旧結果による成功へ変換しない。

## 検索用コンポーネントの検証契約

コンポーネントは、固定した識別情報と依存関係に一致し、再構築可能で、使用する環境・設定で動作することを確認してから利用可能とする。検証には、通常検索と同じ入力整形・tokenizer・推論経路による実モデルの文書・query embedding と、ベクトル演算依存の動作確認を含める。ファイルの存在やモデルのロード成功だけで代替しない。

検証結果をコンポーネント・runtime・実行環境・設定条件と対応付け、変更後の条件へ適用できない過去の成功を流用しない。通常検索では使用するコンポーネントの適合性を確認し、不足・不一致・未検証なら失敗させて `cmoc doctor` を案内する。通常検索で download/build やコンポーネントの変更は行わない。

準備・修復と通常起動時の検査の分担は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「検索用コンポーネントの準備と検査」に従う。

## identity と保存先

索引 identity は worktree の実体と、分類・モデル入力・推論・保存形式の互換条件を識別する。同じ path の別 worktree や、互換性のない索引・cache を取り違えない。

索引と cache は `{{work-root}}/.cmoc/gu/document_search/` に置き、同じ worktree 実体の互換条件内で使用する。コンポーネントとその検証記録、共有資源の調停情報は `{{cmoc-root}}/.cmoc/gu/document_search/` に置き、同じ cmoc installation の repository・worktree・process 間で共有する。これらは再生成可能な管理物であり、非追跡保証は `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「管理領域の非追跡保証」に従う。

互換性を失った管理物は検索へ公開せず、使用中の資源を保護しながら不要な索引・cache・コンポーネントを回収する。worktree 終了時は、対応する接続・処理の停止後にその worktree の管理物を削除し、共有コンポーネントや他の worktree の索引を保持する。異常終了後も利用状態と保存内容を確認して復旧できるようにする。

## 排他、期限、終了

同じ cmoc installation の検索・同期・doctor 検証は、モデル常駐枠 1 を共有する。必要な操作時にロードし、要求終了時に解放する。索引とコンポーネントの同時利用・更新・回収を循環待ちなく調停し、使用中の資源の破壊や準備途中の公開を防ぐ。準備を完了できない場合も、既存の正常なコンポーネントを保護する。

MCP 検索要求では、進捗のある同期には時間を与えつつ、待機・停滞と要求全体を有限時間で打ち切る。期限は日時の変更に左右されずに判定する。期限設定の意味は次のとおりとし、値・型・制約は本書の「設定と未確定事項」の委譲先に従う。

| 設定 field | 対象とする時間 |
| --- | --- |
| `resource_wait_timeout_seconds` | 要求内の累積資源待ち時間。 |
| `sync_no_progress_timeout_seconds` | 各自動同期で実際の処理完了が進まない時間。資源待ちは除く。 |
| `post_sync_search_timeout_seconds` | 初回同期完了から検索の完了・打切りを判断するまで。待機と再同期も含む。 |
| `search_request_timeout_seconds` | 要求受付から停止処理へ移るまでの全体上限。進捗や再同期で延長しない。 |
| `request_timeout_seconds` | コンポーネント検証の推論要求。 |
| `startup_timeout_seconds`、`shutdown_grace_seconds` | 起動期限と、収束しない worker を停止する前の終了猶予。 |

処理中の通知や同じ処理の繰返しだけを進捗として期限を延ばさない。MCP 検索要求で適用中の期限に達したら処理を打ち切り、期限超過として返す。取消は別の失敗として識別する。外側の tool 期限との関係は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。

doctor preprocess の索引同期には、初回構築や大量の差分を処理するため、資源待ちや worker 起動を含めてタイムアウトを設定しない。コンポーネントの検証期限は索引同期へ適用しない。

失敗・取消・期限超過・接続終了では、動作中の処理の収束または停止・回収を確認してから資源の保護を解く。収束しなければ有限の終了猶予後に子 process とその descendant を停止・回収する。親の異常終了でもモデルや子 process を孤立させず、二重ロードを防ぐ。これは doctor の処理にも適用する。

## stdio MCP と失敗の公開

公開 tool は検索だけとし、query と任意の候補数上限 `limit` を受け取る。`tools/list` の公開定義だけで、補足 prompt や仕様文書を読まずに利用できるようにする。正確な詳細は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の次の定義へ委譲する。

| 委譲先 | 所有する詳細 |
| --- | --- |
| `SEARCH_MCP_SERVER`、`SEARCH_TOOL_NAME`、`SearchErrorCode` | 公開名と失敗 code。 |
| `build_search_tool_description` | 機能・検索対象・接続の work-root を伝える説明文。 |
| `SEARCH_TOOL_INPUT_SCHEMA` | 引数の構造・制約・意味と省略時の扱い。 |
| `SEARCH_TOOL_OUTPUT_SCHEMA` | 成功・成功ゼロ件・検索失敗の構造と要素の説明。 |

検索結果と検索中の失敗は schema に適合する `structuredContent` と、同じ値の JSON text で返す。検索中の失敗には `isError=true`、code、理由と案内可能な対処方法を付ける。root・列挙・読取、同期・保存、変更競合、未準備、コンポーネント不一致、推論、期限超過、取消を区別する。引数不正は JSON-RPC の入力エラーとして扱う。

公開定義へ agent の判断に不要な内部説明を含めない。stdio の stdout は MCP protocol 専用とする。接続の起動・固定 context・終了は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。

## 設定と未確定事項

tuning 設定の field・型・数値制約・項目間制約・暫定既定値は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `DocumentSearchConfig`、新規生成時の検索設定は同ファイルの `CmocConfig.document_search` へ委譲する。`candidate_count` と `limit` に共通する指定範囲は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `SEARCH_CANDIDATE_COUNT_MIN` と `SEARCH_CANDIDATE_COUNT_MAX` へ委譲する。検索設定と call ごとの有効化は区別する。

設定の保存・検証・不足補完は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「検索設定の検証と補完」に従う。検索・索引同期でも使用する保存済み設定を検証し、起動後の不足や不正を暗黙に補完せず、検索未準備として理由と修復方法を返す。

暫定既定値は利用開始のための値であり、性能保証ではない。全体負荷での時間・メモリ・検索品質の測定と tuning は後続の調整事項とし、数値の合格基準は定めない。

## 製品受入条件

本書と委譲先の契約を、正常系・境界値・失敗・編集競合・並行利用・異常終了からの復旧について検証する。正規の cmoc 起動環境と採用する Codex CLI で、tool の公開・検索・期限・取消・接続終了の連携を確認する。doctor による新環境での準備と再実行、通常起動の未準備検出も対象とする。

過去の PoC の結果を製品での検証完了や性能保証とは扱わず、未検証の環境や条件は区別する。

## 設計判断の経緯

以前の routing 方式から文書検索へ切り替えた理由は、`{{cmoc-root}}/oracle/doc/considered_alternative/index_md_routing.md` の「廃止した INDEX routing」に記録する。
