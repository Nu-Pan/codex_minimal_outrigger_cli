# `acp`

## Summary
- AI エージェント呼び出しに渡す実行条件とプロンプト本文を扱う実装領域。呼び出し目的ごとの role、summary、goal、補助文脈、ファイルアクセス方針、モデル種別、reasoning effort、Structured Output schema の選定と、そこに同梱される標準文書・規則文書の生成をまとめている。
- サブコマンド本体の処理ではなく、別エージェントへ依頼するための AgentCallParameter と構造化プロンプトを追う入口。実装修正、仕様レビュー、目次エントリー生成、TUI 実行パラメータ選定、merge conflict marker 解消など、AI に任せる作業の契約を確認するための領域。

## Read this when
- サブコマンドや内部処理が AI エージェントを呼び出す際、どのような依頼文・標準文書・ファイルアクセス制約・出力 schema を渡しているか確認または変更したいとき。
- AgentCallParameter の構築箇所、モデル種別、reasoning effort、読み取り専用や書き込み許可などのファイルアクセスモードの選択理由を追いたいとき。
- agent に渡す共通プロンプトとして、ファイルアクセス規則、INDEX.md ルーティング規則、oracle / realization の基本概念、レビュー基準、INDEX.md エントリー基準などがどう組み込まれるか確認したいとき。
- 仕様レビュー、apply 系の所見処理、目次生成、TUI 起動前のパラメータ解決、session join の conflict 解消など、AI 呼び出し単位の入力・目的・出力契約を選びたいとき。

## Do not read this when
- CLI 引数解析、サブコマンドの実行順序、git 操作、ファイル走査、永続状態、画面表示、レポート保存など、AI 呼び出しを起動する側の制御フローを調べたいだけのとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode、StructDoc、パスモデルなどの共通型や基盤データ構造そのものを確認したいとき。
- oracle file や realization file の正本仕様本文、個別機能の実装挙動、またはテスト対象を調べたいだけで、agent に渡すプロンプトや Structured Output schema の契約を確認する必要がないとき。
- 実際のサンドボックス enforcement、ファイルアクセス制御の実行時実装、または AI 呼び出し後の結果適用・保存処理を追いたいとき。

## hash
- 9fdb7c0628f430e6df53191a9201dee1918ca21087e622b0b548d133d1623f0d

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
- cmoc の複数サブコマンドから共有される runtime helper 群を置く領域。CLI 実行ラッパー、Codex CLI 呼び出しと profile 生成、設定 JSON の読み書き、content hash、共通エラー整形、Git 操作、実行ログ、root/path 解決、コマンド結果型、session state 永続化などを責務別に分けて扱う。
- 上位コードが共通 runtime 機能へアクセスするための集約 import 境界も含み、個別サブコマンドの業務処理ではなく、その周囲で共通に必要になる実行基盤へ進む入口になる。

## Read this when
- サブコマンド実行時の共通ライフサイクル、開始・完了表示、終了コード化、例外表示、サブコマンドログ連携を確認または変更したいとき。
- Codex CLI の exec/TUI 呼び出し、profile と schema の準備、Structured Output 検証、capacity/quota retry、call log 保存、Codex home や subprocess 環境の扱いを追いたいとき。
- cmoc の実行時設定、content hash、共通エラー、Git repository 状態検査、一時 worktree/branch 操作、ログ JSON Lines、root/path 解決、duration/timestamp 表示など、複数機能から使われる runtime helper を探すとき。
- session/apply branch に紐づく永続 state、branch 名からの session-id 抽出、state file の読み書き、外部コマンドや Codex 呼び出しの共有結果型を確認したいとき。
- 上位モジュールから import できる共通 runtime API の公開面を追加・削除・移動し、既存呼び出し側への影響を確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務フロー、利用者向けコマンド構成、固有の出力内容だけを調べたいとき。その場合は該当 command 実装へ進む。
- path keyword、FileAccessMode、AgentCallParameter、設定データ構造、モデル種別などの概念定義そのものを調べたいとき。その場合は基礎モデルや設定モデルの定義へ進む。
- oracle file、realization file、path model などの正本仕様断片や概念説明を確認したいとき。この領域はそれらを利用する runtime 実装であり、仕様本文の入口ではない。
- ログや state や report を読む側、集計する側、レビューや apply など特定 workflow の高レベル制御を調べたいとき。共通 helper ではなく、その機能を実装する対象へ進む。
- 単にパッケージ境界だけを確認したい場合を除き、具体的な helper の挙動を知りたいときは集約 import 境界ではなく責務別 runtime 実装を直接読む。

## hash
- 72fcaa89c3fcdb91382efb21c5baeb56f04183a1d1c2782bd1873b95a6a90f28

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
- cmoc の各サブコマンド実装を束ねる領域で、利用者向け CLI 操作ごとの実行条件、状態遷移、Git 操作、Codex 呼び出し、report 出力などの入口になる。
- apply、session、review、init、tui、INDEX.md maintenance など、サブコマンド単位の制御フローを追い、必要に応じてさらに個別実装へ進むための分岐点になる。
- 共通 runtime helper そのものではなく、サブコマンドがそれらをどう組み合わせて外部挙動を作るかを確認する場所である。

## Read this when
- cmoc のサブコマンド本体のうち、どの操作の実装を読むべきかを選びたいとき。
- 利用者が実行するコマンドの前提条件、状態更新、Git branch/worktree 操作、Codex 呼び出し、report 生成、失敗時処理の接続を確認・変更したいとき。
- apply run の開始・取り込み・破棄、session の作成・取り込み・破棄、oracle review、init、tui 起動、INDEX.md maintenance など、サブコマンド単位のライフサイクルを調べ始めるとき。
- 個別の共通 helper ではなく、CLI 操作としてのまとまった流れと副作用を確認したいとき。

## Do not read this when
- CLI アプリ全体の command 登録や dispatch 構造だけを確認したいとき。
- Git 実行 wrapper、worktree root 解決、branch 操作、config 読み込み、session state schema、path model、report directory などの共通 runtime 基盤だけを調べたいとき。
- Codex prompt parameter builder、Structured Output schema、Markdown 構造化処理など、サブコマンドから呼ばれる builder や共通処理の詳細だけを確認したいとき。
- oracle file の正本仕様、INDEX.md entry 生成規則、編集禁止領域の原則そのものを確認したいとき。
- 外部挙動を検証するテストケースだけを探しているとき。
- 対象とするサブコマンドや処理領域がすでに特定できているときは、その個別実装へ直接進む。

## hash
- aa6587fb8332ed5200538ab6bbc9f45d36325fd7ff121b9ee2421c50e3451727
