# `acp`

## Summary
- AI agent 呼び出しの入力契約を作る実装領域。用途別に、role・summary・goal・補助文脈・ファイルアクセス条件・モデル種別・reasoning effort・Structured Output schema を組み合わせた呼び出しパラメータを生成する処理と、そこへ差し込む標準プロンプト部品を生成する処理を扱う。
- サブコマンド本体の制御や低レベル実行基盤ではなく、上位処理が AI に何を依頼し、どの規範・制約・出力形式で応答させるかを確認するための入口になる。

## Read this when
- AI agent 呼び出しに渡すプロンプト内容、補助文脈、ファイルアクセス条件、モデル種別、reasoning effort、Structured Output schema の選定や変更を確認したいとき。
- 変更要約、所見列挙・適用、ルーティングエントリー生成、仕様レビュー、所見の採否判定・統合、conflict marker 解消、実行パラメータ選定など、用途別の AI 依頼内容を追いたいとき。
- 仕様ファイルと編集対象ファイルの扱い、ルーティング規則、ファイルアクセス規則、仕様文書基準、編集対象ファイル保守基準、レビュー基準、ルーティングエントリー基準などが、agent 向けプロンプトへどう組み込まれるか確認したいとき。
- ユーザー入力、対象ファイル内容、差分、レビュー所見、競合箇所、標準文書などの補助情報が、AI 呼び出し時の文脈としてどのように渡されるかを調べたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、作業順序、状態保存、表示、外部コマンド実行など、AI 呼び出し builder を使う側の制御フローだけを調べたいとき。
- AI 呼び出し基盤の型定義、Structured Output 実行器、構造化文書レンダリング、path model、git wrapper などの低レベル共通部品そのものを確認したいとき。
- 仕様本文、テスト本文、個別レビュー基準の正本内容、または生成されたルーティングエントリーの文面そのものを読みたいだけのとき。
- 実ファイル編集、差分分類、merge conflict 解消アルゴリズム、git merge、worktree 操作など、AI への依頼後に行われる具体的な下位処理を調べたいとき。

## hash
- dc6e4d3f587f59405552b72bd38f5f2299ebcd0ca1481c2d2f8652e20babeb07

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
- cmoc の共有 runtime helper 群をまとめる領域。CLI サブコマンド実行の共通ラッパー、Codex CLI 呼び出し、Codex profile 準備、設定読み書き、content hash、共通エラー表示、Git 操作、実行ログ、root/path 解決、外部コマンド結果型、session state など、上位の command 実装から再利用される実行時基盤を扱う。
- 個別機能の業務フローそのものではなく、複数の上位処理から使われる runtime API、永続状態・ログ・設定・外部プロセス実行・エラー変換・path 導出の入口として位置づけられる。

## Read this when
- サブコマンド実行時の共通ライフサイクル、開始・完了表示、終了コード化、例外表示、サブコマンドログ連携を確認または変更したいとき。
- Codex CLI の exec/TUI 起動、profile・schema・output JSON、stdout/stderr/call log 保存、capacity/quota retry、resume token、validation retry などの呼び出し制御を追いたいとき。
- cmoc の実行時設定、設定ファイルの初期生成・既定値補完・JSON 変換・不正値エラーを扱いたいとき。
- file/text hash、hash 付き生成ファイル、binary 判定など、生成物や内容比較に使う共通処理を確認したいとき。
- cmoc 共通エラー型、利用者向けエラー文面、通常例外からの表示整形を確認または変更したいとき。
- Git command 実行、repository 状態検査、一時 worktree/managed branch の作成削除、Git ignore 判定、.cmoc の Git 管理外保証を扱うとき。
- サブコマンド実行ログ、JSON Lines record、current logger、実行時間・quota wait 集計を確認または変更したいとき。
- repo root、work root、cmoc root、.cmoc 配下の sessions/reports/log/worktrees/state/config、timestamp、duration 表示、作業ディレクトリ一時変更を扱うとき。
- 外部コマンドや Codex exec の共有結果型、または session/apply state file の JSON schema・読み書き・管理 branch からの state 解決を確認したいとき。
- 上位モジュールが利用する共通 runtime symbol の公開入口や import 経路を調整したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、ユーザー向けコマンド構成、処理順を調べたいとき。その場合は command 実装側へ進む。
- path keyword そのものの意味や root path model の概念定義を確認したいだけのとき。その場合は path model の定義を読む。
- 設定値そのもののデータ構造や既定値だけを確認したいとき。その場合は設定モデル定義を読む。
- Agent call parameter、model class、reasoning effort、file access mode など、Codex 呼び出しパラメータの基本定義だけを確認したいとき。
- ログを読む側、集計する側、表示する側の仕様を探しているとき。その場合はそれらの処理を持つ対象へ進む。
- 特定の helper の仕様・例外条件・副作用だけを確認したいときは、集約入口ではなく、その helper の定義本文へ直接進む。

## hash
- 90bb9af438772f1aa9a2429bb71c0a77d5e98758e2c9769ea811ce52799a3fe4

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
- cmoc の Typer ベース CLI の最上位エントリーポイントを定義し、`init`、`tui`、`session`、`apply`、`review`、`indexing` などのサブコマンドを各実装へ委譲する。
- 通常の CLI 引数解析エラーを cmoc 形式のエラーレポートへ変換し、シェル補完時は通常の Typer/Click 処理を通す。
- Codex exec/TUI 呼び出し前に indexing preflight を走らせるラッパーと、indexing 自身や conflict resolution 用途では再帰的な indexing を避ける制御を持つ。

## Read this when
- CLI の最上位コマンド、サブコマンド階層、option の受け取り方、または各サブコマンド実装への委譲先を確認・変更したいとき。
- cmoc の CLI 引数解析失敗時の表示形式、終了コード、補完時の挙動を確認・変更したいとき。
- Codex exec/TUI 呼び出し前に indexing preflight が走る条件、対象 root の決定、再帰防止、skip 条件を確認・変更したいとき。
- 新しいサブコマンドを公開面として追加する、または既存サブコマンドの `command_name`、`command_argv`、注入する runtime 関数を調整したいとき。

## Do not read this when
- 個別サブコマンドの実処理、永続状態操作、Git 操作、review 内容、session/apply の詳細挙動を調べたいだけなら、それぞれの委譲先実装を直接読む。
- Codex runtime の実行方法、エラー描画、repo/work root 解決、git コマンド実行の詳細を調べたいだけなら、runtime 側の実装を読む。
- indexing preflight や INDEX.md 生成処理そのものの詳細を調べたいだけなら、indexing の実装を読む。
- CLI 経由ではない内部 API や設定 schema の詳細を調べたいだけなら、該当する設定・基礎型・runtime の定義を読む。

## hash
- 4477314efa668ce16503f5bac15971b80f5939c8307907ab36b1a85acd31aee3

# `sub_commands`

## Summary
- cmoc の利用者向けサブコマンド実装を集めるディレクトリ。リポジトリ初期化、session の作成・取り込み・破棄、apply の実行・join・破棄、INDEX.md 保守、oracle review、対話型実行の各入口と実行フローを扱う。
- 各サブコマンド実装は、現在 branch、worktree の清潔性、session/apply state、cmoc ignore、専用 worktree/branch、report 出力、Codex 呼び出しなどを組み合わせて利用者操作を実現する。
- session 系と apply 系は下位ディレクトリにまとまり、review 系は対象列挙、finding loop、INDEX 差分取り込み、report 描画に分かれているため、サブコマンド単位の挙動を調べるための入口になる。

## Read this when
- cmoc のサブコマンドがどの実装へ分かれているかを、init、session、apply、indexing、review、TUI の観点で選びたいとき。
- サブコマンド実行時の事前条件確認、branch/worktree 操作、状態ファイル更新、report 生成、利用者向け stdout のどこを読むべきか切り分けたいとき。
- session branch のライフサイクル、apply branch/worktree のライフサイクル、oracle review の一時 worktree、INDEX.md 保守処理など、複数サブコマンドにまたがる操作の入口を探すとき。
- Codex CLI を呼び出すサブコマンド処理で、どの段階で AgentCallParameter builder を使い、結果を状態・commit・report に反映するかを追い始めるとき。

## Do not read this when
- Typer app 全体のコマンド登録、トップレベル CLI wiring、共通 option 定義だけを調べたいとき。
- git 実行 wrapper、repo/work/root path 解決、worktree 操作、branch 操作、state schema、config 読み込み、report directory 解決、CmocError など共通 runtime API そのものを調べたいとき。
- Codex に渡す prompt parameter の具体的な文面、Structured Output schema、complete prompt の構成部品そのものを確認したいとき。
- oracle file の正本仕様内容、oracle/realization の概念、INDEX.md エントリー生成規則など、仕様断片そのものを確認したいとき。
- サブコマンドの外部挙動を検証する realization test だけを探しているとき。

## hash
- 706b0741bf77deb4a16a70a2770167f6c35e4b90c75a00597c8ba716f7a2a6a1
