# `acp`

## Summary
- `src/acp` は、cmoc が AI エージェントを呼び出す直前に使うプロンプト部品、完全プロンプト、AgentCallParameter、Structured Output schema の構築実装をまとめる領域。標準文書の注入、ファイルアクセス規則、oracle/realization/review/index entry 規範、個別サブコマンド用の role・summary・goal・補助入力・モデル設定の対応関係を扱う。
- 下位には、標準 prompt 断片を生成・統合する領域と、apply fork、review oracle、indexing、session join、tui などの処理ごとに AI 呼び出しパラメータを組み立てる領域がある。実際のサブコマンド実行、git 操作、ファイル編集、レビュー結果の永続化ではなく、それらの前段で AI に渡す依頼文と応答契約を決める入口になる。

## Read this when
- AI エージェントへ渡す complete prompt、標準 prompt 断片、補助入力、file access mode、model class、reasoning effort、Structured Output schema の組み合わせを確認または変更したいとき。
- cmoc の apply fork、review oracle、indexing、session join、tui などが、どのような役割・目的・制約・標準文書を付けて AI 呼び出しを行うかを処理別に追いたいとき。
- oracle/realization の基本説明、ファイルアクセス制約、INDEX.md ルーティング規則、oracle review・apply review・index entry の標準を、prompt としてどの文面・順序で構築しているか調べたいとき。
- Structured Output schema を伴う AI 応答が、どの呼び出しビルダーから参照され、どの段階の機械処理可能な結果として期待されているかを確認したいとき。

## Do not read this when
- CLI サブコマンドの登録、引数解析、実行順序、状態管理、git branch や merge の実処理、ファイル保存、レビュー結果の集約・表示など、AI 呼び出し前後の制御フローだけを調べたいとき。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、StructDoc、path model などの基礎型そのものの定義や汎用ユーティリティを確認したいとき。
- oracle file や realization file の本文仕様、または実際にレビュー・修正・要約される対象ファイルの内容を直接調べたいとき。
- 生成済み INDEX.md の管理、リポジトリ全体の目次更新処理、または標準 prompt ではなく個別機能の実行結果を保存・適用する処理を確認したいとき。

## hash
- c7812cd460ab17a414b2e88c47216169b1a1b581995ff92b6e025dd4af49de31

# `basic`

## Summary
- cmoc の基礎的な実装モデルを集める領域。エージェント呼び出し条件、ルートトークン付きパス、規範文書モデル、構造化文書から Markdown への変換といった、上位機能から共有される小さな中核データ構造と変換処理を扱う。
- 外部コマンド実行、CLI 表示、永続状態、ファイル入出力そのものではなく、それらの前提になる抽象パラメータ、パス表現、文書モデルを確認するための入口となる。

## Read this when
- cmoc 内部で共有される基本的な型、列挙、データ構造、変換 helper の責務を確認したいとき。
- AI コーディングエージェント呼び出しに渡す抽象パラメータ、モデル区分、Reasoning effort、ファイルアクセスモードの表現を確認・変更したいとき。
- ルートトークン表記と絶対パスの相互変換、各 root の検出、git worktree に関わるパス解決を確認・変更したいとき。
- 規範文書を realization code 上で表すモデル、要求項目、判断例、構造化ドキュメントへの変換を確認・変更したいとき。
- 見出し階層、本文、コードブロックを組み立てて Markdown 文字列へレンダリングする小さな文書生成処理を確認・変更したいとき。

## Do not read this when
- CLI コマンドの引数定義、サブコマンド、利用者向け表示、JSON 出力 schema などの公開インターフェースを調べたいとき。
- エージェントプロセスの起動、外部コマンド実行、API 呼び出し、実際のファイル読み書きや永続状態操作を調べたいとき。
- 個別タスクのプロンプト生成内容、Structured Output schema の具体的な中身、生成された Markdown の保存先や利用先を調べたいとき。
- 自然言語で書かれた個別の oracle 規範本文そのもの、または oracle file と realization file の一般定義だけを確認したいとき。
- テストケースの期待値や検証観点だけを確認したいとき。

## hash
- 66bbd3e6c8104062e5f092ec021362cdb2daf050525e0e6fe7b0f72db231c419

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
- cmoc の realization implementation のうち、複数の CLI サブコマンドや workflow から共有される実行時 helper 群を収める領域。CLI サブコマンド共通ライフサイクル、Codex CLI exec/TUI 呼び出し、indexing preflight、設定読み書き、内容 hash、共通エラー表示、git 操作、実行ログ、root/path 解決、実行結果型、session state 永続化を扱う。
- 個別サブコマンドの業務処理ではなく、サブコマンド層や上位 workflow が依存する runtime 境界、外部プロセス境界、永続状態・ログ・設定・path の共通 API へ進むための入口になる。
- 一部の対象は互換 import や集約入口として、下位 runtime API をまとめて公開するだけの役割も持つため、具体挙動を読む場合はこの階層内の責務別実装へ進む。

## Read this when
- CLI サブコマンドの開始から完了までの共通出力、終了コード化、例外表示、サブコマンドログ設定など、コマンド横断の実行ライフサイクルを確認または変更したいとき。
- Codex CLI の exec/TUI 呼び出しに関する profile、sandbox、CODEX_HOME、schema、call log、Structured Output 検証、quota/capacity retry、resume、preflight の制御を追いたいとき。
- INDEX.md 自動更新の preflight、対象列挙、hash による鮮度判定、Codex による entry 生成、更新 commit の挙動を確認または変更したいとき。
- 設定ファイル、内容 hash 保存、git 実行・worktree・ignore 判定、root/path 解決、実行ログ、共通エラー、実行結果データ、session state file など、複数機能から再利用される runtime helper の責務境界を探すとき。
- 上位の command や workflow から利用できる共通 runtime API の import 面を確認し、既存 helper を使えるか判断したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務ロジック、利用者向けレポート内容、状態遷移の上位 workflow だけを知りたいとき。その場合はコマンド層や該当 workflow の実装へ直接進む。
- AgentCallParameter、FileAccessMode、設定モデル、path model などの基本データ型や正本仕様上の意味を確認したいだけのとき。その場合は基本層や oracle 側の定義を読む。
- 生成済みログ、state JSON、config JSON、schema store などの実データ内容を調査したいだけのとき。この領域はそれらの保存・読み書き helper であり、個別生成物そのものではない。
- 特定の runtime helper の具体的な入出力、副作用、失敗条件が分かっており、対象の責務別実装へ直接進めるとき。集約入口や隣接 helper を広く読む必要はない。
- テスト期待値や fixture の調整だけを行うとき。まず該当する test 側を読み、共通 runtime の挙動変更が必要だと分かった場合にこの領域へ戻る。

## hash
- 66141b09c68540d151cddaf806ad63f81a7e9118a29621c4298da0d1f039bcd3

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
- cmoc の各利用者向けサブコマンドを CLI runtime 上で実行するための実装領域であり、初期化、indexing、TUI 起動、session 操作、apply 操作、review oracle 実行の入口をまとめる。
- 各サブコマンドで必要な実行前条件の検査、work root/repository root の選択、session state の確認・更新、branch/worktree 操作、Codex exec/TUI 呼び出し、利用者向け出力や report 生成への接続を扱う。
- 個別コマンド固有の大きな制御は下位 package または補助モジュールに分かれており、この階層はサブコマンド単位で読む先を選ぶための入口になる。

## Read this when
- cmoc のサブコマンド実装がどこから起動され、CLI runtime、preflight、command name、command argv、Codex 実行 callback へどう接続されるかを確認・変更したいとき。
- 初期化、indexing、TUI、session、apply、review oracle のいずれかの利用者向けコマンドについて、実行条件、状態遷移、branch/worktree 操作、成功時出力、失敗時処理の入口を探したいとき。
- session branch の作成・破棄・join、apply 用 worktree での finding 適用と取り込み、review 用 worktree での oracle review と INDEX.md 反映など、サブコマンド横断で CLI 操作の流れを比較したいとき。
- サブコマンドが共通 runtime、indexing 共通処理、prompt builder、report renderer、git helper、設定読み込み、状態ファイル操作へどこから依存しているかをたどりたいとき。
- 利用者が実行するコマンドの外側の配線ではなく、コマンド本体に近い orchestration と、その下位処理への分岐点を確認したいとき。

## Do not read this when
- Typer app へのトップレベル登録、CLI 全体のコマンドツリー構成、entrypoint の import 配線だけを確認したいとき。
- git command wrapper、path model、設定モデル、state file の低レベル読み書き、共通 logging、report directory、timestamp など、サブコマンド固有でない runtime helper の詳細だけを調べたいとき。
- Codex に渡す prompt builder、Structured Output schema、AgentCallParameter の共通仕様、complete prompt 生成など、ACP 構築そのものの詳細だけを確認したいとき。
- oracle file の正本仕様断片、CLI 外部仕様、INDEX.md エントリー生成規約、review や apply の判断基準そのものを確認したいとき。
- 特定の session/apply/review 操作の内部処理だけを調べたいことが既に分かっている場合は、この階層全体ではなく該当する下位 package または補助モジュールへ直接進む。

## hash
- 461f2545a1c9e9286cae4c76c0282f103dabdb4b09dcf066ef46b70df5e8a7b5
