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
- cmoc の realization implementation のうち、複数のサブコマンドや runtime 層から共有される実行時 helper 群をまとめる領域。CLI 実行ライフサイクル、Codex 呼び出し、設定入出力、内容 hash 保存、共通エラー、Git 操作、実行ログ、runtime path、結果モデル、永続 session state など、横断的な基盤処理への入口になる。
- 責務別の小さな module と、既存 import path を維持する集約入口が混在しており、個別サブコマンドの業務処理ではなく、サブコマンド群が共通利用する runtime 境界を確認するための階層である。

## Read this when
- CLI サブコマンドの開始・完了表示、終了コード化、例外表示、サブコマンド logger の設定範囲など、共通実行ライフサイクルを調べるとき。
- Codex exec/TUI の profile 準備、呼び出し、Structured Output 検証、retry、quota/capacity 制御、resume、call log、subcommand event、preflight など、Codex runtime 全体または責務別入口を探すとき。
- 設定ファイルの読み書き、既定値補完、不正 JSON や型不正の利用者向けエラー化を確認または変更するとき。
- 内容 hash、hashed file 保存、binary 判定、生成物や cache 的な出力の内容ベース保存処理を調べるとき。
- cmoc 共通例外、利用者向け Markdown エラーレポート、Next actions、detail、call stack の出力構造を確認または変更するとき。
- Git コマンド実行、branch・HEAD・clean worktree 判定、cmoc 管理 branch、run worktree、ignore/exclude 制御など、Git 状態や Git 操作の共通 helper を調べるとき。
- サブコマンド実行ログ、JSON Lines event、quota 待機時間、実行時間計測、context-local logger を確認または変更するとき。
- 実行時の repo/work/cmoc root 解決、cmoc 管理ディレクトリ、config/state/log/worktree/schema path、timestamp、memo 配下判定、作業ディレクトリ一時変更を扱うとき。
- 外部コマンド結果や Codex exec 結果として、終了コード、標準入出力、生成 text/JSON、profile/schema、log path、elapsed、quota 情報を運ぶ共有データ構造を確認するとき。
- session branch や apply branch に紐づく永続 session state、state file の JSON 入出力、branch 名からの session-id 抽出、active session 探索を調べるとき。
- 複数の runtime 共通部品をまとめて import している呼び出し側の依存関係や、公開入口から利用可能な共通部品の範囲を把握したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、dispatch、利用者向け出力内容そのものを調べたいとき。その場合はサブコマンド実装や CLI ルーティング側へ進む。
- oracle file の正本仕様、path 概念そのもの、oracle/realization の分類、INDEX.md 生成規則やルーティング文書の仕様を確認したいとき。この階層は realization implementation の共通 runtime helper であり、正本仕様の置き場ではない。
- 特定機能の高レベルな workflow、状態遷移、レポート内容、出力 schema の意味を調べたいだけのとき。その機能を持つ上位実装または仕様文書を読む方がよい。
- Codex profile 名、設定値、AgentCallParameter、FileAccessMode、モデルや reasoning effort などの入力データ構造そのものを確認したいだけのとき。データモデルや設定定義側へ進む。
- ログや状態ファイルを読む側、集計する側、表示する側の仕様や実装を探しているとき。ここは主に生成・保存・受け渡しの共通 helper を扱う。
- 外部コマンドや Git 操作を伴わない純粋なドメイン処理、構造化テキスト解析、Markdown 処理、テスト固有 fixture の期待値だけを調べるとき。
- 既存 import path の互換入口ではなく、個別機能の実装詳細を直接変更したいとき。集約入口ではなく該当責務の module へ進む。

## hash
- 2a2e2ff001b9a9d23ae8262b2ee304a713549dd29cd4138c3bd9462b84aa58ff

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
- CLI サブコマンド実装群をまとめる領域。初期化、対話的 Codex TUI 起動、INDEX.md 自動保守、review oracle、apply 系操作、session 系操作の入口と、それらから分かれる下位処理へのルーティングを担う。
- 各サブコマンドは CLI runtime や git/state/path などの共通基盤を利用しつつ、実行前提の確認、branch・worktree 操作、Codex 実行の接続、レポート生成、cleanup、利用者向け出力など、コマンド単位の制御フローを実装している。
- review oracle については、実行入口、対象列挙、finding loop、INDEX 変更 commit/merge、レポート生成が同階層の複数要素に分かれており、関心に応じてより直接の実装へ進むための入口になる。

## Read this when
- CLI サブコマンドごとの実行順序、前提条件、利用者向け出力、または runtime への接続箇所を調べ始めるとき。
- 初期化、対話的 TUI 起動、INDEX.md 自動更新、review oracle、apply 系操作、session 系操作のうち、どの実装へ進むべきかを切り分けたいとき。
- branch や worktree を伴うサブコマンドの orchestration、cleanup、失敗時処理、report 生成、state 更新の入口を探したいとき。
- review oracle の対象列挙、finding 処理、ルーティング文書差分の commit/merge、レポート生成のどこを読むべきか判断したいとき。
- apply 系または session 系の下位ディレクトリへ進む前に、この階層で扱うコマンド領域全体の責務境界を把握したいとき。

## Do not read this when
- git コマンド wrapper、CLI runtime、設定読み込み、path model、state file 読み書き、timestamp、report root など、複数サブコマンドで共有される低レベル基盤だけを調べたいとき。
- Codex に渡す prompt や Structured Output parameter の具体的な構築内容、Markdown/StructDoc の一般的な描画規則を調べたいときは、prompt や builder 側へ直接進む。
- oracle file、realization file、path keyword、INDEX.md の仕様、review finding の品質基準など、正本仕様断片そのものを確認したいとき。
- 特定のサブコマンドや下位処理がすでに明確な場合は、この領域全体ではなく、その対象の実装へ直接進む。
- 外部挙動をテスト観点から確認したいだけの場合は、対応するテスト領域を読む。

## hash
- 4d5b6c8b7b1fe9d84e4c49962d7b6aa7a08721c4044a6d04e9c4232365c62af3
