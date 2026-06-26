# `acp`

## Summary
- 補助 AI エージェント呼び出しに関する実装をまとめる領域。用途別の呼び出しパラメータ構築と、agent prompt を構成する標準文書・制約文・補助文面の組み立てが下位要素に分かれている。
- cmoc の機能が AI agent に何を依頼し、どのモデル設定・reasoning effort・Structured Output schema・ファイルアクセス制約・標準文書を渡すかを追う入口になる。

## Read this when
- apply、review、session、indexing、TUI などの処理から補助 AI エージェントを呼び出す条件や、渡される role・summary・goal・schema・モデル設定を確認または変更したいとき。
- AI agent に提示される最終 prompt の構成、標準文書の注入、ファイルアクセス規則やルーティング規則の文面を確認または変更したいとき。
- oracle review、realization review、INDEX.md エントリー生成、merge conflict marker 解消など、AI に委譲するサブタスクの依頼内容と構造化出力契約を調べたいとき。

## Do not read this when
- CLI サブコマンドの引数解析、実行順序、git 操作、状態保存、表示処理など、AI 呼び出しパラメータ構築より外側の制御フローを調べたいとき。
- oracle file、realization file、レビュー基準、INDEX.md エントリー基準など、prompt に組み込まれる標準本文そのものを正本として読みたいとき。
- AgentCallParameter、構造化ドキュメント、パス解決、Markdown レンダリング、JSON Schema 読み込みなど、複数領域で共有される基盤型や helper の実装を調べたいとき。
- 個別サブタスクのドメインロジック本体、実際のレビュー判定、git diff 生成、merge conflict marker 検出、TUI 表示や対話処理を調べたいとき。

## hash
- bbf2ca64724028b0dd80c27ac0bd07269d2efdd1c0c45d84bffbdf28ff756dd0

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
- cmoc の共有 runtime helper 群をまとめる realization implementation ディレクトリ。Codex exec/TUI 実行、profile/config、content hashing、CLI 共通ライフサイクル、error、git、logging、path、result、state など、複数サブコマンドから使われる実行時支援を責務別に収める。
- 個別 helper の実装本文に加え、runtime 系 API をまとめて再公開する集約入口や、互換 import path を保つ薄い橋渡しも含むため、共有 runtime API の入口と責務別実装の両方へ進むための階層である。

## Read this when
- CLI サブコマンドに共通する実行前提検査、開始・完了表示、終了コード化、例外処理、サブコマンドログなどの runtime 共通処理を確認または変更したいとき。
- Codex CLI の exec/TUI 呼び出し、profile/schema 準備、CODEX_HOME、sandbox/permission profile、call log、Structured Output 検証、capacity/quota/retry/resume、preflight などの実行時制御を追いたいとき。
- cmoc 設定の読み書き、内容ハッシュ付きファイル保存、利用者向けエラー整形、Git repository/worktree/branch 操作、runtime path 解決、JSON Lines logging、実行結果データ型、session state 永続化など、複数機能で共有される helper の責務境界を探したいとき。
- runtime 系 helper を利用する呼び出し側で、集約入口から import できる API と、責務別 module を直接読むべき API の切り分けを判断したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI 引数定義、入出力内容、dispatch の詳細だけを調べたいときは、そのサブコマンド本体へ進む。
- path keyword や oracle/realization などの正本仕様上の概念定義を確認したいだけのときは、仕様または path model の定義側へ進む。
- INDEX.md の内容生成ロジック、エントリー生成プロンプト、ファイル探索ルールそのものを調べたいときは、indexing や oracle 側の対象へ進む。
- 共有 runtime helper を変更せず、特定機能の高レベルな制御順序、テスト期待値、または利用者向け仕様だけを確認したいときは、より直接の実装・テスト・仕様本文へ進む。

## hash
- d8c90944848409c88d4671ade076706bef39a6c57d29994b0615cd9c37412019

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
- サブコマンド実装群をまとめる領域で、初期化、目次更新、TUI 起動、oracle review、session 操作、apply 操作など、利用者が直接呼び出す CLI 機能の実処理へ進む入口になる。
- 各対象は共通 runtime や低レベル helper ではなく、サブコマンドとしての実行前条件確認、状態遷移、git 操作、Codex 呼び出し、利用者向け出力、失敗時エラー化を組み合わせる orchestration を担う。
- apply と session は下位パッケージに分かれ、review は対象列挙、実行 loop、INDEX 差分処理、report 生成などの helper module に分割されているため、CLI から各処理責務へ読む先を選ぶための階層である。

## Read this when
- cmoc の各サブコマンドの実装入口を探し、どのファイルまたは下位パッケージが目的の CLI 操作を担当するか切り分けたいとき。
- 初期化、目次更新、TUI 起動、oracle review、session branch 操作、apply run/join/abandon など、利用者操作に対応する上位フローを確認したいとき。
- サブコマンド実行時の preflight、session state、branch/worktree 操作、Codex 実行、commit/merge、report 出力がどのコマンド層で接続されるかを追いたいとき。
- review oracle のように複数 helper に分割された処理について、対象列挙、実行 loop、INDEX 差分処理、report 生成のどこへ進むべきか判断したいとき。

## Do not read this when
- Typer アプリ全体のサブコマンド登録、共通 CLI ラッパー、引数 dispatch の構造だけを確認したいとき。
- git 実行 wrapper、path model、config schema、session state schema、cmoc ignore 判定、Codex 実行基盤など、複数サブコマンドから使われる共通 runtime の内部だけを調べたいとき。
- oracle file、realization file、INDEX.md 生成規則、review 観点など、正本仕様やルーティング文書の基準そのものを確認したいとき。
- 個別サブコマンドの詳細責務がすでに分かっており、apply 配下、session 配下、review helper、または特定の単一実装ファイルへ直接進めるとき。

## hash
- 2024a11aabddd72a5dc039f0c0b46e89d945f5ccb6c30e82ae7612c148f1f82a
