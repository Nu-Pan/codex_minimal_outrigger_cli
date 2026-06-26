# `acp`

## Summary
- AI agent 呼び出しに渡す実行パラメータとプロンプト文書断片を組み立てる実装領域。各サブコマンドや処理フェーズ向けに、役割、作業概要、完了条件、ファイルアクセス権限、補助文脈、モデル設定、推論量、Structured Output schema を接続する処理と、そこへ注入される標準規範・ルーティング規則・基礎概念の prompt part を扱う。
- 下位には、フォーク適用、目次エントリー生成、oracle review、session join の conflict 解消、TUI 実行パラメータ解決などの用途別 builder と、file access rule、routing rule、oracle/realization の基本説明、各種 standard を StructDoc として生成する prompt 部品がある。

## Read this when
- AI agent CLI/TUI や内部 agent call に渡す complete prompt、role、summary、goal、補助文脈、ファイルアクセス権限、モデル種別、推論量、Structured Output schema の対応を確認または変更したいとき。
- フォーク適用時の所見列挙・所見対応・変更要約、INDEX.md 用エントリー生成、oracle file レビュー所見の列挙・検証・採否・統合、session join の merge conflict marker 解消、TUI 入力からの実行パラメータ選定のどの呼び出し構成へ進むべきか判断したいとき。
- agent に注入されるファイルアクセス規則、INDEX.md ルーティング規則、oracle と realization の基本概念、oracle standard、realization standard、review/apply/indexing 用の判断基準がどのように prompt 化されるかを追いたいとき。
- raw diff、対象本文、所見リスト、conflict 対象ファイル、利用者入力などの外部文脈が、どの補助 prompt として組み込まれ、どの返却契約で agent に渡されるかを確認したいとき。

## Do not read this when
- CLI サブコマンド全体の制御フロー、引数解析、状態管理、表示、保存、git 操作、merge 実行、差分取得など、agent call parameter 構築の外側にある実処理を調べたいとき。
- AgentCallParameter、FileAccessMode、ModelClass、StructDoc、Standard、Requirement、パス解決などの基礎データ構造や共通ユーティリティそのものを確認したいとき。
- AI agent の実行基盤、プロセス起動、サンドボックス強制、実際のファイルシステム権限制御を探しているとき。
- oracle file や realization file の個別仕様・実装内容そのもの、または review/apply/indexing/session/TUI の利用者向け挙動を調べたいだけのときは、該当する仕様・コマンド実装・テストへ直接進めばよい。

## hash
- cf1b8ebcfb98f1a09a2e515c87928f2818e338ac1454ffb160fded23856ac5a9

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
- cmoc の実行時共通機能を集めた共有 runtime helper 群の領域。Codex 呼び出し、CLI 共通ライフサイクル、設定入出力、内容 hash 保存、共通エラー表示、Git 操作、実行ログ、runtime path、結果モデル、session state など、複数の上位実装から使われる横断的な基盤を扱う。
- 公開 import の集約入口と、責務別に分割された個別 runtime 実装の両方を含み、特定ドメインの詳細へ進む前に共通基盤の読む先を選ぶための入口になる。

## Read this when
- cmoc の上位コマンドや機能実装から使う共通 runtime helper の責務分担を確認し、どの共通実装へ進むべきか選びたいとき。
- Codex exec/TUI 呼び出し、profile/schema 準備、quota/capacity 制御、Structured Output 検証、call log、preflight など Codex runtime 周辺の実装を調査または変更したいとき。
- CLI サブコマンドの共通実行処理、開始・完了表示、終了コード化、例外表示、subcommand logger の設定解除、実行ログ記録を確認または変更したいとき。
- 設定ファイルの読み書き、内容 hash 保存、共通エラーレポート、Git helper、runtime path、実行結果データ、session state JSON など、複数機能で共有される低レベル実行時処理を調べたいとき。
- 新しい共通 runtime 機能を追加する際に、既存の共有 helper、公開 import 面、責務境界、保存先やログ・状態モデルとの関係を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI 引数定義、利用者向け出力 schema、永続データの具体的な内容を調べたいだけのとき。その場合は該当サブコマンドや機能実装へ直接進む。
- cmoc の正本仕様断片、path 用語の仕様定義、INDEX 生成規則、oracle/realization の分類判断を確認したいとき。この領域は realization implementation の共通基盤であり、仕様本文ではない。
- 共通 helper を使う側がどの値を渡すか、どのタイミングで呼び出すかという上位 workflow だけを追いたいとき。その場合は呼び出し元の実装を読む方が直接的。
- テストケース、期待される外部挙動、fixture の確認が目的のとき。その場合は対応する realization test へ進む。

## hash
- 08bfe00a866a5e7b72630a194c0b6c96f35ac751aa23d9b26255e90b89306c48

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
- CLI サブコマンド実装を集約する領域。初期化、TUI 起動、INDEX.md 保守、review oracle、apply、session などの利用者向け操作を、runtime 共通処理や下位 helper に接続する入口になる。
- サブコマンドごとの実行順序、事前条件、状態遷移、Git 操作、利用者向け出力、report 生成などを調べるときに、対象コマンド別の実装へ進むための分岐点として使う。
- review oracle や apply のように複数段階へ分かれる処理では、対象列挙、実行ループ、INDEX 変更処理、report、branch/worktree/process 管理など、どの責務の下位モジュールを読むべきかを切り分ける入口になる。

## Read this when
- cmoc のサブコマンドが CLI から呼ばれた後、どの前提条件を確認し、どの順序で runtime・Git・state・report・出力処理へ進むかを調査または変更したいとき。
- init、tui、indexing、review oracle、apply、session のいずれかの実行フロー、引数由来の制御、利用者向け出力、成功時・失敗時の後処理を確認したいとき。
- review oracle の対象列挙、finding loop、INDEX 変更 commit/merge、report 生成、または apply の fork/join/abandon、apply worktree・branch・process・pid file 管理など、サブコマンド固有の orchestration の読む先を選びたいとき。
- サブコマンドが共通 runtime、config、path model、Git wrapper、Codex 実行 parameter builder などの下位基盤へどう接続しているかを入口から追いたいとき。

## Do not read this when
- CLI 全体のコマンド登録、parser 構成、共通 runtime wrapper、Git コマンド wrapper、設定 schema、path keyword 解決など、サブコマンド個別処理ではない共通基盤そのものを調べたいとき。
- Codex に渡す prompt、AgentCallParameter、structured output parameter の具体的な構築内容だけを確認したいとき。
- oracle file、realization file、INDEX.md、review finding 品質基準などの正本仕様断片やルーティング文書生成規則を確認したいだけのとき。
- 特定のサブコマンドや下位責務が既に分かっており、その個別ファイルまたは下位ディレクトリを直接読めば足りるとき。
- テスト観点から外部挙動を確認したいだけなら、対応する realization test を読む方が直接的。

## hash
- 556ec469e807184f4e42e9ab7f65f47cf6f3bcc1217b6d163ceab265838a4f31
