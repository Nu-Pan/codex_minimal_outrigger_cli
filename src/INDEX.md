# `acp`

## Summary
- AI エージェントへ作業を依頼するための呼び出しパラメータ構築と、呼び出し時に渡す標準 prompt 文書生成を扱う領域。role、summary、goal、補助入力、ファイルアクセス権限、モデル・推論設定、Structured Output 契約、標準文書の注入条件を接続する。
- フォーク適用、目次情報生成、oracle review、session join の conflict marker 解消、TUI 実行パラメータ解決など、機能別に AI へ何をどの条件で依頼するかを定義する入口になる。実際のコマンド制御や後段処理ではなく、下流エージェントに渡す prompt と実行条件を組み立てる層である。
- ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念と品質規範、review 基準、INDEX.md エントリー作成規範などを、AI 呼び出し用の構造化文書として生成する実装も含む。

## Read this when
- AI エージェント呼び出しに渡す prompt 本文、補助入力、標準文書の参照有無、ファイルアクセスモード、モデル種別、推論量、Structured Output 契約を確認または変更したいとき。
- 特定機能が AI に依頼する作業内容や制約を追いたいとき。対象にはフォーク適用の変更要約・所見列挙・修正依頼、INDEX.md 用エントリー生成、oracle review の所見列挙・理由収集・採否判定・整理、session join の conflict marker 解消、TUI の実行パラメータ解決が含まれる。
- 標準 prompt part の本文、complete prompt への注入順序、標準文書間の依存関係、補助 prompt の埋め込み方、呼び出し先向けの用語置換や root token 置換を確認したいとき。
- ファイルアクセス制限、INDEX.md によるルーティング、oracle file と realization file の基本定義、oracle / realization の品質規範、review 所見基準、INDEX.md エントリー作成規範を AI 向け prompt としてどう表現しているか調べたいとき。

## Do not read this when
- 各サブコマンドの実行制御、状態管理、git 操作、ファイル走査、保存、merge 実行、生成結果の表示・通知・永続化など、AI 呼び出し前後の処理本体を調べたいとき。
- レビュー所見を実際に評価・統合・適用する後段処理や、realization file の具体的な修正ロジックを探しているとき。
- AgentCallParameter、FileAccessMode、構造化文書、path token、root 解決などの基礎型や共通基盤そのものを確認したいとき。
- CLI コマンド、永続状態、外部プロセス実行、入出力 schema の定義、個別 oracle file・realization file・テストの内容を確認したいだけで、AI 呼び出し用 prompt や呼び出し条件を変更しないとき。

## hash
- 4ccfcb82ac8bbefa988a871a78098c27162f684df65d9a852f960aff3197c1ca

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
- cmoc の実行時共通機能を集めた実装領域。CLI サブコマンドの共通実行ライフサイクル、Codex CLI exec/TUI 呼び出し、設定入出力、内容 hash 保存、共通エラー表示、Git 操作、ログ、runtime path、結果モデル、session state など、複数の上位機能から再利用される runtime helper 群への入口になる。
- 共通入口用の集約・互換 import と、責務別に分割された実装の両方を含むため、横断的にどの runtime 部品が存在するかを把握する起点として使える。個別の振る舞いを変更する場合は、この階層で該当責務の本文へ進む。

## Read this when
- CLI サブコマンドに共通する開始・完了表示、終了コード化、例外表示、subcommand logger の設定範囲を確認または変更したいとき。
- Codex CLI の exec 実行、TUI 起動、profile 生成、Structured Output schema、resume token、quota/capacity retry、call log、console 表示、indexing preflight のどれかに関わる runtime 実装を探したいとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正 JSON や不正値の利用者向けエラー化を扱う共通処理を確認したいとき。
- 内容 hash による保存、ファイルや文字列の SHA-256 digest、binary 判定など、runtime 生成物やキャッシュ的な出力の共通保存 helper を確認したいとき。
- cmoc 共通例外、利用者向け Markdown エラーレポート、Next actions、detail、Call stack の組み立てを確認または変更したいとき。
- Git コマンド実行、branch・HEAD・clean worktree 判定、run worktree 作成削除、cmoc 管理 branch、ignore/exclude 更新などの低レベル Git helper を調べたいとき。
- サブコマンド実行ログの JSON Lines event、経過時間、Codex quota 待機時間の集約、現在 logger を runtime helper から参照する仕組みを確認したいとき。
- 実行時の root 解決、cmoc 管理ディレクトリ、設定・状態・ログ・worktree・schema などの配置、timestamp や経過時間表示、memo 配下判定を確認したいとき。
- 外部コマンド結果や Codex exec 結果として、stdout/stderr、生成物、ログ path、profile/schema、経過時間、quota 待機情報を運ぶ共有データ構造を確認したいとき。
- session branch と apply branch に紐づく永続 session state の JSON 入出力、保存先、branch 名からの session-id 抽出、active session 探索を調べたいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、利用者向け出力内容そのものを調べたいとき。その場合はサブコマンド実装側へ進む。
- 正本仕様断片、パス概念そのもの、oracle file と realization file の定義、INDEX.md 生成規則を確認したいとき。この領域は実装 helper であり、仕様判断の根拠は対応する仕様文書を読む。
- テスト期待値や fixture、特定の外部挙動の検証内容だけを確認したいとき。その場合はテスト領域の該当本文へ進む。
- 個別機能の高レベル workflow だけを把握したいとき。共通 helper の詳細に入る前に、その workflow を所有する上位実装から読む方がよい。
- ファイル名や配置だけを一覧したいとき。ここで読むべき対象は、runtime 共通責務の変更・調査がある場合に絞る。

## hash
- 4a52c7ef3508834fb9ac90a2aa260d98f0e00efee430c34bde4dca5b2f9d081e

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
