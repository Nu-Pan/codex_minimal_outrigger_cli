# `acp`

## Summary
- AI agent 呼び出しに渡す実行パラメータとプロンプト本文を構築する実装領域。各サブコマンドや対話実行が委譲する AI タスクについて、役割、目的、補助文脈、ファイルアクセス権限、モデル種別、reasoning 設定、Structured Output schema を対応づける。
- 扱うタスクは、変更差分の要約、realization file の所見列挙と修正依頼、oracle file レビューの所見列挙・検証・採否判定・整理、merge conflict marker 解消、INDEX.md エントリー生成、TUI 実行前のパラメータ選定に分かれる。
- 共通プロンプト部品として、ファイルアクセス規則、INDEX.md による読み進め方、oracle / realization の基本概念、oracle standard、realization standard、レビュー標準、INDEX.md エントリー標準を構造化文書として生成し、必要な依存関係に応じて完全なプロンプトへ注入する。

## Read this when
- AI agent に委譲する処理で、どの role、summary、goal、補助プロンプト、標準文書、ファイルアクセスモード、モデルクラス、reasoning effort、出力 schema を使うか確認または変更したいとき。
- 変更要約、実装所見、所見修正、oracle file レビュー、conflict 解消、目次エントリー生成、TUI 実行パラメータ選定など、サブタスク別の AI 呼び出し設定を追いたいとき。
- 対象ファイル、差分テキスト、既知所見、擁護・反証理由、conflict 対象一覧、ユーザー入力プロンプトなどの入力文脈が、AI 向けプロンプトへどう埋め込まれるか確認したいとき。
- ファイルアクセス規則、ルーティング規則、oracle / realization の概念説明、各種標準文書のプロンプト本文や、それらが完全なプロンプトへ追加される条件を確認したいとき。

## Do not read this when
- 各サブコマンドの CLI 引数解析、サブコマンド登録、実行順序、Git 操作、worktree 操作、結果保存、UI 表示など、AI 呼び出しを起動する側や呼び出し後の制御フローだけを調べたいとき。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、StructDoc、パス解決など、呼び出しパラメータや構造化文書を支える共通型・共通 helper の実装そのものを確認したいとき。
- 実際にレビュー・修正・conflict 解消される個別の oracle file や realization file の本文を確認すれば足りるとき。
- AI agent の外部プロセス起動、LLM 応答処理、Structured Output の解析、レビュー結果や所見リストの永続化・集約・適用可否判定を調べたいとき。

## hash
- 91829103b565dec94b86be3238b7837dbdcc19630f839271177e5c62a36920f0

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
- cmoc の共通 runtime helper 群をまとめる領域。CLI サブコマンド実行の共通ラッパー、Codex CLI 呼び出し、profile・設定・content hash、共通エラー、Git 操作、実行ログ、runtime path、外部コマンド結果型、session state など、複数の上位モジュールから使われる実行時支援を扱う。
- 上位コード向けには主要 runtime API の集約入口があり、具体的な挙動は責務別の下位実装に分かれている。

## Read this when
- cmoc の実行時共通処理や、複数サブコマンドから共有される helper の所在を探したいとき。
- CLI サブコマンドの開始・完了表示、終了コード化、例外表示、サブコマンドログ設定など、コマンド本体の外側にある共通実行ライフサイクルを確認したいとき。
- Codex CLI の exec/TUI 起動、profile 生成、structured output schema、呼び出しログ、stdout/stderr/output 保存、capacity/quota retry、resume token を伴う再開処理を追いたいとき。
- 設定ファイルの読み書き、content hash、共通エラー表示、Git repository/worktree 操作、runtime root や .cmoc 配下パス、実行ログ、結果型、session state のいずれかに関わる runtime helper を調査・変更したいとき。
- 上位モジュールから利用できる共通 runtime API の公開入口と、個別 helper の定義場所を切り分けたいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、ユーザー向けコマンド構成そのものを調べたいとき。その場合は command 実装側を読む。
- path keyword の概念定義や oracle 上の正本仕様断片を確認したいとき。その場合は path model や oracle 側の本文を読む。
- テスト fixture や期待挙動から確認する方が直接的な変更を行うとき。その場合は対応する test 側を読む。
- 単にパッケージ境界だけを確認したい場合を除き、具体的な runtime 挙動を調べる目的でパッケージ初期化本文に進む必要はない。

## hash
- d62438efb3f1d4e4ca4db8b72cba84a32e2d5e1a7c90ce280d27e37a7c87a49b

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
- Typer による cmoc CLI の最上位エントリーポイントを定義し、session・apply・review などのサブコマンド群を各実装関数へ接続する。
- Codex 実行・TUI 実行の直前に indexing preflight を挟む wrapper と、再入防止・用途別 skip 判定を持つ。
- 通常の CLI 引数解析エラーを cmoc のエラー表示形式へ変換する Typer group を提供する。

## Read this when
- CLI の公開コマンド構成、サブコマンド名、option、各コマンドが呼び出す実装関数を確認・変更したいとき。
- Codex exec または Codex TUI 呼び出し前に indexing が実行される条件、skip 条件、対象 root の決定方法を調べたいとき。
- Typer や click の引数解析エラーが、cmoc のエラーレポートへ変換される入口を確認したいとき。
- アプリケーション起動時に呼ばれる CLI root と、各 subcommand group の登録関係を追いたいとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや状態更新の詳細だけを調べたいときは、ここではなく対応する sub_commands 配下の実装を読む。
- runtime の外部コマンド実行、git 実行、repo/work root 解決、エラー描画の詳細を調べたいときは、ここではなく runtime 側の実装を読む。
- indexing preflight の具体的な走査・生成ロジックを調べたいときは、ここではなく indexing command 側を読む。
- 設定値の構造や AgentCallParameter の内容を調べたいだけのときは、それぞれの定義元を読む。

## hash
- 2042f0df636939b33c38361126b44e08a0d2c3c0f1df794096e3f0ba5b9baf58

# `sub_commands`

## Summary
- cmoc の各サブコマンド実装へ進むための入口。初期化、INDEX.md 保守、対話型実行、oracle review、apply run、session lifecycle など、利用者が実行する command 単位の統括フローを扱う。
- サブコマンドごとの実行前提検証、clean worktree 確認、branch/worktree 操作、状態更新、Codex CLI 呼び出し、利用者向け出力や report 生成への接続を確認するための階層。
- 下位には、apply 系、session 系、review 系の分割実装と、初期化・indexing・TUI など個別サブコマンド本体が並び、目的の command behavior から読む先を選ぶための分岐点になる。

## Read this when
- cmoc のサブコマンドが、CLI 起動後にどの順序で検証・状態確認・Git 操作・Codex 呼び出し・出力生成を行うか調べたいとき。
- session の開始・join・abandon、apply run の開始・join・破棄、oracle review の実行、INDEX.md 保守、初期化、TUI 起動など、利用者向け command の制御フローを確認・変更したいとき。
- サブコマンド単位で branch、worktree、session state、report、commit、merge conflict、cleanup の扱いを追いたいとき。
- 個別 helper ではなく、複数の下位処理をどの command がどう接続しているかを入口から把握したいとき。
- CLI の外部挙動に近い層で、成功時・失敗時のメッセージ、warning、保存 report、状態更新の出所を探したいとき。

## Do not read this when
- repo root、work root、path keyword、git 実行 wrapper、config 読み込み、cmoc ignore、clean worktree 判定、状態保存などの共通 runtime primitive だけを調べたいとき。
- Codex CLI に渡す prompt、AgentCallParameter、Structured Output schema、parameter builder の具体的な文面や構造だけを確認したいとき。
- oracle file の正本仕様内容、INDEX.md エントリー生成規則、oracle と realization の関係、path model の定義を確認したいとき。
- サブコマンドの実装本体ではなく、自動テストから外部挙動や期待結果を先に確認したいとき。
- 生成済み report、生成済み INDEX.md、過去実行結果など、実行後の成果物そのものを読みたいだけのとき。

## hash
- c7e7980de9cc581ee6a84bd40f344123028aac698de3e605bde2762e91867850
