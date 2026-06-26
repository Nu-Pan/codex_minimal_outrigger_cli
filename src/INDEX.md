# `acp`

## Summary
- AI エージェント呼び出しに渡すパラメータと標準プロンプト部品を構築する実装領域。用途別の role、goal、補助入力、読み書き制約、モデル設定、reasoning effort、Structured Output schema への接続と、oracle・realization・review・ルーティング文書などの標準文書を agent 向け prompt に組み立てる処理を扱う。
- apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成など、各機能が agent に何を読ませ、何を返させ、どの権限で動かすかを確認する入口である。

## Read this when
- cmoc の機能が AI エージェントを呼び出す際の prompt 構成、補助入力、対象パスや差分の埋め込み、ファイルアクセスモード、モデル種別、reasoning effort、出力 schema の対応を確認・変更したいとき。
- oracle file、realization file、oracle standard、realization standard、review standard、apply review standard、INDEX.md エントリー標準などを、agent prompt としてどの順序・依存関係で注入しているか調べたいとき。
- apply 系で、差分要約、ファイル単位の所見列挙、所見対応作業の agent 呼び出し条件や出力契約を追いたいとき。
- oracle review 系で、新規所見列挙、所見の擁護・反証理由列挙、採否判定、所見リスト整理の prompt と Structured Output schema を確認したいとき。
- session join の merge conflict marker 解消、TUI 実行前の権限・標準参照要否判定、INDEX.md エントリー生成など、特定用途の事前解決 agent 呼び出しを調べたいとき。
- agent に提示されるファイルアクセス規則、INDEX.md を使う読み進め方、oracle file と realization file の基本概念、レビューや実装品質に関する標準文言を変更したいとき。

## Do not read this when
- CLI サブコマンド全体の実行順序、引数解析、永続状態、git 操作、フォーク作成・統合、merge conflict marker の検出、生成結果の保存など、agent 呼び出しパラメータ構築の外側を調べたいとき。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、構造化ドキュメント、標準項目、パス解決などの基本データ構造や共通 helper だけを確認したいとき。
- oracle file や realization file の個別本文、または正本仕様断片そのものを読みたいだけで、agent prompt への注入方法を変更しないとき。
- 実際の対象ファイル探索、git diff 生成、変更ファイル抽出、レビュー所見の永続化、所見適用後の作業制御など、prompt に渡す材料を作る側または結果を処理する側の詳細を調べたいとき。
- 生成済み INDEX.md の内容評価や、ルーティング文書の文面作成だけが目的で、標準文書生成処理や agent 呼び出しパラメータの実装を確認する必要がないとき。

## hash
- b449f59beb7b6e0bb094015d8ef2ed93b760fb3b5e08e1b6b462f7328354f46a

# `basic`

## Summary
- cmoc の複数領域から共有される基礎的なデータ構造と小さな変換処理をまとめる実装領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパスの解決、規範文書の構造化、構造化文章から Markdown へのレンダリングを扱う。
- バックエンド固有の実モデル名や外部コマンド形式、個別の CLI 制御、正本仕様本文そのものではなく、それらを実装側で受け渡し・表現・変換するための共通入口として位置づく。

## Read this when
- cmoc 内部で共有される基礎型、列挙、データ構造、軽量な変換 helper の責務を確認または変更したいとき。
- エージェント呼び出しに渡すモデル区分、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema パスの保持形式を確認したいとき。
- ファイル・ディレクトリパスをルートトークン付き表記と実パスの間で変換する処理、またはルートトークンなし相対パスの拒否や git worktree に応じたルート判定を調べたいとき。
- 規範文書をコード上で表すための要求ラベル、背景・要求・判断例の保持形式、または規範オブジェクトから構造化文章を生成する処理を確認したいとき。
- 見出し階層、本文、コードブロックから Markdown を生成する処理や、空行整理・コードフェンス・三重引用文字列のインデント正規化を確認したいとき。

## Do not read this when
- 具体的なバックエンド名、実モデル名、CLI 引数、外部コマンド呼び出し形式への変換や実行制御を調べたいだけのとき。
- プロンプト本文のテンプレート、タスク種別ごとの文章生成ルール、または Structured Output schema ファイル自体の内容を確認したいとき。
- 個別コマンドの入出力、サブコマンドのルーティング、永続状態、ユーザー向け CLI 挙動を調べたいとき。
- 正本仕様断片としての規範内容そのものや、人間が責任を持つ仕様文書を確認したいとき。
- 特定ファイルの読み書き、ファイル内容の解析・生成、テスト側の具体ケースを調べたいとき。

## hash
- 8a11d480e62c928a2a4e5efe3559a84a61076f8705b24eb1216191d7d6d3c421

# `cmoc_runtime.py`

## Summary
- 互換用の薄い入口であり、実体のランタイム実装を別モジュールから読み込んで、この import path 自体を実装モジュールへ差し替える。
- 旧来の直接 import 経路や公開設定上の import 経路を残すための橋渡しで、責務固有のランタイム処理はここには置かない。

## Read this when
- トップレベルのランタイム import path がどの実装へ接続されるかを確認したいとき。
- 互換 import 経路の維持・削除条件や、直接 import している呼び出し元への影響を確認したいとき。
- ランタイム実装を移動・分割したあと、この互換入口を残す必要があるか判断したいとき。

## Do not read this when
- ランタイム処理そのものの挙動、引数処理、状態管理、出力生成を調べたいとき。その場合は実体の実装モジュールを読む。
- 新しいランタイム機能や責務固有の処理を実装したいとき。この互換入口ではなく実体側のモジュールを読む。
- パッケージ公開設定やエントリーポイント定義を確認したいだけのとき。その場合は設定ファイルを読む。

## hash
- 223b9df223b1746d08a7487389b45587c37917fa6e9b6d75d8dbb48985527074

# `commons`

## Summary
- cmoc の realization implementation のうち、複数の CLI サブコマンドや上位機能から共有される runtime helper 群をまとめる領域。Codex 呼び出し、CLI 実行ライフサイクル、設定入出力、内容ハッシュ、共通エラー、Git 操作、実行ログ、path 解決、結果型、session state 永続化など、個別機能から横断利用される実行時基盤を扱う。
- この階層は共通 runtime API の公開入口と責務別実装への入口を兼ねる。まとめて import される公開面を確認する場合は集約入口を、具体的な挙動や失敗時処理を確認する場合は対象機能に対応する実装へ進むための起点になる。

## Read this when
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外表示、ログ記録、現在 logger 管理など、サブコマンド横断の実行制御を確認または変更したいとき。
- Codex CLI の exec/TUI 呼び出しについて、profile/schema 準備、subprocess 実行、Structured Output 検証、capacity retry、quota wait、resume、call log、subcommand event、失敗時例外化などの runtime 制御を追いたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、永続化用 JSON との相互変換、不正な JSON や型・値の利用者向けエラー化を扱うとき。
- 文字列やファイル内容の SHA-256 digest、内容ハッシュ付きファイルの保存、既存内容と同一な場合の再書き込み抑制、粗い binary 判定を使う共通処理を探すとき。
- cmoc 共通の独自実行時エラー構造や、例外を利用者向けの Summary、Next actions、Detail、Call stack 付き表示へ整形する処理を確認したいとき。
- Git コマンド実行の共通 wrapper、branch・HEAD・worktree 状態検査、管理 branch 判定、run worktree 作成削除、内部ディレクトリの ignore 初期化や検証を調べたいとき。
- サブコマンド単位の JSON Lines 実行ログ、record 基本項目、経過時間や quota 待機時間の集計、context-local な current logger の受け渡しを確認したいとき。
- 実行時の root path 解決、cmoc 管理ディレクトリやログ・state・config の保存先導出、timestamp・duration 表示、一時的な作業ディレクトリ変更を扱うとき。
- 外部コマンド結果や Codex exec 結果として共有されるデータ型のフィールドを確認または変更したいとき。
- session state file の schema、読み書き、branch 名からの session-id 抽出、session/apply 状態断片、home branch に紐づく active session 検出を確認したいとき。
- 複数の共通 runtime 機能を呼び出し側からまとめて利用する import 経路や、外部へ露出している共通 runtime API の一覧を確認したいとき。

## Do not read this when
- 個別 CLI サブコマンドの業務ロジック、引数定義、dispatch、利用者向け出力、永続データの具体的な読み書き手順だけを調べたいとき。その場合は該当サブコマンドや上位機能の実装へ進む。
- path キーワードそのものの意味や、root 種別の概念定義を確認したいだけのとき。その場合は path model の仕様または定義側を読む。
- INDEX.md 生成の内容ロジック、エントリー生成プロンプト、oracle 文書の正本仕様、routing rule そのものを調べたいとき。共通 runtime helper ではなく、indexing や oracle 側の対象へ進む。
- ログや状態ファイルを読む側、集計する側、表示する側の仕様や実装を探しているとき。ここは主に runtime 側の生成・保存・共通管理を扱う。
- Codex profile、設定モデル、AgentCallParameter、FileAccessMode、CmocConfig などのデータ構造定義そのものを確認したいだけのとき。該当する model 定義へ直接進む。
- Git 操作や Codex 呼び出しが、個別コマンドのどのタイミングで使われるかという上位フローだけを知りたいとき。先に呼び出し元の command 実装を読む。
- 共通 runtime API へ公開するかどうかをまだ判断しておらず、新しい機能の置き場所だけを広く探しているとき。対象機能に近い既存実装や呼び出し元から確認する方が適切。

## hash
- abf10d6edc0f465c93272120910a2c73bfec8b80082089b119e257ca2a1e2e95

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
- cmoc の CLI 起動点として Typer アプリを構成し、最上位コマンドと session・apply・review のサブコマンドを各実装関数へ接続する。
- 通常の CLI 引数解析失敗を cmoc 共通のエラーレポート形式へ変換し、シェル補完時は通常の Typer/Click 処理に委ねる。

## Read this when
- 利用者が実行するコマンド名、サブコマンド階層、CLI option の入口定義を確認・変更したいとき。
- CLI 引数解析エラーの表示形式、終了コード、補完時の扱いを確認・変更したいとき。
- サブコマンドの実処理へ到達するまでのディスパッチ経路を追いたいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、永続状態操作、外部コマンド実行の詳細を調べたいときは、ここではなく各サブコマンド実装を読む。
- cmoc 共通エラー型やエラー表示そのものの構造を変更したいときは、CLI 入口ではなく共通ランタイム側を読む。
- テスト方針や仕様断片を調べたいだけで、CLI コマンド登録や引数解析の入口に関心がないとき。

## hash
- 9948446cc3191114d645d8bdd77b57fbcc0fb537b825a2834b17cf15a1b84f93

# `sub_commands`

## Summary
- cmoc のサブコマンド実装を集めた領域で、初期化、ルーティング文書更新、対話実行、session 操作、apply 操作、oracle review の各 CLI 処理への入口になる。
- 各サブコマンドは共通 runtime に接続され、branch/worktree/state の事前条件確認、Codex 実行、git 操作、report 出力、後片付けなどをコマンド単位または補助責務単位に分けて扱う。
- session と apply は下位コマンド群として分かれ、review は対象列挙、Codex review loop、INDEX 差分処理、report 描画などの補助実装を同階層に持つ。

## Read this when
- cmoc のサブコマンド実装のうち、どのコマンドまたは補助モジュールへ進むべきかを選びたいとき。
- CLI 入口から共通 runtime、Codex 実行、git 操作、state 更新、report 生成へ処理がどう接続されるかを調べ始めるとき。
- init、indexing、tui、review oracle、session fork/join/abandon、apply fork/join/abandon の実行条件や上位フローを確認したいとき。
- session branch、apply branch、review/apply worktree、INDEX 更新 commit、merge conflict 解決、実行結果 report など、サブコマンド固有の orchestration 境界を把握したいとき。

## Do not read this when
- サブコマンドを登録する最上位 CLI parser や Typer command 定義全体だけを調べたいときは、CLI 起動側を直接読む。
- git wrapper、path model、state schema、設定読み込み、worktree helper、Codex 実行 wrapper などの共通 runtime の内部仕様だけを調べたいときは、共通 runtime 側へ進む。
- Codex に渡す prompt や Structured Output schema の本文だけを変更したいときは、各 parameter builder 側へ直接進む。
- oracle file の正本仕様、realization/oracle の概念、INDEX.md エントリー生成規則そのものを調べたいときは、仕様文書または対応する builder/runtime の対象へ進む。
- 個別の下位コマンドや補助責務がすでに分かっているときは、この階層全体ではなく該当する実装へ直接進む。

## hash
- c71eb75e3cde24dbf24796e4d157af7fc3850e4f30b33577045f34523cacb360
