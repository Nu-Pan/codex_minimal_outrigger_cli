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
- cmoc の realization implementation のうち、CLI 実行ライフサイクル、Codex 呼び出し、設定入出力、content hashing、エラー整形、Git 操作、実行ログ、path 解決、結果型、永続状態などを支える共通 runtime helper 群を収める領域。
- 複数の上位機能から共有される低レベル寄りの実行時処理と、それらをまとめて利用するための集約入口を扱う。個別サブコマンドの業務ロジックではなく、サブコマンドや Codex 実行を支える共通基盤を探す入口になる。

## Read this when
- CLI サブコマンドを共通ラッパーで実行する流れ、開始・完了・失敗時の標準出力、終了コード化、サブコマンドログ設定、例外の利用者向け表示を確認したいとき。
- Codex CLI の exec または対話起動について、profile/schema 準備、argv・cwd・環境変数、call log、Structured Output 検証、capacity retry、quota wait、resume 継続、preflight 実行前フックなどの runtime 制御を調べたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、永続化 JSON との相互変換、不正設定のエラー化を確認または変更したいとき。
- 文字列やファイル内容の SHA-256 digest、内容アドレス型ファイルの書き込み、binary file 判定など、内容ハッシュに関する共通 helper を探すとき。
- cmoc 共通の実行時エラー表現、利用者向けエラー文面、通常例外の整形、または Git コマンド失敗時の共通エラー化を確認したいとき。
- Git repository 状態の検査、一時 worktree や managed branch の作成・削除、Git ignore 判定、`.cmoc` の追跡除外保証などの共通 Git helper を調べたいとき。
- サブコマンド実行ログの JSON Lines 追記、current logger の context-local 管理、quota 待機時間や実行時間の計測を確認したいとき。
- 実行時 root path、cmoc 管理ディレクトリ、sessions・reports・logs・worktrees・state・config の保存先、timestamp や duration 表示、作業ディレクトリ一時変更を扱う共通処理を確認したいとき。
- 外部コマンド結果や Codex exec 結果の共有データ型、session/apply の永続状態 JSON、管理 branch 名と session_id の対応、active session 探索を確認または変更したいとき。
- runtime 系 helper の公開 API をどの集約入口から import できるか、または再公開範囲を整理する必要があるとき。

## Do not read this when
- 個別サブコマンドの業務フロー、引数定義、ユーザー向けコマンド仕様、機能固有の状態更新だけを調べたいときは、そのサブコマンド実装へ進む。
- path キーワードそのものの概念定義や `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の意味を確認したいだけのときは、path model の正本仕様または定義実装へ進む。
- INDEX.md 生成の内容ロジック、エントリー生成プロンプト、ファイル探索ルールそのものを調べたいときは、indexing や oracle 周辺の実装へ進む。
- 設定モデル、AgentCallParameter、FileAccessMode、CmocConfig などのデータ構造そのものを確認したいだけのときは、それぞれのモデル定義へ進む。
- ログや状態ファイルを読む側、集計する側、表示する側の仕様を調べたいときは、この共通書き込み・保持層ではなく利用側の実装へ進む。
- Codex や Git を使う上位機能の高レベルな制御順序だけを知りたいときは、共通 helper ではなく呼び出し元の feature 実装へ進む。

## hash
- 4cb37e74d7da93f9c292b1c8cd6a9e0d0e17ae48fa38dae59c8428ce1289e041

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
- CLI の各サブコマンド実装を集約する領域。初期化、ルーティング文書更新、対話実行、セッション操作、apply 実行、oracle review など、利用者が直接起動する処理の入口を探すためのルーティング対象。
- 各実装は共通 CLI 実行基盤、preflight、git 操作、状態管理、worktree 操作、report 出力、Codex 呼び出しなどを組み合わせる orchestration を担い、低レベル helper ではなくサブコマンド単位の制御順序を確認する入口になる。
- 配下には、個別サブコマンドの入口モジュールと、複数ファイルに分かれたサブコマンド領域が並び、対象コマンドが未確定な場合に責務境界を切り分けるための階層として位置づく。

## Read this when
- CLI から起動されるサブコマンドの実行入口、前提条件、利用者向け出力、エラー時挙動、または共通 CLI runner との接続を調べたいとき。
- 初期化、ルーティング文書更新、対話実行、session 操作、apply 操作、oracle review のどの実装へ進むべきかを選びたいとき。
- サブコマンドが worktree、branch、session state、git 操作、Codex 実行、report 作成、cleanup をどの高レベル順序で組み合わせるか確認したいとき。
- 複数のサブコマンドにまたがる変更で、個別実装へ進む前に同階層の責務分担と読む順序を判断したいとき。

## Do not read this when
- サブコマンドから呼ばれる低レベル runtime helper、git 実行 wrapper、path model、状態ファイル schema、設定モデルなどの共通部品だけを調べたいとき。
- Codex に渡す prompt、Structured Output parameter、entry 生成 parameter、review 用 parameter など、サブコマンドから呼ばれる builder 側の詳細だけを変更したいとき。
- oracle file の正本仕様、realization/oracle の概念定義、ルーティング文書そのものの一般仕様を確認したいとき。
- 対象サブコマンドや下位 helper が既に明確で、この階層全体の責務境界を確認する必要がないとき。

## hash
- fc36668888fe7bead4c615a2f10e7b3f1febcf524baeed44956fa86680f927be
