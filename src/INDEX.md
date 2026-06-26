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
- サブコマンド実装を集める領域で、初期化、目次更新、TUI 起動、session 操作、apply 操作、review oracle の各実行入口と補助処理へ進むための起点になる。
- 同階層には単体サブコマンドの orchestration と、review や apply の下位 helper、session 系の下位パッケージが並び、CLI 実行前提、git 操作、状態更新、Codex 呼び出し、report 生成などサブコマンド別の責務境界を選ぶために使う。

## Read this when
- どのサブコマンド実装を読むべきかを、初期化、目次更新、TUI、session、apply、review oracle の単位で切り分けたいとき。
- サブコマンドごとの実行フロー、preflight、branch/worktree 操作、状態更新、Codex 実行、利用者向け出力や report 生成への接続を確認したいとき。
- review oracle の対象列挙、finding loop、INDEX 差分 commit・merge、report 保存など、review 系 helper のどこから読むべきか判断したいとき。
- apply run の開始・破棄・join、session branch への取り込み、apply state/process/worktree 管理など、apply 系実装への入口を探しているとき。
- session fork、join、abandon の実行条件、git 操作、rollback、merge conflict、状態遷移の実装を探しているとき。

## Do not read this when
- CLI アプリ全体のサブコマンド登録や Typer ルーティングだけを確認したいとき。
- session state schema、path model、config、git command wrapper、ignore 判定、timestamp、report 保存先など、複数サブコマンドで共有される runtime 基盤そのものを調べたいとき。
- Codex に渡す個別 prompt、AgentCallParameter、Structured Output schema の本文だけを確認したいとき。
- oracle file、realization file、INDEX.md 生成規則、パス語彙など、サブコマンド実装ではなく cmoc 全体の正本仕様やルーティング方針を確認したいとき。
- 対象が session、apply、review oracle の特定 helper まで明確に決まっているときは、この階層で止まらず該当する下位対象へ直接進む。

## hash
- 55a209ad764c7d251b4f8cdcad9bc8397f8147079e958bbfd0ee24ce7d8bb2e6
