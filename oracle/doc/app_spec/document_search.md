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

chunk の embedding は、計算できたものから推論出力の妥当性と現在の許可・本文との対応を確認し、都度索引へ永続化する。全対象の計算完了を待って一括で検証・反映してはならない。途中の失敗・取消・期限超過でも反映済みの有効な結果を保持し、次回の同期で現在の許可・本文・互換条件を再確認して再利用する。未計算・検証未完了・不正な結果を反映済みとして扱わない。この逐次反映は、検索要求時の自動同期と doctor preprocess に共通とする。

索引への逐次反映と同期全体の完了を区別し、検索に必要な同期を完了できなければ、その要求は失敗として返す。反映済みの一部だけを使った検索結果や旧結果を、現在の許可集合に対する正常な検索結果として返してはならない。正常に列挙・確認できた空集合や、すべての文書が空白である状態は成功ゼロ件とする。root 消失・差替え、列挙失敗、読取不能を空集合として扱わない。

query embedding と、query・モデル条件・chunk 内容に対応する再ランキング結果を cache する。cache hit でも現在の許可と本文を確認する。検索に使った索引・cache と返却する path・箇所・抜粋が現在確認した本文に対応することを返却前に検証する。編集や scope 変更で不一致となった場合は、期限内に再同期してやり直すか、変更競合として失敗させる。

file tree 全体の原子的 snapshot や、最後の照合後まで編集を阻止する保証は要求しない。索引操作の排他を編集 workload 全体の排他へ拡張しない。列挙回数、SQLite の table 構造、分割アルゴリズムは固定しないが、分割は採用 tokenizer の上限と原文箇所の対応を守り、長文を黙って切り捨てない。

## 初期方式と推論の失敗

初期実装は Python が分類、対象制御、本文確認、差分同期、SQLite 保存、排他、および stdio MCP を担当する。候補検索は sqlite-vec による cosine 距離の全件比較とし、候補を実モデルで再ランキングする。

分割・embedding・rerank は、Python が渡した許可本文だけを処理する推論専用 Node.js 子 process と node-llama-cpp が担当する。worker は検索対象の決定や repository の走査をしない。モデルは Qwen3-Embedding-4B と Qwen3-Reranker-4B の Q4_K_M 配布物を初期採用し、系列・サイズを暗黙に変更しない。取得・準備と通常起動時の検査の責務は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「検索用コンポーネントの準備と検査」に従う。

入力ごとに embedding が存在し、所定次元で、有限かつ非ゼロであることを検査する。候補ごとに有効な実採点を得られることを検査し、欠落、NaN、不正次元、モデル・worker の失敗を、正常ゼロ件や cosine だけの成功へ変換しない。context 超過も切捨て成功にしない。

初期 runtime の native 空採点を正常なゼロ score と区別するため、raw 採点を検査する。内部 API を使う場合は、コンポーネントの準備・更新時に固定版の存在・入出力・欠落検出の互換検査を通す。通常要求では当該操作前に版と API の適合を確認し、採点ごとの raw 値を検査する。guard が成立しなければ失敗させる。同じ失敗契約を満たす下位 API への置換は許容するが、別 runtime ではモデル入力、tokenizer、pooling、次元、採点、取消・解放を再検証する。内部 API の破損を silent fallback の根拠にしてはならない。

初期採用する検索用コンポーネントの正確な識別情報、モデル入力条件、互換検査対象は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `INITIAL_SEARCH_MATERIALS`、`EMBEDDING_QUERY_TEMPLATE`、`RERANKER_INPUT_FORMAT`、`RAW_RANKING_API` へ委譲する。この識別情報は準備と再利用可否の照合に共用し、PoC の一時ファイルを実行時の参照先にしない。

## 検索用コンポーネントの検証契約

コンポーネントを利用可能と判定するには、次のすべてを満たすことを確認する。取得完了、ファイルの存在、設定の構文検証、またはモデルのロード成功だけでは代替しない。

- 本書の「初期方式と推論の失敗」の委譲先が所有する、固定したコンポーネントの識別情報と一致する。モデルの checksum、tokenizer metadata、pooling、次元を含めて照合する。
- 推移的依存を含む完全な lock と native 配布物の版・integrity を固定し、コンポーネントの定義と整合させる。初期実装用の CPU native 配布物を固定して再構築できるようにし、実際に使用する runtime とベクトル演算依存をロード・使用できることを確認する。
- 本書の「初期方式と推論の失敗」が定める runtime の互換検査と raw 採点 guard が成立する。
- 通常検索と同じ入力整形・tokenizer・推論経路および使用する検索設定で、実モデルによる文書・query の embedding と候補の rerank を実行し、同節の出力検査を満たす。保存済みの embedding・採点 cache を返すだけでは、この検証の実行とみなさない。

実モデルの検証には、repository 本文の列挙や索引を必要としない検証入力を使用する。検証結果は、コンポーネントの identity、runtime、実行環境、および検証した設定条件と対応付け、現在の条件への適用可否を確認できるようにする。条件の変更の影響を確認できない場合や、検証未完了の場合は、過去の成功を準備済みの根拠にしない。記録の形式や検証入力の具体的な文面は固定しない。

通常検索では download/build を行わず、その操作で使用するコンポーネントの identity と適合条件を再確認する。変更検出後の未検証のコンポーネントを使わず、不足・不一致・利用不能を本書の「stdio MCP と失敗の公開」に従って失敗として返す。コンポーネントの修復先は `cmoc doctor` として案内する。検索 worker は取得済みのコンポーネントを変更しない。

## identity と保存先

索引 identity は、正規化した worktree の実体、実効閲覧範囲、分類契約、および推論・保存条件を区別する。推論・保存条件にはモデルの配布物、tokenizer、入力整形、分割、pooling、次元、context、runtime、および保存形式の互換性を含める。同じ path の別 worktree 実体を取り違えず、互換性のない索引や cache を暗黙に流用しない。正規化や hash の具体的アルゴリズムは、この区別を満たす範囲で選べる。

| 管理物 | 所有 root と保存先 | 共有範囲 |
|---|---|---|
| 索引・query cache・採点 cache | `{{work-root}}/.cmoc/gu/document_search/indexes/<identity>/` | 同じ worktree 実体・実効閲覧範囲・互換条件だけ |
| 索引 lock | `{{work-root}}/.cmoc/gu/document_search/locks/` | 同じ索引を使う全 process。互換性変更時も旧利用者と回収を調停する |
| 検索用コンポーネント（モデル・tokenizer・推論 runtime・ベクトル演算依存）と、その検証記録 | `{{cmoc-root}}/.cmoc/gu/document_search/materials/` | 同じ正規化済み cmoc-root を使う全 repository・worktree・process |
| モデル常駐枠の調停情報 | `{{cmoc-root}}/.cmoc/gu/document_search/residency/` | 上記の共有管理単位に属する全索引の検索・同期と doctor の実モデル検証 |

常駐枠を call、worktree、索引ごとに複製しない。別の cmoc installation を含むホスト全体のメモリ上限は、この管理単位では保証しない。これらはすべて非追跡の再生成可能な管理物であり、`.cmoc/gt`、Git commit、workload の成果差分へ含めない。非追跡保証は `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「管理領域の非追跡保証」を正本とする。

scope 縮小・互換性変更後は旧 identity を新接続から公開しない。ディスク上の旧管理物を残すことと公開することを区別する。Python の管理処理が利用中・待機中の接続を確認し、参照されない旧索引・cache を回収する。使用中の索引やモデルを削除しない。保持期間と回収頻度は固定せず、secure erase は要求しない。

worktree 終了時は、終了処理の所有者が対応する接続と要求を停止・回収した後に、その worktree の索引・cache・lock を削除する。共有コンポーネントや他の worktree の索引は削除しない。異常終了で残った管理物は次の利用・回収時に実体と利用状態を検査し、反映済み結果の扱いは本書の「同期と cache」に従う。

## 排他、期限、終了

初期構成は共有管理単位全体でモデル常駐枠を 1 とし、embedding と reranker を交互にロードして、要求終了時にモデルを解放する。doctor の実モデル検証も同じ常駐枠を使用する。接続時はモデルをロードせず、必要な操作まで遅延する。Codex call の並列数は別の制御であり、モデルの常駐数へ転用しない。

共有コンポーネントの準備・切替・回収は、同じ cmoc-root を使用する全 repository・worktree・process 間で調停する。複数の doctor と検索が競合しても、使用中のコンポーネントを上書き・削除せず、取得・構築・検証の途中状態を利用者へ公開しない。必要な検証を完了した整合するコンポーネントだけを利用可能にする。

準備の失敗・取消・異常終了では、未完了のコンポーネントを準備済みとして残さず、既存の正常なコンポーネントを保護する。再実行時は残存物と利用状態を確認して修復できるようにする。既存のコンポーネントを保持できても、今回必要な identity や適合条件を満たさなければ、古いコンポーネントで成功を代替しない。

同じ索引への検索・索引同期・回収は整合性を保つよう調停する。コンポーネントの調停、索引 lock、および常駐枠の取得順序を全経路で整合させ、循環待ちを作らない。

検索要求時の自動同期は、要求受付から測る検索要求の期限に含める。この期限には、コンポーネント・索引・常駐枠の待機、同期、推論、返却前照合を含める。

doctor preprocess の索引同期は、長時間かかる初回構築や大量の差分を検索要求の前に処理するため、タイムアウトを設定しない。コンポーネント・索引・常駐枠の待機、worker 起動、分割・embedding、索引への反映を含め、検索用の起動・要求期限や別の処理期限で打ち切らない。コンポーネントの準備・検証と索引同期は区別し、コンポーネントの検証に適用する期限を索引同期へ流用しない。

取消・期限超過・MCP close/EOF では、Python の要求所有者が処理の収束または停止を確認してから索引 lock と常駐枠を解放する。推論が収束しなければ有限の終了猶予後に子 process を停止して回収する。期限到達と停止完了は別の時点であり、応答 deadline のために動作中の worker の保護を先に解放してはならない。doctor preprocess の索引同期にも、取消・失敗時の停止・回収と有限の終了猶予を適用する。

MCP process の終了処理は推論子とその descendant の回収まで責任を持つ。親の強制終了時も子を孤立常駐させず、子の終了まで常駐枠を占有させるか、同等の調停により二重ロードを防ぐ。

doctor によるコンポーネントの検証でも、推論に使用する設定の期限と、動作中の worker を保護したまま停止・回収してから解放する契約を適用する。準備・検証のために起動した子 process は、収束または停止を確認するまでコンポーネントの保護を維持し、doctor の終了後にモデルや子 process を残さない。

## stdio MCP と失敗の公開

公開 tool は検索だけとし、任意ファイル get/resource は必要構成にしない。query と任意の結果件数だけを受け取り、候補数を超える結果件数指定によって候補探索範囲や内部設定を変更しない。tool 名、引数 schema、結果・失敗の正確な型は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `SEARCH_MCP_SERVER`、`SEARCH_TOOL_NAME`、`SEARCH_TOOL_INPUT_SCHEMA`、`SearchResult`、`SearchFailure`、`SearchHit`、`SearchErrorCode` へ委譲する。

成功結果と検索失敗は機械的に識別可能にする。引数不正は MCP の入力エラー、検索中の失敗は `isError=true` と失敗 code・説明で返す。範囲不正、root/列挙/読取失敗、同期・保存失敗、本文変更競合、検索未準備、コンポーネントの不一致、推論失敗、期限超過、取消を区別する。stdio の stdout は MCP protocol 専用とし、診断や native 出力を混入させない。

Codex process ごとに独立した接続と固定 context を持つ。起動と argv 注入は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。PoC の自作 protocol 実装を製品の固定要件にせず、採用する SDK または実装で相互運用を検証する。

## 設定と未確定事項

必要な tuning 設定の field・型・数値制約・項目間制約・暫定既定値は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `DocumentSearchConfig` へ、新規生成時の検索設定の状態は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CmocConfig.document_search` へ委譲する。コンポーネントの identity と caller の閲覧範囲を、自由な repository 設定や MCP 入力によって置換しない。検索設定と call ごとの検索有効化・閲覧範囲は区別する。

設定の保存先、通常起動時の厳格な検証、明示的な `cmoc doctor` での不足補完・保存・診断は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「検索設定の検証と補完」を正本とする。

暫定既定値は、固定した初期のコンポーネントでの利用を開始するための値として採用する。chunk に対して context に余地を持たせ、候補数と threads を抑える。起動・要求の期限と終了猶予の適用範囲は、本書の「排他、期限、終了」に従う。最適値、全体負荷での応答時間・メモリ特性、環境別 tuning は後続の調整事項であり、メモリ上限・応答時間の人間指定合格値はない。

検索・索引同期では、その要求で使う保存済み設定を共通の検証にかけ、起動後の削除・不足・不正化も検出する。不備を暗黙に補完したり、以前の正常な設定へ戻したりせず、検索未準備として理由と修復方法を返す。有効な変更を使う場合も、本書の「identity と保存先」に従って索引・cache の互換性を判定する。コンポーネントの不足・不一致と入力ごとの context 超過・推論失敗は、本書の「初期方式と推論の失敗」「stdio MCP と失敗の公開」に従って引き続き区別する。doctor の検証成功をこれらの検査の代替にしない。

## 実現性の根拠と製品受入条件

2026-09-25 の PoC は、Python 制御、独立 stdio MCP client、指定 4B + 4B の CPU 推論、日本語検索、実再ランキング、保存済み追加・変更・削除・空白化、取消と終了後の復旧について条件付きの実現性を示した。CPU・4 文書 6 chunks の単発比較では、両モデル保持の観測 peak RSS 約 9.71 GiB／差分検索約 1.92 秒、交互ロード約 5.10 GiB／約 8.57 秒だった。query・採点 cache と常駐枠 1・要求終了時解放にも実測がある。これらは観測条件付きの判断材料であり、合格閾値・一般性能保証・製品採用完了を表さない。一時報告や PoC コードは正本所有者・永続参照先にしない。

製品の受入条件として、次を確認する。

- 実際の caller の閲覧範囲と分類を結合し、nested owning repository、root/nested/local/global ignore、tracked ignored directory、pruning 境界・特殊 file、Git 処理回数の不変条件、許可外本文の非流入、scope 縮小、差替え競合を検証する。
- 本書の「検索用コンポーネントの検証契約」と、vector/採点欠落の失敗識別を検証する。内部 API を置換する場合も同じ契約を検査する。
- doctor preprocess の通常起動・明示 doctor の両経路で、検索用の期限を超える索引構築を完了できることと、検索要求時の自動同期には期限が適用されることを検証する。各同期経路で、全対象の完了前に計算済み chunk が検証・永続化され、途中の失敗・取消後も有効な反映済み結果を再利用できることを確認する。期限のある経路では期限超過後の再利用も確認する。同期未完了を正常な検索結果として返さないことも検証する。
- 正規の cmoc 起動環境で Codex の live discovery/search/deadline/取消/close と、親・子の強制終了後の回収・復旧を検証する。PoC は argv 設定と独立 client までで、CODEX_HOME の installation_id への書込み条件を満たせず live 接続は未検証である。HOME/CODEX_HOME や permission の迂回変更で代替しない。
- doctor の起動基盤だけを用意した新環境で、`cmoc doctor` により固定依存・モデルの配布物を再構築して検証できることを確認する。正常なコンポーネントの再利用、取得・構築・検証の失敗時の非正常終了と再実行、複数 doctor と使用中のコンポーネントの保護、通常起動の未準備検出と修復案内、通常検索で追加 download/build がないことを確認する。linked worktree を含む各所有 root の非追跡と、採用 MCP 実装の相互運用も確認する。GPU、32K context、別 OS・別 runtime は検証済みとして扱わない。

暫定値の後続調整では、許可文書全体で初回・無変更・少数差分・異 query・並列待機の時間とメモリを測る。小集合から全体時間を線形外挿して確定しない。この全体測定と最適値の探索は、暫定値の採用や設定補完の導入の受入条件に含めず、上記の統合検証条件は維持する。

## 設計判断の経緯

以前の routing 方式から文書検索へ切り替えた理由は、`{{cmoc-root}}/oracle/doc/considered_alternative/index_md_routing.md` の「廃止した INDEX routing」に記録する。
