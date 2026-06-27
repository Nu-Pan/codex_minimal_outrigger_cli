# `acp`

## Summary
- AI エージェント呼び出し基盤のうち、呼び出しごとの役割・目的・補助文脈・権限・モデル設定・返却契約を構成する実装と、そこへ注入する標準プロンプト断片を扱う領域。
- フォーク適用、ルーティング文書エントリー生成、正本仕様断片レビュー、セッション結合時の衝突解消、対話入力からの実行パラメータ選定など、機能別のエージェント呼び出し設定へ進む入口になる。
- 実際の業務処理、差分解析、ファイル更新、所見の保存・統合処理、CLI の制御フローそのものではなく、下流エージェントへ何をどの条件で依頼するかを組み立てる責務を持つ。

## Read this when
- 各処理から AI エージェントへ渡す役割、作業概要、完了条件、補助文脈、ファイルアクセス権限、モデル種別、推論量、返却契約を確認または変更したいとき。
- フォーク適用時の変更要約・所見列挙・所見対応、ルーティング文書エントリー生成、正本仕様断片レビューの所見列挙・検証・採否・整理、セッション結合時の衝突解消、対話入力からの実行パラメータ選定の呼び出し設定を探すとき。
- AI に渡す標準プロンプトが、ファイルアクセス規則、ルーティング規則、正本仕様断片と具体化ファイルの基本概念、正本仕様断片規範、具体化ファイル規範、レビュー規範、ルーティング文書エントリー規範のどれを含むか確認したいとき。
- 差分、対象本文、既知所見、所見本文、衝突対象、利用者入力などが、どのような補助文脈として完全プロンプトへ埋め込まれるかを追いたいとき。
- Structured Output schema とエージェント呼び出しの対応、または返却形の制約を機能別に確認したいとき。

## Do not read this when
- サブコマンド全体の実行順序、状態管理、保存、表示、外部コマンド実行、ファイル更新など、AI 呼び出しパラメータ構築の外側にある制御フローを調べたいとき。
- git 操作、差分取得、マージ実行、衝突検出、所見リストの永続化、編集操作の適用など、実処理そのものを探しているとき。
- 構造化文書、標準規範、エージェント呼び出しパラメータ、パス解決、Markdown レンダリングなどの汎用データ構造や共通 helper だけを確認したいとき。
- 個別の正本仕様断片や具体化ファイルの本文内容、または生成済みのレビュー結果・所見・要約・ルーティング文書エントリーそのものを確認したいとき。
- 特定の標準プロンプト断片だけを変更することが分かっている場合は、呼び出し設定全体ではなく該当する下位領域へ直接進めばよい。

## hash
- 5d55af86e80d0e6dad16b2b5bbcdf9fec0e3b60972279b2a246fc5d5684775d5

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
- cmoc の realization implementation で共有される実行時 helper 群をまとめる領域。CLI サブコマンド共通ライフサイクル、Codex exec/TUI 呼び出し、profile・preflight・call log、設定入出力、内容 hash 保存、共通エラー表示、Git 操作、runtime path、実行結果モデル、session state、サブコマンドログなど、複数の上位機能から使われる基盤処理への入口になる。
- 利用側が共通 runtime 機能を一か所から import するための集約面と、責務別の下位 runtime 実装が同居している。特定の共有機能を変更する場合は、まずこの領域で該当責務の実装を選び、個別サブコマンドや仕様断片ではなく共通基盤として扱うべき処理かを確認する。

## Read this when
- CLI サブコマンドに共通する開始・完了表示、終了コード化、例外表示、サブコマンドログ、現在 logger の設定解除などの実行ライフサイクルを確認または変更したいとき。
- Codex CLI の exec 実行、TUI 起動、profile 生成、schema 保存、resume token、quota/capacity 制御、Structured Output 検証、call log、preflight 実行など、Codex 呼び出し runtime の共通処理を調べたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正 JSON や型不一致の利用者向けエラー化など、設定永続化の共通処理を確認または変更したいとき。
- ファイル内容や文字列内容の SHA-256 digest、内容 hash を使った保存、binary 判定など、内容ベースの小さな共有 helper を調べたいとき。
- 利用者向け Markdown エラーレポート、共通実行時例外、復旧案・詳細・Call stack の表示形式を確認または変更したいとき。
- Git コマンド実行、branch・HEAD・worktree cleanliness、run 用 worktree、branch 削除、Git ignore 判定、cmoc 管理領域を追跡対象外にする処理を調べたいとき。
- 実行時 root 解決、cmoc 管理ディレクトリ、設定・state・log・worktree・schema 保存先、timestamp、経過時間表示、memo 配下判定などの runtime path helper を確認したいとき。
- 外部コマンド結果や Codex exec 結果を運ぶ共有データ構造、または session branch/apply branch に紐づく永続 session state の JSON 入出力を確認したいとき。
- 複数の runtime helper に分かれた共通機能について、実装側からどの公開名で import できるか、または新しい共有 runtime 機能を集約 import 面へ載せるべきか判断したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、ユーザー操作ごとの具体的な永続データ内容を調べたいだけのとき。その場合は各サブコマンドや機能実装へ直接進む。
- oracle file の正本仕様断片、path keyword の概念定義、oracle/realization の分類規則、INDEX.md 生成規則を確認したいとき。この領域は仕様本文ではなく realization implementation の共有 runtime 基盤である。
- 設定データクラス、AgentCallParameter、FileAccessMode、モデル設定など、入力データ構造そのものの定義だけを確認したいとき。その場合はモデル定義側を読む。
- ログや状態を読む側・集計する側・表示する側の高レベル仕様を探しているとき。ここは主に保存・受け渡し・runtime 管理の共通処理を扱う。
- 特定機能がどの prefix・suffix・content・path・設定値を渡すかという上位の呼び出し判断だけを調べたいとき。その場合はその機能の呼び出し側を読む。
- Codex や Git 以外の個別外部ツール連携、または上位 workflow のプロンプト生成・状態遷移・レポート生成だけを追いたいとき。

## hash
- 62a1441903c60bfa0e9f34d06e8f35512bf7d32f67a574c0b93564495fda77ce

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
- CLI サブコマンド実装を集約する領域。初期化、TUI 起動、INDEX.md 保守、review oracle、apply、session 操作など、利用者が呼び出す上位コマンドの実行入口と orchestration を扱う。
- 各対象は共通 runtime や低レベル helper を直接実装する場ではなく、branch・worktree・state・report・Codex 実行・git 操作などの共通基盤をサブコマンド固有の制御フローへ接続する入口として位置づく。
- apply と session は下位パッケージに具体的なサブコマンド実装を持ち、review oracle は対象列挙、反復処理、INDEX 変更処理、レポート生成などの役割ごとに分割されたモジュールへ進むための分岐点になる。

## Read this when
- cmoc の個別サブコマンドが、どの前提条件、実行順序、状態遷移、git/worktree 操作、利用者向け出力で動くかを調査または変更したいとき。
- init、tui、indexing、review oracle、apply、session のうち、どの実装へ進むべきかをサブコマンド単位で切り分けたいとき。
- review oracle の scope 対象列挙、review loop、INDEX 変更 commit/merge、report 生成、または apply run や session lifecycle の上位制御を追いたいとき。
- INDEX.md 自動保守の preflight、対象選別、既存エントリー再利用、Codex によるエントリー生成、Markdown 描画、更新差分 commit の流れを確認したいとき。
- Codex TUI 起動前の依頼文編集、TUI 用パラメータ解決、complete prompt 保存、AgentCallParameter 構築など、TUI サブコマンド固有の制御を確認したいとき。

## Do not read this when
- git wrapper、config 読み込み、path model、state file 永続化、timestamp、reports directory、Codex 外部プロセス実行など、複数サブコマンドで使う共通 runtime 基盤そのものを調べたいとき。
- oracle file や realization file の概念、正本仕様断片、ルーティング文書の品質基準、INDEX.md エントリー生成規則など、仕様文書側の内容を確認したいだけのとき。
- Codex に渡す prompt や Structured Output parameter の具体的な構築だけを調べたいときは、各 parameter builder 側を読む方が直接的。
- テスト観点から外部挙動を確認したいだけなら、対応する test 配下の対象を読む方が直接的。
- apply や session の具体的な下位操作、review oracle の対象列挙・loop・report・INDEX merge など、読むべき個別モジュールが既に分かっているときは、その対象へ直接進めばよい。

## hash
- 591d77ed2e2258b8fe5d6047f410f0de15126e404c43f03dea5c2c3ae97bbf62
