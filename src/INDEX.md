# `acp`

## Summary
- AI エージェント呼び出しに関する実装領域。用途別の呼び出しパラメータ構築と、agent に渡す prompt 部品の構築を扱う。
- apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成などで、role、goal、補助入力、読み書き権限、モデル設定、Structured Output 契約、標準規則文をどのように agent へ渡すかを確認する入口となる。
- CLI 実行制御、git 操作、仕様本文、汎用データ構造そのものではなく、AI agent へ渡す内容と制約を組み立てる責務に絞られた領域。

## Read this when
- cmoc の機能が AI agent を呼び出す際に、どの prompt、入力情報、ファイルアクセス条件、モデル設定、出力 schema を使うか確認・変更したいとき。
- apply 系の後段処理、oracle review、session join の conflict 解消、TUI 実行前判定、INDEX.md エントリー生成など、特定用途の agent 呼び出し条件と出力契約を追いたいとき。
- agent に渡されるファイルアクセス規則、ルーティング規則、oracle/realization の基本概念、標準文、レビュー規範、INDEX.md エントリー生成規範などの prompt 文面を確認・変更したいとき。
- 標準 prompt 群や追加 prompt が完全な agent prompt に組み込まれる依存関係、注入位置、表現のサニタイズを調べたいとき。

## Do not read this when
- サブコマンド全体の実行順序、CLI 引数解析、git 操作、フォーク作成・統合、merge conflict marker 検出、生成結果の保存など、agent 呼び出しパラメータ構築の外側を調べたいとき。
- oracle file、realization file、review standard、apply review standard、realization standard など、prompt に含められる標準文書や仕様本文そのものを読みたいとき。
- StructDoc、Standard、Requirement、FileAccessMode、RootToken、AgentCallParameter など、基盤データ構造や列挙値そのものだけを確認したいとき。
- 個別の所見カテゴリ、レビュー判断基準、対象ファイル探索、git diff 生成、変更ファイル抽出など、agent に渡す材料を作る前段の詳細を調べたいとき。
- 生成済み INDEX.md の内容評価や、ルーティング文書一般の書き方だけを確認したいとき。

## hash
- baf1e8de76508471a80d1cbc96d896f2f71a04a5b727a80e9865239783605f5f

# `basic`

## Summary
- cmoc の実装で広く使われる基礎的な型・変換・文書生成部品をまとめる領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパスの解決、規範データの構造化、階層文書の Markdown レンダリングを扱う。
- 個別の CLI コマンドや外部バックエンド呼び出しそのものではなく、上位処理と実現処理が共有する入力仕様、パス表記、構造化文書表現の入口になる。

## Read this when
- エージェント呼び出しに渡すモデル区分、reasoning effort、ファイルアクセス区分、プロンプト、Structured Output schema 参照の保持形式を確認または変更したいとき。
- cmoc 内で `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのルートトークン付きパスを扱う処理や、絶対パスとの相互変換、相対パス拒否の挙動を確認したいとき。
- 規範文書を表すデータ構造、必須・禁止・推奨・許容の要求ラベル、背景・要求・判断例への変換や入力検証を確認したいとき。
- 階層化された自然言語文書やコードブロックを Markdown として生成する基本部品、見出し深さ、空行圧縮、本文正規化の挙動を確認したいとき。

## Do not read this when
- 具体的なバックエンド名、実モデル名、CLI 引数、外部コマンド実行形式への変換や呼び出し制御を調べたいだけのとき。
- プロンプト本文のテンプレート、タスク種別ごとの文章生成、Structured Output schema ファイル自体の内容を確認したいとき。
- 個別コマンドの入出力、サブコマンド制御、永続状態、ユーザー向け CLI 挙動を調べたいとき。
- 既存 Markdown の解析、ファイル内容の読み書き、生成済み文書やテスト期待値の具体ケースを確認したいとき。

## hash
- 409b2d79788a2ba3d4db9aca9bbe3794aa6c54b1fee51125127aa7576ab441d9

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
- CLI サブコマンド実装をまとめる領域。初期化、TUI 起動、目次保守、review oracle、apply、session 系操作など、利用者が直接実行する cmoc の上位制御へ進む入口になる。
- 各サブコマンドは runtime、git、state、Codex 呼び出し、worktree/branch 操作、レポート生成などを下位 helper に委譲しつつ、実行前条件、実行順序、成功・失敗時の出力や cleanup を結合する。
- apply と session は下位パッケージに分かれ、review oracle は対象列挙、レビュー loop、INDEX 差分処理、report 生成に分割されているため、サブコマンド単位で読む先を選ぶための中継点として使う。

## Read this when
- cmoc のサブコマンド実行フローや、どのサブコマンド実装へ進むべきかを切り分けたいとき。
- 初期化、TUI 起動、目次保守、review oracle、apply、session のいずれかについて、CLI runtime との接続、実行前条件、git 操作、state 更新、Codex 呼び出し、利用者向け出力の入口を探したいとき。
- review oracle の対象列挙、finding 処理、INDEX 変更 commit、merge、report 生成など、review 系の責務分割を把握して読む先を選びたいとき。
- apply run の開始、join、abandon、process 停止、worktree/branch cleanup、report 生成など、apply 系 lifecycle のどの実装を読むべきか判断したいとき。
- session の開始、join、破棄に関する branch 条件、clean worktree、session state、merge conflict、cleanup などの実装入口を探したいとき。
- INDEX.md 保守処理として、対象列挙、hash による再生成判定、Structured Output からのエントリー生成、lock、commit 条件を確認したいとき。

## Do not read this when
- CLI 全体の Typer 登録、共通 runtime、git wrapper、state schema、path keyword、設定モデルなど、サブコマンド横断の共通基盤だけを調べたいとき。
- oracle の正本仕様、INDEX.md 生成規則、realization/oracle の概念、path model など、仕様文書そのものを確認したいとき。
- 特定サブコマンド内の下位責務がすでに分かっており、対象列挙、レビュー loop、report 生成、apply process 管理などの個別 helper へ直接進めるとき。
- 実装ではなく外部挙動をテスト観点から確認したいだけのときは、対応するテスト側を読む。
- Codex prompt や Structured Output parameter の本文、complete prompt 構築規則、設定値の定義だけを変更したいときは、それぞれの parameter builder や設定・文書構造側を読む。

## hash
- f9fbb7ad02a1ed0ecff8e832f5e98bb318ef77cc79dac935e28006ea7e92e840
