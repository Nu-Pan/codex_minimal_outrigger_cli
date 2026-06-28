# `acp`

## Summary
- AI エージェント呼び出しに関わる realization implementation の上位領域であり、呼び出しパラメータを組み立てる処理と、その complete prompt に差し込む標準プロンプト断片の構築処理を収める。
- 各機能が AI に渡す role、summary、goal、補助入力、ファイルアクセス制約、標準参照、モデル・reasoning、Structured Output schema をどのように定めるかを追うための入口になる。
- 変更要約、実装所見調査、INDEX エントリー生成、oracle review、merge conflict marker 解消、TUI 実行パラメータ選定など、AI に依頼する作業の呼び出し条件と応答契約へ進む起点になる。

## Read this when
- cmoc の処理が AI エージェントを呼び出す直前に、どの入力・権限・モデル設定・Structured Output schema を渡しているかを確認または変更したいとき。
- AI 呼び出し用 complete prompt に含まれる基本情報、ファイルアクセス制約、ルーティング規則、oracle/realization の概念、レビュー基準、INDEX エントリー規範の生成箇所を探したいとき。
- 変更差分要約、レビュー所見列挙、所見対応、INDEX エントリー生成、oracle 関連レビュー、merge conflict marker 解消など、個別の AI 作業依頼のプロンプト設計や応答 schema を調べたいとき。
- AI 呼び出しの入口と、そこから利用される標準プロンプト断片の関係を同じ領域で把握したいとき。

## Do not read this when
- サブコマンド登録、CLI 引数解析、実行順序、状態管理、git 操作、ファイル更新、結果保存・表示など、AI 呼び出し前後の制御フローだけを調べたいとき。
- path model、StructDoc、Markdown rendering、AgentCallParameter、FileAccessMode などの基礎型や汎用構造化文書処理そのものを確認したいとき。
- oracle file や realization file の本文仕様、または実際にレビュー・修正される対象ファイルの内容を直接読みたいとき。
- 生成済みの INDEX.md の保存・更新・描画や、リポジトリ全体のルーティング文書管理だけを調べたいとき。

## hash
- 63862674c39d794f60eebc7f8c42cce2cd8120e1cca897c9bea5d72afcc91b6b

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
- cmoc の realization implementation のうち、複数のコマンドや上位処理から使われる共通 runtime helper 群を収める領域。
- Codex 呼び出し、CLI サブコマンド実行、設定、内容 hash、エラー表示、Git 操作、ログ、path、結果モデル、session state、INDEX.md 自動更新 preflight など、横断的な実行時支援への入口になる。
- 多くの対象は責務別の実装本体または互換 import・集約 import として分かれており、個別コマンドの業務ロジックではなく、共有される runtime 境界を確認するための階層である。

## Read this when
- 複数のサブコマンドや上位モジュールから共通利用される runtime API の所在を探したいとき。
- Codex exec/TUI 呼び出し、preflight、quota/capacity retry、Structured Output 検証、call log、profile、CODEX_HOME、sandbox/file access mode など Codex 実行基盤を確認または変更したいとき。
- CLI サブコマンド共通 wrapper、stdout/stderr の扱い、終了コード化、例外表示、サブコマンド event log、完了サマリーなど実行ライフサイクル共通処理を追うとき。
- 設定ファイルの読み書き、内容 hash 保存、Git worktree/branch/ignore 操作、runtime path、結果データ構造、session state 永続化など、単一機能ではなく共通 helper として再利用される処理を探すとき。
- INDEX.md 自動更新の preflight、対象探索、entry hash 検証、Codex によるエントリー生成、更新 commit 作成の実装経路を調べるとき。

## Do not read this when
- 個別サブコマンドの入力解析、業務ロジック、利用者向け出力、永続データ更新の流れだけを知りたいときは、該当コマンドの実装へ直接進む。
- path model、oracle/realization の定義、INDEX.md やログの正本仕様など、人間が所有する仕様断片そのものを確認したいときは、oracle 側の本文を読む。
- 特定のテスト期待値や fixture を確認したいだけのときは、対応する realization test を読む。
- 生成済みルーティング文書の内容を読むだけで、自動生成・更新・hash 判定・preflight の仕組みを追う必要がないとき。
- 単一の責務を持つ下位対象が既に分かっているときは、この階層全体ではなく、その責務を担当する本文へ直接進む。

## hash
- 1e5cf890b4d77ddb0e89adb304f4d58459f8ace01d94252720deb43554d3ec13

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
- CLI サブコマンドの実行本体を集める領域。初期化、indexing、TUI、session、apply、review oracle など、利用者操作を CLI runtime に接続する各サブコマンド実装への入口になる。
- 各サブコマンドは、実行前条件の確認、work root/session branch/worktree/state/report などの実行環境操作、git や Codex 呼び出しへの委譲、利用者向け出力を扱う。詳細な共通 helper や prompt 構築、低レベル状態操作そのものは主に他領域へ委譲される。

## Read this when
- CLI サブコマンドごとの実行入口、run_cli_subcommand への渡し方、command 名や argv、preflight、runtime 選択、利用者向け出力の起点を探したいとき。
- init、indexing、tui、session、apply、review oracle のどの実装へ進むべきかを、サブコマンド単位で選びたいとき。
- session branch、apply branch/worktree、review worktree、初期化時の git 状態復元、INDEX.md maintenance 実行、TUI prompt 保存など、サブコマンド固有のライフサイクル制御を調べ始めるとき。
- サブコマンド実行中に Codex subprocess、git 操作、state file、report、cleanup、merge conflict、自動解決処理などへどの入口から入るかをたどりたいとき。

## Do not read this when
- Typer app へのサブコマンド登録、トップレベル CLI parser、共通 command 定義だけを確認したいとき。
- git command wrapper、CLI runtime、path model、設定読み込み、state schema、report directory、timestamp、ignore 判定などの共通 helper 自体を調べたいとき。
- Codex prompt、Structured Output、ACP parameter、resolve parameter などの具体的な生成内容だけを確認したいとき。
- oracle の正本仕様断片、INDEX.md 生成規則、path token 仕様、realization/oracle の一般原則を確認したいとき。
- サブコマンドの実装ではなく、自動テストの期待挙動、fixture、または利用者向け仕様文書を直接確認したいとき。

## hash
- 240379b7dcf8e4f77399198190d69f8c66435ec42b65852684cfa437e5375cd8
