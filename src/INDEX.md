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
- cmoc の各サブコマンド実装を集約する領域で、初期化、INDEX.md 保守、対話型 Codex 起動、oracle review、session 操作、apply 実行と取り込みの入口になる。
- 各サブコマンドは Typer から呼ばれる実行関数として、共通 runtime helper を使いながら worktree cleanliness、managed branch、session/apply state、Git 操作、Codex 呼び出し、report 出力などの制御を担う。
- review 系は統括フローから対象列挙、finding loop、INDEX.md 差分取り込み、report 描画へ分かれ、apply/session 系は下位ディレクトリ内で fork/join/abandon と補助処理へ分かれている。

## Read this when
- cmoc のサブコマンド単位の実行フローや、どの実装へ進むべきかを調べ始めるとき。
- init、indexing、tui、review oracle、session fork/join/abandon、apply fork/join/abandon の入口実装や相互の責務境界を確認したいとき。
- サブコマンド実行時の preflight、branch/worktree 操作、session/apply state 遷移、Codex 呼び出し、report 生成、cleanup や warning 出力を追うとき。
- oracle review の対象選定、finding 検証・判定ループ、INDEX.md 変更の取り込み、review report の生成に関わる実装へ進む入口を探すとき。
- apply run の isolated worktree 実行、finding 適用、禁止対象差分の rollback、join 時の想定外差分・merge conflict、abandon cleanup を扱う実装へ進む入口を探すとき。
- session branch の作成、home branch への merge、conflict 解決依頼、破棄時の state rollback や branch cleanup を扱う実装へ進む入口を探すとき。

## Do not read this when
- CLI アプリ全体の command 登録、Typer app の配線、トップレベル dispatch だけを確認したいとき。
- Git wrapper、path model、worktree root、config、state schema、report directory、timestamp、binary 判定、git ignored 判定などの共通 runtime helper 自体を調べたいとき。
- Codex に渡す prompt 文面や Structured Output schema の詳細だけを確認したいときは、AgentCallParameter builder 側を読む。
- oracle file の正本仕様、INDEX.md エントリー生成規則、編集禁止領域などの原則そのものを確認したいときは、oracle 側の仕様断片を読む。
- 生成済み report、log、state file、INDEX.md の個別内容を確認したいだけのときは、それぞれの出力先や対象階層を直接読む。
- 個別の apply 操作または session 操作がすでに決まっているときは、対応する下位実装へ直接進む。

## hash
- 229b703109f71c2a404d960f4042eb0fbf80357b988569ee2865f120e5706034
