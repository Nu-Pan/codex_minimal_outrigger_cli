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
- cmoc の実行時共通処理を集めた realization implementation 領域。Codex CLI 実行/TUI 起動、profile 準備、設定永続化、content hash、CLI サブコマンド共通ライフサイクル、エラー整形、Git 操作、JSON Lines ログ、runtime path、実行結果型、session state など、複数の上位機能から再利用される helper 群への入口になる。
- 集約 import 入口と責務別 runtime module が同居しており、呼び出し側が共通 API の公開面を確認する場合は集約層を、個別挙動や副作用を確認する場合は該当する責務別実装へ進むための階層である。

## Read this when
- cmoc の複数サブコマンドや上位処理から共有される runtime helper の配置と責務分担を確認したいとき。
- Codex CLI exec/TUI の起動、profile/schema/log 準備、retry、quota/capacity 制御、Structured Output 検証、call log 記録、preflight など Codex runtime 周辺の共通実装を探すとき。
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外処理、work root 検査、subcommand log 設定を確認または変更したいとき。
- 設定ファイルの読み書き、既定値補完、不正 JSON や不正値の利用者向けエラー化を扱う共通処理を探すとき。
- SHA-256 digest、内容アドレス型ファイル書き込み、binary file 判定など content hash 系 helper を探すとき。
- cmoc 共通の実行時エラー表現、利用者向けエラー文面整形、Git repository/worktree 操作、runtime path 導出、JSON Lines ログ、実行結果データ型、session state 永続化を確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI 引数定義、利用者向け入出力の具体内容を調べたいだけのときは、該当するサブコマンド実装へ直接進む。
- path keyword や root 種別そのものの正本仕様を確認したいときは、path model の仕様または定義側を読む。
- 設定データクラス、AgentCallParameter、FileAccessMode などの型定義そのものを確認したいだけのときは、モデル定義側を読む。
- INDEX.md 生成ロジック、oracle file の正本仕様、prompt、ファイル探索ルールを調べたいときは、それぞれの indexing や oracle 関連の対象へ進む。
- 特定機能の高レベルな制御順序やテスト期待値を確認したいときに、その機能専用の実装・テストがより直接の読む先として存在する場合。

## hash
- d728c2759472924a5d25cae13c00ceeb0541e4bfebc8390b3f2bcf8917475eb9

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
- cmoc のサブコマンド実装を集める領域。init、indexing、TUI、session、apply、oracle review など、利用者向け CLI 操作の実行時フローと orchestration への入口になる。
- 各サブコマンドは、共通 runtime や状態管理 helper を呼び出しながら、前提確認、branch/worktree 操作、Codex 呼び出し、report 出力、後片付けなどを具体的な CLI 処理として接続する。
- サブコマンド共通の登録や Typer 配線だけでなく、個別業務処理の入口を探すための階層であり、詳細は apply・session・review 系 helper などの下位対象へ分かれている。

## Read this when
- cmoc の利用者向けサブコマンドが、どの実装領域に分かれているかを把握し、init、indexing、TUI、session、apply、review の読む先を選びたいとき。
- CLI 操作から共通 runtime、session state、git branch/worktree 操作、Codex 実行、report 生成へつながる orchestration の入口を探すとき。
- apply run、session fork/join/abandon、oracle review、INDEX.md 更新、TUI 起動など、特定サブコマンドの実行順序や前提条件を確認・変更するための起点が必要なとき。
- サブコマンド単位で責務境界を見分け、下位 helper module と CLI コマンド本体のどちらを読むべきか判断したいとき。

## Do not read this when
- cmoc の path 概念、git wrapper、config、state file、binary 判定、git ignore 判定、Codex 実行 wrapper など、複数サブコマンドで使う共通 runtime の内部実装だけを確認したいとき。
- oracle file、realization file、INDEX.md 生成規則、review 観点など、正本仕様断片そのものを確認したいとき。
- session state の schema、AgentCallParameter、prompt builder、structured output parameter など、サブコマンドから呼ばれるデータモデルやパラメータ生成の詳細だけを確認したいとき。
- 個別のサブコマンドや helper module の読む先がすでに分かっている場合は、この階層ではなく該当する下位対象へ直接進む。

## hash
- 9e500f32172087989b48bca1bba73663f65ec0dfaf67935f818f38e79852e5b4
