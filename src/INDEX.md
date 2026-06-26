# `acp`

## Summary
- AI エージェント呼び出しに渡す内容を組み立てる領域。用途別の role、goal、補助 prompt、対象パスや差分などの埋め込み、読み書き制約、モデル設定、Structured Output schema への接続を扱う。
- agent prompt を構成する標準文書・ファイルアクセス規則・ルーティング規則などの部品と、それらを apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成などの個別用途へ接続する実装への入口になる。

## Read this when
- cmoc が Codex などの AI agent に渡す prompt、補助入力、読み書き制約、Structured Output schema、モデル指定などの組み立て方を確認・変更したいとき。
- apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成など、サブ機能別の agent 呼び出し条件と出力契約を追いたいとき。
- agent prompt に含めるファイルアクセス規則、ルーティング規則、oracle・realization・review・INDEX.md エントリー標準文書の構成や注入順序を確認したいとき。
- CLI 本体から agent を呼ぶ前に、どの用途でどの role・goal・標準文書・追加 prompt・対象パス情報を渡しているかを調べたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の実行順序、git 操作、fork 作成・統合、状態ファイル保存など、agent 呼び出しパラメータ構築の外側を調べたいとき。
- oracle file、realization file、各種 review standard などの正本仕様本文そのものを読みたいとき。
- path model、構造化ドキュメント表現、AgentCallParameter の基本定義、Markdown rendering など、prompt 構築で使われる汎用基盤だけを確認したいとき。
- 実際の対象ファイル探索、git diff 生成、変更ファイル抽出、変更ファイル列挙、merge conflict marker 検出など、agent に渡す材料を作る側の処理詳細を調べたいとき。

## hash
- a3c2f582d1d6ef6cf53aa5fbaa9aa6142a721b7d8d2844aa6bc9f8d086d34a02

# `basic`

## Summary
- バックエンド非依存の基礎データ構造と小さな文書生成ヘルパーを集めた実装領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパス解決、規範文書モデル、構造化文書の Markdown レンダリングを扱う。
- 上位の CLI・制御処理・仕様生成処理から共有される基本型や変換処理を確認する入口であり、具体的なバックエンド実行、コマンド UI、個別仕様本文、テスト構成へ進む前に基礎表現を確認するための対象。

## Read this when
- cmoc 内部で共有されるモデル区分、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema パスなど、エージェント呼び出し入力の保持形式を確認または変更したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` を含むパス表記の意味、探索規則、実パスとの相互変換、ルートトークンなし相対パスの拒否条件を確認したいとき。
- 規範文書をコード上で表す型、要求ラベル、要求本文の保持単位、規範オブジェクトから構造化ドキュメントを生成する処理を確認したいとき。
- 見出しツリー、本文文字列、コードブロックを組み合わせた構造化文書から Markdown を生成する処理や、空行整理・コードフェンス・インデント正規化の挙動を確認したいとき。
- 複数の上位機能から使われる基礎表現の責務境界を確認し、変更先が呼び出し制御、パスモデル、規範モデル、Markdown レンダリングのどれに属するか切り分けたいとき。

## Do not read this when
- 具体的なバックエンド名、実モデル名、CLI 引数、外部コマンド呼び出し、権限指定への変換ロジックを確認したいだけのとき。
- CLI サブコマンドの利用者向け挙動、画面出力、終了コード、永続状態操作、ファイル走査の業務ロジックを調べたいとき。
- 個別の正本仕様断片や oracle file の本文内容、仕様管理上の所有関係や編集責務だけを確認したいとき。
- Structured Output schema ファイル自体の内容、JSON schema の仕様、または特定コマンドの出力 schema を確認したいとき。
- プロンプト本文の組み立て、テンプレート内容、タスク種別ごとの文章生成ルール、または生成済み Markdown 文書の内容そのものを調べたいとき。
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
- cmoc の realization implementation における共有 runtime helper 群をまとめる領域。CLI サブコマンド共通ライフサイクル、Codex exec/TUI 呼び出し、profile・preflight・logging、設定入出力、content hash、共通 error、Git 操作、path 解決、外部実行結果、session state など、複数機能から利用される実行時基盤を扱う。
- この階層には、複数の runtime API を一か所から再公開する集約入口と、責務別の具体的な runtime 実装が並ぶ。呼び出し側が共有 helper を使う入口を探す場合にも、個別 runtime 挙動の実装先へ進む場合にも起点になる。

## Read this when
- CLI サブコマンドに共通する開始・完了表示、終了コード化、例外処理、サブコマンドログ、work root 実行前提などの runtime 制御を確認または変更したいとき。
- Codex CLI の exec 実行、TUI 起動、profile/schema 準備、Structured Output 検証、capacity retry、quota wait/probe、resume 継続、call log 保存、preflight 実行など Codex 呼び出し基盤を調べたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正設定の利用者向けエラー化、内容ハッシュ付きファイル保存、binary 判定など、複数機能から使う低レベル helper を確認したいとき。
- cmoc 共通の error 表現、Git repository/worktree/branch 操作、subcommand event logging、runtime path 解決、外部コマンドや Codex 実行結果の共有データ型、session state 永続化を調べたいとき。
- runtime 系 helper の公開 API を追加・削除・整理する変更や、複数の runtime 領域をまたぐ呼び出し側の依存先を判断したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI 引数定義、入出力内容、dispatch の詳細だけを調べたいときは、そのサブコマンド本体へ進む。
- path keyword の概念定義や oracle による正本仕様断片を確認したいときは、path model や oracle 側の文書・実装へ進む。
- ログや state を読む側・集計する側・表示する側の仕様を調べたいだけのときは、それらの利用側実装へ進む。
- 特定機能のテスト期待値や fixture から外部挙動を確認する方が直接的なときは、対応する test 領域へ進む。
- 共有 runtime helper を使わない局所的な画面表示、prompt 生成、INDEX.md 内容生成、conflict resolution、session/apply など上位機能の制御を変更したいだけのときは、該当する上位実装へ直接進む。

## hash
- 235b846c3b9c7f2c48501dafcb291b1a3351360d56418fad135ca51929befe46

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
- CLI のサブコマンド実装を集約する領域で、初期化、目次更新、TUI 起動、session 操作、apply 操作、oracle review など利用者が直接起動する機能ごとの入口を収める。
- 各サブコマンドは共通 runtime や helper へ処理を委譲しながら、実行前条件、branch/worktree/state の制御、Codex 呼び出し、git 操作、利用者向け出力、report 生成などを CLI 層として接続する位置づけにある。
- 下位には apply 系・session 系のまとまりと、indexing、init、review、review helper、TUI などの個別実装があり、サブコマンド単位の責務分担を選ぶための起点になる。

## Read this when
- cmoc の利用者向けサブコマンドのうち、どの実装または下位 helper を読むべきかを切り分けたいとき。
- init、indexing、tui、session、apply、review oracle の実行フロー、前提条件、状態遷移、git/worktree 操作、Codex 実行との接続を確認したいとき。
- session branch、apply branch、review branch、worktree、session state、report、INDEX 更新など、サブコマンド起点で発生する副作用の流れを追いたいとき。
- CLI 層から対象列挙、loop 制御、report 生成、merge/conflict 処理などの helper へ値がどう渡るかを把握したいとき。

## Do not read this when
- git wrapper、Codex 実行 wrapper、設定モデル、path model、session state schema、ignore 判定など、複数サブコマンドから使われる共通 runtime の内部実装だけを調べたいとき。
- oracle file、realization file、INDEX.md 生成規則、正本仕様断片の記述方針など、仕様文書やルーティング文書の基準を確認したいとき。
- テストコードだけを確認したい、または特定の共通 helper の単体挙動を調べたいとき。
- 対象のサブコマンドや helper が明確に決まっている場合は、この階層ではなく該当する下位対象へ直接進む。

## hash
- 45abf16ad66ba7fad197a9b73e00088df1f52c0f2ba0bece5aef4a469b25affb
