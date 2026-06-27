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
- CLI 実行基盤で横断利用される共有 runtime helper 群をまとめる領域。サブコマンド共通の実行ライフサイクル、設定入出力、エラー表示、Git 操作、ログ、実行時パス、永続状態、外部コマンド結果、内容 hash 保存、Codex exec/TUI 呼び出しと profile・preflight 制御などを扱う。
- 個別実装は責務別に分割され、一部は既存 import 経路を保つための薄い再エクスポート入口として置かれている。共通 runtime API の公開面を見渡す入口としても、具体的な runtime 挙動の定義元へ進む入口としても使う。

## Read this when
- サブコマンド全体に共通する開始・完了表示、終了コード化、例外処理、事前検査、ログ設定などの実行制御を確認または変更したいとき。
- cmoc 設定の永続化形式、読み書き、既定値補完、不正設定のエラー化を調べたいとき。
- Git 状態確認、cmoc 管理 branch、run worktree、ignore/exclude 操作など、複数コマンドから使われる Git helper を確認したいとき。
- 実行時 root、管理ディレクトリ、設定・状態・ログ・レポートの配置、timestamp や `<work-root>/memo` 判定など、runtime path helper を追いたいとき。
- サブコマンド単位または Codex 呼び出し単位のログ、console 表示、quota 待機時間や elapsed の記録を確認したいとき。
- Codex CLI の exec/TUI 起動、profile 生成、schema 保存、Structured Output 検証、capacity/quota retry、resume、preflight、call log、`.agents` 変更拒否を調べたいとき。
- session/apply に紐づく永続 state の JSON 入出力、branch 名からの session-id 抽出、active session 探索を扱うとき。
- 外部コマンド結果や Codex exec 結果を運ぶ共有データ構造、または内容 hash に基づく保存・binary 判定 helper を確認したいとき。
- 共通 runtime API の import 入口や、既存 import path と責務別実装の接続関係を把握したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、ユーザー向け workflow、出力 schema を調べたいだけのとき。その場合は呼び出し側のサブコマンド実装へ進む。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などの概念定義や正本仕様を確認したいとき。その場合は path model や oracle 側の仕様を読む。
- oracle file、realization file、INDEX.md 生成規則、ルーティング文書の仕様判断をしたいとき。この領域は実行時 helper の実装であり、正本仕様そのものではない。
- 設定データクラス、AgentCallParameter、FileAccessMode、モデル設定など、入力モデル自体の定義だけを確認したいときは、それぞれのモデル定義元を読む。
- ログや状態やレポートの内容を読む側・集計する側・表示する側の仕様を調べたいときは、その利用側へ進む。
- Codex や Git を使わない純粋なドメイン処理、テスト期待値、上位 command の制御フローだけを確認したいとき。

## hash
- 80a759569b7925fb6c0957eee2b311c1e9d9b8e9313b526232d63900324a7c9a

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
- CLI サブコマンドの実行本体を集める領域。初期化、セッション lifecycle、apply run、review oracle、ルーティング文書更新、TUI 起動など、利用者操作ごとの orchestration と副作用を扱う。
- 各サブコマンドは共通 runtime や下位 helper を呼び出しながら、事前条件確認、状態遷移、branch/worktree/process 操作、report 生成、利用者向け出力を接続する入口として位置づく。
- 上位の command tree や共通 runtime API ではなく、サブコマンド単位の実行順序、失敗条件、状態更新、git/worktree/process/report への具体的な接続関係を追うためのまとまり。

## Read this when
- cmoc の各サブコマンドがどの前提条件で実行を拒否し、どの順序で状態・branch・worktree・process・report を更新するかを確認または変更したいとき。
- session の開始・完了・破棄、apply run の開始・破棄・join、review oracle の対象列挙から report 出力までなど、利用者操作ごとの lifecycle を追いたいとき。
- 初期化処理、TUI 起動、INDEX.md 自動更新、review 用 INDEX 差分 commit/merge など、特定サブコマンドの実行制御と共通 helper への接続を調べたいとき。
- サブコマンド実行中の clean worktree 要求、active session 判定、apply state 判定、merge conflict 処理、cleanup、エラー時 report などの制御境界を調査したいとき。

## Do not read this when
- Typer へのコマンド登録、CLI option 定義、root command tree だけを確認したいときは、CLI 定義側を読む方が直接的。
- repo root 探索、git 実行 wrapper、worktree helper、設定読み込み、state file 永続化、timestamp、report directory など、複数サブコマンドで使う共通 runtime API の定義だけを調べたいとき。
- Codex に渡す prompt、Structured Output schema、parameter builder の具体的な構築内容だけを確認したいときは、prompt や builder を担当する領域へ進む。
- oracle file、realization file、path keyword、INDEX.md 生成規則などの正本仕様断片を確認したいときは、仕様断片側を読む。
- 特定サブコマンドの外部挙動をテスト観点から確認したいだけのときは、対応するテストを読む。

## hash
- 41a8f30c1b2a5cbb99b8127bbb1aefd32616cfe253255a3609d2c0bc4f610ac8
