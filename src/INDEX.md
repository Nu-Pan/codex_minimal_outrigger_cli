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
- cmoc の realization implementation のうち、複数機能から使われる実行時共通 helper 群をまとめる領域。CLI サブコマンド共通ライフサイクル、Codex exec/TUI 呼び出し、profile・設定・内容保存・エラー表示・Git 操作・ログ・runtime path・実行結果・session state など、上位機能が共有する runtime 基盤への入口になる。
- 公開 import 集約、互換 import 入口、責務別 runtime 実装、軽量なデータ保持型が同じ階層に置かれており、特定機能の業務処理ではなく、cmoc 全体の実行時支援や横断的な副作用制御を調べるための下位要素へ進むために読む対象である。

## Read this when
- CLI サブコマンド全体に共通する開始・完了表示、終了コード化、例外処理、事前検査、実行ログ設定の流れを確認または変更したいとき。
- Codex CLI の exec 実行または対話型起動について、profile 準備、schema、call log、標準入出力、retry、quota/capacity 制御、resume、Structured Output 検証、preflight のどこを読むべきか切り分けたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正 JSON や不正値の利用者向けエラー化を扱う実装を探しているとき。
- ファイル内容の digest 計算、内容ベース保存、binary 判定、または生成物・キャッシュ的出力の共通保存 helper を確認したいとき。
- 利用者向け Markdown エラーレポート、共通例外、Next actions、Detail、Call stack の出力構造を調べたいとき。
- Git コマンド実行、branch・HEAD・worktree cleanliness、run 用 worktree、branch 削除、cmoc 管理領域の Git ignore 処理を確認または変更したいとき。
- サブコマンド単位の JSON Lines 実行ログ、current logger、経過時間、quota 待機時間、Codex 呼び出し完了サマリーの共通表示を追いたいとき。
- 実行時 root、cmoc 管理ディレクトリ、設定・state・log・reports・worktrees・sessions などの配置、時刻文字列、作業ディレクトリ一時変更、memo 配下判定を扱う共通 path helper を探すとき。
- 外部コマンド結果や Codex exec 結果をどのデータ構造で運ぶか、戻り値モデルの保持項目を確認したいとき。
- session branch や apply branch に紐づく永続 session state の JSON 入出力、保存先解決、branch 名からの session-id 抽出、active session 探索を調べたいとき。
- 複数の runtime helper を一か所から import する公開入口や、旧来 import path を維持する互換入口を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、dispatch、利用者向け command 固有出力を調べたいだけのときは、該当する上位サブコマンド実装へ進む。
- oracle file にある正本仕様断片、path token の概念定義、oracle/realization の分類規則、INDEX 生成規則そのものを確認したいときは、仕様側の本文へ進む。
- 特定機能のプロンプト生成、レビュー、適用、初期化、レポート生成などの高レベル workflow を調べたいときは、この共通 runtime helper 群ではなく、その機能を持つ実装へ進む。
- Codex profile 名、設定値、モデル、reasoning effort、入力データクラスなどの定義だけを確認したいときは、定義元のモデルや設定側へ直接進む。
- ログや状態の保存先を使う側、集計する側、表示する側の仕様を調べたいときは、この階層の保存・記録 helper ではなく、それらを読み取る上位処理へ進む。
- 単にファイル名や配置だけを一覧したい場合は、自然言語のルーティング情報ではなく機械的なファイル一覧で足りる。

## hash
- 08ce43d60cefe3d5f2bc372254ea4329447e39a9c17bf66f0a8bbf61c2df64d7

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
- CLI の各サブコマンド実装を束ねる領域。初期化、TUI 起動、INDEX.md 保守、review oracle、apply、session 操作など、利用者が実行するコマンドの上位 orchestration への入口になる。
- 各対象は、CLI runtime への接続、事前条件確認、git branch/worktree/state/report などの共通基盤との接続、利用者向け出力、失敗時処理を扱い、詳細な共通 helper や prompt/schema 構築へ進む前の分岐点として使う。

## Read this when
- 特定サブコマンドの実行順序、前提条件、状態遷移、git 操作、利用者向け出力、失敗時の後片付けや report 生成の入口を探したいとき。
- 初期化、TUI、INDEX.md 自動保守、review oracle、apply run、session 作成・取り込み・破棄のどの実装へ進むべきかを切り分けたいとき。
- review oracle の対象列挙、finding loop、INDEX 変更の commit/merge、report 生成など、review 処理全体の中で読むべき責務単位を選びたいとき。
- apply fork/join/abandon、apply branch と session branch、isolated worktree、pid file、process 停止、report、cleanup など apply ライフサイクル関連の読む先を選びたいとき。
- session branch と active state をまたぐ branch 作成、home branch への統合、merge しない破棄、conflict 処理など session 操作固有の CLI 制御を調べたいとき。

## Do not read this when
- git 実行 wrapper、state file 永続化、config 読み込み、path model、timestamp、reports directory など、複数サブコマンドで使われる runtime 共通基盤そのものを調べたいとき。
- Codex に渡す prompt、AgentCallParameter、Structured Output parameter、complete prompt、StructDoc 描画などの具体的な構築規則だけを確認したいとき。
- oracle file、realization file、INDEX.md、review finding 品質基準などの正本仕様断片やルーティング文書生成規則を確認したいだけのとき。
- サブコマンドの外部挙動をテスト観点から確認したいだけのときは、対応するテストへ進む方が直接的。
- 個別サブコマンドに関係しない一般的なパッケージ構成や、低レベル helper の内部実装だけを調べたいとき。

## hash
- 44bc81f9148394d4eb336251ac628a3a0fbb8b4260df5ce566c177418b019f60
