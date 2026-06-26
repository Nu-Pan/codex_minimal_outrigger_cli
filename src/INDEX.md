# `acp`

## Summary
- AI エージェントへ作業を委譲するためのプロンプトと呼び出し条件を構築する実装領域。差分要約、所見列挙・採否・統合・修正、ルーティング文書エントリー生成、実行パラメータ選定、merge conflict marker 解消などの用途ごとに、役割、目的、補助文脈、ファイルアクセス制約、参照する標準文書、モデル設定、構造化応答の受け取り方を組み立てる。
- 共通プロンプト部品として、ファイルアクセス規則、ルーティング規則、oracle と realization の基本説明、oracle・realization・レビュー・適用後レビュー・ルーティング文書エントリーの標準文書を構造化文書として生成し、用途別の呼び出し定義から必要なものを注入する入口でもある。

## Read this when
- AI エージェント呼び出しに渡す最終プロンプトの構成、標準文書の注入条件、補助文脈の埋め込み方、ファイルアクセス制約、モデル種別、推論強度、構造化応答 schema の対応を確認・変更したいとき。
- 差分要約、適用後レビュー所見の列挙、所見に基づく realization file 修正、oracle file レビュー所見の列挙・擁護・反証・採否判定・統合、ルーティング文書エントリー生成、TUI 実行前のパラメータ選定、または conflict marker 解消を AI に依頼する条件を追いたいとき。
- 元プロンプト、対象パス、git diff、既知所見、所見本文、擁護理由・反証理由、conflict 対象一覧などの入力が、AI agent 向けプロンプトのどの補助文脈として渡るか確認したいとき。
- ファイルアクセス規則、ルーティング規則、oracle と realization の基本説明、各種標準文書が agent prompt 内でどの文面・順序・依存関係で組み立てられるか確認したいとき。

## Do not read this when
- サブコマンドの引数解析、実行順序、状態ファイルの保存、git 操作、差分取得、conflict marker の検出など、AI 呼び出しパラメータ構築より外側の制御フローを調べたいとき。
- 構造化文書型、標準項目型、パス解決、ファイルアクセスモード、モデル種別、エージェント呼び出しパラメータそのものの共通定義を調べたいだけのとき。
- 実際に生成された個別の所見、変更要約、採否判定、修正内容、または対象コードの妥当性を確認したいだけで、AI に渡すプロンプトや呼び出し条件を変更しないとき。
- CLI の外部挙動、利用者向け出力、テスト fixture、または特定サブコマンドの実行ロジックを調べたいとき。AI agent への依頼文や標準文書注入ではなく、その前後の処理を読む方が直接的な場合はそちらへ進む。

## hash
- 5c767d0aed2ee21f1e7b8b8dc947b492495d8a25a59beff6f01a3338d6993736

# `basic`

## Summary
- cmoc の実装全体で共有される基本的な値オブジェクトと小規模ヘルパーを扱う領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパス表記、規範データ構造、Markdown 向け構造化文書レンダリングなど、上位機能が前提として使う基礎部品を定義する。
- backend 実行、CLI コマンド、仕様管理、テスト実行などの具体的な業務フローへ進む前に、それらが依存する抽象的な入力値・パス解決・文書表現の責務境界を確認する入口になる。

## Read this when
- エージェント呼び出しに渡すモデル品質階層、reasoning effort、ファイルアクセス権限、プロンプト、Structured Output schema、追加書き込み許可パスなどの論理的な指定値を確認・変更したいとき。
- cmoc 内で扱うパス文字列を絶対パスへ解決する規則や、ルートトークン付き表記と実パスの相互変換を確認・変更したいとき。
- 規範をコード上のデータ構造として表現し、要求項目や判断例を構造化文書へ変換する処理を確認したいとき。
- 見出し階層を持つ自然言語文書やコードブロックを組み立て、Markdown 文字列として出力する小さな文書レンダリング処理を確認したいとき。
- 上位の CLI や realization 処理を読む前に、共有される基礎概念の型、入力検証、変換処理の責務を把握したいとき。

## Do not read this when
- 実際の backend が受理するモデル名、サンドボックス設定、プロセス起動、標準入出力、実行結果解析、エラー処理を探しているとき。
- 利用者向け CLI サブコマンドの引数、出力、終了コード、個別コマンドが組み立てるプロンプト本文を確認したいとき。
- oracle file と realization file の所有関係、編集権限、正本仕様断片としての内容そのものを確認したいとき。
- 個別機能がどの作業ディレクトリでファイルを作成・更新するかという業務ロジックや永続状態の扱いを調べたいとき。
- 既存 Markdown の解析、Markdown 以外の出力形式、または構造化文書モデルを必要としない単純な文字列整形を探しているとき。
- テスト構成、fixture、テストケース追加先を探しているとき。

## hash
- 4ed54299b1f479741f38c7c63bcb2752f40ccc691700bc40cb978066521796fc

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
- cmoc の実行時共通処理を集めた実装領域。CLI サブコマンドの共通ライフサイクル、Codex exec/TUI 呼び出し、設定入出力、内容ハッシュ、利用者向けエラー、Git 操作、実行ログ、runtime path、結果型、永続 state など、複数の上位機能から共有される runtime helper 群への入口になる。
- この階層は個別サブコマンドの業務処理ではなく、サブコマンドや workflow から横断的に使われる低レベルから中位の共通部品を責務別に分けている。共通 API の集約面も含むため、共有 helper の公開範囲を確認する起点にもなる。

## Read this when
- CLI サブコマンドの開始・完了表示、終了コード化、例外表示、実行ログ、quota 待機時間など、サブコマンド共通の実行制御を確認または変更したいとき。
- Codex CLI の exec または対話起動について、profile 生成、sandbox/permission 設定、schema/output/call log、retry、Structured Output 検証、capacity/quota 判定、resume 継続、preflight、完了サマリー表示などの runtime 制御を追いたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正 JSON や不正値の利用者向けエラー化、永続化形式の変換を確認または変更したいとき。
- 実行時に使う内容ハッシュ、ハッシュ付きファイル保存、binary 判定、root path 解決、管理ディレクトリ配下の保存先、timestamp、作業ディレクトリ一時変更などの共通 helper を探しているとき。
- cmoc 共通の利用者向けエラー表現、Git repository/worktree/branch の状態確認や後始末、サブコマンド単位の JSON Lines ログ、外部コマンドや Codex 実行結果の共有型を確認したいとき。
- session branch や apply branch に紐づく永続 state の schema、読み書き、branch 名からの session-id 抽出、active session 探索を確認または変更したいとき。
- 上位実装から runtime helper をまとめて import できる公開面を確認し、新しい共有 helper の公開や不要な公開 import の整理を行いたいとき。

## Do not read this when
- 個別サブコマンドの業務処理、Typer command 登録、引数定義、workflow 固有の制御順を調べたいだけのとき。その場合は該当する上位の command や workflow 実装へ進む。
- path keyword の概念定義や oracle 上の root モデルそのものを確認したいとき。この階層では実行時 helper としての path 解決を扱うだけなので、正本仕様側の path model を読む。
- INDEX.md 生成ロジック、エントリー生成プロンプト、oracle 文書の内容、仕様レビュー規則など、routing や oracle の本文仕様を調べたいとき。
- 特定機能の利用者向け外部挙動だけを確認したいとき。共通 runtime の副作用や helper 境界を変更しないなら、対象機能の実装またはテストを直接読む方がよい。
- Codex CLI 自体の仕様、認証ファイルの内部形式、LLM 出力品質、一般的な Git 操作の説明など、cmoc の runtime 実装外の挙動を調べたいとき。

## hash
- 1c942e786ab52bcbf3a5fa5847c6bea1938ecf2f56b97220fdae0e66c2308b0c

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
- CLI サブコマンドの実行入口と、その周辺の orchestration をまとめる実装領域。初期化、ルーティング文書更新、対話的 TUI 起動、session の作成・取り込み・破棄、apply run の開始・取り込み・破棄、oracle review の実行を扱う。
- 各サブコマンドは共通 runtime、状態管理、git/worktree 操作、Codex 呼び出し、report 生成などを接続する位置づけであり、低レベル helper や状態 schema そのものよりも、利用者向け command の前提条件・実行順序・失敗時処理を追う入口になる。
- apply、session、review には下位 module があり、branch/worktree lifecycle、状態遷移、cleanup、merge/conflict 処理、対象列挙、report 描画などの段階別実装へ進むための切り分け点になる。

## Read this when
- CLI サブコマンドの外部挙動に対応する実装入口、実行前条件、状態遷移、git 操作、Codex 呼び出し、stdout/report 出力の流れを確認または変更したいとき。
- init、indexing、tui、session、apply、review oracle のどの処理領域へ進むべきかを、サブコマンド単位で切り分けたいとき。
- session branch、apply branch、isolated worktree、review worktree、INDEX.md 更新 commit、merge conflict 解決、cleanup warning など、サブコマンド実行全体にまたがる制御を追いたいとき。
- 共通 CLI 実行 wrapper や indexing preflight が各サブコマンドからどのタイミングで呼ばれ、利用者操作と内部 helper がどう接続されるかを確認したいとき。

## Do not read this when
- 状態ファイルの schema、path model、git wrapper、worktree helper、config model、timestamp、report directory など、共通基盤の内部実装だけを調べたいときは runtime や utility 側へ進む。
- Codex に渡す prompt、Structured Output schema、AgentCallParameter の詳細な組み立てだけを確認したいときは、各 builder 側へ進む。
- サブコマンドの外部挙動を検証するテスト、fixture、期待出力を調べたいときは、対応するテスト領域へ進む。
- oracle file の正本仕様、review 観点、INDEX.md エントリー生成方針そのものを確認したいときは、oracle 側の文書へ進む。
- apply、session、review のうち確認したい段階がすでに明確で、開始・取り込み・破棄・対象列挙・loop・report・merge 処理などの下位対象へ直接進めるときは、この階層全体ではなく該当する下位実装を読む。

## hash
- 3e4ee66ce4e3ffeb5c660dc235ca33441e0687906525a8fbaa987be29609b434
