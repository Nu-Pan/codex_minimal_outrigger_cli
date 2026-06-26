# `acp`

## Summary
- AI agent 呼び出しに渡す入力を構築する領域。用途別の role、summary、goal、補助プロンプト、ファイルアクセス条件、Structured Output schema、モデル・reasoning 設定を組み合わせ、最終的な呼び出しパラメータへ接続する実装を扱う。
- 共通プロンプト断片を構築する領域でもあり、oracle と realization の基本説明、oracle・realization・review・apply review・routing・INDEX.md entry・file access rule などの標準文書を構造化文書として生成する。
- 実際のサブコマンド実行、git 操作、状態管理、対象ファイル探索そのものではなく、AI agent に何を読ませ、どの制約で、どの形式の応答を求めるかを確認する入口となる。

## Read this when
- AI agent 呼び出しの role、goal、summary、補助入力、ファイルアクセスモード、標準プロンプト注入、Structured Output schema、モデル設定や reasoning effort の組み合わせを確認・変更したいとき。
- apply 系で、差分要約、対象ファイルごとの所見列挙、検出済み所見の修正適用など、fork 後に agent へ渡す条件と返却契約を追いたいとき。
- oracle review 系で、新規所見列挙、所見の擁護・反証理由、採否判定、所見リスト整理を agent に生成させるプロンプトと schema を確認したいとき。
- session join の conflict marker 解消や、TUI 実行前のファイルアクセスモード・標準参照要否判定など、特定用途の事前判断を agent に依頼するパラメータ構築を調べたいとき。
- INDEX.md エントリー生成で、対象本文の渡し方、既存 INDEX.md を根拠にしない制約、読み取り専用条件、エントリー生成用 schema への接続を確認したいとき。
- oracle file・realization file の基本説明、各種標準、routing rule、file access rule など、複数の agent call で共通利用されるプロンプト本文の生成内容を確認・変更したいとき。

## Do not read this when
- CLI 引数解析、サブコマンドの実行順序、git branch や diff の操作、worktree 作成・統合、永続状態の保存や削除など、agent 呼び出しパラメータ構築の外側を調べたいとき。
- oracle file や realization file の正本仕様・実装本文そのもの、または実際にレビュー・適用される対象ファイルの内容を読みたいとき。
- merge conflict marker の検出、変更ファイル抽出、git diff 生成、所見カテゴリの収集など、agent に渡す材料を作る前段のアルゴリズムを確認したいとき。
- AgentCallParameter や StructDoc などの基礎型、path model、Markdown rendering、JSON schema 実行基盤だけを調べたいとき。
- 生成済み INDEX.md の妥当性評価や、ルーティング文書の一般的な書き方だけを確認したいとき。

## hash
- c7a0bed765c0c2bdf0e1fcc099c579eb487f9fb994d5c3c424f716aadded8a98

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
- cmoc の実行時共通 helper 群を収める領域。CLI サブコマンド共通ライフサイクル、Codex exec/TUI 呼び出し、profile・設定・content hash・エラー・Git・logging・path・result・state など、複数機能から共有される runtime 基盤を扱う。
- 個別責務の実装に加えて、runtime 系 API を呼び出し側へまとめて再公開する集約入口や、互換 import path を保つ薄い橋渡しも含む。

## Read this when
- サブコマンド実行、Codex 呼び出し、設定永続化、Git 操作、実行ログ、path 解決、状態ファイル、共通エラー表示など、複数の上位機能から使われる runtime helper の責務境界を確認したいとき。
- runtime 系の共通 API をどこから import できるか、または集約入口の再公開範囲を変更すべきか判断したいとき。
- Codex CLI 実行に関する profile 準備、exec retry、Structured Output 検証、quota/capacity 制御、TUI 起動、call log 保存、preflight 実行前フックのいずれかを確認・変更したいとき。
- cmoc の設定ファイル、content hash 保存、利用者向けエラー整形、Git repository/worktree 状態、サブコマンド JSON Lines log、runtime path、共有結果型、session/apply 永続状態の共通実装へ進む入口を探しているとき。

## Do not read this when
- 個別 CLI サブコマンドの業務ロジック、引数定義、dispatch、利用者向け入出力だけを調べたいとき。その場合は各サブコマンド本体へ進む。
- path keyword の正本定義、oracle file、INDEX.md 生成仕様など、runtime helper ではなく仕様断片や概念定義そのものを確認したいとき。
- 特定機能の高レベルな処理順序や domain logic を追いたいだけで、共通 runtime helper の入出力・副作用・失敗時挙動に触れないとき。
- テスト期待値や fixture から挙動を確認する方が直接的な変更で、共有 runtime 実装の責務や API を変更しないとき。

## hash
- 8d6164347a52ae3d229e894b8a90a85aa3299a731dd99d3df002efa40b017dc7

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
- CLI サブコマンド実装を集める領域で、初期化、TUI 起動、ルーティング目次更新、review oracle、session 操作、apply 系実行ライフサイクルなど、利用者が直接呼び出す機能の入口になる。
- 各サブコマンドは共通 CLI 実行ラッパー、indexing preflight、git/worktree/session state 操作、Codex 実行、利用者向け Markdown 出力や report 生成などを接続する orchestration を担い、詳細な共通処理や helper 実装へ進む前の切り分け点になる。

## Read this when
- どのサブコマンド実装を読むべきか未確定で、初期化、目次更新、TUI、review oracle、session fork/join/abandon、apply 系操作の責務境界を比較したいとき。
- 利用者向け CLI コマンドの入口、実行前提、共通 runner との接続、サブコマンド固有の状態遷移、出力や report 生成までの高レベルな制御順序を追いたいとき。
- review oracle の対象列挙・実行 loop・INDEX 差分 commit・report、または apply run の開始・破棄・join・process 管理・結果 report など、複数 helper を束ねる実行フローを調べる入口が必要なとき。
- session branch の作成・取り込み・破棄、作業ツリー初期化、ルーティング目次生成、Codex TUI 起動など、サブコマンド単位の外部挙動や失敗時挙動を確認または変更したいとき。

## Do not read this when
- git 実行 wrapper、path model、設定読み込み、状態ファイル I/O、worktree 操作、ignore 判定、timestamp 生成など、サブコマンドから呼ばれる共通 runtime 実装そのものを調べたいとき。
- oracle file、realization file、ルーティング文書、session state schema、prompt 構築、Structured Output schema など、CLI サブコマンド入口ではない仕様・データ構造・生成パラメータを確認したいとき。
- 特定のサブコマンドや下位 helper が読む対象として既に分かっており、この階層で責務境界を比較する必要がないとき。
- 自動テストや oracle 側の正本仕様断片を調べたいだけで、実装側のサブコマンド orchestration を追う必要がないとき。

## hash
- e88a96512118de2d78ef961a780a081abb2f3cd2ee0b2c1e83d26b4f3d170cf6
