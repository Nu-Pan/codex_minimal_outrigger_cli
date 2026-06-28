# `acp`

## Summary
- AI agent 呼び出しに関わる実装をまとめた領域。呼び出し直前に渡すパラメータ構築と、プロンプトを構成する標準文書・規則部品の生成が主な入口になる。
- 対象は、各機能の role、goal、補助入力、ファイルアクセス権限、モデル・reasoning、Structured Output schema の選定と、oracle・realization・review・INDEX.md エントリーなどの標準プロンプト部品である。
- CLI の実行制御や git 操作、ファイル更新、結果の保存・表示そのものではなく、それらの処理が AI agent に依頼する内容と応答契約を組み立てる層を扱う。

## Read this when
- cmoc の機能が AI agent へ何を依頼し、どの制約・標準文書・Structured Output schema を付けて呼び出すかを確認または変更したいとき。
- 変更要約、実装所見調査、所見対応、INDEX.md エントリー生成、oracle レビュー、merge conflict marker 解消、TUI 実行条件選定など、個別の AI 作業依頼のプロンプト設計へ進みたいとき。
- ファイル読み書き制約、INDEX.md ルーティング規則、oracle と realization の基本概念、各種レビュー基準など、AI agent に渡す標準プロンプト部品の生成処理を探したいとき。
- AgentCallParameter に渡る role、summary、goal、aux_prompt、標準参照、file access mode、model class、reasoning effort の対応関係を、処理領域ごとに追いたいとき。

## Do not read this when
- サブコマンド登録、CLI 引数解析、実行順序、状態管理、git branch 操作、merge 実行、ファイルシステム走査や保存など、AI 呼び出し前後の制御フローだけを調べたいとき。
- StructDoc、Markdown rendering、path model、root token、AgentCallParameter、FileAccessMode など、プロンプトや呼び出し条件に埋め込まれる基礎型そのものを確認したいとき。
- oracle file、realization file、テスト、または実際に修正・レビューされる対象ファイルの本文を直接読みたいとき。
- AI 応答後の結果集約、保存、表示、適用可否判断、テスト実行、ユーザー通知、生成済み INDEX.md の描画・更新・保存だけを調べたいとき。

## hash
- c62355f2df833e43f5c3e8ed4d436cc9a0905e98f8227289a5443454bb3bf4bf

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
- cmoc の realization implementation に属する共通 runtime helper 群のディレクトリ。Codex 呼び出し、CLI サブコマンド共通ライフサイクル、設定、内容 hash、エラー表示、Git 操作、ログ、パス、結果モデル、永続 state、ルーティング文書の自動更新など、複数の上位機能から再利用される実行時基盤を集めている。
- この階層は個別コマンドの業務処理ではなく、上位コマンドが共通して使う実行時境界や補助 API への入口である。集約 import 面、責務別 runtime 実装、互換 import 面が混在するため、共通処理の種類を見分けて下位対象へ進むための起点になる。

## Read this when
- CLI サブコマンド実行時の共通フロー、ログ、終了コード、例外表示、標準サマリー出力など、個別コマンドをまたぐ runtime 挙動を調べたいとき。
- Codex exec/TUI 呼び出しの profile 準備、sandbox、CODEX_HOME、Structured Output schema、retry、quota/capacity 制御、call log、preflight などの実行時境界を確認または変更したいとき。
- 設定ファイル、内容 hash 保存、binary 判定、Git 状態・worktree・ignore 操作、path 解決、timestamp、ログ保存先、結果モデル、session state 永続化など、複数機能から使われる共通 helper の実装先を探すとき。
- Codex 呼び出し前のルーティング文書自動更新、対象列挙、hash 検証、エントリー生成、Markdown 描画、更新 commit 作成条件などの indexing 実行経路を追うとき。
- 上位実装から import される共通 runtime API の公開面や、責務分割後も維持されている互換 import 境界を確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務ロジック、表示内容、状態遷移ワークフローそのものを調べたいとき。その場合はコマンド層や該当する上位 workflow の実装へ進む。
- パス概念、oracle file、realization file、session state などの正本仕様断片を確認したいとき。その場合は対応する oracle 側の本文を読む。
- 生成済みのルーティング文書の内容を読むだけで、自動生成・更新ロジックや preflight 経路を追う必要がないとき。
- 外部ライブラリや Codex CLI 本体の仕様、jsonschema の検証仕様、Python 標準例外機構など、cmoc の wrapper 実装外の仕様を調べたいだけのとき。
- 単一の上位機能で渡している具体的な引数、prefix、suffix、保存内容、AgentCallParameter の組み立てなどを知りたいとき。その場合はその呼び出し元の実装へ直接進む。

## hash
- de2bd961d4cc05c4d7e53073acedf8a325b82402ff3cd8860b937560254c65a6

# `config`

## Summary
- リポジトリごとに変わる cmoc の挙動設定を集約する領域で、永続化される設定 JSON に対応する Python 側の設定データ構造と既定値を扱う。
- AI エージェント呼び出しの並列数、Codex CLI に渡すモデル名・reasoning effort 名の対応、apply fork や review oracle の処理上限など、設定として調整される値の入口になる。

## Read this when
- リポジトリごとの cmoc 設定項目、既定値、設定データ構造を確認または変更したいとき。
- 永続化される設定 JSON と Python 側の設定クラスとの対応を追いたいとき。
- Codex CLI に渡すモデル種別や reasoning effort の対応表を確認または変更したいとき。
- AI エージェント呼び出しの並列数や、apply fork・review oracle などのサブコマンド挙動を調整する設定値を確認または変更したいとき。

## Do not read this when
- 設定ファイルの読み書き、JSON 変換、初期化時の同期処理そのものの実装を探しているとき。
- モデル種別や reasoning effort の概念定義そのものを確認したいとき。
- 各サブコマンドの実行ロジック、レビュー所見の生成・マージ・検証処理を確認したいとき。
- cmoc のパス語彙、oracle file、realization file などの基本概念を調べたいとき。

## hash
- a242e188b7c03be1ee0f0161de15a75b353c820a470ff59f3bab33bcd903ffd8

# `main.py`

## Summary
- cmoc の最上位 CLI を構成し、Typer アプリケーション、`session`・`apply`・`review` のサブコマンドグループ、各 CLI コマンドから実装関数への委譲を定義する実装入口。
- 通常の CLI 引数解析エラーを cmoc 形式のエラーレポートへ変換する Typer group を定義し、補完実行時だけ通常の Click/Typer 処理へ逃がす。
- console script から `cmoc` としてアプリケーションを起動するためのトップレベル関数を持つ。

## Read this when
- cmoc の公開 CLI コマンド構成、サブコマンド名、option 名、デフォルト値、各コマンドがどの実装関数へ委譲されるかを確認または変更したいとき。
- CLI 引数解析エラーを cmoc の `CmocError` と `render_error` で表示する挙動、または shell completion 時の例外処理分岐を確認または変更したいとき。
- `cmoc` console script 起動時に Typer app がどの `prog_name` で呼ばれるか、またはトップレベル app とサブ Typer app の接続を確認したいとき。

## Do not read this when
- 個別サブコマンドの本体処理、永続状態操作、git 操作、worktree 操作、レビュー処理、INDEX.md 更新処理の詳細を知りたいだけのときは、各サブコマンド実装を直接読む。
- CLI から呼ばれる実装関数の内部エラー生成、ドメインロジック、入出力ファイルの内容を調べたいだけのときは、この入口ではなく委譲先を読む。
- Typer や Click の一般的な使い方、または cmoc 外のパッケージ設定だけを調べたいときは、この対象を読む優先度は低い。

## hash
- 8e9205551785f5e63cb72c666b12049b600ee51d0e204d4198c7d568ba55a7a3

# `sub_commands`

## Summary
- cmoc の利用者向けサブコマンド実装を集約する領域。CLI runtime から各サブコマンド本体を起動し、事前条件確認、git branch・worktree・状態ファイル操作、Codex 実行、report 生成、利用者向け Markdown 出力までを各コマンドの責務に応じて接続する。
- session lifecycle、apply run、review oracle、indexing maintenance、初期化、TUI 起動といった上位操作の入口であり、共通 runtime や prompt builder、状態モデル、indexing 共通処理へ処理を委譲する前後の orchestration を読むための階層である。
- 特に managed branch 上の状態遷移、isolated worktree での実行、merge・cleanup・rollback・conflict handling、実行結果 report など、利用者操作と永続状態・git 状態が結びつく制御の入口として位置づく。

## Read this when
- cmoc のサブコマンドが CLI runtime からどのように起動され、command 名、argv、preflight、Codex 実行関数、work root runtime の指定がどう渡るかを確認・変更したいとき。
- session の開始、home branch への合流、merge せず破棄する操作など、session branch と session state の lifecycle を利用者操作の入口から追いたいとき。
- apply run の開始、finding 適用 loop、変更 commit、完了後の join、未 join run の abandon、実行中 process の追跡・停止、apply state の遷移と cleanup を調べたいとき。
- review oracle の実行条件、対象 oracle file の列挙、finding の enumerate・merge・validate・judge、INDEX.md 変更の commit・merge、review report 生成までの流れを追いたいとき。
- INDEX.md maintenance をサブコマンドとして起動する流れ、実行前の clean worktree・ignore 条件、lock 付き更新、更新結果 commit、更新件数出力の接続点を確認したいとき。
- 初期化時の .cmoc ignore 保証、設定同期、初期化 commit、利用者の staged 差分や .gitignore 状態の退避・復元、成功時出力を確認・変更したいとき。
- TUI 用の依頼文編集、エディタ選択、元 prompt と完全 prompt の保存、resolve parameter 実行、許可 file access mode 検査、Codex TUI 起動までの流れを確認したいとき。
- サブコマンド固有の merge conflict report、force-resolve、INDEX.md conflict の機械解決、想定外差分の検出、失敗時 report、warning 出力など、利用者操作に伴う異常系制御を調べたいとき。

## Do not read this when
- CLI 全体のトップレベル登録、Typer app 構成、エントリーポイントの配線だけを確認したいときは、CLI 起動側の実装を直接読む。
- git 実行 wrapper、path 解決、worktree 一般操作、clean worktree 判定、state file の schema・永続化形式、config 読み込みなど、複数領域で使う共通 runtime の詳細だけを調べたいとき。
- Codex に渡す prompt や Structured Output parameter の具体的な本文生成だけを確認したいときは、各 builder 側を読む。
- INDEX.md の本文生成、差分検出、更新対象探索、lock や commit 処理の内部詳細を調べたいだけなら、indexing 共通処理側を読む。
- oracle file、realization file、path token、root memo、cmoc ignore、session state などの概念定義や正本仕様断片を確認したいだけのときは、対応する oracle や basic model 側を読む。
- サブコマンドの外部仕様や利用者向け要求だけを確認したい場合で、実装上の状態遷移、git 操作、cleanup、report rendering を追う必要がないとき。
- テストケース、fixture、生成キャッシュ、実行ログ、または個々の LLM 出力品質を確認したいとき。

## hash
- 9933933ac7951b3a71903ed31ce851c7e42c8842b71ab738e4edbbe7a7843dd1
