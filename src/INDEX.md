# `acp`

## Summary
- AI エージェント呼び出しに渡す完全な依頼文と実行条件を組み立てる実装領域。役割、作業概要、完了条件、補助文脈、ファイルアクセス制約、利用モデル種別、推論強度、機械処理用の出力 schema を、用途ごとの呼び出しパラメータとしてまとめる。
- 下位には、所見列挙・所見対応・変更要約、仕様文書レビュー、merge conflict 解消、ルーティング文書エントリー生成、TUI 実行パラメータ選定などの個別 AI 呼び出し仕様と、各呼び出しへ差し込む標準文書・規則文書・概念説明の prompt 部品が含まれる。
- 個別サブコマンドの外側の制御ではなく、AI にどの文脈を読ませ、どの権限で作業させ、どの基準文書と出力形式を与えるかを確認する入口になる。

## Read this when
- cmoc から AI エージェントへ渡す prompt、AgentCallParameter、file access mode、model class、reasoning effort、Structured Output schema の組み合わせを確認または変更したいとき。
- 所見列挙、所見対応、変更要約、仕様文書レビュー、所見理由の検証、所見採否判定、所見整理、merge conflict 解消、ルーティング文書エントリー生成、TUI 実行パラメータ選定のいずれかで、AI 呼び出し前に構築される依頼文と補助文脈を追いたいとき。
- oracle file、realization file、git diff、conflict 対象ファイル、ユーザー入力 prompt、既知所見、理由リストなどを、AI 呼び出しの補助文脈としてどのように埋め込むか調べたいとき。
- AI に提示するファイルアクセス規則、ルーティング規則、oracle file と realization file の概念説明、oracle・realization・review・apply review・INDEX.md エントリーの各基準文書を、構造化ドキュメントとして組み立てる実装を確認したいとき。
- 標準文書を完全な prompt へ合成する順序、標準同士の依存関係、Codex CLI 向けの用語置換や root token 置換を確認したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の制御フロー、対象ファイル列挙、git 操作、ブランチ操作、永続状態の保存、表示、並列実行など、AI 呼び出しパラメータ構築の外側を調べたいとき。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、StructDoc、標準文書型、path model、root token 解決などの共通型や汎用 helper の定義そのものを調べたいとき。
- 正本仕様としての oracle file 本文を確認したいとき、または標準文書の人間管理仕様を変更・レビューしたいとき。実装された prompt 部品ではなく、対応する oracle 側の本文を直接読むべきである。
- 実際の oracle file や realization file の内容、個別差分、conflict marker の具体的な解析、所見データの保存形式、変更カテゴリ分類、またはテスト期待値を確認したいとき。
- AI 呼び出し実行処理、サンドボックスや権限適用の実体、外部コマンド実行、エディタ入力、TUI 表示、人間向け出力、補助スクリプト、生成キャッシュを調べたいとき。

## hash
- a9ef1ea3401b413710c88ab882df3bb7be98b2246855f867866af6ae8eda4786

# `basic`

## Summary
- cmoc の実装全体で共有される基礎的な型・変換部品を集めた領域。AI エージェント呼び出し条件、ルートトークン付きパス表記、規範データ、構造化文書の Markdown レンダリングといった、上位機能から再利用される小さな中核モデルを扱う。
- CLI 個別処理やサブプロセス起動などの利用者向けワークフローそのものではなく、それらを支える抽象値、データ構造、文書生成補助、パス解決規則を確認する入口になる。

## Read this when
- cmoc 内部で共有される基本モデルや値オブジェクトの責務、必須フィールド、値検証、変換処理を確認したいとき。
- AI コーディングエージェントへ渡す抽象的な呼び出し条件、モデル品質、推論量、ファイルアクセス権限、Structured Output schema 指定、書き込み許可パスの表現を確認したいとき。
- ルートトークン付きパス表記を実パスへ解決する規則、実パスをトークン基準の表記へ戻す処理、linked worktree や git common dir を含むルート判定を追いたいとき。
- 規範をコード上で保持するデータ構造、要求ラベル、要求本文の単位、規範オブジェクトから構造化文書を作る流れを確認したいとき。
- 内部で組み立てた階層的な自然言語文書を Markdown 見出し、本文、コードブロックとしてレンダリングする処理を確認・変更したいとき。
- 上位モジュールの実装前に、パス、文書、規範、エージェント呼び出し条件について既存の共通部品を使えるか確認したいとき。

## Do not read this when
- CLI サブコマンドの引数定義、画面出力、終了コード、ユーザー操作単位の挙動を調べたいとき。
- 具体的な AI バックエンド名、実モデル名、API 呼び出し形式、権限フラグへの変換処理、または実際のエージェントプロセス起動を探しているとき。
- プロンプト本文の生成規則、テンプレート内容、外部コマンド実行、標準入出力、サブプロセス制御を調べたいとき。
- 個別の正本仕様断片そのものの内容、oracle file の編集方針、仕様管理上の所有関係だけを確認したいとき。
- 既存 Markdown を解析して構造化データへ変換する処理、永続状態、Git 操作、テスト構成や fixture の追加先を探しているとき。

## hash
- 49534930b9cdb9652c55e5e64db692898d6bc6a1a68f0808a946df77f1e14989

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
- cmoc の実行時共通処理を集めた実装領域。CLI サブコマンド実行の共通ライフサイクル、Codex CLI 呼び出し、profile/schema 準備、設定読み書き、内容 hash、共通エラー、Git 操作、ログ、root/path 解決、結果型、session state 永続化などを扱う。
- 個別サブコマンドの業務処理そのものではなく、それらから横断的に利用される runtime helper、型、例外変換、永続化・ログ・外部コマンド実行の入口として位置づく。

## Read this when
- サブコマンド実装から共通利用する runtime helper、型、定数、例外、結果型の所在を探したいとき。
- CLI サブコマンドの開始・完了表示、終了コード化、例外表示、サブコマンドログ設定など、実行ラッパーの共通挙動を確認または変更したいとき。
- Codex CLI の exec/TUI 起動、profile/schema/log path 準備、Structured Output 検証、retry、quota/capacity error 対応、resume 継続を調べたいとき。
- Codex 実行前の indexing preflight 登録・解除・skip 条件・再入防止・排他制御を確認したいとき。
- Codex home 検証、sandbox/permission profile 生成、Codex JSONL からの error/resume/output 抽出など、Codex 呼び出し周辺の補助処理を扱うとき。
- `.cmoc` 配下の設定読み書き、既定値補完、不正 JSON や不正設定値の利用者向けエラー変換を確認したいとき。
- file/text hash、hash 付き生成ファイル、binary 判定など、内容ベースの共通処理を使うまたは変更したいとき。
- cmoc 共通の実行時エラー構造、利用者向け `# ERROR` 出力、通常例外の整形を確認したいとき。
- Git コマンド実行、repository 状態検査、一時 worktree/branch の作成・削除、`.cmoc` ignore 検証、Git ignore 判定を扱うとき。
- サブコマンド実行ログの JSON Lines 追記、current logger の context-local 管理、実行時間や quota wait の計測を確認したいとき。
- 実行時の root path 解決、`.cmoc` 配下の保存先導出、timestamp/duration 表示、作業ディレクトリ一時変更を扱うとき。
- 外部コマンド結果や Codex exec 結果の共有データ型、session/apply state の読み書き、branch 名からの session-id 抽出、active session 探索を確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務フロー、利用者向けコマンド構成だけを調べたいとき。その場合は該当する command 実装へ進む。
- path keyword や root 種別の概念定義そのものを確認したいとき。その場合は path model の定義を読む。
- 設定値や基本データ構造の定義、モデル種別、reasoning effort、agent call parameter などの型定義だけを確認したいとき。その場合はモデル定義側を読む。
- INDEX.md 生成ロジック、エントリー生成プロンプト、ファイル探索ルールそのものを調べたいとき。
- ログや state を読む側、集計する側、レポート表示する側の仕様を探しているとき。
- テスト観点や fixture から期待挙動を確認する方が直接的なとき。
- oracle の正本仕様断片を確認したいとき。この領域は realization implementation であり、正本仕様の入口ではない。

## hash
- d98ad7b890103a0ef8e8df32f506f6aa4aaa0a7fd814c4fd0e663b4d21836fa4

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
- CLI サブコマンドの利用者向け実行処理をまとめる実装領域。初期化、ルーティング文書更新、対話的 Codex 起動、session の開始・取り込み・破棄、apply run の開始・取り込み・破棄、oracle review の実行と report 生成を扱う。
- 各サブコマンドは、引数・前提条件・branch/worktree 操作・状態更新・Codex 呼び出し・利用者向け出力を、runtime、状態定義、prompt builder、設定、report 保存などの共通基盤へ接続する役割を持つ。
- apply、session、review など処理群ごとに下位対象が分かれているため、CLI 層から特定業務フローの実装入口を探すためのルーティング対象。

## Read this when
- cmoc のサブコマンドが、どの前提条件を確認し、どの runtime helper や Codex 実行を呼び、どの状態遷移や stdout/report 出力を行うかを追いたいとき。
- init、indexing、tui、session fork/join/abandon、apply fork/join/abandon、review oracle のいずれかの実行フロー、失敗条件、cleanup、warning、report 生成を確認または変更したいとき。
- session branch、apply branch、isolated worktree、review worktree、INDEX 更新、merge conflict 解決、編集禁止対象の差分復元など、サブコマンド単位で接続される制御の入口を探したいとき。
- CLI から下位 helper へ渡される主要な値、特に session state、apply state、scope、config、worktree、branch、commit、finding、report path の流れを把握したいとき。

## Do not read this when
- CLI 全体のアプリケーション構成、サブコマンド登録の最上位定義、共通 command dispatch だけを確認したいときは、より上位の CLI 実装を読む。
- git 実行 wrapper、worktree 操作、state schema、path model、timestamp、設定読み込み、report directory、CmocError など共通基盤そのものの内部実装を調べたいときは、runtime や共通 utility 側を読む。
- Codex に渡す prompt や Structured Output schema の具体的な定義だけを確認したいときは、builder 側を読む。
- 各サブコマンドの外部挙動を検証するテスト、fixture、期待出力だけを確認したいときは、対応するテスト領域を読む。

## hash
- c80579e5e41bc35ac26a0f621ea592d6de75c4a444d0df64efdc0d4ac9ed3299
