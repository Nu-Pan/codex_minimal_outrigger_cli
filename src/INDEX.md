# `acp`

## Summary
- ACP 関連の realization implementation をまとめる領域。AI agent 呼び出し用の builder と、agent に渡す標準 prompt part の構築処理を下位に持ち、役割・目的・補助文脈・権限・モデル設定・Structured Output schema・標準規則文を agent call へ接続する入口になる。
- 実際の CLI 制御、永続状態、git 操作、差分解析、レビュー判定、ファイル更新そのものではなく、下流 AI に依頼する作業内容と返却契約、またはその prompt に含める規則文を構成するための領域である。

## Read this when
- AI agent へ渡す prompt、role、summary、goal、補助文脈、ファイルアクセス権限、モデル設定、Structured Output schema の接続を確認または変更したいとき。
- フォーク適用、INDEX.md 用エントリー生成、oracle review、session conflict 解消、TUI 入力解決などの各機能が、どのような agent 呼び出しパラメータを組み立てているかを追いたいとき。
- file access rule、routing rule、oracle/realization の基本概念、oracle・realization・review・index entry の各標準など、AI に提示する標準 prompt part の生成箇所を調べたいとき。
- 対象本文、raw diff、oracle file、既存所見、対象ファイル一覧、利用者入力などが、どのような補助文脈として agent prompt に埋め込まれるかを確認したいとき。

## Do not read this when
- CLI コマンド全体の制御フロー、保存、表示、状態管理、ユーザー入出力、git 操作、merge や conflict 検出など、agent 呼び出しパラメータ構築の外側にある実処理を調べたいとき。
- 差分解析、レビュー所見の統合・重複排除、修正結果の検証、ファイル更新など、AI に渡す prompt や schema の構成ではない実処理を探しているとき。
- Standard、Requirement、StructDoc、Markdown rendering、path token、パスモデル、ACP の基礎型など、複数領域で共有される汎用部品そのものを変更したいとき。
- 特定の oracle file、realization file、差分本文、または個別 schema 項目の詳細だけを読みたいときは、該当する本文または schema へ直接進めばよい。

## hash
- 6935451526c2a50197d85c6bd2c14a9a832d36b8b7037c6296cd21af025a8ea7

# `basic`

## Summary
- cmoc の実装全体で共有される基礎モデルと小さな文書処理ユーティリティを置く領域。エージェント呼び出し条件、ルートトークン付きパス解決、規範文書モデル、階層文書から Markdown への変換といった、特定の CLI サブコマンドより下位の共通概念を扱う。
- バックエンド固有の API 値、個別コマンドの実行フロー、ファイル読み書きそのものではなく、それらの上位処理が参照する抽象的な型・変換・検証・レンダリングの入口として位置づけられる。

## Read this when
- モデルクラス、reasoning effort、ファイルアクセスモード、Structured Output schema の有無など、AI コーディングエージェント呼び出し条件をコード上でどう保持するか確認したいとき。
- ルートトークン付きパス表記を実パスへ解決する挙動、または実パスをルートトークン付き表記へ戻す挙動を確認・変更したいとき。
- main worktree、linked worktree、現在の worktree、Git common dir などを使った cmoc 固有のルート探索や失敗条件を調べたいとき。
- 規範文書を構成する見出し、背景、要求、判断例、要求項目ラベルを実装上のモデルとしてどう検証・保持するか確認したいとき。
- 規範文書モデルや階層化された自然言語文書を、表示・文書用の構造化表現または Markdown 文字列へ変換する処理を確認したいとき。
- 文書本文やコードブロックのインデント正規化、空行整理、Markdown 見出し階層の扱いを確認・変更したいとき。

## Do not read this when
- 個別サブコマンドの CLI 引数、出力 schema、実行順序、ユーザー向け入出力を調べたいとき。
- エージェントプロセスの起動、外部コマンド実行、API 呼び出し、バックエンド固有のモデル名や権限表現への変換処理を探しているとき。
- ファイル内容の読み書き、INDEX 生成、oracle file と realization file の分類、永続状態操作など、基礎モデルを使った業務ロジックを調べたいとき。
- 自然言語で書かれた個別の規範本文や正本仕様断片そのものを読みたいとき。
- 生成された Markdown の保存先、利用元、CLI からの呼び出し経路だけを確認したいとき。
- テストで期待される外部挙動だけを確認したい場合で、共通モデルや内部変換の詳細まで不要なとき。

## hash
- d1d69ef3a0bf213c284d4c2b95623804491fbf9ff997ac57263f1648cb474fbe

# `cmoc_runtime.py`

## Summary
- 公開モジュール名を既存の実体モジュールへ差し替えるだけの互換レイヤー。実装本体は別モジュールに委譲し、この入口から import する利用者にも同じ実体を見せるために、実行時のモジュール登録を置き換える。
- 既存の呼び出し元や配布設定が古い import path を参照している期間だけ残す移行用コードであり、責務別の実行時モジュールまたは実体モジュールへ参照元が移った後は削除対象になる。

## Read this when
- 公開されている古い import path と実体モジュールの対応関係を確認したいとき。
- 互換 import path を残す理由、削除条件、または移行状況を調べるとき。
- この入口を import した場合に、どのモジュール実体が利用されるかを確認したいとき。

## Do not read this when
- 実行時処理そのもののロジック、設定解釈、状態操作、CLI 挙動を調べたいとき。この対象は実装本体ではなく委譲だけを行う。
- 新しい実行時機能を追加・修正したいとき。互換入口ではなく、実体側または責務別の実行時モジュールを読む方が直接的である。
- 互換 import path の削除可否と無関係な一般的なモジュール探索やパス定義を調べたいとき。

## hash
- a36ad0b5d09cbe7d2be546fdafcd27ff3ddaf803744331274a69fb25f15cd7ee

# `commons`

## Summary
- cmoc の実行時共通 helper 群をまとめる実装領域。CLI サブコマンドの共通実行枠、Codex exec/TUI 呼び出し、profile・設定・内容保存・エラー・Git・ログ・path・結果・session state など、複数機能から再利用される runtime 支援を扱う。
- 個別機能の業務ロジックではなく、サブコマンドや上位 workflow が共有する実行基盤、入出力モデル、失敗時表示、永続状態、外部コマンド連携への入口として位置づく。

## Read this when
- CLI サブコマンドを共通の実行ライフサイクル、標準出力、終了コード、例外表示、サブコマンドログへ接続する処理を確認・変更したいとき。
- Codex CLI の exec または対話起動について、profile/schema 準備、sandbox・writable roots、call log、stdout/stderr/output log、Structured Output 検証、capacity retry、quota 待機、resume、subcommand event などの runtime 制御を調べたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、永続化 JSON との変換、不正設定の利用者向けエラー化を扱うとき。
- 内容 hash に基づくファイル保存、digest 計算、binary 判定など、生成物やキャッシュ的出力の共通保存 helper を確認したいとき。
- 利用者向け Markdown エラーレポート、共通例外、復旧案内、詳細情報、Call stack の表示形式を確認・変更したいとき。
- Git コマンド実行、branch/HEAD/clean worktree 判定、cmoc 管理 branch、run worktree、ignore/exclude 操作など、Git 状態や worktree 操作の共通処理を調べたいとき。
- サブコマンド実行ログ、Codex 呼び出し完了サマリー、quota 待機時間、context-local logger など、runtime ログの記録・表示を確認したいとき。
- 実行時 root、cmoc 管理ディレクトリ、設定・state・log・worktree・schema 保存先、時刻文字列、memo 配下判定、作業ディレクトリ一時変更を扱うとき。
- 外部コマンド結果や Codex exec 結果として運ぶ戻り値データ、生成物、ログパス、profile/schema、経過時間、quota 待機情報の共有モデルを確認したいとき。
- session/apply branch に紐づく永続 session state、branch 名からの session-id 抽出、state file の読み書き、active session 探索を調べたいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、command 登録、利用者向けの固有出力だけを確認したいときは、そのサブコマンド実装へ進む。
- oracle file の正本仕様、path 概念そのもの、INDEX.md 生成規則、ルーティング文書仕様を確認したいときは、仕様文書や該当する生成処理へ進む。
- 設定値や入力モデルのデータクラス定義そのもの、モデル名や reasoning effort の保持元、公開 schema の仕様だけを調べたいときは、各モデル定義または設定保持側へ進む。
- Codex や Git を利用する上位 workflow の意味や分岐だけを知りたいときは、まず呼び出し側を読み、共通 runtime の詳細が必要になった場合にこの領域へ戻る。
- ログや状態を読む・集計する・表示する側の仕様、レポート内容、CLI の高レベルな制御フローだけを調べたいときは、それぞれの処理を持つ対象へ進む。
- 純粋なテスト期待値や fixture の確認だけが目的で、共通 runtime の型・副作用・失敗時挙動を変更しないときは、対応するテスト領域を直接読む。

## hash
- 9d7ffaad5033c42359d47e86e9543749b407dda48769c36afc8110e11d5a80ee

# `config`

## Summary
- cmoc のリポジトリ単位設定を定義する領域。AI 呼び出しの並列数、Codex CLI に渡すモデル・reasoning effort の対応、apply fork や review oracle のループ上限など、利用者が調整可能な設定値のまとまりを扱う。

## Read this when
- リポジトリごとに永続化される cmoc 設定の項目、既定値、責務境界を確認したいとき。
- Codex CLI に渡すモデル名や reasoning effort 名と、内部表現との対応を確認または変更したいとき。
- AI エージェント呼び出しの最大並列数、apply fork の処理上限、review oracle の各種ループ上限を確認または変更したいとき。
- 設定 JSON の生成・同期・人間編集を前提に、利用者調整可能な値として何が集約されているかを把握したいとき。

## Do not read this when
- 設定ファイルの実際の読み書き、JSON 変換、init 時の生成・同期手順を確認したいとき。
- モデルクラスや reasoning effort そのものの定義、意味、列挙値を確認したいとき。
- 各サブコマンドの実行ロジック、ループ処理、所見生成、apply fork の詳細挙動を追いたいとき。
- cmoc 全体のパス語彙や repo-root・work-root などの定義を確認したいとき。

## hash
- a242e188b7c03be1ee0f0161de15a75b353c820a470ff59f3bab33bcd903ffd8

# `main.py`

## Summary
- Typer による cmoc の最上位 CLI 入口を定義し、`session`、`apply`、`review` などのサブコマンド階層と各 command から実装関数への委譲を束ねる。
- 補完時を除く通常の Click 引数解析エラーを cmoc 共通のエラーレポート形式へ変換する Typer group を含む。
- console script 実行時に cmoc のコマンド名で Typer app を起動する薄いエントリーポイントである。

## Read this when
- cmoc の公開 CLI コマンド構成、サブコマンド名、option 名、または command から呼ばれる実装関数の対応を確認したいとき。
- CLI 引数解析失敗時のエラー表示、終了コード、補完時の例外扱いを調べるとき。
- 新しい top-level command、サブコマンド階層、または Typer command 入口を追加・削除・改名するとき。
- console script から cmoc がどの Typer app を起動するかを確認するとき。

## Do not read this when
- 個別コマンドの実際の処理内容、状態更新、git 操作、worktree 操作、review 実行内容を知りたいだけなら、ここではなく各 command の委譲先実装を読む。
- cmoc の共通エラー型やエラー描画の詳細を変更したいだけなら、ここではなく runtime 側の定義を読む。
- INDEX.md 生成処理そのもの、oracle review の実行ロジック、session/apply の join/fork/abandon の内部仕様を調べたいだけなら、対応する下位実装を直接読む。

## hash
- 1ae81e8854b36901ae139d89729fd33b79be4d1d5836d0a7f352c4e8c307c293

# `sub_commands`

## Summary
- CLI の各サブコマンド実装を集めるディレクトリ。初期化、TUI 起動、INDEX.md 自動保守、review oracle、session 操作、apply 操作など、利用者向けコマンドの実行入口と上位 orchestration へ進むための起点になる。
- 各サブコマンド本体は CLI runtime や git/state/path/config などの共通基盤を呼び出し、引数で選ばれた処理の前提確認、状態遷移、worktree/branch 操作、Codex 実行、利用者向け出力を接続する役割を持つ。
- review oracle や apply/session のように下位モジュールへ分割された領域では、対象列挙、loop、report、merge、process 管理などの詳細実装へ読み進むための入口として機能する。

## Read this when
- 特定の CLI サブコマンドがどの実装へ対応しているか、またはサブコマンド単位の実行順序・前提条件・状態更新・出力を確認したいとき。
- `cmoc init`、`cmoc tui`、INDEX.md 自動保守、review oracle、session 系、apply 系の上位フローを調査または変更したいとき。
- CLI runtime、git 操作、state 永続化、Codex 実行、report 生成などの共通 helper が、利用者向けサブコマンドからどのように呼び出されるかを追いたいとき。
- review oracle の対象列挙・finding loop・INDEX 変更 commit/merge・report 出力、または session/apply の branch/worktree/process 制御について、まず読むべき下位実装を切り分けたいとき。

## Do not read this when
- Typer の最上位コマンド登録、設定 schema、path model、git wrapper、state file schema など、サブコマンド本体ではなく共通基盤だけを調べたいとき。
- oracle の正本仕様、realization 全体の設計方針、INDEX.md エントリー生成規則そのものを確認したいとき。
- 個別 helper の責務がすでに明確で、review の対象列挙・loop・report・INDEX merge、apply runtime helper、session state 操作などへ直接進めるとき。
- 自動テストの期待挙動だけを確認したいときは、対応するテスト側を読む方が直接的。

## hash
- df5b100a442dd209fdbf3944294a1e8045923c3207e6b69c1b57f2913165394a
