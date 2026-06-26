# `acp`

## Summary
- ACP 領域のエージェント呼び出しパラメータ構築と、呼び出し時に注入するプロンプト部品を扱う入口。用途別の role、goal、補助入力、読み書き制約、モデル設定、Structured Output 契約と、標準文書・ルーティング規則・レビュー規範などの prompt part 生成へ分岐する。
- apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成などで、エージェントに何を渡し、どの制約で、どの形式の出力を求めるかを確認するための領域。

## Read this when
- cmoc の機能が AI エージェントを呼び出す際の入力埋め込み、プロンプト構成、ファイルアクセス条件、モデル・reasoning effort、Structured Output schema への接続を確認・変更したいとき。
- apply 後段処理、oracle review、session join の conflict 解消、TUI 実行前判定、INDEX.md エントリー生成など、用途別の agent call parameter を追いたいとき。
- oracle file、realization file、ファイルアクセス規則、INDEX.md ルーティング、レビュー基準、INDEX エントリー規範などが、ACP 向けプロンプト本文としてどう生成・統合されるかを調べたいとき。

## Do not read this when
- CLI サブコマンド全体の実行順序、引数解析、git 操作、フォーク作成・統合、merge conflict marker 検出、生成結果の保存など、エージェント呼び出しパラメータ構築の外側を調べたいとき。
- oracle file や realization file の標準文書本文そのもの、レビュー判断基準そのもの、汎用データ型、パス解決 helper、構造化ドキュメント表現だけを確認したいとき。
- 外部エージェントとの通信処理、状態管理、テスト、または生成済みプロンプトを使う側の実装を調べたいとき。

## hash
- 8ef3ba634d84776ae73dce485dc46aa80129cf11198400c6364399870331d591

# `basic`

## Summary
- cmoc の realization implementation のうち、複数の上位処理から共有される基礎データ構造と変換部品を集めた領域。エージェント呼び出しパラメータ、root token 付きパス解決、規範文書モデル、構造化 Markdown 生成といった、CLI 個別処理より下位の共通概念を扱う。
- ここにある各実装は、具体的なサブコマンドや外部バックエンド呼び出しそのものではなく、それらが参照する論理入力、パス表記、文書表現、レンダリングの基盤として読む入口になる。

## Read this when
- cmoc 内部で共有される基本型、列挙、データ構造、または Markdown 文書生成部品の責務境界を確認・変更したいとき。
- エージェント呼び出しの論理パラメータ、root token 表記の実パス解決、規範文書の構造化、階層文書の Markdown 化のいずれかに関わる実装を探すとき。
- CLI 個別コマンドや realization 側の上位処理を読む前に、それらが前提にしている共通モデルや入力仕様を確認したいとき。

## Do not read this when
- 個別サブコマンドの実行フロー、CLI 引数、出力 schema、外部コマンド呼び出し、永続状態管理を直接調べたいとき。
- oracle file の正本仕様断片そのもの、各規範の具体的な要求文、または既存 Markdown 文書の本文内容を確認・変更したいとき。
- ファイル内容の読み書き、INDEX.md 生成、oracle file と realization file の分類など、基礎モデルを利用する上位処理だけを調べたいとき。

## hash
- 7f1c5fac1be83faa722d59f44307c9adbd03556e3e2cee68a70a6dc612da77c9

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
- cmoc の実行時共通基盤をまとめる実装領域。CLI サブコマンドの共通ライフサイクル、Codex exec/TUI 呼び出し、設定入出力、内容 hash、共通エラー表示、Git 操作、JSON Lines ログ、root/path 解決、外部実行結果、session state など、複数の上位機能から共有される runtime helper を扱う。
- 上位のコマンド実装が個別業務ロジックを進めるために利用する低レベル寄りの支援層であり、共有 API の集約入口と、責務別の runtime 実装本文へ進むための入口になる。

## Read this when
- CLI サブコマンドに共通する開始・完了表示、終了コード化、例外表示、サブコマンドログ、現在 logger の扱いを確認または変更したいとき。
- Codex CLI を cmoc から呼び出す runtime 制御を調べたいとき。特に profile/schema 準備、exec retry、Structured Output 検証、quota/capacity 処理、resume、TUI 起動、call log、indexing preflight の経路を追うとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正 JSON や不正値の利用者向けエラー化を確認または変更したいとき。
- 共通の内容 hash 計算、hash 名付きファイル保存、binary 判定など、runtime 生成物や cache 的出力の低レベル helper を確認したいとき。
- cmoc 共通例外と Markdown エラーレポート、Next actions、Detail、Call stack の表示形式を確認または変更したいとき。
- Git 状態の取得、clean worktree 検査、管理 branch 判定、worktree 作成・削除、内部ディレクトリの ignore 初期化など、cmoc 内から Git を扱う共通処理を確認したいとき。
- 実行ログの JSON Lines record、quota 待機時間や elapsed の計測、context-local なサブコマンド logger の受け渡しを調べたいとき。
- 実行時 root の解決、内部保存先、timestamp、duration 表示、処理中の一時的な cwd 変更を扱う共通 helper を確認したいとき。
- 外部コマンド結果や Codex exec 結果を、どの不変データ構造で上位へ渡すか確認したいとき。
- session branch と apply branch に紐づく永続 session state の JSON 入出力、branch 名からの session-id 抽出、active session 探索を確認または変更したいとき。
- 複数の共有 runtime 機能をまとめて import する公開入口や、外部へ露出する共通 runtime API の一覧を把握したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、dispatch、利用者向けの機能別出力だけを調べたいとき。その場合は該当する上位コマンド実装へ進む。
- Agent 呼び出しパラメータ、設定値、path keyword などの基本データ構造や概念定義そのものを確認したいだけのとき。その場合は基本モデルや設定モデルの定義を直接読む。
- oracle file の正本仕様断片、CLI 公開仕様、INDEX.md 生成仕様、routing 文書の規則を確認したいとき。この階層はそれらを具体化する共有 runtime 実装であり、正本仕様の本文ではない。
- テストケース、fixture、期待される外部挙動の検証観点を確認したいとき。その場合は対応するテスト領域を読む。
- 特定機能の上位 workflow で、どのタイミングで共有 helper が呼ばれるかだけを知りたいとき。まず呼び出し側の実装を読み、必要になった場合だけこの階層の該当 runtime helper へ進む。
- ログや状態ファイルを読む側、集計する側、レポート化する側の仕様や実装を探しているとき。この階層は主に runtime 中の生成・保存・受け渡しを扱う。

## hash
- b12c552619460bf10c26a6bb9a66d30c3466e290e000e18bb0770def933f5752

# `config`

## Summary
- 開発対象リポジトリごとに変わる cmoc 設定を表す dataclass 群を扱う領域。
- AI エージェント呼び出しの並列数、Codex CLI 向けモデル名と reasoning effort、apply fork と review oracle のループ上限など、永続化される設定値の既定値を確認する入口になる。
- 人間が編集するリポジトリ別設定面に含まれる値の定義を追うための対象であり、設定ファイルの入出力処理そのものは別領域に分かれる。

## Read this when
- リポジトリ別に保持される cmoc 設定項目や既定値を確認・変更したいとき。
- 初期化時に生成・同期される設定ファイルへ含める値や、Enum 系の値を JSON 保存向けに扱う前提を確認したいとき。
- Codex CLI に渡すモデル名、reasoning effort 名、AI 呼び出し並列数、apply fork や review oracle の処理回数上限を調整したいとき。

## Do not read this when
- CLI 引数、サブコマンド構文、実行時の入出力フローを調べたいだけのとき。
- 設定ファイルの実際の読み書き、JSON 変換処理、または `.cmoc` 配下のパス解決処理を調べたいとき。
- oracle file、realization file、パスキーワード定義、INDEX.md 生成ルールそのものを確認したいとき。

## hash
- 324dfe3034cabedbb119cb79c0c59fcdd422ac0747dbbc5e095eba5140bb0d71

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
- CLI の各サブコマンド実装をまとめる領域。初期化、TUI 起動、INDEX 生成、review oracle、apply、session 操作など、利用者が実行する上位コマンドの入口と実行ライフサイクルを扱う。
- サブコマンドごとの事前条件、runtime 連携、worktree・branch・state・report・cleanup・Codex 呼び出しへの接続を調べる際に、対象コマンドまたは下位モジュールへ進むための分岐点になる。
- apply と session は下位パッケージにまとまっており、review oracle は対象列挙、実行 loop、INDEX 差分処理、report 生成などの責務別モジュールに分かれている。

## Read this when
- cmoc のサブコマンド実行フロー、事前条件、利用者向け出力、branch・worktree・state・report の扱いを調査または変更したいとき。
- init、tui、indexing、review oracle、apply、session のうち、どの実装を読むべきかを切り分けたいとき。
- review oracle の上位制御、対象列挙、Codex review loop、ルーティング文書差分の commit・merge、Markdown report 生成の接続関係を追いたいとき。
- apply fork・join・abandon や session start・join・abandon など、実行中の状態遷移、branch 操作、cleanup、process 管理を扱う入口を探したいとき。
- Codex 実行前の INDEX 生成 preflight、TUI 用 prompt 作成、初期化時の ignore 保証や設定同期など、CLI から共通 runtime helper を呼び出す境界を確認したいとき。

## Do not read this when
- git wrapper、config 読み込み、path 解決、state file 永続化、timestamp、report directory、Codex 外部プロセス実行など、サブコマンドに依存しない共通 runtime 基盤そのものを調べたいとき。
- Codex に渡す prompt、AgentCallParameter、Structured Output parameter の本文や schema 定義だけを確認したいとき。
- oracle file の正本仕様、realization 品質基準、INDEX.md の生成規則やルーティング文書の仕様そのものを確認したいとき。
- テスト観点から外部挙動を確認したいだけで、実装の実行順序や責務分担を読む必要がないとき。
- 対象サブコマンドや責務が既に特定できており、その個別ファイルまたは下位パッケージを直接読めば足りるとき。

## hash
- 4431672e3a7774def34c2267cf6d28b829486798f8732022d85a7fc28977d23c
