# `acp`

## Summary
- AI agent 呼び出しに関わる実装をまとめる領域で、呼び出しパラメータを構築する builder 群と、agent に渡す構造化プロンプト部品の入口になる。
- 上位機能ごとの prompt、Structured Output schema、model class、reasoning effort、ファイルアクセス権限の組み合わせと、role・summary・goal・各種規則文書などの prompt 構成を確認するためのまとまり。

## Read this when
- cmoc の機能が AI Agent CLI/TUI や OpenAI API 相当を呼び出す際に、どの条件・補助文脈・構造化出力で実行されるかを調べたいとき。
- 変更要約、レビュー、INDEX.md エントリー生成、merge conflict marker 解消、TUI 実行など、AI 向け prompt と Structured Output schema の対応を確認したいとき。
- agent に渡すファイルアクセス規則、ルーティング規則、oracle / realization の概念説明、各種標準文書の prompt 文言や組み立て順を確認・変更したいとき。
- AI 呼び出しごとのモデル種別、reasoning effort、読み取り専用・編集許可などの実行条件を追いたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、Git 操作、branch/worktree 操作、ファイル走査、結果保存、TUI 表示など、AI 呼び出しを利用する側の実行制御を調べたいとき。
- oracle file、realization file、review standard、INDEX.md entry standard、path keyword など、prompt に埋め込まれる概念や仕様そのものを本文として読みたいとき。
- AgentCallParameter、path 解決、Markdown 構造化、schema 基盤、外部プロセス起動、LLM 応答処理など、個別の prompt・builder より下位または利用側の共通基盤を調べたいとき。
- 個別の対象ファイルやテスト本文を確認したいだけで、AI 呼び出し契約や agent 向け prompt 構成を変更しないとき。

## hash
- 6c693676ae17f509fcbdb3038d5bd2ab54fab2b86507725214bb9da6b20537a0

# `basic`

## Summary
- cmoc の実装全体で共有される基礎的な型・変換ヘルパーをまとめる領域。エージェント呼び出しパラメータ、ルートトークン付きパス解決、規範データ構造、構造化文書から Markdown へのレンダリングを扱う。
- 特定の CLI サブコマンドや業務フローではなく、複数の上位実装から参照される抽象値、パス表現、仕様・文書表現の共通部品を確認する入口になる。

## Read this when
- エージェント呼び出しに渡す論理的なモデル指定、Reasoning effort、ファイルアクセスモード、Structured Output schema パスなどの共通パラメータ構造を確認・変更したいとき。
- cmoc で使う `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` 付きパス表記と実パスの相互変換、ルート探索、相対パス入力の扱いを確認・変更したいとき。
- 規範をコード上で表すデータ構造、要求ラベル、要求本文、判断例、構造化ドキュメントへの変換を確認・変更したいとき。
- 階層化された自然言語文書、仕様断片、レポート、プロンプトなどを Markdown 見出し・本文・コードブロックとしてレンダリングする共通処理を確認・変更したいとき。
- 上位機能で使う前提となる、型定義、入力検証、文書表現、Markdown 出力の境界を先に把握したいとき。

## Do not read this when
- CLI サブコマンドの引数定義、画面出力、終了コード、利用者向けコマンド挙動だけを調べたいとき。
- バックエンドが実際に受理する具体的なモデル名や Reasoning effort、ファイルアクセス指定への変換処理を探しているとき。
- プロンプト本文の生成ロジック、タスク別テンプレート、呼び出し実行の制御フローを調べたいとき。
- 個別機能がどの作業ディレクトリでファイルを作成・更新するか、永続状態や Git 操作をどう扱うかという業務ロジックを確認したいとき。
- 既存 Markdown の解析、INDEX.md のルーティング規則そのもの、正本仕様断片の内容や編集方針を確認したいとき。
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
- cmoc の realization implementation のうち、複数の CLI command や上位モジュールから共有される runtime helper 群をまとめる領域。Codex CLI 呼び出し、profile 準備、設定読み書き、content hash、共通エラー表示、Git 操作、実行ログ、root/path 解決、実行結果型、session/apply state など、サブコマンド横断で使う実行時支援を扱う。
- 個別機能の業務ロジックではなく、上位の command 実装が共通 runtime 能力へアクセスするための実装群と、その公開 import 境界を提供する階層である。

## Read this when
- CLI サブコマンド間で共有される runtime 実行フロー、Codex 呼び出し、Git 操作、設定、ログ、path、状態、エラー、結果型のいずれかを確認または変更したいとき。
- 上位 command から利用できる共通 runtime API の入口や、下位 helper の責務分担を把握したいとき。
- Codex CLI exec/TUI 呼び出し、profile/schema 準備、quota/capacity retry、Structured Output 検証、subprocess 結果の CmocError 化を追いたいとき。
- `.cmoc` 配下の config、sessions、reports、logs、worktrees、state、schema など、実行時ファイルの読み書きや配置規則に関わる共通処理を調べたいとき。
- cmoc 管理 branch、worktree、session-id、active session、Git clean 判定など、Git repository 状態や永続状態を runtime 層で扱う箇所を探すとき。

## Do not read this when
- 個別 CLI subcommand の引数定義、dispatch、業務ロジック、生成ファイル内容、ユーザー向け出力順だけを知りたいとき。その場合は command 実装側へ進む。
- path keyword の概念定義そのものや `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の正本説明を確認したいとき。その場合は path model を扱う正本または定義側を読む。
- 設定値、AgentCallParameter、FileAccessMode、model class、reasoning effort などのデータ構造そのものを変更したいとき。その場合はそれぞれの型定義・設定定義側へ進む。
- ログを読む側、集計する側、表示する側、または INDEX.md の hash 更新ロジックを調べたいとき。共通 runtime の書き込み helper ではなく、対象機能の実装へ進む。
- 単にパッケージが存在するか、公開 import を持つかだけを確認したいときはパッケージ入口や集約入口だけで足りるため、下位 runtime 実装群を順に読む必要はない。

## hash
- 72f13772bc401c91734b66806edf15b91ee745bbcb09d1b981700635653d82f6

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
- cmoc の最上位 CLI アプリケーションを組み立て、Typer/click の引数解析エラーを cmoc 形式のエラー表示へ変換する入口実装。
- init、tui、indexing、session、apply、review の各コマンドを登録し、実処理は対応するサブコマンド実装へ委譲する。
- Codex exec/tui 呼び出し前に indexing preflight を実行する薄いラッパーを提供し、indexing 自身や conflict resolution 用途では再帰的な事前 indexing を避ける。

## Read this when
- cmoc コマンド全体の起動入口、サブコマンド階層、コマンド名、CLI option の接続箇所を確認したいとき。
- Codex exec/tui を呼ぶ前に indexing preflight がどの条件で走るか、またはスキップされるかを確認したいとき。
- CLI 引数解析エラーが通常の Typer/click 表示ではなく cmoc のエラーレポートとして出る経路を調べたいとき。
- サブコマンド実装に渡される依存関数や引数が、CLI 層でどのように配線されているかを確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、永続状態操作、git 操作、oracle review、session/apply の詳細挙動を知りたいだけのとき。
- Codex runtime 呼び出し、エラー描画、リポジトリルート判定、work root 判定などの共通 runtime 実装を調べたいとき。
- 設定モデル、AgentCallParameter、または各サブコマンドのテスト観点を調べたいとき。
- INDEX.md エントリー生成そのものの仕様や、indexing preflight の内部処理を確認したいとき。

## hash
- e97a446e3d7fe4dc8d22fc8b8b0a3576381e37e5109f36170669b124d0aa9148

# `sub_commands`

## Summary
- cmoc のサブコマンド実装をまとめる領域。初期化、INDEX.md maintenance、対話型実行、oracle review、session lifecycle、apply lifecycle の各コマンド本体と、そのコマンド固有の補助処理を扱う。
- CLI 登録や低レベル runtime ではなく、サブコマンドを実行したときの前提条件確認、状態遷移、Git/worktree 操作、Codex 呼び出し、利用者向け出力や report 生成へ進むための入口になる。
- session と apply は下位ディレクトリに lifecycle 操作がまとまっており、review は対象列挙、finding loop、INDEX.md 取り込み、report 描画の補助モジュールへ分かれている。

## Read this when
- cmoc の特定サブコマンドがどの実装領域にあるかを切り分けたいとき。
- 初期化、INDEX.md maintenance、対話型実行、oracle review、session fork/join/abandon、apply fork/join/abandon の実行条件、状態更新、Git 操作、出力や report 生成を確認・変更したいとき。
- サブコマンド固有の Codex 呼び出しや、isolated worktree/branch を使う review・apply・session の上位フローを追いたいとき。
- サブコマンド実装変更やテスト追加のために、単体コマンド本体、review 補助、session lifecycle、apply lifecycle のどこへ進むべきか判断したいとき。

## Do not read this when
- Typer app へのコマンド登録、引数 parser、トップレベル dispatch だけを確認したいときは、CLI アプリ組み立て側を読む。
- repo root/work root の決定、git command wrapper、worktree 操作、branch 操作、設定読み込み、session state schema、path keyword などの共通 runtime helper 自体を調べたいときは、runtime や状態モデルの実装を読む。
- Codex prompt parameter の文面や Structured Output schema の定義そのものを確認したいときは、acp builder 側を読む。
- oracle file の正本仕様、realization file の定義、INDEX.md エントリー生成規則など、サブコマンド実行制御ではなく仕様断片やルーティング文書の規則を調べたいときは、oracle 側の本文を読む。

## hash
- 5f8fb834fb173d34f516432d519dbb803ca2925c1bb1abecd4a833dc9ba3e4e2
