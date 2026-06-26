# `acp`

## Summary
- AI エージェント呼び出しに関する実装領域。上位コマンドが AI に処理を委ねる直前の呼び出し条件を組み立てる builder 群と、その prompt 本文へ注入する標準文書・規則・基礎説明の部品群を扱う。
- role、summary、goal、補助プロンプト、参照標準、ファイルアクセス規則、モデル種別、推論量、Structured Output schema などの agent call 契約を作る入口であり、用途別の呼び出しパラメータ構築と共通 prompt 断片生成へ進むための分岐点である。
- フォーク適用、目次エントリー生成、oracle review、session conflict 解消、TUI 実行パラメータ解決など、個別処理を AI に依頼するための条件設定を扱うが、実際の差分解析、git 操作、CLI/TUI 制御、結果検証、保存処理そのものは対象外である。

## Read this when
- AI エージェントに渡す complete prompt、補助プロンプト、参照標準、ファイルアクセス権限、モデル設定、Structured Output schema の対応関係を確認または変更したいとき。
- 上位コマンドの各フェーズが、どの種類の agent 呼び出しや prompt 部品に接続されるかを追いたいとき。
- raw diff、対象パス、レビュー所見、元プロンプト、conflict 対象ファイル一覧などの入力が、AI への作業指示や出力契約にどう埋め込まれるかを確認したいとき。
- agent call 用パラメータを作る処理を読むべきか、prompt 本文に含める規則・標準・基礎説明を作る処理を読むべきか判断したいとき。

## Do not read this when
- コマンド全体の実行フロー、サブコマンド入口、状態管理、ファイル走査、保存、通知、CLI/TUI 入出力など、AI 呼び出し条件を作る前後の外側の制御を調べたいとき。
- git 操作、ブランチ操作、merge 実行、conflict 検出、差分取得、作業ツリー反映など、実際のリポジトリ操作を調べたいとき。
- AI 呼び出し後の結果検証、レビュー所見の統合、修正結果の確認、テスト実行など、builder が返したパラメータを使った後段処理を調べたいとき。
- StructDoc、Standard、Requirement、AgentCallParameter、ファイルアクセスモード、パス解決、Structured Output schema の項目名や型など、汎用部品や schema 定義そのものを確認したいとき。
- 特定の oracle file や realization file の本文内容、または個別機能の仕様そのものを確認したいとき。

## hash
- 459e0244636e6f374738ffd593a2ed04db4038bce5e94a74e1f181612dc07535

# `basic`

## Summary
- AI コーディングエージェント呼び出し条件、ルートトークン付きパス解決、規範文書モデル、構造化自然言語文書の Markdown 化という、cmoc の基礎的な実装モデルを集めた領域。
- 特定の CLI サブコマンドや業務フローではなく、他の実装が参照する抽象的な値、文書表現、パス表記、レンダリング補助を確認する入口として位置づけられる。
- oracle 側の概念を realization として扱うための小さな基盤実装や、複数箇所から使われる可能性のある基本データ構造を探すときの起点になる。

## Read this when
- cmoc 内部で共有される基礎モデルや抽象値の定義を確認・変更したいとき。
- エージェント呼び出しのモデル区分、Reasoning effort、ファイルアクセスモード、Structured Output schema の有無といった実行条件の保持方法を調べるとき。
- ルートトークン表記と実パスの相互変換、各 root の探索規則、ルートトークンなし相対パスの拒否条件を確認するとき。
- 規範文書をコード上で表すモデル、要求項目の保持、構造化文書への変換を確認するとき。
- 見出し階層、本文、コードブロックから Markdown 文字列を生成する基本処理や、インデント・空行の正規化を調べるとき。

## Do not read this when
- CLI サブコマンドの引数解析、入出力、外部コマンド実行、永続状態操作など、具体的な実行フローを調べたいとき。
- 個別タスクのプロンプト内容、生成される Structured Output schema の具体的な中身、または特定バックエンド向けの値解決を探しているとき。
- 自然言語で書かれた個別の規範本文そのものや、oracle file の正本仕様断片を確認したいとき。
- INDEX 生成や文書ルーティング規則そのものを調べたいとき。
- テストから期待外部挙動を確認したいだけで、基礎モデルの実装詳細を読む必要がないとき。

## hash
- 05b3886670c04664122b7a883b413760ebccf3603e081a43895f4266ad14bc2f

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
