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
- CLI のサブコマンド実装を集約する領域。初期化、対話型実行、INDEX.md maintenance、oracle review、session lifecycle、apply lifecycle など、利用者が起動する主要操作の上位フローを扱う。
- 各実装は、サブコマンド固有の実行前提確認、runtime helper や Codex 呼び出し builder への接続、Git branch/worktree/state/report などの副作用の順序、利用者向け出力の組み立てを担う。
- review と apply は、対象列挙、loop、INDEX 取り込み、report、join/cleanup などが下位要素に分かれており、該当する lifecycle の入口から詳細担当へ進むための階層になっている。

## Read this when
- cmoc の個別サブコマンドがどの実装へ分かれているかを把握し、初期化、TUI、INDEX.md maintenance、oracle review、session、apply のいずれを読むべきか選びたいとき。
- サブコマンド実行時の上位制御フロー、実行条件、状態遷移、Git 操作、worktree/branch lifecycle、report 生成、利用者向け出力の接続先を探したいとき。
- oracle review の対象列挙、finding loop、INDEX.md merge、report rendering など、review 系の責務分担から読むファイルを絞りたいとき。
- apply run の開始、破棄、join、report、実行中 process 状態、apply worktree/branch cleanup など、apply 系 lifecycle の入口を探したいとき。
- session start/join/abandon、active session branch、home branch への取り込み、破棄、merge conflict 解消など、session 系操作の実装入口を探したいとき。
- INDEX.md maintenance の実行本体、または初期化や対話型実行のサブコマンド固有処理を確認・変更する入口を探したいとき。

## Do not read this when
- Typer アプリ全体の組み立てや、サブコマンド登録だけを確認したいときは、CLI routing を担う上位実装を読む方が直接的。
- repo root、path keyword、worktree root、git command wrapper、設定読み込み、状態保存、cmoc ignore、エラー表示などの共通 runtime primitive 自体を調べたいときは、runtime 側を読む。
- Codex に渡す prompt 文面、AgentCallParameter builder、Structured Output schema の具体定義だけを確認したいときは、builder 側の担当実装を読む。
- oracle file の正本仕様内容、INDEX.md エントリー生成規則、path 用語の定義、oracle と realization の関係を調べたいときは、oracle 側の仕様断片を読む。
- サブコマンドの外部挙動をテスト観点から確認したいだけで、実装本体の制御フローを読む必要がまだないときは、対応するテストを読む。

## hash
- 6695000791bc145a26e097e808173aa083dc62c990f8bee9cacef069bf7a08aa
