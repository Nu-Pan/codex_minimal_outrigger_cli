# cmoc 専用文書検索

## 目的と責務

agent が必要な正本の原文へ到達するため、cmoc は日本語を含む意味検索と再ランキングを提供する。検索対象の厳密な限定、保存済み編集の反映、失敗の識別を、速度やメモリ削減のために緩めない。検索結果は参照先を選ぶ情報であり、正本や現在の原文の代わりにはならない。

本書は検索の意味仕様を所有する。初期方式と、方式にかかわらず維持する契約を分けて定める。QMD 本体・SDK・CLI・QMD MCP は実行時依存に含めない。HTTP 待受、共有推論サーバー、独立した query expansion model、QMD 全機能との互換性、および推論エンジンやベクトル演算の自作は non-goal とする。既存のキーワード検索をこの機能へ再実装することも必須ではない。

## 対象と信頼境界

検索の許可集合は、次の三条件の積集合とする。

- call の work-root において、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md` の「分類結果」「traversal と事前 pruning」に従って oracle file と分類される。
- `{{work-root}}/oracle/doc` 内の Markdown（拡張子 `.md`）である。
- 信頼された cmoc caller が確定した、その call の実効閲覧範囲に含まれる。

分類は owning repository、tracked/ignored、全 ignore source、nested repository、symlink、非通常ファイル、および pruning 境界の既存契約を維持する。検索用 glob を分類器の代替にしてはならない。列挙時の Git 処理回数には、同文書の「Git ignore 判定の性能不変条件」を適用する。

caller は file access mode と workload 固有の閲覧制限を合わせて実効閲覧範囲を確定し、構造化した値を起動管理経路から渡す。prompt、query、モデル出力から権限を推測しない。追加の閲覧禁止を構造化できない場合の call 開始判断は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。mode 名だけを理由に全文書の閲覧を許可してはならない。

範囲は work-root 相対の正規化済み path による許可 file・許可 subtree と除外 file・除外 subtree で表し、除外を優先する。subtree は path component 境界で判定する。絶対 path、親参照、空 path、不正な型、または未確定の範囲を受理せず、全体への fallback を行わない。明示された空の範囲は有効な空集合であり、未指定とは区別する。

work-root と repo-root は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「agent call の path context」に従う。閲覧範囲の正確な field・型・既定値と検索有効化の表現は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/basic.py` の `DocumentSearchScope` と `AgentCallParameter` へ委譲する。call の途中で scope を変更する必要がある場合は、信頼された caller が旧接続を停止して新しい context を作る。MCP 引数から root、任意 path、scope、索引 identity を指定・変更できないようにする。

Python は本文を読む前に許可と種類を確認する。親 directory や leaf の symlink 差替えを含め、確認した対象と安全に開けた regular file の一致を検証し、境界を確認できなければ失敗させる。許可外の本文は tokenizer、embedding、reranker、保存物、cache、結果、抜粋へ流入させない。検索用の読み取り権限は、agent の直接参照の権限を拡張しない。

## 検索と routing

agent はベクトル検索、既存のキーワード検索、原文への直接参照を、目的に応じて単独でも組み合わせても使える。選択と順序を固定しない。ベクトル検索は許可された oracle/doc の候補を探す手段とし、oracle/src と oracle/test は直接参照または既存の文字列検索で確認する。

結果には元ファイルの work-root 相対 path、該当箇所、および抜粋を含める。agent は必要な現在原文を開いて判断し、食い違う場合も原文を優先する。ゼロ件は仕様の不存在や調査の網羅性を証明しない。失敗をゼロ件と解釈せず、別の許可された手段で調査を続ける場合も失敗した検索を成功として扱わない。

正確な agent 向け文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/routing.py` の `build_routing_policy` へ委譲する。文面だけで利用可能な手段、原文確認、範囲制限が分かるようにする。モデル常駐、SQLite、排他アルゴリズム、仕様文書の構成など、agent の判断に不要な内部説明は含めない。完全 prompt への組込みは、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲し、検索の有効状態を実際の call と一致させる。

## 同期と cache

検索要求ごとに現在の許可集合と本文を確認し、追加・変更・削除・空白化を反映してから検索する。未作成の索引は構築する。未変更の埋め込みは再利用し、削除・許可対象外化・空白化した文書の旧 chunk は検索に使わない。本文変更後も同じ process で次の検索へ反映できなければならない。

同期の途中状態は公開しない。全必要処理を完了した整合する世代だけを使い、同期失敗後に旧結果を最新として返さない。正常に列挙・確認できた空集合や、すべての文書が空白である状態は成功ゼロ件とする。root 消失・差替え、列挙失敗、読取不能を空集合として扱わない。

query embedding と、query・モデル条件・chunk 内容に対応する再ランキング結果を cache する。cache hit でも現在の許可と本文を確認する。保存済みの世代と返却する path・箇所・抜粋が現在確認した本文に対応することを返却前に検証する。編集や scope 変更で不一致となった場合は、期限内に再同期してやり直すか、変更競合として失敗させる。

file tree 全体の原子的 snapshot や、最後の照合後まで編集を阻止する保証は要求しない。索引操作の排他を編集 workload 全体の排他へ拡張しない。列挙回数、SQLite の table 構造、分割アルゴリズムは固定しないが、分割は採用 tokenizer の上限と原文箇所の対応を守り、長文を黙って切り捨てない。

## 初期方式と推論の失敗

初期実装は Python が分類、対象制御、本文確認、差分同期、SQLite 保存、排他、および stdio MCP を担当する。候補検索は sqlite-vec による cosine 距離の全件比較とし、候補を実モデルで再ランキングする。

分割・embedding・rerank は、Python が渡した許可本文だけを処理する推論専用 Node.js 子 process と node-llama-cpp が担当する。worker は検索対象の決定や repository の走査をしない。モデルは Qwen3-Embedding-4B と Qwen3-Reranker-4B の Q4_K_M 配布物を初期採用し、系列・サイズを暗黙に変更しない。取得と準備の責務は `{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` の「文書検索のセットアップ」に従う。

入力ごとに embedding が存在し、所定次元で、有限かつ非ゼロであることを検査する。候補ごとに有効な実採点を得られることを検査し、欠落、NaN、不正次元、モデル・worker の失敗を、正常ゼロ件や cosine だけの成功へ変換しない。context 超過も切捨て成功にしない。

初期 runtime の native 空採点を正常なゼロ score と区別するため、raw 採点を検査する。内部 API を使う場合は、セットアップ・更新時に固定版の存在・入出力・欠落検出の互換検査を通す。通常要求では当該操作前に版と API の適合を確認し、採点ごとの raw 値を検査する。guard が成立しなければ失敗させる。同じ失敗契約を満たす下位 API への置換は許容するが、別 runtime ではモデル入力、tokenizer、pooling、次元、採点、取消・解放を再検証する。内部 API の破損を silent fallback の根拠にしてはならない。

正確な初期資材識別情報、モデル入力条件、互換検査対象は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `INITIAL_SEARCH_MATERIALS`、`EMBEDDING_QUERY_TEMPLATE`、`RERANKER_INPUT_FORMAT`、`RAW_RANKING_API` へ委譲する。この識別情報はセットアップと再利用可否の照合に共用し、PoC の一時ファイルを実行時の参照先にしない。

## identity と保存先

索引 identity は、正規化した worktree の実体、実効閲覧範囲、分類契約、および推論・保存条件を区別する。推論・保存条件にはモデル資材、tokenizer、入力整形、分割、pooling、次元、context、runtime、および保存形式の互換性を含める。同じ path の別 worktree 実体を取り違えず、互換性のない索引や cache を暗黙に流用しない。正規化や hash の具体的アルゴリズムは、この区別を満たす範囲で選べる。

| 管理物 | 所有 root と保存先 | 共有範囲 |
|---|---|---|
| 索引・query cache・採点 cache | `{{work-root}}/.cmoc/gu/document_search/indexes/<identity>/` | 同じ worktree 実体・実効閲覧範囲・互換条件だけ |
| 索引 lock | `{{work-root}}/.cmoc/gu/document_search/locks/` | 同じ索引を使う全 process。互換性変更時も旧利用者と回収を調停する |
| モデル・tokenizer と推論 runtime の資材 | `{{cmoc-root}}/.cmoc/gu/document_search/materials/` | 同じ正規化済み cmoc-root を使う全 repository・worktree・process |
| モデル常駐枠の調停情報 | `{{cmoc-root}}/.cmoc/gu/document_search/residency/` | 上記の共有管理単位に属する全索引と明示同期 |

常駐枠を call、worktree、索引ごとに複製しない。別の cmoc installation を含むホスト全体のメモリ上限は、この管理単位では保証しない。これらはすべて非追跡の再生成可能な管理物であり、`.cmoc/gt`、Git commit、workload の成果差分へ含めない。非追跡保証は `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「管理領域の非追跡保証」を正本とする。

scope 縮小・互換性変更後は旧 identity を新接続から公開しない。ディスク上の旧管理物を残すことと公開することを区別する。Python の管理処理が利用中・待機中の接続を確認し、参照されない旧索引・cache を回収する。使用中の索引やモデルを削除しない。保持期間と回収頻度は固定せず、secure erase は要求しない。

worktree 終了時は、終了処理の所有者が対応する接続と要求を停止・回収した後に、その worktree の索引・cache・lock を削除する。共有資材や他の worktree の索引は削除しない。異常終了で残った管理物は次の利用・回収時に実体と利用状態を検査し、未完了世代を公開しない。

## 排他、期限、終了

初期構成は共有管理単位全体でモデル常駐枠を 1 とし、embedding と reranker を交互にロードして、要求終了時にモデルを解放する。接続時はモデルをロードせず、必要な操作まで遅延する。Codex call の並列数は別の制御であり、モデルの常駐数へ転用しない。

同じ索引への検索・明示同期・回収は整合性を保つよう調停する。索引 lock と常駐枠の取得順序を全経路で整合させ、循環待ちを作らない。期限は要求受付から測り、索引と常駐枠の待機、同期、推論、返却前照合を含む。

取消・期限超過・MCP close/EOF では、Python の要求所有者が処理の収束または停止を確認してから索引 lock と常駐枠を解放する。推論が収束しなければ有限の終了猶予後に子 process を停止して回収する。期限到達と停止完了は別の時点であり、応答 deadline のために動作中の worker の保護を先に解放してはならない。

MCP process の終了処理は推論子とその descendant の回収まで責任を持つ。親の強制終了時も子を孤立常駐させず、子の終了まで常駐枠を占有させるか、同等の調停により二重ロードを防ぐ。

## stdio MCP と失敗の公開

公開 tool は検索だけとし、任意ファイル get/resource は必要構成にしない。query と任意の結果件数だけを受け取り、候補数を超える結果件数指定によって候補探索範囲や内部設定を変更しない。tool 名、引数 schema、結果・失敗の正確な型は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `SEARCH_MCP_SERVER`、`SEARCH_TOOL_NAME`、`SEARCH_TOOL_INPUT_SCHEMA`、`SearchResult`、`SearchFailure`、`SearchHit`、`SearchErrorCode` へ委譲する。

成功結果と検索失敗は機械的に識別可能にする。引数不正は MCP の入力エラー、検索中の失敗は `isError=true` と失敗 code・説明で返す。範囲不正、root/列挙/読取失敗、同期・保存失敗、本文変更競合、検索未準備、資材不一致、推論失敗、期限超過、取消を区別する。stdio の stdout は MCP protocol 専用とし、診断や native 出力を混入させない。

Codex process ごとに独立した接続と固定 context を持つ。起動と argv 注入は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。PoC の自作 protocol 実装を製品の固定要件にせず、採用する SDK または実装で相互運用を検証する。

## 設定と未確定事項

必要な tuning 設定の field・型・既定状態は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `DocumentSearchConfig` と、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CmocConfig.document_search` へ委譲する。資材 identity と caller の閲覧範囲を、自由な repository 設定や MCP 入力によって置換しない。

chunk、overlap、候補数、batch、context、threads、起動・要求期限、終了猶予の製品初期値は、許可された実文書全体と並列待機の測定後に確定する。現時点では tuning 未設定を表現し、必要な検索・明示同期には検索未準備として通知する。未設定を無期限待機や仮の PoC 値へ変換しない。メモリ上限・応答時間の人間指定合格値はない。

## 実現性の根拠と製品受入条件

2026-09-25 の PoC は、Python 制御、独立 stdio MCP client、指定 4B + 4B の CPU 推論、日本語検索、実再ランキング、保存済み追加・変更・削除・空白化、取消と終了後の復旧について条件付きの実現性を示した。CPU・4 文書 6 chunks の単発比較では、両モデル保持の観測 peak RSS 約 9.71 GiB／差分検索約 1.92 秒、交互ロード約 5.10 GiB／約 8.57 秒だった。query・採点 cache と常駐枠 1・要求終了時解放にも実測がある。これらは観測条件付きの判断材料であり、合格閾値・一般性能保証・製品採用完了を表さない。一時報告や PoC コードは正本所有者・永続参照先にしない。

製品化は、仕様改訂 → 中核実装と call 接続 → 残る統合検証 → INDEX 撤去を含む切替の順に進める。後続で次を確認する。以下を本書の編集によって実施済みとしてはならない。

- 実際の caller の閲覧範囲と分類を結合し、nested owning repository、root/nested/local/global ignore、tracked ignored directory、pruning 境界・特殊 file、Git 処理回数の不変条件、許可外本文の非流入、scope 縮小、差替え競合を検証する。
- 固定 runtime の raw 採点 guard の互換性、vector/採点欠落の失敗識別、モデル入力と tokenizer・pooling・次元を検証する。内部 API を置換する場合も同じ契約を検査する。
- 正規の cmoc 起動環境で Codex の live discovery/search/deadline/取消/close と、親・子の強制終了後の回収・復旧を検証する。PoC は argv 設定と独立 client までで、CODEX_HOME の installation_id への書込み条件を満たせず live 接続は未検証である。HOME/CODEX_HOME や permission の迂回変更で代替しない。
- 許可文書全体で初回・無変更・少数差分・異 query・並列待機の時間とメモリを測り、tuning の初期値を確定する。小集合から全体時間を線形外挿して確定しない。
- 固定依存・モデル資材から新環境を再構築し、通常検索で追加 download/build がないこと、linked worktree を含む非追跡、採用 MCP 実装の相互運用を確認する。GPU、32K context、別 OS・別 runtime は検証済みとして扱わない。

## 旧方式の廃止

INDEX 生成 agent・schema・モデル設定、生成 preflight、自動 commit、merge・許容差分の特例、専用分類・書込禁止・テスト選択規定は廃止し、後方互換経路を設けない。明示同期の入口は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/indexing.md` の「cmoc indexing」に従う。doctor など検索と無関係な管理責務は維持する。

廃止の経緯は `{{cmoc-root}}/oracle/doc/considered_alternative/index_md_routing.md` の「廃止した INDEX routing」に記録する。生成済み INDEX の撤去は製品切替の作業であり、この仕様を編集するセッションに別途与えられた routing・アクセス制限を変更する根拠にはならない。
