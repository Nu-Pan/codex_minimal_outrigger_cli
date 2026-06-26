# `acp`

## Summary
- `src/acp` は、AI agent call parameter と agent prompt の構築を担う実装領域。用途別の builder と、共通 prompt 部品を生成する prompt_parts を下位に持ち、role、goal、補助文脈、ファイルアクセス規則、ルーティング規則、標準文書、Structured Output schema を agent 呼び出しへ渡す形にまとめる入口になる。

## Read this when
- cmoc が Codex/AI agent へ渡す prompt、モデル種別、推論強度、ファイルアクセスモード、Structured Output schema の組み立てを追いたいとき。
- indexing、apply 後レビュー、oracle review、session join、TUI parameter 解決など、サブコマンドや処理段階ごとの agent 呼び出し内容を確認または変更したいとき。
- oracle/realization の基本説明、ファイルアクセス規則、ルーティング規則、各種 standard 文書がどのように complete prompt に注入されるか確認したいとき。

## Do not read this when
- CLI サブコマンド全体の実行順序、引数解析、git 操作、状態保存、画面表示など、agent 呼び出し前後の制御フローを調べたいとき。
- path model、構造化文書型、AgentCallParameter や FileAccessMode などの基礎データ型そのものを調べたいとき。
- oracle file や realization file の正本仕様本文、レビュー判断基準の詳細、生成済み INDEX.md の内容そのものを読みたいとき。

## hash
- bbf2ca64724028b0dd80c27ac0bd07269d2efdd1c0c45d84bffbdf28ff756dd0

# `basic`

## Summary
- cmoc の実装で横断的に使われる基礎データ構造と小さな共通ヘルパーを置く領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパス解決、規範文書モデル、構造化自然言語文書の Markdown 化を扱う。
- CLI コマンドや個別業務処理そのものではなく、上位実装が共有する入力仕様、パス表現、規範表現、文書レンダリングの土台を確認する入口になる。

## Read this when
- エージェント呼び出しに渡すモデル区分、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema パスの保持形式を確認または変更したいとき。
- cmoc 内のパス文字列や Path を絶対パスへ解決する規則、または実パスをルートトークン付き表記へ戻す規則を確認または変更したいとき。
- <cmoc-root>、<repo-root>、<run-root>、<work-root> の意味や探索条件、linked worktree を含む git worktree 判定を追いたいとき。
- 規範をコード上で表すクラス、要求ラベル、要求本文の保持単位、規範オブジェクトから構造化ドキュメントを生成する処理を確認したいとき。
- 見出し階層を持つ自然言語文書をプログラム上で組み立て、Markdown 文字列として出力する共通処理を確認または変更したいとき。

## Do not read this when
- 利用者向け CLI サブコマンドの引数、出力、終了コード、外部コマンド呼び出し形式を確認したいだけのとき。
- 具体的なバックエンド名、実モデル名、CLI 権限指定など、論理パラメータを外部実行形式へ変換する処理を探しているとき。
- プロンプト本文のテンプレート、タスク種別ごとの文章生成ルール、または Structured Output schema ファイル自体の内容を確認したいとき。
- 個別の正本仕様断片そのもの、oracle file と realization file の所有関係、または仕様管理上の分類だけを確認したいとき。
- Markdown の解析、既存 Markdown からの構造抽出、テスト構成、fixture、テストケース追加先を探しているとき。

## hash
- 4e50895bd9496806c613801172ca13cf3d64a38a0c452796748d3317a3dd90e0

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
- CLI サブコマンド実装を集約する階層で、初期化、目次更新、対話 TUI、session 操作、apply 実行、oracle review などの利用者向け操作から各実処理へ進む入口になる。
- 各サブコマンドは、共通の実行前検証、設定・状態読み込み、git branch/worktree 操作、Codex 実行、report 生成、利用者向け出力を組み合わせて、cmoc の主要ワークフローを制御する。
- 処理全体を接続する CLI orchestration と、review 対象列挙・review loop・review report・routing document 差分 merge などの補助実装へ分岐する階層でもある。

## Read this when
- 利用者が実行するサブコマンドの処理入口を探し、どの実装へ進むべきかを選びたいとき。
- init、indexing、tui、session、apply、review などの上位 CLI 操作について、実行順序、事前条件、状態更新、branch/worktree 操作、出力や report 生成の接続を把握したいとき。
- oracle review の対象列挙、Codex review loop、INDEX 変更 commit/merge、review report 生成など、review サブコマンド配下の責務分担を調べたいとき。
- apply run の開始・進行・停止・破棄・取り込みや、session branch の作成・取り込み・破棄など、複数の git 状態と cmoc state をまたぐサブコマンド制御を追いたいとき。
- 目次更新や TUI 起動のように、Codex 呼び出しパラメータ、Structured Output、prompt 生成、対象走査、既存内容の再利用がサブコマンドからどう起動されるかを確認したいとき。

## Do not read this when
- CLI サブコマンドから呼ばれる共通 runtime、git command wrapper、path model、state schema、設定モデルなどの低レベル共通部品そのものを調べたいとき。
- oracle file、realization file、INDEX.md 生成規則、正本仕様断片の記述方針など、仕様文書やルーティング文書の概念を確認したいとき。
- 特定の helper の責務がすでに分かっており、review 対象列挙、review loop、review report、review index 操作、apply の各個別操作などへ直接進めるとき。
- Codex CLI に渡す prompt や parameter builder の内容だけ、または Markdown/Structured Output の共通レンダリング仕様だけを確認したいとき。
- サブコマンドの利用者向け orchestration ではなく、ignore 判定、repo/work root 解決、report 保存先、lock、timestamp、外部コマンド実行の共通実装だけを変更したいとき。

## hash
- 25181e36763a74aeb9002115c378d2db0b68ff63049e533f349c7b2bf961f6d8
