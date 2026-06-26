# `acp`

## Summary
- AI agent 呼び出しに渡すプロンプトと実行パラメータを組み立てる実装領域。用途別の role、goal、補助文脈、file access mode、model class、reasoning effort、Structured Output schema を定義する処理と、それらに注入される共通標準プロンプト部品を扱う。
- レビュー、差分要約、oracle レビュー、merge conflict 解消、ルーティング文書エントリー生成、TUI パラメータ解決など、cmoc の各機能が AI agent に何をどの条件で依頼するかを追う入口になる。

## Read this when
- cmoc の機能が AI agent へ渡す complete prompt、補助文脈、標準文書、アクセス権限、モデル設定、Structured Output schema を確認または変更したいとき。
- レビュー所見、所見修正依頼、差分要約、oracle レビュー、conflict 解消、INDEX.md エントリー生成、TUI パラメータ解決などの AI 呼び出し契約を調べたいとき。
- oracle file、realization file、レビュー、ファイルアクセス、ルーティング、INDEX.md エントリー規範など、agent prompt に含める共通規則の文面や注入関係を確認したいとき。
- 対象パス、git diff、所見リスト、既知理由、conflict 対象一覧、元プロンプトなどが AI 入力へどう埋め込まれるかを追いたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の制御フロー、git コマンド実行、ファイル探索、保存、表示、ブランチ操作など、AI 呼び出しパラメータ構築の外側を調べたいとき。
- 構造化文書の基盤型、Markdown レンダリング、AgentCallParameter 型、file access rule、パス解決など、プロンプトやパラメータ部品を利用する汎用基盤そのものを調べたいとき。
- oracle file や realization file の本文、個別仕様、個別実装、テスト内容を直接確認したいとき。
- 生成済みルーティング文書の内容や各エントリーの妥当性だけを確認したいとき。

## hash
- 3e420b7b21f9254be4f947ebc029debfbca25f96c8b8450711d93ea24bb645c5

# `basic`

## Summary
- cmoc の実装で共通に使う基礎部品を集めた領域。エージェント呼び出し条件の抽象型、ルートトークン付きパスの解決、規範データの表現、構造化文書から Markdown へのレンダリングを扱う。
- 上位の CLI や個別ワークフローから直接利用される低水準のモデル・変換処理への入口であり、バックエンド固有処理や利用者向けコマンド挙動へ進む前に、共通データ構造や共通変換規則を確認する場所である。

## Read this when
- cmoc 内部で共有される基本的な型、値オブジェクト、文書構築ヘルパー、パス解決ヘルパーのどれを読むべきか判断したいとき。
- エージェント呼び出しに渡す論理的なモデル種別、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema 指定の表現を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` を含むパス表記を実パスへ解決する挙動や、実パスをルートトークン表記へ戻す挙動を確認したいとき。
- 規範をコード上のデータ構造として保持し、背景・要求・判断例を構造化文書へ変換する処理を確認したいとき。
- 階層化された自然言語文書やコードブロックを Markdown 見出し付きの文字列へレンダリングする処理を確認したいとき。

## Do not read this when
- 利用者向け CLI サブコマンドの引数、画面出力、終了コード、実行フローを調べたいとき。
- 具体的なバックエンドが受理するモデル名、reasoning effort 値、サンドボックス設定、サブプロセス起動方法への変換を調べたいとき。
- 個別の正本仕様断片そのもの、oracle file の編集方針、仕様管理上の所有関係を確認したいとき。
- 既存 Markdown を解析して構造化データへ変換する処理や、汎用 Markdown パーサを探しているとき。
- テスト構成、fixture、テストケース追加先、または個別機能の作業ディレクトリ上の副作用を調べたいとき。

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
- cmoc の realization implementation のうち、複数サブコマンドや runtime 層から共有される実行時 helper 群を集める領域。Codex CLI 呼び出し、profile 生成、設定ファイル入出力、content hash、共通エラー、Git 操作、ログ、root/path 解決、外部コマンド結果型、session state など、機能実装の土台になる共通処理への入口になる。
- 個別 module は、公開 import 面だけを束ねるもの、サブコマンド実行ライフサイクルを包むもの、Codex exec/TUI を制御するもの、低レベルな path・git・logging・state・config 補助を担うものに分かれているため、cmoc の業務 workflow 本体ではなく共通 runtime の責務境界を確認するための階層である。

## Read this when
- サブコマンドや workflow 実装から再利用する runtime helper、共有データ型、共通エラー、ログ、path、Git、設定、状態管理、Codex 呼び出し周辺の実装を探したいとき。
- Codex exec/TUI の起動前準備、profile/schema/log path、Structured Output 検証、retry、quota/capacity 制御、call log、console/subcommand log event の責務分担をたどりたいとき。
- CLI サブコマンドの共通ラッパー、実行前チェック、開始・完了表示、終了コード化、例外表示、実行時間や quota wait を含む完了サマリーを確認または変更したいとき。
- cmoc 設定ファイルの永続化形式、content hash、binary 判定、CmocError 表現、Git repository/worktree 操作、JSON Lines 実行ログ、root/path 解決、CommandResult/CodexExecResult、session state の読み書きなど、横断的な runtime 基盤を確認または変更したいとき。
- 新しい共通 helper を置く場所、既存 helper の公開 import 面、または複数上位 module から共有される処理の責務境界を判断したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、利用者向けコマンド構成、workflow 全体の高レベル制御だけを調べたいとき。その場合は該当 command や workflow 実装へ進む。
- path keyword や oracle/realization の正本仕様、INDEX.md 生成方針、仕様断片の意味を確認したいとき。その場合は oracle 側の仕様文書や path model 定義を読む。
- テスト期待値や fixture から外部挙動を確認する方が直接的なとき。この階層は主に実装共通部であり、テスト観点だけなら対応する realization test へ進む。
- 特定 helper の詳細な入力、出力、失敗時挙動を変更したい対象がすでに分かっているときは、この階層全体ではなく該当する責務別 module を直接読む。
- 公開 API でも共有 runtime でもない、単一機能内に閉じた小さな処理や UI/出力文言の業務固有ロジックを探しているとき。

## hash
- 697c673933c5697ef5f1696ef587eaaefd923a73689315dda55af126ed9e8172

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
- cmoc の実行入口として Typer アプリケーションを構築し、トップレベルコマンドと `session`、`apply`、`review` 配下のサブコマンドを各実装関数へ接続する CLI 配線を担う。
- 通常の CLI 引数解析エラーを cmoc 共通のエラーレポート形式へ変換する TyperGroup 拡張を含み、シェル補完時は通常の Typer/Click 処理に委ねる。
- 個々のサブコマンドの業務ロジックは保持せず、各サブコマンド実装モジュールへの入口として位置づけられる。

## Read this when
- cmoc コマンド全体の起動経路、Typer アプリケーション構成、サブコマンド階層を確認したいとき。
- 新しい CLI サブコマンドや option を公開面として追加・削除・改名し、対応する実装関数との接続を変更したいとき。
- CLI 引数解析失敗時の表示形式、終了コード、補完時の例外処理回避を確認または変更したいとき。
- `init`、`tui`、`indexing`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracle` がどの実装関数へ委譲されるかを確認したいとき。

## Do not read this when
- 各サブコマンドの具体的な処理内容、状態更新、Git 操作、ファイル生成、レビュー判定の詳細だけを調べたいときは、対応するサブコマンド実装を直接読む。
- cmoc 共通エラー型やエラーレンダリングそのものの仕様・実装を調べたいときは、共通ランタイム側を読む。
- path keyword、oracle file、realization file などの正本仕様上の概念定義を調べたいときは、oracle 側の仕様断片を読む。
- テスト観点や期待される CLI 外部挙動を確認したいだけで、CLI 配線や引数定義を変更しないときは、対象サブコマンドに対応するテストを読む。

## hash
- b6ef09b427ea27ff526149b8d840553659470844d3284c42e959505fec5a9395

# `sub_commands`

## Summary
- CLI サブコマンド本体と、その実行ライフサイクルを支える下位 helper をまとめる実装領域。初期化、ルーティング文書更新、対話的 TUI 起動、oracle review、session 操作、apply run の開始・破棄・取り込みを扱う。
- 各サブコマンドは共通実行 wrapper へ接続され、必要に応じて cmoc ignore の保証、clean worktree 確認、session/apply state の読み書き、git branch/worktree 操作、Codex exec/TUI 呼び出し、report 出力を組み合わせる。
- session と apply は下位ディレクトリにまとまった実装を持ち、review は対象列挙・finding loop・INDEX 変更 merge・report 描画などに分割されているため、どの利用者向けサブコマンド段階を読むかを選ぶ入口になる。

## Read this when
- 利用者向けサブコマンドの実装入口、実行前提、状態遷移、git 操作、Codex 呼び出し、stdout/report 出力の流れを確認または変更したいとき。
- cmoc init、cmoc indexing、cmoc tui、cmoc review oracle、cmoc session 系、cmoc apply 系のうち、どの実装または下位 helper を読むべきか切り分けたいとき。
- CLI 実行 wrapper に渡す command 名・argv、preflight、cmoc ignore 保証、clean worktree 要求、branch/worktree 作成や削除、state file 更新がサブコマンド内でどう接続されるか追いたいとき。
- oracle review の一時 review worktree、finding の列挙・検証・判定、INDEX.md 差分の commit/merge、review report 生成に関する実装入口を探すとき。
- apply run の isolated worktree 実行、finding 適用、編集禁止対象の rollback、process id 管理、apply branch の join/abandon、想定外差分検出、apply report 生成に関する実装入口を探すとき。
- session branch の fork/join/abandon、home branch への merge、merge conflict の Codex 解消依頼、session state 更新に関する実装入口を探すとき。

## Do not read this when
- Typer app 全体の構成、トップレベルのコマンド登録、アプリケーション起動点だけを調べたいときは、CLI を組み立てる上位実装を読む。
- git 実行 wrapper、repo/work root 判定、worktree 作成削除、state schema、config 読み込み、timestamp、report directory、CmocError などの共通基盤そのものを調べたいときは、runtime や model 側を読む。
- Codex に渡す prompt や Structured Output schema の内容だけを確認したいときは、サブコマンド本体ではなく対応する parameter builder 側を読む。
- 各サブコマンドの外部挙動を検証するテストケース、fixture、期待出力だけを確認したいときは、対応する test 領域を読む。
- oracle file と realization file の正本上の意味、レビュー基準、ルーティング文書生成基準などの仕様断片を確認したいときは、oracle 側の文書を読む。

## hash
- c571d237da10fb805d15405c2c135c7068f9522a7b432119247a235c44339e99
