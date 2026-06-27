# `acp`

## Summary
- AI エージェント呼び出し用の部品を扱う領域で、呼び出しパラメータを組み立てる側と、プロンプト本文に注入する標準文書片を構築する側への入口になる。
- AI に渡す役割、制約、補助入力、モデル・reasoning、file access mode、Structured Output schema、complete prompt などを確認するための階層である。
- 実際のワークフロー実行や状態更新ではなく、各機能が AI にどのような条件と出力契約で応答を求めるかを追うために読む。

## Read this when
- AI エージェント呼び出しに渡す parameter、complete prompt、モデル・reasoning、file access mode、Structured Output schema の構築箇所を探したいとき。
- apply fork、indexing、oracle review、session conflict 解消、TUI parameter resolve などで、呼び出し側が AI に渡す役割・制約・補助入力・出力契約を確認したいとき。
- oracle/realization の基本概念、ファイルアクセス規則、ルーティング規則、各種 standard、review 判定基準など、プロンプトへ注入される標準文書片の責務分担を確認したいとき。
- 個別ワークフローの処理本体ではなく、そのワークフロー内の AI 呼び出し条件やプロンプト設計を変更・検証したいとき。

## Do not read this when
- AI 呼び出し後の実処理、CLI サブコマンドの配線、git 操作、ファイルシステム更新、状態管理、結果の保存・表示・適用制御を調べたいとき。
- StructDoc、Standard、Requirement、path model、file access mode、AgentCallParameter など、プロンプト構築が参照する共通基盤そのものを確認・変更したいとき。
- 個別の oracle file、realization file、レビュー対象ファイルの本文や差分を確認したいだけのとき。
- INDEX.md 全体の走査・更新・保存、生成済みエントリーの markdown 描画、またはルーティング文書一般の規約を確認したいとき。

## hash
- 5fb41909e6a30e0fa2be5b1334cb0125abf46a493c87269337445cc1610d9ce0

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
- CLI サブコマンドの実行入口と、各サブコマンド固有の制御をまとめる実装領域。runtime wrapper への接続、preflight、利用者向け出力、状態更新、git 操作、Codex exec/TUI 呼び出し、report 生成などをサブコマンド単位で扱う。
- 初期化、INDEX maintenance、対話的 TUI、session lifecycle、apply lifecycle、review oracle の実行フローへ進むための入口になる。共通 runtime や schema そのものではなく、CLI 操作としてそれらをどう組み合わせるかを確認する対象。
- apply、session、review のように下位 package へ分かれる領域では、まずこの階層で該当する操作種別を見極めてから、個別の開始・取り込み・破棄・report・対象列挙・merge 処理へ進む。

## Read this when
- 特定の CLI サブコマンドが runtime にどう接続され、command 名、argv、preflight、Codex exec/TUI callback、stdout、終了条件をどう扱うかを確認・変更したいとき。
- cmoc の初期化、INDEX.md maintenance、対話的 TUI 起動、session の開始・取り込み・破棄、apply の開始・取り込み・破棄、review oracle の実行のどれに関する実装へ進むべきか判断したいとき。
- サブコマンド実行時の work root/repo root、clean worktree 要求、cmoc ignore 保証、設定読み込み、state 更新、branch/worktree 操作、commit/merge/cleanup の組み合わせを追いたいとき。
- apply run の isolated worktree 作成、finding 適用、差分 commit、report 生成、pid file 管理、join 時の想定外差分検出や conflict 解決を扱う入口を探すとき。
- session branch の作成、home branch への merge、conflict 解決依頼、session state 更新、session branch 削除、abandon 時 rollback を扱う入口を探すとき。
- review oracle の対象列挙、review loop、finding の統合・検証・判定、INDEX.md 変更の commit/merge、review report 生成をサブコマンド実行フロー上で確認したいとき。
- 利用者が編集する prompt から完全 prompt を作成し、TUI 起動パラメータを解決して Codex TUI を起動する流れを確認・変更したいとき。

## Do not read this when
- CLI サブコマンド固有の実行順序ではなく、git command wrapper、runtime 共通処理、path model、config schema、state schema、timestamp、report root など共有基盤だけを調べたいとき。
- Codex に渡す prompt parameter や Structured Output parameter の本文・schema だけを確認したいときは、builder や prompt 構築側を直接読む。
- INDEX.md の内容生成、差分検出、lock、commit など共通 indexing 実装そのものを調べたいときは、サブコマンド入口ではなく共通 indexing 実装を読む。
- oracle file と realization file の概念定義、正本仕様断片、review oracle の基準、INDEX.md エントリー生成規則を確認したいだけのとき。
- サブコマンドの外部挙動をテスト観点から確認したいだけのときは、対応するテストへ進む。
- 対象が特定済みで、apply/session/review の下位処理や report 描画、対象列挙、merge helper だけを局所的に調べる場合は、この階層全体ではなく該当する下位対象を直接読む。

## hash
- e9a07bc20665ada4e6a60281620d7e5be3e1a2f149c8f22cddf0fc29bb86d8bb
