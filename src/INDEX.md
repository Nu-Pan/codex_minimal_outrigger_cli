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
- cmoc の共有 runtime helper 群をまとめる実装ディレクトリ。Codex CLI 呼び出し、profile 生成、設定読み書き、content hash、共通エラー、Git 操作、実行ログ、root/path 解決、結果型、session state、CLI サブコマンド実行ラッパーなど、複数の上位モジュールから使われる共通処理への入口になる。
- この階層には、上位コード向けの集約 import 境界と、責務別に分かれた runtime 実装本文が置かれている。共通 runtime API の公開面を確認する場合は集約入口へ、具体的な挙動を変更する場合は該当責務の実装へ進む。

## Read this when
- cmoc 全体で共有される runtime helper、結果型、状態型、path helper、git helper、logging、Codex 呼び出し処理などの所在を探したいとき。
- CLI サブコマンドの共通実行ライフサイクル、開始・完了表示、終了コード化、例外表示、実行前チェック、サブコマンドログ連携を確認または変更したいとき。
- Codex CLI の exec / TUI 呼び出し、Structured Output 検証、capacity / quota retry、profile 生成、Codex home 検証、call log、resume token、Codex 出力 JSON 読み取りを扱うとき。
- `.cmoc/config.json` の読み書き、既定値補完、不正設定のエラー化、または `.cmoc` 配下の sessions / reports / logs / worktrees / state / config などの path 導出を追うとき。
- cmoc 共通の CmocError、利用者向けエラー表示、外部コマンド結果型、Codex 実行結果型、session state file の JSON schema・保存・復元・session-id 解決を確認したいとき。
- Git repository 状態検査、一時 worktree / managed branch の作成・削除、`.cmoc` の git ignore 保証、git ignore 判定、Git コマンド失敗時の cmoc エラー化を扱うとき。
- 実行ログの JSON Lines 書き込み、current logger の context-local 管理、実行時間や quota wait の計測、hash 付きファイル生成や binary 判定など、複数箇所から共有される低レベル処理を変更したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、prompt 作成、利用者向けコマンド構成や高レベルな制御順だけを調べたいとき。その場合は対応する command 実装へ進む。
- path keyword や `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の概念定義そのものを確認したいとき。その場合は path model の定義へ進む。
- 設定値、AgentCallParameter、FileAccessMode、モデル種別、reasoning effort などのデータ構造そのものだけを確認したいとき。その場合はそれらを定義する対象へ進む。
- ログを読む側、集計する側、レポート表示側、または Codex 呼び出しを使う各サブコマンド側の業務ロジックを調べたいとき。
- oracle file と realization file の概念、編集ルール、正本仕様断片としての扱いを確認したいとき。その場合は oracle 側の仕様文書へ進む。

## hash
- bc7bf3f76af3d69d9843147dd242337ad49ccc6d7645a236fff49aefb772124e

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
- cmoc の各サブコマンド本体を実装する領域で、初期化、INDEX.md 保守、対話実行、oracle review、session 操作、apply 実行 lifecycle の入口になる。
- 各サブコマンドは、branch/worktree/state の事前条件確認、Git 操作、Codex 呼び出し、report 生成、利用者向け stdout、失敗時のエラー化や cleanup をそれぞれの責務範囲で扱う。
- session と apply は下位ディレクトリにまとまっており、session branch の作成・取り込み・破棄や、isolated apply worktree 上での finding 列挙・適用・join・abandon を調べる起点になる。
- oracle review は統括フロー、対象 oracle file 列挙、finding loop、INDEX.md 差分取り込み、review report 描画に分割されており、review 処理のどの段階を読むべきか選ぶ入口になる。

## Read this when
- cmoc の特定サブコマンド実装へ進む前に、初期化、indexing、tui、review、session、apply のどの領域を読むべきか判断したいとき。
- サブコマンド実行時の事前条件、clean worktree 要求、cmoc ignore 確認、branch/worktree/state 操作、stdout 出力、cleanup、エラー処理の入口を探したいとき。
- session branch の作成、home branch への join、session abandon、session join conflict 解決など、session lifecycle の実装を調べ始めるとき。
- apply run の開始、Codex による finding 列挙・適用、apply branch/worktree 管理、編集禁止対象 rollback、process id 管理、join/abandon、report 生成を調べ始めるとき。
- oracle review の active session 制約、一時 worktree/branch、対象 oracle file 選定、finding の列挙・統合・検証・判定、INDEX.md merge、report 出力の接続を追いたいとき。
- 現在の work root に対する INDEX.md 更新、対象除外条件、既存 entry の鮮度判定、Codex CLI による entry 生成、indexing commit を確認または変更したいとき。
- 利用者がエディタで書いた依頼文から完成プロンプトを作り、許可された file access mode で Codex TUI を起動する流れを確認または変更したいとき。

## Do not read this when
- サブコマンドの Typer 登録、トップレベル CLI dispatch、共通 option wiring だけを調べたいとき。
- Git command wrapper、repo/work root 判定、path model、config 読み込み、state schema、report directory 解決、CmocError 表示などの共通 runtime helper 自体を調べたいとき。
- Codex 呼び出しへ渡す prompt 文面、AgentCallParameter builder、Structured Output schema の定義だけを確認したいとき。
- oracle file の正本仕様、INDEX.md entry 標準、review oracle 標準、apply review 標準など、仕様断片そのものを確認したいとき。
- サブコマンドの外部挙動を検証する既存テストや fixture だけを探しているとき。
- 生成済み report、log、state file、過去実行結果の個別内容を確認したいだけのとき。

## hash
- 5514cc30de93e700372ecf0ed269eb8b19e0c5a82091dd19656472ec6fc7a7eb
