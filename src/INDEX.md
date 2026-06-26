# `acp`

## Summary
- AI エージェントに渡す完全な呼び出し条件を構築する ACP 実装の領域。用途別の role、summary、goal、補助入力、ファイルアクセスモード、モデル区分、reasoning effort、Structured Output schema への接続と、そこへ注入される標準プロンプト部品を扱う。
- apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成など、サブ機能が agent に何を読ませ、どの権限で何を返させるかを確認する入口になる。

## Read this when
- cmoc のサブ機能が AI エージェントを呼び出す際の prompt 全体、補助入力、権限、モデル設定、出力 schema の対応を確認または変更したいとき。
- apply 系で、差分要約、realization file の所見列挙、検出済み所見への修正依頼など、後段 agent 呼び出しの条件や出力契約を追いたいとき。
- oracle review 系で、新規所見列挙、所見の擁護・反証理由追加、採否判定、所見リスト整理を agent に依頼する prompt と schema を確認したいとき。
- session join の merge conflict marker 解消、TUI 実行前のファイルアクセスモードや標準文書参照要否の選定など、特定用途の事前解決 agent 呼び出しを調べたいとき。
- agent prompt に含めるファイルアクセス規則、ルーティング規則、oracle と realization の基本概念、各種 standard、INDEX.md エントリー標準の生成内容や注入条件を扱うとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の実行順序、git 操作、fork 作成・統合、merge conflict marker 検出、生成結果の保存など、agent 呼び出しパラメータ構築の外側を調べたいとき。
- AgentCallParameter や FileAccessMode などの共通データ型そのもの、構造化ドキュメントの低レベル表現、Markdown rendering、パス解決 helper の基本実装だけを確認したいとき。
- oracle file、realization file、レビュー対象ファイル、git diff、変更ファイル一覧など、agent に渡される材料を作る側の探索・収集アルゴリズムを調べたいとき。
- 標準文書や仕様本文を読むこと自体が目的で、prompt にどう注入されるかや agent 呼び出し条件を確認しないとき。
- 生成済み INDEX.md の内容評価、ルーティング文書一般の書き方、または個別の実装・テスト修正だけが目的で、ACP の prompt 構築や標準プロンプト部品に触れないとき。

## hash
- 57fdfc1bf8cbb62c03b5cb03b2565d3de15fe8b7e3e68bfbce86071132f8bd48

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
- cmoc の実行時に複数領域から共有される runtime helper 群を集めた implementation directory。Codex CLI 呼び出し、CLI サブコマンド共通ライフサイクル、設定入出力、内容ハッシュ、エラー整形、Git 操作、ログ、root/path 解決、外部コマンド結果型、session state 永続化など、上位コマンドが横断的に使う基盤処理への入口になる。
- 個別機能の実装 module と、それらをまとめて再公開する集約入口が同階層にあり、上位の CLI command や workflow 実装から共通 runtime API の責務境界を確認するための領域である。

## Read this when
- CLI サブコマンド全体で共通する開始・完了表示、終了コード化、例外表示、サブコマンドログ記録、runtime root の使い分けを確認または変更したいとき。
- Codex exec/TUI 呼び出しの profile 準備、schema 準備、subprocess 実行、call log、Structured Output 検証、capacity retry、quota wait、resume 継続、preflight、console 表示の runtime 制御を追いたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、永続化形式、不正 JSON や不正値の利用者向けエラー化を扱う共通処理を探すとき。
- 文字列やファイル内容の SHA-256 digest、内容アドレス型ファイルの保存、binary file 判定など、内容ハッシュ系の小さな共通 helper を確認したいとき。
- cmoc 共通の独自例外構造、通常例外の利用者向けエラー整形、Summary・Next actions・Detail・Call stack の出力構造を確認したいとき。
- Git コマンド実行、branch/worktree 状態検査、実行用 worktree 作成・削除、cmoc 内部ディレクトリの Git 追跡除外など、複数コマンドで共有される Git 処理を確認したいとき。
- サブコマンド実行ログや Codex 呼び出し完了サマリーの記録・表示、quota 待機時間や実行時間の集計、context-local logger の扱いを調べたいとき。
- 実行時の repo root・work root・cmoc root 解決、.cmoc 配下の sessions・reports・logs・worktrees・state・config の配置、timestamp や duration 表示、作業ディレクトリ一時変更を確認したいとき。
- 外部コマンド結果や Codex exec 結果として共有される戻り値フィールド、または session/apply の永続状態 schema と branch 名からの state 特定を確認したいとき。
- 上位実装が複数の共通 runtime 機能をまとめて import する公開入口や、runtime API として外部へ露出する要素の整理をしたいとき。

## Do not read this when
- 個別 CLI サブコマンドの業務処理、引数定義、Typer app 登録、利用者向けコマンド出力だけを調べたいときは、コマンド実装側へ進む。
- path キーワードそのものの正本定義や oracle 上の仕様断片を確認したいときは、oracle 側の path model や該当仕様本文を読む。
- 設定データクラス、AgentCallParameter、FileAccessMode、CmocConfig などのデータ構造そのものを確認したいだけなら、モデル定義側を読む。
- INDEX.md の生成ロジック、エントリー生成プロンプト、ファイル探索ルール、indexing の本文生成仕様を調べたいときは、この階層の runtime preflight ではなく indexing 実装や仕様本文へ進む。
- 特定機能の外部挙動を検証するテストケースや fixture を確認したいときは、対応する test 領域へ進む。
- oracle file の内容、正本仕様の変更可否、仕様標準、実装標準、ルーティング標準を確認したいときは、この realization implementation ではなく oracle 文書を読む。

## hash
- 9fd6263c41e960a9ad4922d0e5859e7731e2aa7049f68870a043be7c511e13cc

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
- cmoc の CLI 起動点として Typer アプリを構成し、最上位コマンドと session・apply・review のサブコマンドを各実装関数へ接続する。
- 通常の CLI 引数解析失敗を cmoc 共通のエラーレポート形式へ変換し、シェル補完時は通常の Typer/Click 処理に委ねる。

## Read this when
- 利用者が実行するコマンド名、サブコマンド階層、CLI option の入口定義を確認・変更したいとき。
- CLI 引数解析エラーの表示形式、終了コード、補完時の扱いを確認・変更したいとき。
- サブコマンドの実処理へ到達するまでのディスパッチ経路を追いたいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、永続状態操作、外部コマンド実行の詳細を調べたいときは、ここではなく各サブコマンド実装を読む。
- cmoc 共通エラー型やエラー表示そのものの構造を変更したいときは、CLI 入口ではなく共通ランタイム側を読む。
- テスト方針や仕様断片を調べたいだけで、CLI コマンド登録や引数解析の入口に関心がないとき。

## hash
- 9948446cc3191114d645d8bdd77b57fbcc0fb537b825a2834b17cf15a1b84f93

# `sub_commands`

## Summary
- CLI の各サブコマンド実装へ進むための入口となる領域。初期化、ルーティング文書更新、session 管理、apply 実行、oracle review、TUI 起動など、利用者が直接呼ぶ上位コマンドの制御フローを扱う。
- 各サブコマンドは共通 runtime や git/helper 層を呼び出しながら、事前条件確認、状態遷移、branch/worktree 操作、Codex 実行、出力・report 生成、cleanup を組み合わせる orchestration 層として分かれている。
- review や apply のように内部処理が複数段階に分かれる機能では、対象列挙、実行 loop、report、INDEX 変更処理などの下位モジュールへ進むための分岐点になる。

## Read this when
- 利用者向けサブコマンドの実行順序、事前条件、状態変更、git branch/worktree 操作、標準出力や report 生成を調べたいとき。
- init、indexing、session、apply、review、TUI のどの実装領域へ進むべきか判断したいとき。
- 共通 CLI runtime から個別サブコマンド実装へ、また個別サブコマンドから Codex 実行・git 操作・状態ファイル操作へどう接続されるかを追い始めるとき。
- oracle review の対象列挙、finding loop、INDEX 差分 commit/merge、report 出力など、review 固有の責務境界を切り分けたいとき。
- apply run の開始、join、abandon、process 管理、fork report、apply branch/worktree cleanup など、apply 固有のライフサイクルを調べたいとき。
- ルーティング文書更新の対象選定、既存 entry 再利用、hash 鮮度判定、除外条件、Codex への entry 生成依頼、Markdown 描画を確認したいとき。

## Do not read this when
- CLI 全体の argument parser 登録、共通 runtime wrapper、ログ基盤、設定読み込み、path model、git command wrapper など、サブコマンド固有でない低レベル基盤だけを調べたいとき。
- session state や apply state の schema、永続化形式、active session 探索など、状態モデルそのものを直接確認したいとき。
- Codex に渡す prompt 本文、Structured Output schema、AgentCallParameter の詳細な組み立てだけを変更したいときは、parameter builder 側へ直接進む。
- oracle file の正本仕様、realization/oracle の概念定義、INDEX.md 生成規則そのものを調べたいとき。
- 個別サブコマンドの外部挙動をテストで確認したいだけで、内部の orchestration や helper 呼び出し順を読む必要がないとき。

## hash
- 883d78cc0c7f2d17619a621d96844afd962b415ed361f76845b1ed7ea4380587
