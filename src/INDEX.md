# `acp`

## Summary
- AI agent 呼び出しに関する実装をまとめる領域。呼び出しパラメータを機能別に組み立てる層と、agent に渡す構造化プロンプト部品・標準文書を組み立てる層を扱う。
- フォーク適用、INDEX.md エントリー生成、oracle review、session conflict marker 解消、TUI 実行パラメータ解決などの機能が、下流 agent に何をどの条件で依頼するかを確認する入口になる。

## Read this when
- AI agent 呼び出しに渡す role、summary、goal、補助入力、標準文書、ファイルアクセス規則、モデル種別、推論量、Structured Output 契約を機能別に確認または変更したいとき。
- agent call 用の完全なプロンプトが、どの標準部品をどの順序・依存関係で含め、追加プロンプトや入力データとどう結合されるかを追いたいとき。
- INDEX.md エントリー生成、oracle review、apply review、session join の conflict marker 解消、TUI の実行パラメータ解決などで、AI へ渡す依頼条件やプロンプト本文を調べたいとき。
- プロンプト中の root token 置換、ツール固有用語の呼び出し先向け置換、oracle file・realization file・review 系標準文書の agent 向け文面を確認したいとき。

## Do not read this when
- 各サブコマンドの実行制御、状態管理、git 操作、ファイル走査、保存、merge 実行など、AI 呼び出し前後の処理本体を調べたいとき。
- StructDoc、Standard、Requirement、AgentCallParameter、FileAccessMode、パスモデルなど、プロンプトや呼び出し条件を支える基礎型そのものを調べたいとき。
- oracle review や apply review の生成結果を実際に評価・統合・適用する後段処理、または結果の表示・通知・永続化を探しているとき。
- 個別の Structured Output schema の項目構造だけを確認したいときは、該当する schema 定義へ直接進めばよい。

## hash
- 73c9dd8d91278c07320911af8656b93045afba2178a99ce2ffdcf695a78f2ecb

# `basic`

## Summary
- cmoc の実装全体で共有される基礎モデルと小さな文書処理ユーティリティを置く領域。エージェント呼び出し条件、ルートトークン付きパス解決、規範文書モデル、階層文書から Markdown への変換といった、特定の CLI サブコマンドより下位の共通概念を扱う。
- バックエンド固有の API 値、個別コマンドの実行フロー、ファイル読み書きそのものではなく、それらの上位処理が参照する抽象的な型・変換・検証・レンダリングの入口として位置づけられる。

## Read this when
- モデルクラス、reasoning effort、ファイルアクセスモード、Structured Output schema の有無など、AI コーディングエージェント呼び出し条件をコード上でどう保持するか確認したいとき。
- ルートトークン付きパス表記を実パスへ解決する挙動、または実パスをルートトークン付き表記へ戻す挙動を確認・変更したいとき。
- main worktree、linked worktree、現在の worktree、Git common dir などを使った cmoc 固有のルート探索や失敗条件を調べたいとき。
- 規範文書を構成する見出し、背景、要求、判断例、要求項目ラベルを実装上のモデルとしてどう検証・保持するか確認したいとき。
- 規範文書モデルや階層化された自然言語文書を、表示・文書用の構造化表現または Markdown 文字列へ変換する処理を確認したいとき。
- 文書本文やコードブロックのインデント正規化、空行整理、Markdown 見出し階層の扱いを確認・変更したいとき。

## Do not read this when
- 個別サブコマンドの CLI 引数、出力 schema、実行順序、ユーザー向け入出力を調べたいとき。
- エージェントプロセスの起動、外部コマンド実行、API 呼び出し、バックエンド固有のモデル名や権限表現への変換処理を探しているとき。
- ファイル内容の読み書き、INDEX 生成、oracle file と realization file の分類、永続状態操作など、基礎モデルを使った業務ロジックを調べたいとき。
- 自然言語で書かれた個別の規範本文や正本仕様断片そのものを読みたいとき。
- 生成された Markdown の保存先、利用元、CLI からの呼び出し経路だけを確認したいとき。
- テストで期待される外部挙動だけを確認したい場合で、共通モデルや内部変換の詳細まで不要なとき。

## hash
- d1d69ef3a0bf213c284d4c2b95623804491fbf9ff997ac57263f1648cb474fbe

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
- cmoc の realization implementation のうち、複数のサブコマンドや runtime 層から共有される実行時 helper 群をまとめる領域。CLI 実行ライフサイクル、Codex 呼び出し、設定入出力、内容 hash 保存、共通エラー、Git 操作、実行ログ、runtime path、結果モデル、永続 session state など、横断的な基盤処理への入口になる。
- 責務別の小さな module と、既存 import path を維持する集約入口が混在しており、個別サブコマンドの業務処理ではなく、サブコマンド群が共通利用する runtime 境界を確認するための階層である。

## Read this when
- CLI サブコマンドの開始・完了表示、終了コード化、例外表示、サブコマンド logger の設定範囲など、共通実行ライフサイクルを調べるとき。
- Codex exec/TUI の profile 準備、呼び出し、Structured Output 検証、retry、quota/capacity 制御、resume、call log、subcommand event、preflight など、Codex runtime 全体または責務別入口を探すとき。
- 設定ファイルの読み書き、既定値補完、不正 JSON や型不正の利用者向けエラー化を確認または変更するとき。
- 内容 hash、hashed file 保存、binary 判定、生成物や cache 的な出力の内容ベース保存処理を調べるとき。
- cmoc 共通例外、利用者向け Markdown エラーレポート、Next actions、detail、call stack の出力構造を確認または変更するとき。
- Git コマンド実行、branch・HEAD・clean worktree 判定、cmoc 管理 branch、run worktree、ignore/exclude 制御など、Git 状態や Git 操作の共通 helper を調べるとき。
- サブコマンド実行ログ、JSON Lines event、quota 待機時間、実行時間計測、context-local logger を確認または変更するとき。
- 実行時の repo/work/cmoc root 解決、cmoc 管理ディレクトリ、config/state/log/worktree/schema path、timestamp、memo 配下判定、作業ディレクトリ一時変更を扱うとき。
- 外部コマンド結果や Codex exec 結果として、終了コード、標準入出力、生成 text/JSON、profile/schema、log path、elapsed、quota 情報を運ぶ共有データ構造を確認するとき。
- session branch や apply branch に紐づく永続 session state、state file の JSON 入出力、branch 名からの session-id 抽出、active session 探索を調べるとき。
- 複数の runtime 共通部品をまとめて import している呼び出し側の依存関係や、公開入口から利用可能な共通部品の範囲を把握したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、dispatch、利用者向け出力内容そのものを調べたいとき。その場合はサブコマンド実装や CLI ルーティング側へ進む。
- oracle file の正本仕様、path 概念そのもの、oracle/realization の分類、INDEX.md 生成規則やルーティング文書の仕様を確認したいとき。この階層は realization implementation の共通 runtime helper であり、正本仕様の置き場ではない。
- 特定機能の高レベルな workflow、状態遷移、レポート内容、出力 schema の意味を調べたいだけのとき。その機能を持つ上位実装または仕様文書を読む方がよい。
- Codex profile 名、設定値、AgentCallParameter、FileAccessMode、モデルや reasoning effort などの入力データ構造そのものを確認したいだけのとき。データモデルや設定定義側へ進む。
- ログや状態ファイルを読む側、集計する側、表示する側の仕様や実装を探しているとき。ここは主に生成・保存・受け渡しの共通 helper を扱う。
- 外部コマンドや Git 操作を伴わない純粋なドメイン処理、構造化テキスト解析、Markdown 処理、テスト固有 fixture の期待値だけを調べるとき。
- 既存 import path の互換入口ではなく、個別機能の実装詳細を直接変更したいとき。集約入口ではなく該当責務の module へ進む。

## hash
- 2a2e2ff001b9a9d23ae8262b2ee304a713549dd29cd4138c3bd9462b84aa58ff

# `config`

## Summary
- cmoc のリポジトリ単位設定モデルを扱う領域であり、並列実行数、Codex CLI 向けモデル・reasoning effort の対応、apply fork や eval-oracle の上限値など、設定として保持される値と既定値の構造を確認する入口である。
- 設定モデルには enum 系キーを含むため、永続化や同期で enum を値へ変換して扱う前提を確認したい場合の参照先になる。

## Read this when
- リポジトリ単位の cmoc 設定項目、既定値、設定 dataclass の構造を確認または変更したいとき。
- Codex CLI に渡すモデル名や reasoning effort 名と、cmoc 内部の分類 enum との対応を確認または変更したいとき。
- apply fork や eval-oracle の処理回数・処理件数の上限など、サブコマンド挙動に影響する設定値を探しているとき。
- 設定の永続化、同期、JSON 化に関わる処理で、設定モデルに含まれる値や enum を値として保存する前提を確認したいとき。

## Do not read this when
- 設定ファイルの読み書き、JSON 変換、同期、初期化コマンドの実装手順そのものを調べたいだけのとき。
- CLI サブコマンドの実行フロー、プロンプト生成、外部プロセス呼び出し、評価ロジック本体を調べたいとき。
- path token、作業ツリー、リポジトリルートなどのパス概念の定義を確認したいとき。
- 設定値ではなく、モデル分類や reasoning effort 分類そのものの定義・意味を確認したいとき。

## hash
- 02110b92f454d5ff6a730409465dda019584fe9bb54975ad9299f42ff8183434

# `main.py`

## Summary
- Typer による cmoc の最上位 CLI エントリーポイントを定義する実装。
- `session` と `apply` のサブアプリを組み立て、`init`、`tui`、`session fork/join/abandon`、`apply fork/join/abandon`、`eval-oracle`、`indexing` の各 CLI コマンドを対応する実装関数へ委譲する。
- 補完時を除く通常の Click 引数解析エラーを cmoc のエラーレポート形式へ変換する Typer group と、console script からアプリを起動する入口を持つ。

## Read this when
- cmoc の利用者向け CLI コマンド名、サブコマンド構造、option、引数の入口定義を確認・変更したいとき。
- CLI の引数解析失敗時に表示される cmoc 形式のエラー変換処理を確認・変更したいとき。
- 既存サブコマンド実装がどの CLI コマンドから呼ばれるかを追跡したいとき。
- console script から Typer app がどの `prog_name` で起動されるかを確認したいとき。

## Do not read this when
- 各コマンドの実際の業務処理、branch 操作、worktree 操作、review 実行、INDEX.md 更新処理の詳細を調べたいときは、ここではなく委譲先のサブコマンド実装を読む。
- cmoc の正本仕様断片を確認したいときは、ここではなく oracle file を読む。
- 個別コマンドのテスト観点や期待される外部挙動を確認したいときは、対応する realization test を読む。
- path keyword、work root、run root、work root などの用語定義を確認したいときは、ここではなく正本側の path model を読む。

## hash
- ad0ee6a7e833c4c47d169ecb0378085c3438e629a099842c04af1aa760543fb2

# `sub_commands`

## Summary
- src/sub_commands は cmoc の CLI サブコマンド実装を集約する領域で、初期化、対話実行、INDEX.md 保守、eval-oracle、session、apply などの利用者操作ごとの実行入口を下位要素へ振り分ける。
- 各下位要素は CLI runtime を通じた制御フロー、preflight、git・worktree・branch 操作、状態更新、Codex 呼び出し、利用者向け report や stdout 出力など、サブコマンド単位の orchestration と周辺 helper の入口になる。

## Read this when
- サブコマンドごとの実行入口、起動条件、preflight、利用者向け出力、状態遷移、branch/worktree 操作の読む先を選びたいとき。
- cmoc init、TUI 実行、INDEX.md 自動保守、eval-oracle、session 操作、apply 操作のどの実装へ進むべきかを切り分けたいとき。
- review oracle の対象列挙、finding loop、索引変更 merge、report 生成など、eval-oracle の下位責務の入口を探したいとき。
- apply や session のように複数ファイル・下位ディレクトリへ分かれたサブコマンド実装について、全体像を把握してから具体的な処理へ進みたいとき。

## Do not read this when
- git command wrapper、CLI runtime、設定読み込み、path model、state file 読み書き、report root など、複数領域で使う共通基盤そのものを調べたいとき。
- oracle file、realization file、INDEX.md エントリー標準、path token などの正本仕様や共通概念を確認したいとき。
- 特定サブコマンド内のさらに明確な責務が分かっている場合は、この領域全体ではなく該当する下位ファイルまたは下位ディレクトリへ直接進むとき。
- サブコマンド実装ではなくテスト上の外部挙動や回帰条件だけを確認したいとき。

## hash
- 0774dbcb595c272d0542a4d5787a8401eb8d47748de5f77418dd8067f8427ccf
