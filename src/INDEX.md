# `acp`

## Summary
- AI エージェントに渡す完全な呼び出し条件を構築する ACP 実装の領域。用途別の role、summary、goal、補助入力、ファイルアクセスモード、モデル区分、reasoning effort、Structured Output schema への接続と、そこへ注入される標準プロンプト部品を扱う。
- apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成など、サブ機能が agent に何を読ませ、どの権限で何を返させるかを確認する入口になる。

## Read this when
- cmoc のサブ機能が AI エージェントを呼び出す際の prompt 全体、補助入力、権限、モデル設定、出力 schema の対応を確認または変更したいとき。
- apply 系で、差分要約、realization file の所見列挙、検出済み所見への修正依頼など、後段 agent 呼び出しの条件や出力契約を追いたいとき。
- oracle review 系で、新規所見列挙、所見の擁護・反証理由追加、採否判定、所見リスト整理を agent に依頼する prompt と schema を確認したいとき。
- session join の merge conflict marker 解消、TUI 実行前のファイルアクセスモードや標準文書参照要否の選定など、特定用途の事前解決 agent 呼び出しを調べたいとき。
- agent prompt に含めるファイルアクセス規則、ルーティング規則、oracle と realization の基本概念、各種 standard、INDEX.md エントリー標準の生成内容や注入条件を扱うとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の実行順序、git 操作、fork 作成・統合、merge conflict marker 検出、生成結果の保存など、agent 呼び出しパラメータ構築の外側を調べたいとき。
- AgentCallParameter や FileAccessMode などの共通データ型そのもの、構造化ドキュメントの低レベル表現、Markdown rendering、パス解決 helper の基本実装だけを確認したいとき。
- oracle file、realization file、レビュー対象ファイル、git diff、変更ファイル一覧など、agent に渡される材料を作る側の探索・収集アルゴリズムを調べたいとき。
- 標準文書や仕様本文を読むこと自体が目的で、prompt にどう注入されるかや agent 呼び出し条件を確認しないとき。
- 生成済み INDEX.md の内容評価、ルーティング文書一般の書き方、または個別の実装・テスト修正だけが目的で、ACP の prompt 構築や標準プロンプト部品に触れないとき。

## hash
- 57fdfc1bf8cbb62c03b5cb03b2565d3de15fe8b7e3e68bfbce86071132f8bd48

# `basic`

## Summary
- バックエンド非依存の基礎データ構造と小さな文書生成ヘルパーを集めた実装領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパス解決、規範文書モデル、構造化文書の Markdown レンダリングを扱う。
- 上位の CLI・制御処理・仕様生成処理から共有される基本型や変換処理を確認する入口であり、具体的なバックエンド実行、コマンド UI、個別仕様本文、テスト構成へ進む前に基礎表現を確認するための対象。

## Read this when
- cmoc 内部で共有されるモデル区分、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema パスなど、エージェント呼び出し入力の保持形式を確認または変更したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` を含むパス表記の意味、探索規則、実パスとの相互変換、ルートトークンなし相対パスの拒否条件を確認したいとき。
- 規範文書をコード上で表す型、要求ラベル、要求本文の保持単位、規範オブジェクトから構造化ドキュメントを生成する処理を確認したいとき。
- 見出しツリー、本文文字列、コードブロックを組み合わせた構造化文書から Markdown を生成する処理や、空行整理・コードフェンス・インデント正規化の挙動を確認したいとき。
- 複数の上位機能から使われる基礎表現の責務境界を確認し、変更先が呼び出し制御、パスモデル、規範モデル、Markdown レンダリングのどれに属するか切り分けたいとき。

## Do not read this when
- 具体的なバックエンド名、実モデル名、CLI 引数、外部コマンド呼び出し、権限指定への変換ロジックを確認したいだけのとき。
- CLI サブコマンドの利用者向け挙動、画面出力、終了コード、永続状態操作、ファイル走査の業務ロジックを調べたいとき。
- 個別の正本仕様断片や oracle file の本文内容、仕様管理上の所有関係や編集責務だけを確認したいとき。
- Structured Output schema ファイル自体の内容、JSON schema の仕様、または特定コマンドの出力 schema を確認したいとき。
- プロンプト本文の組み立て、テンプレート内容、タスク種別ごとの文章生成ルール、または生成済み Markdown 文書の内容そのものを調べたいとき。
- テスト構成、fixture、テストケース追加先を探しているとき。

## hash
- 8d94dca84d270b4fa4b33e15e66d16c39720978cb8732957988df4509bf46751

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
