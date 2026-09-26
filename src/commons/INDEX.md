# `__init__.py`

## Summary
- commons パッケージを cmoc の共通 runtime helper 群として説明する docstring。パッケージ全体の位置づけを確認する入口です。

## Read this when
- commons パッケージが担う全体的な役割を確認するとき。

## Do not read this when
- 個々の helper の挙動や実行フローを調べるときは、該当する runtime モジュールを直接読んでください。

## hash
- 8b50d22749d6fd880d430c393e14c6dcb919038e7b9c7ec76288c523c3d58b34

# `cmoc_runtime.py`

## Summary
- 複数の実行経路で共有する runtime API の集約窓口で、設定・Git・Codex 実行・状態管理などの機能を再公開する。

## Read this when
- 共有 runtime API の公開範囲や、各実行経路が使う共通機能を確認するとき。

## Do not read this when
- 特定の機能の内部動作や変更箇所を調べるときは、その機能を実装する下位モジュールを直接読む。

## hash
- 1ec72860ce36bfc1b0297b91db09cb85700ed32add3ae7215d7e10387ed46550

# `document_search_worker`

## Summary
- Python が許可した文書や検索語を受け取り、固定された Node 推論環境で文書・クエリの埋め込みと候補文書の再ランキングを行う worker と、その配布依存を担う。
- 推論要求の検証、トークン上限に基づくチャンク分割、ベクトルとスコアの検査、親プロセス終了の監視を含む。

## Read this when
- 埋め込みや再ランキングの Node 側処理、チャンク分割、推論要求・応答の検証、worker の依存パッケージを変更・調査するとき。

## Do not read this when
- 対象文書の列挙や閲覧範囲、索引同期・検索結果の組み立て、Python 側のプロセス起動・資材検証・キャンセル・期限管理を調べるときは、それらを担う Python 側の文書検索処理から確認する。

## hash
- 6d1cc79a2776a3d21bd8c5a88cf8ef4f2169ab573c57928452c670d786c4941b

# `prompt_editor_input.py`

## Summary
- `cmoc tui`、`cmoc oracle edit`、`cmoc oracle investigation` の依頼文・指示をエディタから受け取る共通入口。入力用ファイルの予約、エディタ起動、handoff の開始、入力の確定保存と抽出を担う。
- プロンプト雛形の構築や Codex の起動設定は呼び出し側に委ね、ここではエディタ入力の受け渡しを扱う。

## Read this when
- これらのコマンドに共通するエディタの選択・起動、handoff 開始、入力の保存・抽出の挙動を変更または追跡するとき。
- エディタ入力の保存先の検証や、保存時のエラー処理との連携を確認するとき。

## Do not read this when
- 特定コマンドのプロンプト雛形や、入力後の Codex 起動設定だけを変更するときは、そのコマンドやプロンプト構築の担当箇所を確認する。
- handoff の通信認証・IPC・target のライフサイクルなどの実装だけを変更するときは、handoff のランタイム担当箇所を直接確認する。

## hash
- 5350b9e1fa5ac518ba0a30ef4b5390e8e5e6e9e2d53854d6a1f7fdbd0b748447

# `runtime_cli.py`

## Summary
- 全 CLI サブコマンド共通の実行開始から終端処理までを統括し、前処理、診断ログ、フィードバック収集、例外・中断の扱い、終端結果の確定と通知を調整する。
- 個々のサブコマンドの処理内容ではなく、共通の実行ライフサイクルやその終端結果への反映を変更するときの入口。

## Read this when
- サブコマンド共通の初期化、実装呼び出し、後処理の順序やコンテキスト管理を変更するとき。
- 例外やユーザー中断の分類、進行状況の記録、終端結果の統合・表示・通知など、複数コマンドに共通する振る舞いを変更するとき。

## Do not read this when
- 特定サブコマンドの処理や設定だけを変更するときは、そのコマンドの実装から確認する。
- ログ記録、エラー表現、レポート保存、フィードバック収集、TUI 起動後の復旧や通知など、個別の共通機能の内部だけを変更し、この実行ライフサイクルとの連携に影響しないときは、その機能の担当実装から確認する。

## hash
- 5acdf958750e735c0e4d6cfd32396d12c341d68db7750117edf2ad6cb5f1d3a2

# `runtime_codex.py`

## Summary
- Codex の exec と対話 TUI の実装関数を共有ランタイム API として再公開する入口。個別の起動処理や実行制御は含まない。

## Read this when
- 共有ランタイムから利用する Codex 実行 API の公開範囲や import を変更・確認するとき。
- Codex exec と TUI の呼び出し関数が共有入口から公開されているか確認するとき。

## Do not read this when
- exec の出力検証、回復、再試行などの実行時挙動を調べるときは、exec の実装を直接読む。
- TUI のプロセス起動、call log、通知 callback などを調べるときは、TUI の実装を直接読む。

## hash
- cc80041004f69b74468dbd703e186f058a367b85f21904b0b419d3a38cd687c2

# `runtime_codex_exec.py`

## Summary
- Codex exec の呼び出し全体を制御し、実行記録、回復待ち後の再開、Structured Output の検証と補正を連携させる。
- 個々の subprocess 準備や回復待ちの仕組みではなく、それらを組み合わせる呼び出し側の制御を調べる入口。

## Read this when
- Codex exec の呼び出し手順、実行記録、結果の組み立てを変更・調査するとき。
- Structured Output の検証、補正 turn、補正中の作業成果物の保護を変更・調査するとき。
- quota または一時障害からの回復確認後に、元の call を再開する流れを変更・調査するとき。

## Do not read this when
- Codex CLI の argv・環境・schema 準備、実行結果の分類など、subprocess 境界の個別処理を調べるときは、その処理を担う対象から確認する。
- 回復待ちの共有、probe の集約、中断伝播そのものを調べるときは、回復待ち機構を担う対象から確認する。
- Codex 呼び出し失敗の共通エラーテキスト変換だけを調べるときは、その変換を担う対象から確認する。

## hash
- e56520fc9aec386dc49fe79864bac60767bd87dd73a92e0deaf19985bc659eac

# `runtime_codex_logging.py`

## Summary
- Codex exec と TUI の呼び出し失敗例外を、共通のエラーテキストへ変換する。
- CmocError では概要と詳細をまとめ、それ以外の例外では文字列表現を使う。

## Read this when
- Codex exec または TUI の失敗 event に記録される例外文の扱いを変更・調査するとき。
- CmocError と通常の例外で Codex 呼び出しのエラー記録がどう変わるか確認するとき。

## Do not read this when
- Codex の起動、出力処理、再試行、回復処理、call log の作成方法を調べるときは、それぞれの実行制御側を確認する。
- 端末向け失敗 report の表示や復旧案を調べるときは、共通の例外描画処理を確認する。

## hash
- dbc22241cdd8af0da9bd7074e31f3617345bcf1035252f3a0ed0d40cce7b117e

# `runtime_codex_profile.py`

## Summary
- Codex CLI の起動設定と実行結果の解釈を担い、call ごとの argv・環境変数の組み立て、子プロセスの追跡と終了、schema の配置、JSONL 出力の判定をまとめる。
- 起動時と終了時に共有する subprocess 境界の処理を確認・変更するときの入口。

## Read this when
- agent call の sandbox、Codex CLI 設定や MCP 接続、CODEX_HOME・環境変数の組み立てを変更するとき。
- editing run での Codex 子プロセス追跡、process group の停止や後始末を調べるとき。
- schema の配置、出力 JSON・JSONL の読み取り、resume token や Codex call の成否判定を変更するとき。

## Do not read this when
- quota・一時障害の回復待ち、probe の共有、中断や待機時間の制御が対象なら、回復待ちの調整を担う実装から確認するとき。
- 文書検索・feedback・editor input handoff の MCP サーバー内部の処理が対象で、Codex 起動時の接続設定を変更しないとき。

## hash
- 00bb11146fb8fd28740235ac15715210238cec63ae4e371767d881482c0244c3

# `runtime_codex_recovery.py`

## Summary
- quota・一時障害からの回復待機を管理し、同じ条件の Codex call 間で probe と待機を共有します。
- 待機中の中断伝達、回復イベント記録、理由別の待ち時間集計も担います。

## Read this when
- 回復待機の集約条件や、quota・一時障害の待機中に起きる中断・ログ・時間集計を調べるとき。
- 回復待機へ入る前後の中断状態の伝達や、シグナル handler の設置・復元を調べるとき。

## Do not read this when
- Codex CLI の起動、結果分類、probe の実行、回復後の再開処理を調べるときは、まず runtime_codex_exec.py を読む。
- サブコマンド全体の実行ライフサイクルや interruptible の設定箇所を調べるときは、まず runtime_cli.py を読む。

## hash
- d31ca3cfcce60d91b2449e9d4ff413d9f911650b03b59e2868243a0c8574519b

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出し固有の起動準備、プロセス実行、call log と結果記録をまとめた入口です。

## Read this when
- cmoc から Codex TUI を起動する際の設定検証、作業場所や環境の準備、通知 callback の設定、実行結果の記録やエラー処理を調べるとき。
- TUI 呼び出しに editor input handoff や feedback 用の環境情報を渡す流れを変更するとき。

## Do not read this when
- 共通の Codex CLI 環境、設定上書き、subprocess 起動の挙動を変更するときは、その共通処理を確認するとき。
- 非対話型 Codex exec の出力検証、補正、再開処理を変更するとき。
- TUI 起動前の INDEX 更新や subcommand 側の prompt・引数生成、通知 callback の内部動作を変更するとき。

## hash
- 62811e0fac78a60c799432f482ea88bcb59880589f1a73896fff0f978d61e428

# `runtime_config.py`

## Summary
- cmoc の実行時設定を JSON と設定オブジェクト間で変換し、検証、既定値の補完、読み書き、同期を担う。
- Codex の provider・agent-call 設定や document-search tuning の永続化と、設定エラーの利用者向け処理を扱う。

## Read this when
- 設定 JSON の読み込み・保存・初期化や、不正値の検出と既定値の補完がどこで行われるか調べるとき。
- Codex 設定や document-search tuning が JSON へ変換される際の値検証を確認するとき。

## Do not read this when
- 設定項目の正本となる型や既定値そのものを確認するときは、設定定義を直接読む。
- 設定ファイルの保存先の決まりや、各コマンドでの設定の使われ方を調べるときは、パス解決や呼び出し元の実装から確認する。

## hash
- 823c8d3c8388e53ddd9c3348c9a18ad9538105f7d1b758aa51539e2a2662a2c3

# `runtime_content.py`

## Summary
- ファイル内容・文字列の SHA-256 算出、内容由来の hash 名での保存、読み取り可否と NUL byte による粗い binary 判定を提供する共有 runtime helper 群です。
- symlink の hash ではリンク文字列を対象にし、hash 名での保存では同じ directory 内の一時 file を使って置換します。

## Read this when
- 内容 hash の対象や symlink の扱い、hash 名での保存時の既存 file・symlink の処理、binary 判定の共通動作を調べる、または変更する場合。
- 複数の runtime workflow で共有される hash・保存・binary 判定の primitive 自体を変更する場合。

## Do not read this when
- index 対象の選択、directory hash の組み立て、entry の更新判断だけを扱う場合は、indexing lifecycle の実装から確認してください。
- refactor 調査履歴の同期や Structured Output schema の取得・利用フローだけを扱う場合は、それぞれの workflow の実装から確認してください。

## hash
- 655ad0b996b073ecc238dbb4e924f6d0e8137ef4dbec086d3f7dcc9b36b4d7df

# `runtime_doctor.py`

## Summary
- 各サブコマンドに共通する doctor preprocess の実行、修復ロック、管理パスの保証、runtime state の同期、reporter の事前検証、修復 commit を担います。複数 root と一時 Git index の退避・合成・復元を含む lifecycle の入口です。

## Read this when
- doctor preprocess の処理順、複数 root への適用、失敗時の index 復元、修復差分だけを commit する動作を変更・調査するとき。
- .cmoc/gu の非追跡保証、.agents の追跡保証、config または refactor state の同期、feedback reporter の事前検証が preprocess 全体でどう組み合わさるか確認するとき。

## Do not read this when
- config の検証・読み書き・同期だけを変更するときは runtime_config.py を確認してください。
- refactor state の schema、entry 集合、同期規則だけを変更するときは runtime_refactor.py を確認してください。
- 共通 Git 操作や ignore 規則の実装だけを変更するときは runtime_git.py を確認してください。
- cmoc doctor の CLI 呼び出しやサブコマンド固有の表示・引数処理だけを変更するときは src/sub_commands/doctor.py と src/commons/runtime_cli.py を確認してください。

## hash
- 02cb5143a64b19fb0db7e9c9e097b4e444c0049bbeaad7d1d198cac774a3babc

# `runtime_document_search.py`

## Summary
- 許可された oracle/doc Markdown の安全な読取、索引の差分同期、ベクトル検索と再ランキングを担う検索コア。
- 索引・cache の整合性や排他、期限、検索結果を返す前の原文確認を扱う。

## Read this when
- 許可文書の読取・同期、索引 identity、cache、候補検索や再ランキングの挙動を変更するとき。
- 同期や検索中の排他、期限・取消、索引の解放、結果と現在の原文との整合性を調べるとき。

## Do not read this when
- 閲覧範囲の構築、正規化、許可判定の規則だけを変更するときは、範囲を扱うモジュールを直接読む。
- stdio MCP の初期化、tool 公開、JSON-RPC、要求の取消・終了だけを変更するときは、MCP server の実装を直接読む。
- Node worker の起動や推論資材の準備だけを変更するときは、worker・セットアップの実装を直接読む。検索の意味仕様を確認するときは正本仕様を読む。

## hash
- fcbf47608d06db9e5ff687df5b732fcf5b05250914d5d1df875b5692f1353b74

# `runtime_document_search_mcp.py`

## Summary
- 固定された起動 context のもとで、文書検索 MCP の JSON-RPC 要求を受け付け、検索処理へ渡して応答する stdio server。要求の検証、結果の変換、取消と終了処理を担う。

## Read this when
- initialize・ping・tool discovery・tool call の JSON-RPC/MCP 処理や、引数・応答の扱いを変更するとき。
- 起動引数から work root・閲覧範囲・検索設定を受け取る処理や、検索結果・失敗の MCP 応答への変換を変更するとき。
- 通知、要求取消、stdin EOF、SIGTERM、stdout の protocol 出力を含む server の要求ライフサイクルを変更するとき。

## Do not read this when
- 許可文書の列挙・読取、scope 判定、差分同期、索引、候補検索、推論や再ランキングを変更するときは、検索処理本体から確認する。
- 公開 tool の識別子・入力 schema・設定型・閲覧範囲型の契約を変更するときは、それらを定義する oracle の正本から確認する。
- Codex 設定への MCP server の注入や call ごとの起動 context の組み立てを変更するときは、その設定を担う実装から確認する。

## hash
- 5d6841753907294b90cd4bb838a470515da4b8f735a69d67a851b0f4305576ca

# `runtime_document_search_scope.py`

## Summary
- 信頼された呼び出し元が文書検索に渡す閲覧範囲について、標準範囲の用意、`DocumentSearchScope` の検証・正規化、文書の許可判定を担う共通補助です。

## Read this when
- 文書検索を呼び出す側の実効閲覧範囲を設定・変更するときや、許可・除外範囲の評価を確認するとき。
- 追加の閲覧制限がない呼び出し元向けの標準範囲を確認するとき。

## Do not read this when
- 文書の走査、索引の同期・生成、検索処理が対象なら、それらを担う検索実装から確認してください。
- `DocumentSearchScope` のデータ型や検索の有効化条件、正本仕様上の受け入れ条件を変更する場合は、それらの定義から確認してください。

## hash
- 2544c1eb167662bc018a45e94f967e0efca7e552d8714e3e52eb0ccf8877e19a

# `runtime_document_search_setup.py`

## Summary
- 文書検索用の共有資材を非追跡領域に準備し、固定モデルと実行環境の検証後に利用可能な状態を公開するセットアップ入口です。

## Read this when
- 共有資材の配置・再構築、モデル取得時のサイズやチェックサム検証、実行環境の版確認、実モデルでの互換性検査、またはセットアップ結果の出力を変更・調査するとき。
- セットアップ前に共有保存先の非追跡状態を確かめる処理の流れを追うとき。

## Do not read this when
- 文書の列挙・同期・索引・検索、検索範囲、MCP の要求処理を変更するときは、検索の実行側から確認してください。
- Node worker の推論処理や配布資材そのものを変更するときは、それらの実装・資材を直接確認してください。
- 採用するモデルや実行環境の識別情報、検索の意味仕様を変更するときは、それぞれの正本から確認してください。

## hash
- 1812b1903ea8289c885b4a0de0b36d8448d524471f2eb9c7a815a6650de8bbb5

# `runtime_document_search_worker.py`

## Summary
- 文書検索用の固定資材と Node 実行環境の整合性を検証し、Python から推論プロセスを起動して、要求・期限・キャンセル・終了処理を扱う。
- 推論プロセスとの受け渡しや資材検証など、Python 側の実行境界を変更するときの入口。

## Read this when
- 固定資材のハッシュ・版の照合、推論プロセスへの要求形式、FD 継承、タイムアウト・キャンセル時の停止と回収、応答処理を変更または調査するとき。
- 検索処理の呼び出し元ではなく、推論プロセスの起動と管理の挙動を確認するとき。

## Do not read this when
- 文書の列挙・同期、索引や検索結果の処理、検索 API の挙動を調べるときは、検索処理本体から確認する。
- モデルや Node 資材のダウンロード・配置・互換性プローブを調べるときは、資材準備処理から確認する。
- チャンク分割、埋め込み、再順位付けなど Node 内の推論内容を変更するときは、Node worker の実装から確認する。

## hash
- 31890b29e05c7f35a091d5c03ee8ed8889f657080d687ea3b1cf45820f95fb99

# `runtime_editor_input_handoff.py`

## Summary
- editor input file 一つを対象とする一時 handoff target のサーバー側ライフサイクルを担い、ガイドの保持・取得、送信内容の検証・上書き、終了時の target 無効化とガイド削除を行う。
- 入力 file の安全性と target 固有の受付・後処理を調べる際の入口。

## Read this when
- editor input file の regular file・symlink 検証や、handoff による本文置換の安全性を変更・調査するとき。
- 一時 target の起動、認証済み接続の受付、submission の直列処理、終了時の drain とガイド削除を変更・調査するとき。
- target が保持するガイドの作成・取得と、その期間中の扱いを確認するとき。

## Do not read this when
- editor input の予約、エディタ起動、終了後の本文読み取り・確定保存を調べる場合は、入力編集の呼び出し側から確認する。
- 共有 schema、環境変数、target ID の形式、共通認証・client transport を調べる場合は、handoff protocol の定義へ進む。
- MCP tool の公開、agent 入力の検証、handoff 本文の生成、target への送信を調べる場合は、MCP server 側を確認する。
- agent 向け指示文やガイドの正確な文面を調べる場合は、prompt builder とガイド生成の正本へ進む。

## hash
- 6de2f85902dfd93f0b0786fcafd25fee61571abc12fd1650b8021d3c79b3e93d

# `runtime_editor_input_handoff_mcp.py`

## Summary
- Codex TUI が起動する stdio MCP server の受付点として、ガイド取得と上書きの呼び出しを振り分け、結果を MCP 応答へ変換する。
- 上書きでは、入力と起動元情報から本文を組み立て、同じ repository の active target へ届ける。MCP の受付・中継を扱うときの入口であり、共有 transport や target の実装とは責務が異なる。

## Read this when
- stdio MCP の JSON-RPC 処理、tool の公開・振り分け、入力検証後の結果やエラーの扱いを変更・確認するとき。
- ガイド取得から上書きまでの中継、送信元情報の利用、本文 builder の呼び出し、target への要求送信を追うとき。

## Do not read this when
- 入力 schema、target ID の解釈、認証や socket transport の共通処理を変更するときは、共有 protocol と正本 schema を直接確認する。
- Codex が MCP server を起動する設定、tool の有効化、環境変数の受け渡しを変更するときは、Codex 実行設定を直接確認する。
- ガイドや生成本文の正確な文面・構成を変更するときは、それぞれを定義する正本の builder と仕様を直接確認する。

## hash
- 9f2add3e38e2d306ff499ae271e5f5d7624273e4f742f1862921fc347f00170f

# `runtime_editor_input_handoff_protocol.py`

## Summary
- editor input handoff の共有 protocol 層。正本 schema の読み込み・検証、呼び出し元情報の受け渡し、target の repository routing、認証 transport と応答 framing を担う。
- 複数の handoff runtime が共有する境界や通信仕様を調べる際の入口。target の lifecycle や MCP tool の個別処理ではなく、共通の routing・transport を確認するために読む。

## Read this when
- handoff の schema 読み込み・入力検証の挙動を変更または調査するとき。
- subprocess 環境を介した送信元情報や repository の受け渡しを追うとき。
- target ID の repository 対応、認証 handshake、protocol version、応答 framing を変更または調査するとき。

## Do not read this when
- target の開始・終了、ガイド保持、editor input file の検証や書き込みを調べる場合は、target lifecycle を担う実装から確認する。
- agent 向け MCP tool、tool 呼び出しの処理、項目別入力から本文を作る流れを調べる場合は、MCP interface と本文 builder の実装から確認する。

## hash
- 17d3c7257e2338323ead131a3d0f8beb583dbd014227078b8c17c2fbd1b7e5b3

# `runtime_errors.py`

## Summary
- 共通の実行時例外に利用者向けの説明と診断情報を保持し、診断値の安全な文字列化と簡潔なエラー表示を担う実装層です。
- 個別の失敗条件や通常の終端レポートを定義する場所ではなく、共通例外とログ未初期化時の表示処理を確認する入口です。

## Read this when
- 共通例外が保持する情報や診断値の文字列化・簡易表示の挙動を変更または調査するとき。
- ログ初期化前や CLI 引数解析時にエラーがどう表示されるかを調べるとき。

## Do not read this when
- 特定の操作がどの条件で失敗するか、どの復旧手順を示すかを調べるときは、その処理の実装を直接確認してください。
- 通常の終端レポートの形式やエラー分類の規範を確認するときは、レポート・ログの実装または正本仕様を直接確認してください。

## hash
- 7aebf501056b06c1339e7a20e20c997aec60001f55a492420dbdf02dc935e836

# `runtime_feedback.py`

## Summary
- サブコマンドごとの feedback collector と、Codex call ごとの capability 登録、並列受付、rate limit、終了時の drain を管理する。
- agent observation と許可された machine event の保存連携、利用不能時の非致命な degraded 動作、reporter/collector の doctor 検査を扱う。feedback の実行時ライフサイクルと event detector を確認する入口。

## Read this when
- feedback を invocation や Codex call に紐づける処理、並列受付や終了時の drain、accepted observation の連携を変更・調査するとき。
- reporter/collector の利用可能性検査や、stable event を machine observation に変換する detector の条件を確認するとき。

## Do not read this when
- agent に公開する MCP request handling や payload の転送契約を調べるだけなら、MCP reporter の担当箇所を直接読む。
- payload schema・検証、secret redaction、path evidence、immutable observation の生成や保存を調べるだけなら、observation storage の担当箇所を直接読む。

## hash
- 847c2b8a0b1acb62d7737dda1971470d944fe7685bbd2d0da83d02bb013f30d9

# `runtime_feedback_intake.py`

## Summary
- 保存済み feedback observation の受理順序と intake 境界を管理し、remediation wave へ渡す pending input を確定する。publication 後は、処理済み observation の受理記録の cleanup も担う。

## Read this when
- observation の durable な受理順序、wave に含める入力境界、または publication 後の受理記録 cleanup を調べるとき。

## Do not read this when
- observation payload の検査・masking・raw 保存や collector の受付 lifecycle を調べるときは、それらを担う raw store・collector 側から確認する。
- wave の処理内容、run artifact、checkpoint、report cut、publication state を調べるときは、remediation・run state・feedback state 側から確認する。

## hash
- d730f6473bea9a4f073c847ff531d9441da323b88e7ab22bff7e38c078e740e6

# `runtime_feedback_reporter.py`

## Summary
- Codex call ごとの stdio MCP endpoint として `submit_observation` を公開し、JSON-RPC request を処理して loopback collector へ送信し、その応答を検証して返す。
- 担当範囲は reporter 側の MCP protocol と collector への通信境界。collector の call 管理や observation の検証・保存を調べる入口ではない。

## Read this when
- `cmoc_feedback.submit_observation` の初期化、tool 公開、call 処理、JSON-RPC response を調べるとき。
- reporter から collector への引き渡し、接続に必要な実行時 context、通信失敗や collector 応答の扱いを調べるとき。

## Do not read this when
- 入力項目や制約、observation の受理条件・redaction・保存形式を調べるときは、正本の入力 schema と feedback 仕様、collector/store 層を読む。
- reporter の起動、call ごとの環境設定、Codex MCP 設定への組み込みを調べるときは、実行時の invocation/profile 統合を読む。

## hash
- 0dd124d5c38a80dfd33af41625b587248d28cbfe98a57b1d9450903d751c0f26

# `runtime_feedback_run_state.py`

## Summary
- feedback report run の intake wave、seal、join に関する immutable artifact の保存・参照・整合性検証を担う。
- run manifest の追記・回復規則と、remediation checkpoint の監査記録・判定根拠の検証をまとめる。

## Read this when
- feedback run の wave や seal/join artifact の保存、参照、hash 検証、manifest との整合性を調べるとき。
- artifact 保存後に manifest 更新が中断した場合の回復や、run manifest の追記専用規則を確認するとき。
- remediation checkpoint の検証、issue の判定根拠、再確認履歴や監査記録の整合性を調べるとき。

## Do not read this when
- active generation、current pointer、publication 全体や cleanup の状態遷移を調べるときは、feedback state 全体を管理する実装から読む。
- feedback report の修復手順、commit・rollback、join・finalization の制御フローを調べるときは、その処理を調整する subcommand 実装から読む。
- 実装の挙動ではなく要求の正本を確認するときは、この実装が根拠としている feedback state の oracle 仕様を読む。

## hash
- 0404f94e892378154337bd1f7a78b743a2ad2a3013549ee94d88c531b1ea22cc

# `runtime_feedback_state.py`

## Summary
- Raw observation の envelope、issue と machine aggregate、report cut、active generation／current pointer の整合性を検証し、publication、cleanup、cut の破棄を扱う。
- report cut から generation の切替後まで、永続 state をまたぐ復旧と遷移の一貫性を追う入口。

## Read this when
- current pointer が選ぶ active state や issue・aggregate record の検証、破損調査をするとき。
- report cut の固定入力、checkpoint、incomplete 診断、再開・復旧の整合性を調べるとき。
- generation の公開、current pointer の切替、切替後の cleanup、未公開 cut の破棄を変更・調査するとき。
- feedback raw observation の envelope 検査規則を確認するとき。

## Do not read this when
- invocation collector、call-scoped reporter、detector の受付や停止だけを扱うときは、それらの lifecycle を担う対象へ進む。
- raw observation の受付 schema、secret masking、path fingerprint、immutable 保存だけを扱うときは raw store の対象へ、receipt の順序や high-watermark だけを扱うときは intake の対象へ進む。
- feedback run の wave、seal、join、run artifact の保存・検証だけを扱うときは run state の対象へ進む。
- CLI の操作手順や Markdown report の内容・表示だけを扱うときは、subcommand の orchestration または report 生成を担う対象へ進む。

## hash
- b9e12ba3380ce025ad0f63bc7b211b53e3cec0061e94c1787ad86db49932ac93

# `runtime_feedback_store.py`

## Summary
- agent と機械 rule の feedback observation を検証し、secret masking と evidence path の処理を経て immutable raw record として保存する。raw observation の列挙と未処理件数の計算も担う。

## Read this when
- observation の受理検査、secret masking、repo 内 evidence path の正規化や fingerprint、raw record の保存・回復を調べるとき。
- raw observation の列挙や、未処理件数と通知条件を調べるとき。

## Do not read this when
- MCP の JSON-RPC transport、agent-facing tool 結果、capability の受け渡し、Codex call の開始・終了が対象なら、reporter/client または collector lifecycle の担当箇所から読む。
- durable な受理順序と high-watermark の receipt 管理、または report cut・active state の検証や publication が対象なら、それぞれの担当箇所から読む。

## hash
- cd470dabdd57221f2964d0db231c6a7ddd75aa12302e26a85ca77bbbaf894062

# `runtime_git.py`

## Summary
- Git コマンド、branch 状態、worktree の安全な作成・削除、作業状態の snapshot を扱う共通境界です。
- Git ignore の確認と `.cmoc/gu` の除外保証、および nested repository を考慮した oracle/realization file の列挙・分類を担います。
- コマンドや上位の run・doctor・refactor 処理から呼ばれる低水準の Git 処理を確認する入口です。

## Read this when
- Git コマンドの実行結果、branch や worktree の検証、未コミット差分の判定を変更・調査するとき。
- worktree の作成・削除や snapshot の取得・復元に関する挙動を確認するとき。
- ignore 判定、`.cmoc/gu` の除外、または oracle/realization file の列挙・分類を変更・調査するとき。

## Do not read this when
- repository/work root や cmoc の保存先、cwd 切替などの path 解決が対象なら、runtime_paths の処理から確認するとき。
- run、doctor、refactor など上位コマンドの処理手順や判断が対象で、Git の低水準処理に関係しないときは、それぞれの担当モジュールから確認するとき。
- 利用者向けエラーの構造や表示、コマンド結果モデルだけが対象なら、runtime_errors または runtime_results から確認するとき。

## hash
- 4f9a8ec28d7dd8c79abfa768244ffe15c2ec2ce41879d84503cf893d8c06900d

# `runtime_logging.py`

## Summary
- サブコマンド単位の JSON Lines イベント、警告、step 計測、待機時間を記録し、後続処理が参照するイベント記録を提供する。
- ネストした runtime helper から現在の logger を任意に参照・差し替えできるようにする。

## Read this when
- イベントの記録・flush 順序、並行書き込み、終端イベントの回復、警告処理を変更するとき。
- step 計測、待機時間の集計、または実行中 logger の共有方法を変更するとき。
- 診断ログとイベント記録がレポートや feedback 検出へ渡る流れを追うとき。

## Do not read this when
- ログ保存先、パス予約、時刻表記、経過時間の整形だけを変更するときは、それらを担う runtime の共通機能を読む。
- feedback の受付・収集・判定・保存の仕様や動作を変更するときは、その一連の処理を担う機能を直接読む。
- サブコマンドの起動・終了処理や終端結果の分類を変更するときは、実行ライフサイクルを統括する機能を読む。
- primary report の項目、描画、保存を変更するときは、レポートを担う機能を読む。
- Codex call の起動や再試行・回復の動作を変更するときは、その実行・回復を担う機能を読む。

## hash
- 17aa6c7d735a6dc9a11efaca54d933225621da3bb0f035f427af123401ad933f

# `runtime_merge_conflict.py`

## Summary
- run と session の join で共有する、Git merge 競合の検出・解消確定処理を担う。内容競合の agent 委譲、refactor 管理 state の競合統合、変更範囲と競合 marker の検証、merge commit までを確認する入口。

## Read this when
- merge 後の未統合 path がどう解消・検証・commit されるかを変更または調査するとき。
- 内容競合と refactor 管理 state の競合が、共有処理でどう分けて扱われるか確認するとき。

## Do not read this when
- 競合発生前の merge 条件、run/session 固有の手順、agent へ渡す指示を調べるときは、該当する join の流れや指示構築へ進む。
- refactor state の通常の schema 検証や同期規則を調べるときは、その state 管理処理へ進む。

## hash
- cdf6c156f1e9c632c5d1c4fee1499815414f77f138dae2aba909c3264b93892e

# `runtime_paths.py`

## Summary
- repository/worktree root の実行時解決を起点 path に対応させ、cmoc 管理データの保存先と memo 配下の判定を提供する。
- 実行時刻・経過時間の整形と、process-wide な cwd 切替の直列化・復元を担う。

## Read this when
- root 解決で起点 path がどう扱われ、解決失敗がどう実行時エラーになるかを確認するとき。
- cmoc 管理データの保存先の導出や、tracked / untracked の区分、memo 配下の判定を確認するとき。
- 時刻・経過時間の表記や、時刻付き path の重複予約を調べるとき。
- 一時的な cwd 切替の排他制御、復元、切替中かどうかの判定を調べるとき。

## Do not read this when
- root placeholder の定義や共通の path 解決規則そのものを調べる場合は、共有 path model の項目から確認する。
- 実行時エラーの保持形式や描画を調べる場合はエラー処理の項目を、個別コマンドの保存データ形式を調べる場合はそのコマンドや schema の項目を確認する。

## hash
- 8a017cb7f721c5291df27f535e8fb948d67d887ae9abd5b0a167fb4d91e5a0d3

# `runtime_primary_report.py`

## Summary
- 非対話サブコマンドの終了時に、一次報告用の invocation 情報を集め、保存済み報告を確認して実行記録を補うか、未作成なら fallback 報告を生成・保存する共通処理を担う。
- 報告の保存確認と既存報告の安全な更新も扱う。個別コマンドの項目定義や本文描画ではなく、報告の生成・保存ライフサイクルを調べる入口となる。

## Read this when
- サブコマンドの終了経路で、保存済み報告の検証・実行記録の追記や fallback 生成がどう行われるかを確認・変更するとき。
- invocation 中に確定した項目と終了結果からの値をどう集約するか、または報告の保存失敗がどう扱われるかを調べるとき。
- 予約済みパスへの保存、保存済み内容の検証、既存報告の置換方法を確認するとき。

## Do not read this when
- コマンドごとの報告先・必須項目・テンプレートを決めるときは、個別報告の定義を担当する箇所から確認する。
- 報告本文の Markdown 構成や実行記録の描画・エスケープを調べるときは、描画を担当する箇所へ進む。
- ある項目の値が特定コマンドの処理中にどこで決まるかを追うときは、その値を設定するコマンド処理を確認する。

## hash
- b93e848cca2f1e31b4783371cac8bf5d79ed8e1efc773d878d6ce3f99b5cbdc8

# `runtime_primary_report_render.py`

## Summary
- 個別の report 定義を受け取り、fallback primary report の本文を Markdown と YAML front matter で描画する。サブコマンド別の結果に、終端状態・warning とエラー・次の操作・関連ログをまとめる。
- Codex call の保存済み最終出力と受理済み feedback observation を実行記録に整形する。他の report writer が使う実行段階・関連ログ・YAML 値の描画 helper も提供する。

## Read this when
- fallback primary report のサブコマンド別本文や、終端結果・warning とエラー・次の操作の表示を変更するとき。
- 実行記録に載る Codex 出力や受理済み observation の整形、または他の report に共用される実行段階・関連ログ・YAML 値の表示を変更するとき。

## Do not read this when
- どのコマンドに fallback report を適用するか、保存先・項目定義や保存・更新処理を変更するときは、report 定義または保存処理の実装から確認する。
- editing run の fork・join・abandon report 固有の内容や保存構成を変更するときは、その report writer を直接確認する。共通表示 helper の変更時だけここを確認する。

## hash
- 71c2106a9dc594976576a21dc4945dea0d5bfc12ca7024ae3ae9adf771b26bef

# `runtime_primary_report_specs.py`

## Summary
- 非対話サブコマンド向け fallback primary report の個別定義を集約し、コマンド名から各 report の保存先や役割、描画に使う定義を引く入口。保存処理や本文生成そのものではなく、コマンドごとの定義を担う。
- TUI 通知境界のサブコマンドと oracle investigation は登録対象外。

## Read this when
- 非対話サブコマンドの fallback primary report の有無や個別定義を追加・変更し、共通処理が選ぶ定義を確認するとき。

## Do not read this when
- report の保存・検証や共通情報の組立を調べるときは、その実行処理へ直接進む。
- 選択済み定義から report 本文を組み立てる方法を調べるときは、描画処理へ直接進む。
- TUI 通知や oracle investigation の report を調べるときは、それぞれの処理へ直接進む。

## hash
- 00b9f9f90e771fda23daba3ad22f7298a8c55ee722b50bc244c83d4ef0920192

# `runtime_refactor.py`

## Summary
- oracle／realization file ごとの refactor 調査 state を検証・読み込み・保存し、ファイル集合と内容ハッシュに応じて調査要否を同期する。
- 調査対象の選択と、新しい調査サイクルで全対象を調査必須にする処理を担う。

## Read this when
- refactor の調査履歴 state の検証・永続化や、変更された file を再調査対象にする条件を確認・変更するとき。
- 次に調査する対象の選択順や、調査サイクルの開始時に対象を再設定する処理を確認・変更するとき。

## Do not read this when
- oracle／realization file の列挙や分類の動作だけを確認・変更するときは、Git による file 分類を担う境界を読む。
- state の保存先だけを確認・変更するときは、path を定義する境界を読む。

## hash
- ce6d02c55f306b2ef28ece6045424dd668556d9e5a880211f5224de89953f27d

# `runtime_results.py`

## Summary
- CLI・外部コマンド・Codex exec が共有する結果データのモデルを定義する。最外側サブコマンドの終端情報、コマンド実行結果、Codex exec の出力と実行情報、Structured Output の検証エラーを扱う。
- Codex exec の Structured Output を呼び出し側が参照するための最小契約も提供する。

## Read this when
- 共有する結果データの構造や整合性条件を変更するとき。
- Codex exec または外部コマンドの結果をどの形で保持し、利用側へ渡すかを追うとき。

## Do not read this when
- コンソール表示、report、ログ、terminal result の意味や規則を確認・変更するときは、出力規則の正本を直接読む。
- Codex exec の呼び出し、Structured Output の補正、再実行などの規則を確認・変更するときは、Codex exec の正本仕様を直接読む。
- 特定サブコマンドの処理手順や結果値の設定方法を変更するときは、そのサブコマンドの実装へ進む。

## hash
- 0e0e254cc674e01b2d54a82f64802d073e4e04634d506c59efc79455c25330b8

# `runtime_run.py`

## Summary
- editing run で共有する worktree の解決、lifecycle lock、process tracking と停止・cleanup を担う共通 runtime の入口。
- 個々の run command の手順ではなく、複数の経路が使う worktree と process cleanup の振る舞いを調べる対象。

## Read this when
- session branch や run branch から worktree を安全に特定する条件、または managed run worktree の検証を調べる・変更するとき。
- editing run 本体や追跡中の Codex child の identity、tracking file、停止、残存 process group の cleanup を調べる・変更するとき。
- session 操作と editing run の開始・終了で共有する lifecycle lock を調べる・変更するとき。

## Do not read this when
- run の開始、状態遷移、差分検査、commit、join・abandon の実行順や cleanup 方針だけを調べる・変更するときは、lifecycle orchestration や該当 command の処理へ進む。
- OS process identity、signal、process group 操作、Codex subprocess の起動・追跡といった下位 primitive だけが対象なら、その Codex runtime helper へ進む。この対象はそれらを run 単位の tracking と cleanup に組み合わせる。
- 利用者向け command semantics を確認するときは command 定義と該当する正本仕様へ進む。ここは共通 runtime の実装を扱う。

## hash
- e4b79dd7896358d8e93f2bde8bb0c9e1a3698c3d4ac4aee8d1405cb328391624

# `runtime_run_join.py`

## Summary
- editing run を session に取り込む共通 runtime 処理です。明示的な run join と feedback remediation の自動 join で使われ、doctor の修復差分の識別、差分検査、merge、post-join の refactor state 同期を担います。
- join 失敗時の session worktree 復元と、merge 済み run の worktree・branch の条件付き cleanup も扱います。active run の選択や workload 固有の完了処理は呼出元が担います。

## Read this when
- 明示的な run join と feedback remediation の自動 join に共通する差分検査、force-resolve、merge、state 同期の挙動を調べたり変更したりするとき。
- merge や post-join の失敗からの復元、または merge 済み run 資源の cleanup 条件を確認するとき。

## Do not read this when
- cmoc run join のコマンド固有の処理順、lock、state・report の完了処理を確認するときは、run join のコマンド実装を読む。
- feedback remediation の wave 処理、manifest、join intent の確定が主題なら、feedback workflow を読む。
- session join の統合処理、または merge 競合の解消アルゴリズムや agent 向け指示が主題なら、それぞれの専用実装を読む。

## hash
- 5fe9ee153680f8ccf773d3a4d0da84d85d9b0078f363b36b52d33d43d3aa20ef

# `runtime_run_lifecycle.py`

## Summary
- editing run の開始、active context の解決・復旧、state 公開と、run 作業単位の commit／rollback や差分 path 分類を担う共通処理。
- 複数の workload や run 処理が共有する lifecycle 基盤であり、個別コマンドの進行や join／merge の実処理は担当しない。

## Read this when
- editing run の開始・復旧・state 遷移や、session と run の branch／worktree の検証を変更するとき。
- workload ごとの許可差分や、run branch の想定外差分の判定を変更するとき。
- 共通の commit／rollback 処理や Git 差分 path の抽出を変更するとき。

## Do not read this when
- join／merge の検査・競合解決・cleanup の処理だけを変更するときは、join 処理を担う共通 helper から確認するとよい。
- 個別コマンドの引数、表示、実行手順だけを変更するときは、該当する subcommand の実装から確認するとよい。

## hash
- eb394ac87d1a669f27b513bda8b130e6fb7dbe7a17950b5795ec01c857d8de95

# `runtime_run_report.py`

## Summary
- 編集 run の fork・join・abandon report を Markdown と YAML Front Matter で組み立て、保存する共通処理。
- 実行段階や関連ログ、変更 path の描画も担うため、個別コマンドの処理ではなく共有 report の形式や保存を確認するときの入口。

## Read this when
- realization apply/refactor の fork report の構成や保存を調べる、または変更するとき。
- run join/abandon report の共通項目、詳細、ログ、変更 path の表示を調べる、または変更するとき。

## Do not read this when
- run の state 遷移、branch/worktree 操作、merge、cleanup 自体を変更するとき。該当する lifecycle の処理から確認する。
- 他のサブコマンド向け fallback report の生成や汎用 rendering を調べるとき。fallback report の実装から確認する。

## hash
- 8bd3e53a80b180d5efe443146380e27977953c9217da1758b3cc7bb411e15793

# `runtime_state.py`

## Summary
- session と編集 run の永続状態モデルを定義し、JSON の構造や値を検証して読み書きする。
- branch 名から session state を特定する共通処理、home branch に紐づく active session の検索、session lifecycle 用の排他 lock を提供する。

## Read this when
- session/run state のスキーマ、読み書き、妥当性検証、branch に基づく state 解決を調査・変更する場合。
- active session の検索や session lifecycle で共有する排他 lock の役割を確認する場合。

## Do not read this when
- 個別の session コマンドの事前条件、branch 操作、状態遷移、終了報告を調べる場合は、該当コマンドの仕様と実装から読む。
- 編集 run の開始から join または abandon までの処理順や workload 固有の挙動を追う場合は、run lifecycle 共通処理または対象 workload の仕様と実装へ進む。

## hash
- 5ea0c7423ab0802ad641c4ab0261df8daafb98ae165de6a3cd56223766a955b0

# `runtime_windows_toast.py`

## Summary
- Windows toast の送信と Codex TUI 完了通知 callback の実行を担い、通知に含める情報、対象 session の判定、turn の重複排除、一時 state の管理を行う。
- 通知処理の失敗を呼び出し元の処理結果へ波及させない境界でもある。

## Read this when
- Windows toast の transport や表示文面、通知失敗時の扱いを変更・調査するとき。
- Codex TUI callback の root session 判定、turn の重複排除、callback state の作成・破棄を変更・調査するとき。

## Do not read this when
- TUI 起動時に callback を登録する条件や hook command の渡し方を調べるときは、TUI process の起動を組み立てる側から確認する。
- サブコマンドの terminal state を決めて通知を呼び出すタイミングを調べるときは、サブコマンド実行を管理する側から確認する。

## hash
- ec2ff9d13fb19e614e1d22b439fa0d5470ba01bdaeddf51c7c37a9bba7130fde
