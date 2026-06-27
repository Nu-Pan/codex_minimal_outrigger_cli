# `acp`

## Summary
- AI agent 呼び出しに渡すプロンプトと実行パラメータを構築する実装領域。role、summary、goal、file access mode、標準文書、補助入力、model/reasoning、Structured Output schema を、用途別の AgentCallParameter として組み立てる処理を扱う。
- 下位には、個別機能ごとの AI 呼び出し条件を作る領域と、完全プロンプトに注入される標準プロンプト片を生成する領域がある。変更要約、apply fork 所見、oracle review、INDEX エントリー生成、merge conflict marker 解消、TUI 実行パラメータ選定などの AI 依頼の入口になる。

## Read this when
- cmoc の機能が AI agent に何を依頼し、どの file access mode、model class、reasoning effort、Structured Output schema で呼び出しているかを確認または変更したいとき。
- AI agent に渡す complete prompt の構成、標準プロンプト片の注入条件、aux_prompt の内容、oracle/realization/basic/routing/file access などの共通説明の組み立てを調べたいとき。
- 変更差分の要約、ファイル単位の所見列挙、所見に基づく realization file 修正、oracle file レビュー所見の列挙・検証・判定・整理、INDEX.md 用エントリー生成、TUI 用パラメータ選択、session join の conflict marker 解消など、AI に依頼する作業単位のプロンプト設計へ進みたいとき。
- Structured Output schema がどの AI 呼び出しに対応し、AI 応答をどの段階で機械処理可能な形に固定しているかを追いたいとき。

## Do not read this when
- CLI サブコマンド登録、引数解析、実行順序、状態管理、git 操作、ファイル保存、結果表示、テスト実行など、AI 呼び出しの前後にある制御フローだけを調べたいとき。
- oracle file や realization file の本文そのもの、または実際にレビュー・修正される対象ファイルの仕様や実装を読みたいとき。
- AgentCallParameter、FileAccessMode、StructDoc、path model、standard 変換などの基礎型・共通データ構造そのものを確認したいとき。
- AI 応答を受け取った後の集約、採否判断、保存、適用、通知などの後続処理を調べたいとき。
- 生成済み INDEX.md の管理、描画、更新、保存といったルーティング文書全体の運用だけを確認したいとき。

## hash
- c605c7cedc52d0d373be9d463427b7d48c5302dc42af3e536c87aed5ab6788df

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
- cmoc の realization implementation のうち、複数の CLI サブコマンドや上位処理から使われる共有 runtime helper 群をまとめる領域。Codex 呼び出し、preflight、設定、内容 hash、エラー表示、Git 操作、ログ、実行時 path、結果モデル、session state、CLI 実行ライフサイクルなど、横断的な実行基盤への入口になる。
- 個別責務ごとの helper 実装に分割されており、共有入口、互換 import、実行制御、データ保持型、永続化、低レベル操作のどれを読むべきかを選ぶための中継階層として位置づけられる。

## Read this when
- サブコマンド固有ではない共通 runtime 層の実装場所を探したいとき。
- Codex exec/TUI 呼び出し、Structured Output 検証、quota/capacity retry、preflight、profile 準備、call log など Codex 実行基盤のどこを読むべきか切り分けたいとき。
- 設定ファイルの読み書き、内容 hash 保存、利用者向けエラー整形、Git worktree/branch/ignore 操作、runtime path 解決、サブコマンドログ、session state などの共有 helper を確認・変更したいとき。
- CLI サブコマンドを共通ライフサイクルで実行する仕組み、標準 stdout、例外時表示、終了コード化、現在のサブコマンド logger の扱いを追いたいとき。
- 複数の runtime helper を横断して公開入口や依存関係を確認したいが、まず責務別の読む先を選びたいとき。

## Do not read this when
- 個別 CLI サブコマンドの業務処理、引数定義、利用者向け入出力そのものを調べたいときは、サブコマンド実装側を読む。
- 正本仕様断片、パス概念そのもの、oracle file と realization file の分類、INDEX 生成規則の仕様を確認したいときは、仕様側の文書を読む。
- テスト期待値や fixture を確認したいだけのときは、対応する realization test 側を読む。
- 共有 runtime helper を使う上位 workflow の全体制御だけを知りたいときは、その workflow を実装する呼び出し側へ進む。
- 特定の責務がすでに分かっているときは、この階層全体ではなく、該当する責務別 runtime 実装へ直接進む。

## hash
- 6dbc065430b7e339ac9cfc4a7145dfc6f0cdd2f2b404fef46ca464e338417572

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
- CLI サブコマンドの実行入口とサブコマンド固有の制御をまとめる実装領域。runtime wrapper への接続、事前条件検証、利用者向け出力、状態更新、branch/worktree 操作、report 生成など、各コマンド操作として共有機能をどう組み合わせるかを扱う。
- 対象範囲は、初期化、INDEX maintenance、対話実行、session の開始・取り込み・破棄、apply の開始・取り込み・破棄、review oracle の対象列挙・実行ループ・INDEX 反映・report 出力に分かれる。
- 共通 runtime、状態 schema、path model、設定 schema、prompt builder、git wrapper そのものではなく、利用者が起動するサブコマンド単位の orchestration へ進むための入口になる。

## Read this when
- CLI から起動される各サブコマンドの実行経路、command name、argv、runtime wrapper への渡し方、preflight や precondition の接続位置を確認したいとき。
- session branch や apply branch を作成・merge・削除し、state file を active、joined、abandoned、ready、running、completed、error へ更新する流れをサブコマンド単位で追いたいとき。
- isolated worktree 上で apply や review を走らせ、Codex 実行、差分 commit、report 保存、session branch への取り込み、worktree/branch cleanup をどこから制御しているかを確認したいとき。
- 初期化、INDEX maintenance、対話的 prompt 編集、review oracle など、利用者操作ごとの stdout、終了コード、エラー時 report、警告表示を確認・変更したいとき。
- サブコマンド固有の merge conflict 処理、想定外差分検出、編集禁止対象 rollback、pid file による実行中 apply process 管理など、共通 helper ではなく操作全体の中での扱いを調べたいとき。
- 同階層のどの下位実装へ進むべきかを判断するために、apply、session、review、init、indexing、tui の責務境界を把握したいとき。

## Do not read this when
- git command 実行 wrapper、repo/work root 解決、branch 判定、clean worktree 判定、cmoc ignore 保証、state file 読み書きなどの共通 runtime helper 自体を調べたいとき。
- session state や apply state の schema、path token の定義、設定ファイル model、timestamp や reports directory の共通規約だけを確認したいとき。
- Codex に渡す prompt parameter や Structured Output schema の本文、prompt part の組み立て規則そのものを調べたいとき。
- INDEX.md の本文生成、差分検出、lock、commit、個別ファイル走査など、共通 indexing 実装の内部を調べたいとき。
- oracle/realization の正本仕様、INDEX.md エントリー生成規則、review/apply の高水準仕様だけを確認したいとき。
- 特定サブコマンドの詳細処理を読む対象がすでに決まっている場合は、この階層全体ではなく該当する下位対象へ直接進む。

## hash
- b543a1a1056b57080256932729a8ffd80dbe4ae056904ab02400323f4c58bfad
