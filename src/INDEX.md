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
- cmoc の実行時に複数のサブコマンドや上位処理から共有される helper・型・例外・結果型・状態管理をまとめた共通実装領域。Codex CLI 呼び出し、profile 構築、preflight、設定読み書き、内容 hash、Git 操作、ログ、root/path 解決、CLI 実行ラッパーなど、個別 workflow の周辺で再利用される runtime 支援への入口になる。
- この階層自体は業務サブコマンド本体ではなく、実行前後の共通ライフサイクル、外部プロセス境界、永続 state、利用者向けエラー変換、保存先 path、ログ記録などの横断的な runtime 責務を探すためのルーティング対象である。

## Read this when
- cmoc の実行時共通 API、共有 helper、共通データ型、例外、ログ、path、設定、Git、Codex 呼び出し周辺の実装入口を探したいとき。
- サブコマンド実装の周囲で共通に行われる、work root 確認、事前検査、ログ設定、終了コード化、例外表示、完了サマリー出力の流れを確認または変更したいとき。
- Codex CLI の exec/TUI 起動、profile や schema の準備、出力 JSON 検証、retry、quota/capacity error、call log、resume 継続など、Codex サブプロセス境界の runtime 制御を追いたいとき。
- 設定ファイルの読み書き、既定値補完、不正設定のエラー化、file access mode から Codex permission profile への変換、Codex home や auth 検証を扱うとき。
- Git repository 状態確認、一時 worktree/branch 管理、.cmoc の ignore 検証、Git ignore 判定など、cmoc が共通利用する Git 操作 helper を確認したいとき。
- 実行ログ、quota 待機時間、実行時間、root/path 解決、.cmoc 配下の保存先、timestamp/duration 表示、作業ディレクトリ一時変更の共通処理を調べたいとき。
- session/apply branch に紐づく state の JSON schema、互換的読み込み、保存、active session 探索、branch 名からの session-id 抽出を確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、利用者向けコマンド構成、画面出力だけを調べたいとき。その場合は各 command 実装へ進む。
- path keyword の概念定義や oracle/realization の正本仕様そのものを確認したいとき。その場合は仕様文書や path model の定義へ進む。
- INDEX.md の生成方針、エントリー生成プロンプト、ファイル探索ルール、indexing 本体のロジックを調べたいとき。ここには Codex 実行前 hook はあるが、indexing 内容生成の本体はない。
- ログを読む側、集計する側、表示する側の仕様や、保存済み実行記録の利用者向け解釈を探しているとき。ここは主にログを書き出す runtime 側である。
- 外部コマンドや Codex 呼び出しの戻り値データ構造だけ、または共通エラーの表示整形だけなど、対象が明確に単一 helper に絞れているときは、この階層全体ではなく該当する個別実装へ直接進む。
- テスト期待値や fixture から挙動を確認する方が直接的な変更を行うとき。その場合は対応する test 側を読む。

## hash
- b262561c20c03b5617ab9774339924c4a5c83d6aee3084f7f41eb08b2cafc93d

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
- cmoc の各サブコマンド本体を実装する領域。初期化、INDEX maintenance、TUI 起動、oracle review、session fork/join/abandon、apply fork/join/abandon など、CLI から呼ばれる業務処理の実行順序と前提条件を扱う。
- 各サブコマンドは共通 CLI 実行 wrapper、git/worktree/state/config/Codex 実行 helper、report 生成、preflight 連携を組み合わせ、利用者向け stdout やエラー条件まで含む orchestration を担う。
- apply と session は下位領域にまとまり、review は対象列挙、finding loop、INDEX 差分の commit/merge、report 描画に分割されているため、サブコマンド単位の入口から詳細 helper へ進むためのルーティング起点になる。

## Read this when
- 特定サブコマンドの実行前条件、状態遷移、branch/worktree 操作、cleanup、利用者向け出力、失敗時の report や warning を確認・変更したいとき。
- cmoc init、indexing、tui、review oracle、session 操作、apply 操作のどの実装へ進むべきかを切り分けたいとき。
- session state や apply state をサブコマンドがどのタイミングで読み書きするか、active/ready/running/completed/error/joined/abandoned などの状態をどの操作が変更するか追いたいとき。
- Codex CLI 呼び出しを伴うサブコマンドで、parameter builder の呼び出し位置、cwd/root/config/purpose の渡し方、実行ループや結果取り込みの流れを確認したいとき。
- INDEX.md 更新 preflight、oracle review、apply finding 適用、session join conflict 解消、TUI prompt 解決など、サブコマンド固有の制御ロジックと共通 runtime helper の接続点を調べたいとき。

## Do not read this when
- Typer app 全体の構成、トップレベルのコマンド登録、CLI 引数定義の全体像だけを調べたいときは、アプリケーション入口側へ進む。
- git 実行 wrapper、worktree 作成・削除、repo/work root 判定、設定読み込み、状態 schema、CmocError、timestamp、report directory などの共通基盤そのものを調べたいときは、runtime や共通 utility 側へ進む。
- Codex に渡す prompt や Structured Output schema、AgentCallParameter の具体的な内容だけを確認したいときは、builder 側へ進む。
- サブコマンドの外部挙動をテスト観点、fixture、期待 stdout/stderr、終了コードから確認したいときは、対応するテスト領域へ進む。
- oracle file の正本仕様や path keyword の定義など、人間意図としての仕様断片を確認したいときは、oracle 側の該当文書へ進む。

## hash
- ac3c05cd025993fe4f16907afd96b9e728de48c50a2acbda4969fada233c4aed
