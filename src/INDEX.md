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
- cmoc の実行時共通基盤を集めた領域。CLI サブコマンドの共通ライフサイクル、Codex exec/TUI 呼び出し、設定入出力、内容ハッシュ、エラー整形、Git 操作、実行ログ、runtime path、結果型、session state など、複数の上位機能から共有される処理を扱う。
- 公開 import の集約入口と、責務別の runtime helper 実装が同居しており、上位コマンドの業務ロジックではなく、共通の実行制御・永続化・外部プロセス連携・利用者向けエラー化を確認するための入口になる。

## Read this when
- CLI サブコマンドに共通する開始、事前検査、ログ設定、例外処理、終了コード化、完了サマリーの挙動を確認または変更したいとき。
- Codex CLI の exec または TUI 呼び出しについて、profile/schema 準備、argv/env/cwd、call log、Structured Output 検証、quota/capacity retry、resume 継続、console/subcommand log 記録の流れを追いたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正 JSON や不正値の利用者向けエラー化、Codex subprocess 用の設定生成を扱う共通処理を探すとき。
- 実行時に使う root path、cmoc 管理ディレクトリ、sessions/reports/logs/worktrees/state/config/schema などの保存先、timestamp や duration 表示、作業ディレクトリ一時変更の共通規則を確認したいとき。
- Git 状態検査、branch/worktree 操作、cmoc 内部ディレクトリの ignore 管理、外部コマンド失敗時の共通エラー化を確認または変更したいとき。
- サブコマンド実行ログ、Codex call log の利用者向け表示、quota wait 集計、context-local な current logger の受け渡しを調べたいとき。
- session state の JSON 永続化、管理 branch からの session-id 復元、apply/session 状態断片の読み書き、前方互換的な state 復元を確認したいとき。
- 複数の共通 runtime API をまとめて import する公開面や、共有される結果データ型・エラー型・内容ハッシュ helper の所在を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、利用者向けのコマンド別出力、状態更新タイミングだけを調べたいとき。その場合は該当コマンド実装へ進む。
- path キーワードそのものの概念定義や、root 種別の正本仕様を確認したいとき。その場合は path model の仕様または定義側を読む。
- INDEX.md の生成方針、エントリー生成プロンプト、ファイル探索ルール、oracle 文書の正本仕様を調べたいとき。ここは runtime helper 側の実装領域であり、仕様本文の入口ではない。
- Codex CLI や Git の外部ツール仕様そのもの、または LLM 出力品質を検証したいとき。ここで扱うのは cmoc からそれらを呼び出す共通実行制御である。
- 特定のデータクラスや設定モデルのフィールド定義だけを確認したいとき。共通 runtime から参照されるモデル定義側を直接読む方が適切である。
- 通常の業務ファイル読み書き、個別 JSON 入出力、テストケースの期待値、またはログを読む側の集計・表示仕様を探しているとき。より直接の実装またはテストへ進む。

## hash
- ed645712c2484daf804b5f910349f77a57c97804ebb06e96054a5adb6b28ece5

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
- cmoc の主要サブコマンド実装を集める入口階層。session、apply、review oracle、indexing、init、tui の各実行フローへ進むためのルーティング起点になる。
- 各サブコマンドは、共通 CLI runner への接続、事前条件確認、git branch/worktree 操作、session/apply state 更新、Codex 実行、report 出力、cleanup などの orchestration を担う。
- apply と session は下位パッケージに fork/join/abandon の実装を分け、review oracle は対象列挙、Codex loop、INDEX 差分処理、report 生成を複数モジュールに分けている。

## Read this when
- cmoc のサブコマンド実装のうち、どの下位モジュールまたは下位パッケージへ進むべきかを選びたいとき。
- session fork/join/abandon、apply fork/join/abandon、review oracle、indexing、init、tui の実行順序、事前条件、状態遷移、出力、cleanup の入口を探すとき。
- サブコマンドから共通 CLI runner、indexing preflight、git/worktree 操作、session state、apply state、Codex 実行、report 生成へどう接続されるかを追いたいとき。
- 管理 branch や一時 worktree を使うサブコマンドの lifecycle、merge conflict 対応、想定外差分検出、process 停止、エラー時 report など、コマンド単位の制御フローを確認または変更したいとき。

## Do not read this when
- Typer app 全体のサブコマンド登録、トップレベル CLI 構成、または共通の起動ラッパーそのものだけを調べたいとき。
- git 実行 wrapper、work root/repo root 解決、session state schema、設定読み込み、path model、ignore 判定など、複数サブコマンドで使う runtime helper の内部仕様を直接確認したいとき。
- Codex に渡す prompt、Structured Output schema、AgentCallParameter の組み立て本文を変更したいときは、各 builder 側の実装へ直接進む。
- oracle file の正本仕様、review 観点、INDEX.md エントリー生成規則、または realization/oracle の概念定義を調べたいとき。
- 対象が特定のサブコマンドや下位処理に決まっている場合は、この階層ではなく該当する個別モジュールまたは下位パッケージへ直接進む。

## hash
- 70f740fe5c51aec0b340c077f5c7fcac48965997dd8971b5ba1cbb4f09e05517
