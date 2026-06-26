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
- cmoc の realization implementation のうち、複数の CLI サブコマンドや上位実装から共有される runtime helper 群をまとめる領域。Codex CLI 実行、profile/config、path、Git、logging、error、content hash、result model、session state、CLI 実行ライフサイクルなど、個別コマンド固有ではない共通処理への入口になる。
- この階層には、公開 import 面をまとめる集約入口、互換 import のための橋渡し、実際の subprocess 制御や永続化・検証・表示を担う責務別 runtime 実装が並ぶ。まずここで共通 runtime 領域かどうかを判断し、必要に応じて Codex 実行制御、profile、path、Git、logging、error、state などの下位対象へ進む。

## Read this when
- 複数のサブコマンドから使われる共通 runtime 処理の実装場所を探しているとき。
- Codex CLI の exec/TUI 起動、profile 生成、schema/output/log 保存、retry、quota/capacity、Structured Output 検証など Codex 実行周辺の共通制御を調べたいとき。
- cmoc 設定の JSON 入出力、既定値補完、不正設定のエラー化、設定ファイルの初期同期を確認または変更したいとき。
- repo root、work root、cmoc root、`.cmoc` 配下の sessions/reports/log/worktrees/state/config など、実行時 path 解決や保存先規則を追いたいとき。
- Git コマンド実行、worktree 作成・削除、branch 状態検査、未コミット差分拒否、cmoc 内部ディレクトリの ignore 処理を共通 helper として扱う箇所を調べたいとき。
- サブコマンド実行ログ、Codex 呼び出しログ、console summary、quota 待機時間、現在 logger の context-local 管理など、runtime logging の共通挙動を確認したいとき。
- cmoc 共通例外、利用者向け Markdown エラーレポート、外部コマンド結果、Codex exec 結果、session state JSON 入出力など、上位処理間で受け渡す共通データやエラー表示を調べたいとき。
- 新しい共有 helper を置くべきか、既存の共通 runtime 実装へ追加すべきか、または個別サブコマンド側に閉じるべきかを判断したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、dispatch、利用者向けの具体的なコマンド挙動だけを調べたいとき。その場合は該当するコマンド実装へ進む。
- path キーワードや oracle/realization の概念定義など、正本仕様断片としての定義を確認したいとき。この階層は realization implementation であり、仕様確認は oracle 側を優先する。
- INDEX.md の生成ルール、ルーティング文書の仕様、エントリー生成プロンプトそのものを調べたいとき。この階層には runtime helper はあるが、正本仕様の本文ではない。
- 特定機能のテスト期待値や外部挙動を確認したいとき。共通 helper の実装ではなく、対応する realization test または oracle の仕様断片を読む方が直接的。
- 単一の上位機能に閉じた処理を変更するだけで、共有 runtime API、保存先、共通ログ、共通エラー、共通状態に触れないとき。
- 既に読むべき責務別対象が分かっており、Codex exec、Codex TUI、profile、config、path、Git、logging、error、state などの具体的な実装だけを確認すれば足りるとき。

## hash
- 571b38ee848a9778a89bd70f7cb4599d0bab5dad067ca76bc30891109d962699

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
- cmoc の利用者向けサブコマンド実行本体をまとめる実装領域。初期化、session の開始・取り込み・破棄、apply の開始・取り込み・破棄、oracle review、INDEX maintenance、Codex TUI 起動まで、CLI runtime と各操作の具体的な状態遷移・git 操作・出力を接続する。
- 各サブコマンドは共通 runtime helper や parameter builder を呼び出す入口として位置づけられ、branch 条件、clean worktree 条件、session/apply state 更新、isolated worktree 作成、report 保存、Codex 呼び出し、cleanup の流れを目的別に追うための分岐点になる。

## Read this when
- cmoc の個別サブコマンドが、どの事前条件で拒否され、どの順序で runtime helper、git 操作、Codex 呼び出し、状態更新、利用者向け出力を行うかを調査または変更したいとき。
- session branch の作成、home branch への merge、merge せず破棄する処理など、session ライフサイクルに関わる CLI 制御を追いたいとき。
- apply run の isolated worktree・apply branch・process id・finding 適用・report・join・abandon・cleanup など、apply 状態遷移全体の読む先を選びたいとき。
- oracle review の対象列挙、finding 生成・検証・判定、INDEX 変更 commit、review branch の merge、review report 生成のどこを読むべきか切り分けたいとき。
- INDEX.md の自動生成・更新・commit、または Codex TUI 起動前の依頼文編集・parameter 解決・complete prompt 保存といった、サブコマンド固有の保守・起動フローを確認したいとき。

## Do not read this when
- Typer app へのコマンド登録や、CLI 全体の構文定義だけを確認したいときは、サブコマンド登録側を読む。
- git wrapper、work root/repo root 解決、session state schema、config 読み込み、report directory、timestamp、ignore 判定などの共通 runtime 基盤そのものを変更したいときは、共通 runtime 側を読む。
- Codex に渡す prompt、Structured Output schema、AgentCallParameter の具体的な組み立てだけを調べたいときは、各 builder 側を読む。
- oracle file、realization file、review finding、INDEX.md エントリー品質基準などの正本仕様断片を確認したいだけのときは、oracle 側の文書を読む。
- サブコマンドの外部挙動をテスト観点で確認したいだけ、または既存テストへケース追加したいだけのときは、対応するテスト領域を読む。

## hash
- 7f286aeb88b03f85769d261e85baec07adab700460a420607e2099113cc12a22
