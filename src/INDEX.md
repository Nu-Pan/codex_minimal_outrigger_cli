# `acp`

## Summary
- AI エージェントへ渡す完全な呼び出しパラメータと、その中核になるプロンプト部品を構築する実装領域。用途別の役割・依頼概要・完了条件・補助文脈・ファイルアクセス権限・モデル種別・推論強度・Structured Output schema を組み合わせ、レビュー、適用後所見、ルーティング文書生成、TUI パラメータ選定、merge conflict marker 解消などのサブタスクを agent call に変換する入口になる。
- 配下には、個別サブコマンドや処理段階ごとの AgentCallParameter 生成実装と、ファイルアクセス規則・ルーティング規則・oracle/realization 基本説明・各種標準文書を構造化プロンプトとして組み立てる共通部品が置かれている。実際の CLI 制御、git 操作、状態保存、画面表示ではなく、AI に何をどの制約と返却契約で依頼するかを扱う。

## Read this when
- AI agent に渡す prompt 本文、補助文脈、標準文書の注入順序、ファイルアクセスモード、モデルクラス、reasoning effort、Structured Output schema の対応関係を確認または変更したいとき。
- 実装適用後の差分要約、realization file の要修正点列挙、検出済み所見の修正依頼、正本仕様断片レビュー、INDEX.md エントリー生成、TUI 実行パラメータ選定、session join 時の merge conflict marker 解消を、どのような agent call として組み立てているか追いたいとき。
- oracle/realization の基本説明、oracle standard、realization standard、oracle review standard、apply review standard、index entry standard、routing rule、file access rule が agent prompt にどの条件で含まれるか確認したいとき。
- 各サブタスクの構造化出力が、変更要約、所見、根拠、採否、整理結果、パラメータ選定理由などをどの schema で返させる設計か確認したいとき。

## Do not read this when
- CLI サブコマンドの引数解析、実行順序、分岐制御、結果の保存・表示・集約、git コマンド実行、セッションやフォークの作成・統合そのものを調べたいとき。
- oracle file、realization file、各種標準文書、レビュー基準、ルーティング文書作成基準の正本本文そのものを読みたいとき。
- 構造化ドキュメント型、AgentCallParameter 型、path model、ファイルアクセスモード enum など、プロンプトを組み立てるために利用される基礎型や共通ユーティリティの定義を調べたいとき。
- TUI の画面表示、エディタ入力取得、コメント除去、入力文字列の strip、対話フローなど、agent call パラメータ選定より外側の UI 実装を調べたいとき。
- 所見抽出やカテゴリ分けの実際の判断基準、個別レビュー対象の内容、git diff 生成方法、変更ファイル抽出、merge conflict marker を編集する実処理そのものを調べたいとき。

## hash
- 3658ba2c30103d4776964cff959c82dcd834962949d9c342d0fae42fa6a40dae

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
- CLI の各サブコマンド実装へ進むための入口。初期化、目次更新、対話的 Codex 起動、session 操作、apply 操作、oracle review など、利用者が直接実行する機能の orchestration 層を扱う。
- 各サブコマンドは、実行前条件の確認、共通 runtime helper への接続、branch/worktree/state/report などの副作用制御、利用者向け出力をまとめ、詳細処理は必要に応じて下位 helper や共通実装へ委譲する。
- サブコマンド単位で読む先を選ぶ階層であり、session、apply、review のような複数 module に分かれる機能では、全体の CLI 接続点と個別 helper の責務境界を見分ける起点になる。

## Read this when
- 利用者向けサブコマンドの実行フロー、前提条件、branch/worktree 操作、状態更新、report 出力、標準出力のどこを確認すべきか選びたいとき。
- 初期化、目次更新、対話的 Codex 起動、session fork/join/abandon、apply fork/join/abandon、oracle review のいずれかの CLI 層の実装入口を探すとき。
- サブコマンドが共通 CLI wrapper、preflight、git helper、Codex 実行、設定読み込み、session state、report 生成などをどの順に接続しているかを把握したいとき。
- 複数 module に分かれる session、apply、review 系処理について、上位の orchestration と下位 helper のどちらを読むべきか判断したいとき。
- 目次生成、review 対象列挙、review loop、review report、review branch の merge、apply runtime process 管理など、サブコマンド配下の個別責務へ進む前に全体の位置づけを確認したいとき。

## Do not read this when
- CLI 全体のコマンド登録、Typer app 構成、共通実行基盤だけを調べたいときは、サブコマンド実装ではなく上位または共通 runtime の実装へ進む。
- git command 実行、work root/repo root 解決、設定 schema、ignore 判定、state file path 算出、timestamp 生成など、複数サブコマンドで共有される低レベル helper の内部だけを確認したいとき。
- Codex に渡す prompt や Structured Output parameter の詳細だけを調べたいときは、各サブコマンドから呼ばれる parameter builder や prompt 構築側を直接読む。
- oracle file、realization file、INDEX.md 生成規則、正本仕様断片の記述方針など、仕様文書やルーティング文書の原則を確認したいだけのとき。
- 対象のサブコマンドや helper がすでに明確で、初期化、目次更新、session、apply、review、TUI の個別本文へ直接進めるとき。

## hash
- 2936683fc3e462e2e8058a3ecba9c9d246704be03d169619953920efc5e51036
