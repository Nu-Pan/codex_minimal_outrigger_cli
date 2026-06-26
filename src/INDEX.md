# `acp`

## Summary
- AI エージェント呼び出しに渡すパラメータとプロンプト本文を構築する実装領域。用途別の role、goal、補助入力、ファイルアクセス制約、モデル種別、reasoning effort、Structured Output schema への接続と、共通の標準プロンプト部品の組み立てを扱う。
- 差分要約、所見列挙・修正依頼、oracle review、merge conflict marker 解消、TUI 実行前のパラメータ選定、INDEX.md エントリー生成など、各機能が AI agent に何を読ませ、どの制約で何を返させるかを追う入口になる。

## Read this when
- cmoc の機能が AI agent を呼び出す際の role、summary、goal、補助 prompt、対象パス・差分・所見などの埋め込み内容を確認または変更したいとき。
- AI agent に適用するファイルアクセスモード、標準プロンプト部品の注入条件、モデル種別、reasoning effort、Structured Output schema の対応付けを調べたいとき。
- apply 系の差分要約、ファイル単位の所見列挙、検出済み所見への修正依頼など、実装レビュー後段の agent call 条件と出力契約を追いたいとき。
- oracle review で新規所見列挙、所見の根拠補強、採否判定、所見統合を生成させる prompt と、oracle standard や review standard の提示方法を確認したいとき。
- session join の conflict marker 解消、TUI 実行前のファイルアクセスモード判定、INDEX.md エントリー生成など、特定用途の事前判断や生成を AI agent に依頼する prompt を実装・検証したいとき。
- oracle file と realization file の基本概念、ファイルアクセス規則、ルーティング規則、oracle standard、realization standard、review standard、apply review standard、index entry standard を AI に渡す文書部品としてどう構成しているか確認したいとき。

## Do not read this when
- CLI サブコマンド全体の実行順序、引数解析、状態保存、git 操作、フォーク作成・統合、merge conflict marker の検出など、AI agent 呼び出しパラメータ構築の外側を調べたいとき。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、StructDoc、Standard、Requirement などの基本データ型そのものの定義や変換処理を変更したいとき。
- oracle file や realization file の個別本文、実際の仕様断片、実装対象コード、テスト対象コードを読みたいだけで、AI に渡す prompt の構成を扱わないとき。
- path model の解決規則、実パス変換、ルート概念の定義、Markdown rendering の一般処理を調べたいとき。
- agent call の実行、返却結果の保存、Structured Output のパース後処理、生成された所見や要約の利用側フローを追いたいとき。
- 生成済み INDEX.md の内容評価や、対象本文を読むべきかというルーティング判断だけを行いたいとき。

## hash
- ba701ba2f3da5c9a0e9ed951f5fcaf40996fffcf3e63cf202458c25f1088eba2

# `basic`

## Summary
- cmoc の実装全体から共有される基礎データ型と小さな変換処理を集めた領域。エージェント呼び出しの論理パラメータ、root token 付きパス表記と実パス解決、規範文書を表す構造、階層化された自然言語文書の Markdown 生成部品を扱う。
- 外部コマンド実行、CLI サブコマンドの制御、具体的なバックエンド向け変換、個別仕様本文ではなく、それらの上位処理から参照される共通モデルと文書組み立て部品への入口になる。

## Read this when
- cmoc 内部で共有する論理的なエージェント呼び出しパラメータ、モデル区分、reasoning effort、ファイルアクセス区分の保持形式を確認または変更したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の意味、探索条件、root token 表記と絶対パスの相互変換、相対パス拒否などのパス解決境界を確認したいとき。
- oracle standard や realization standard のような規範を、背景・要求・判断例を持つ構造として保持し、構造化文書へ変換する処理を確認したいとき。
- 見出し階層、本文文字列、コードブロックから Markdown を生成する基本部品や、三重引用文字列の正規化、空行圧縮の挙動を確認したいとき。
- 上位機能の実装で、まず共有プリミティブ側の型・例外条件・責務境界を確認する必要があるとき。

## Do not read this when
- CLI サブコマンドごとの引数処理、実行フロー、入出力 schema、永続状態操作を調べたいとき。
- バックエンドが受理する具体的なモデル名、権限指定、外部コマンド呼び出し形式への変換ロジックを調べたいとき。
- プロンプト本文のテンプレート、タスク種別ごとの文章生成、Structured Output schema ファイル自体の内容を確認したいとき。
- 個別の正本仕様断片や規範本文そのものを読みたいとき。ここでは規範を表す実装部品だけを扱う。
- 既存 Markdown の解析、ファイル探索、INDEX.md 生成、oracle file と realization file の分類など、共有モデルを使う側の具体的な機能を調べたいとき。

## hash
- 69cdd9fa789cc919411103bc3418deb681bfe2f40a7a138b0cf78eff94af9798

# `cmoc_runtime.py`

## Summary
- 公開モジュール名を既存の実体モジュールへ差し替えるだけの互換レイヤー。実装本体は別モジュールに委譲し、この入口から import する利用者にも同じ実体を見せるために、実行時のモジュール登録を置き換える。
- 既存の呼び出し元や配布設定が古い import path を参照している期間だけ残す移行用コードであり、責務別の実行時モジュールまたは実体モジュールへ参照元が移った後は削除対象になる。

## Read this when
- 公開されている古い import path と実体モジュールの対応関係を確認したいとき。
- 互換 import path を残す理由、削除条件、または移行状況を調べるとき。
- この入口を import した場合に、どのモジュール実体が利用されるかを確認したいとき。

## Do not read this when
- 実行時処理そのもののロジック、設定解釈、状態操作、CLI 挙動を調べたいとき。この対象は実装本体ではなく委譲だけを行う。
- 新しい実行時機能を追加・修正したいとき。互換入口ではなく、実体側または責務別の実行時モジュールを読む方が直接的である。
- 互換 import path の削除可否と無関係な一般的なモジュール探索やパス定義を調べたいとき。

## hash
- a36ad0b5d09cbe7d2be546fdafcd27ff3ddaf803744331274a69fb25f15cd7ee

# `commons`

## Summary
- cmoc の共有ランタイム支援を集約する実装領域。CLI サブコマンド共通ライフサイクル、Codex exec/TUI 呼び出し、設定入出力、内容 hash、共通エラー、Git 操作、ログ、root/path 解決、実行結果型、session state など、複数の上位機能から使われる低レベル runtime helper を扱う。
- 公開 import の集約入口と、責務別の実装本文が同じ階層に置かれており、共通 runtime API の露出範囲を確認する入口にもなる。

## Read this when
- CLI サブコマンドに共通する開始・完了表示、終了コード化、例外表示、サブコマンドログ、現在 logger の扱いを確認または変更したいとき。
- Codex CLI の exec または対話起動について、profile/schema 準備、subprocess 実行、call log、Structured Output 検証、capacity/quota retry、resume 継続、失敗時例外化などの runtime 制御を調べたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正 JSON や不正値のエラー化、Codex profile 生成、CODEX_HOME 検証、sandbox/permission profile 変換を確認したいとき。
- ファイル内容 hash、内容ベース保存、binary 判定、root/path 解決、cmoc 管理ディレクトリやログ・state・config の配置規則、timestamp/duration 表示を扱う共通処理を探すとき。
- cmoc 共通の利用者向けエラーレポート、Git command wrapper、worktree/branch 操作、Git ignore 判定、JSON Lines 実行ログ、quota 待機時間集計、実行結果型、session state JSON 入出力を確認または変更したいとき。
- 複数の runtime helper をまとめて import する公開面を確認し、共通 runtime API へ公開要素を追加・削除・移動する必要があるとき。

## Do not read this when
- 個別 CLI サブコマンドの業務ロジック、引数定義、dispatch、利用者向け通常出力だけを調べたいときは、サブコマンド側の実装へ進む。
- path キーワードそのものの概念定義や oracle/realization の正本仕様を確認したいときは、仕様側の path model や関連 oracle へ進む。
- INDEX.md の生成内容、エントリー生成プロンプト、ルーティング文書の仕様、indexing 本体の探索・更新ロジックを調べたいときは、indexing を担う実装または仕様へ進む。
- 設定値のデータクラス定義、Agent 呼び出しパラメータ、FileAccessMode、モデル名や reasoning effort の列挙値そのものを確認したいだけなら、それらの基本モデル定義へ進む。
- ログや state を読む側・集計する側・表示する側、または Codex 実行結果を利用する上位 workflow の挙動を知りたいときは、その利用側の実装へ進む。
- Git 操作、Codex 呼び出し、path 解決、設定入出力などの具体的な外部挙動をテスト観点で確認したい場合は、対応するテストへ進む。

## hash
- 7b8a10f7bcb0ba22735ae790ab257c26754e7c6d9badf9b3f3542da73d0690eb

# `config`

## Summary
- 開発対象リポジトリごとに変わる cmoc 設定を表す dataclass 群を扱う領域。
- AI エージェント呼び出しの並列数、Codex CLI 向けモデル名と reasoning effort、apply fork と review oracle のループ上限など、永続化される設定値の既定値を確認する入口になる。
- 人間が編集するリポジトリ別設定面に含まれる値の定義を追うための対象であり、設定ファイルの入出力処理そのものは別領域に分かれる。

## Read this when
- リポジトリ別に保持される cmoc 設定項目や既定値を確認・変更したいとき。
- 初期化時に生成・同期される設定ファイルへ含める値や、Enum 系の値を JSON 保存向けに扱う前提を確認したいとき。
- Codex CLI に渡すモデル名、reasoning effort 名、AI 呼び出し並列数、apply fork や review oracle の処理回数上限を調整したいとき。

## Do not read this when
- CLI 引数、サブコマンド構文、実行時の入出力フローを調べたいだけのとき。
- 設定ファイルの実際の読み書き、JSON 変換処理、または `.cmoc` 配下のパス解決処理を調べたいとき。
- oracle file、realization file、パスキーワード定義、INDEX.md 生成ルールそのものを確認したいとき。

## hash
- 324dfe3034cabedbb119cb79c0c59fcdd422ac0747dbbc5e095eba5140bb0d71

# `main.py`

## Summary
- Typer による cmoc の最上位 CLI 入口を定義し、`session`、`apply`、`review` などのサブコマンド階層と各 command から実装関数への委譲を束ねる。
- 補完時を除く通常の Click 引数解析エラーを cmoc 共通のエラーレポート形式へ変換する Typer group を含む。
- console script 実行時に cmoc のコマンド名で Typer app を起動する薄いエントリーポイントである。

## Read this when
- cmoc の公開 CLI コマンド構成、サブコマンド名、option 名、または command から呼ばれる実装関数の対応を確認したいとき。
- CLI 引数解析失敗時のエラー表示、終了コード、補完時の例外扱いを調べるとき。
- 新しい top-level command、サブコマンド階層、または Typer command 入口を追加・削除・改名するとき。
- console script から cmoc がどの Typer app を起動するかを確認するとき。

## Do not read this when
- 個別コマンドの実際の処理内容、状態更新、git 操作、worktree 操作、review 実行内容を知りたいだけなら、ここではなく各 command の委譲先実装を読む。
- cmoc の共通エラー型やエラー描画の詳細を変更したいだけなら、ここではなく runtime 側の定義を読む。
- INDEX.md 生成処理そのもの、oracle review の実行ロジック、session/apply の join/fork/abandon の内部仕様を調べたいだけなら、対応する下位実装を直接読む。

## hash
- 1ae81e8854b36901ae139d89729fd33b79be4d1d5836d0a7f352c4e8c307c293

# `sub_commands`

## Summary
- CLI サブコマンドの実行本体をまとめる領域。初期化、TUI 起動、INDEX 保守、oracle review、session 操作、apply 操作など、利用者が呼び出す上位コマンドの実行フローと runtime 連携への入口になる。
- 各サブコマンドは、事前条件検査、branch・worktree・state・report・出力の制御を担い、詳細な共通処理や Codex 呼び出し用 parameter 生成は下位または別領域の helper に委譲する。
- apply と session はさらに下位ディレクトリへ分かれ、review oracle は対象列挙、実行 loop、INDEX 差分 commit、report 生成などの責務別モジュールへ分かれているため、サブコマンド単位で読む先を選ぶための分岐点として使う。

## Read this when
- 利用者が実行する cmoc サブコマンドの上位フロー、実行前条件、runtime との接続、成功時出力、失敗時の扱いを調査または変更したいとき。
- init、tui、indexing、review oracle、session、apply のうち、どのサブコマンド実装へ進むべきかを切り分けたいとき。
- branch、worktree、clean worktree、session state、apply state、review report、INDEX 更新 commit など、サブコマンド実行に伴う状態遷移や git 操作の入口を探したいとき。
- review oracle の対象列挙、finding loop、INDEX 変更処理、report 生成のどの責務を読むべきか、または apply/session の下位操作のどれを読むべきか判断したいとき。
- CLI から呼び出される処理の統括層と、共通 runtime helper や parameter builder などの下位実装との境界を確認したいとき。

## Do not read this when
- git command wrapper、path 解決、config 読み込み、timestamp、reports directory、state file 永続化など、複数サブコマンドで共有される runtime 基盤そのものを調べたいとき。
- Codex に渡す prompt、AgentCallParameter、Structured Output parameter、complete prompt 生成規則の本文だけを確認したいとき。
- CLI 全体の Typer app 登録、コマンド宣言、引数定義の全体像だけを調べたいとき。
- oracle file の正本仕様、realization 品質基準、INDEX.md 生成規則など、実装ではなく仕様文書を確認したいとき。
- 特定サブコマンドの下位責務が既に分かっており、apply、session、review loop、review targets、review report、review index などの個別モジュールを直接読めば足りるとき。

## hash
- 71ae4d9faefb9bb5d206bf4f28a07f1a47e98cad09e5d9b4b59dfd71b7fc79c9
