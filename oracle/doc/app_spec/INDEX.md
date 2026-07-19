# `cli_auto_completion.md`

## Summary
- CLI の自動補完プローブに関する正本仕様断片。`_CMOC_COMPLETE` が存在する呼び出しを通常実行と区別し、補完処理前の cmoc 固有処理・副作用・不要な標準出力／標準エラー出力を禁止する。CLI 起動処理や補完プローブの挙動を実装・検証する際の仕様上の入口となる。

## Read this when
- `_CMOC_COMPLETE` を用いた自動補完の判定や実行順序を変更するとき
- 自動補完時の副作用、状態検査、ログ・INDEX 更新、エラー出力の扱いを確認するとき
- CLI 補完プローブの stdout／stderr の互換性を実装・テストするとき

## Do not read this when
- 通常のサブコマンド処理、session／run 状態管理、ログ作成、INDEX 更新そのものを変更するとき
- 自動補完とは無関係な CLI 入出力や一般的なエラー処理を確認するとき

## hash
- c6c8f4184e5a5408e45d6fc796612c986a7954e7b2002b30e42c241fd1b590e2

# `cmoc_managed_ollama.md`

## Summary
- cmoc がユーザー空間で管理する、OS ユーザーごとに 1 つのローカル Ollama サービスの正本仕様。サービスのライフサイクル、systemd 設定、モデル・ダウンロード資源の永続化、preflight 排他、GPU 推論を含む起動保証、Codex CLI からの接続方法を定める。

## Read this when
- cmoc managed ollama の準備・起動・修復・停止方針を実装または確認するとき
- Ollama の配置先、モデル pull、永続資源、systemd user service の仕様を確認するとき
- preflight のプロセス間 lock、モデルのロード、GPU 推論確認、CPU フォールバック禁止の挙動を扱うとき
- Codex CLI の model provider argv や localhost:11434 への接続設定を実装・検証するとき

## Do not read this when
- Ollama 管理や cmoc managed ollama の起動保証を扱わず、Codex CLI の一般的な実行規則だけを確認したいときは、codex_exec_rule.md を直接読む
- cmoc managed ollama の仕様ではなく、個別の設定メンバーの詳細挙動を確認したいときは、そのメンバーのコメントを直接読む

## hash
- 199714c69036d89b61f673e97e7611f85864b6c0ab132929aef44694e328a5dd

# `codex_exec_rule.md`

## Summary
- Codex CLI を cmoc から呼び出す際の規約を定義する正本仕様文書。CODEX_HOME の扱い、事前検証、argv による設定上書き、sandbox・ネットワーク・権限制約、プロンプト・ログ・Structured Output の受け渡し、並列実行、失敗時のリトライや quota 待機までを扱う。Codex 呼び出し実装やその設定・検証方法を確認する際の入口となる。

## Read this when
- cmoc の Codex CLI 呼び出し仕様を変更・実装・レビューするとき
- sandbox、permission profile、ネットワーク、モデル、reasoning effort、Structured Output、ログ保存の規約を確認するとき
- Codex CLI 呼び出しの失敗時処理や quota・一時障害時のリトライ方針を確認するとき

## Do not read this when
- Codex CLI 呼び出し以外の機能や一般的な CLI 実装だけを確認するとき
- 個別の AgentCallParameter builder の具体的な実装を直接調査する場合は、まずその builder の正本実装を読むべきとき

## hash
- 46d977b7bf89d0979292e3bbd9bacb61de85ee92cc70ba46f30cfce868a94ef4

# `console_and_file_log.md`

## Summary
- コンソール・ファイル・ログ出力に関する共通仕様を定義する文書。時間・パスの表示形式、サブコマンドログの保存場所・JSON Lines形式・必須イベント、コンソールログの出力先・Markdown形式・開始通知・ステップ通知・Codex CLI通知・完了サマリーを扱う。これらの出力仕様を実装・検証する際の入口となる。

## Read this when
- コンソールに表示する時間やパスの形式を確認するとき
- サブコマンドログの保存先、形式、イベント、flush要件を実装・検証するとき
- サブコマンドのコンソールログに必要な通知項目やステップ番号の形式を確認するとき
- Codex CLI呼び出し通知やサブコマンド完了サマリーの出力要件を確認するとき

## Do not read this when
- ログ出力やコンソール表示の仕様に関係しない機能の実装・調査を行うとき
- 個別サブコマンドの処理手順やCodex CLI呼び出し内容そのものを確認したいときは、対象サブコマンドの仕様・実装を先に読むとき
- 既存ログの具体的な実行結果や履歴を確認したいときは、定義文書ではなく生成されたログファイルを読むとき

## hash
- bd596f8c1d6116a4049645b525a29daf9b75e415e30437e1b627d537b19503ef

# `doctor_preprocess.md`

## Summary
- doctor preprocess の責務・実行手順・検証および修復条件を定義する正本仕様。各サブコマンド開始前の共通環境整備、git 追跡状態、refactor state、managed Ollama service の起動保証、差分 commit の扱いを確認する入口。

## Read this when
- doctor preprocess の検証・修復処理を実装または変更するとき
- サブコマンド共通の事前処理、git 追跡状態、refactor state の同期条件を確認するとき
- cmoc managed ollama service の起動保証を doctor preprocess から扱う条件を確認するとき

## Do not read this when
- doctor preprocess 正常終了後に行う個別サブコマンド固有の事前条件を確認するとき
- managed Ollama service が保証するサービス・モデル状態の詳細だけを確認するときは、指定された managed Ollama 仕様を直接読むとき

## hash
- f6edb357f89af1e6385f520923199961158500f262d58b41edee586ab6d986ab

# `error_handling.md`

## Summary
- 各仕様のエラー終了時の共通ルールを定める。特別な上書きがない場合に、処理を中断し、stdout へ簡潔な説明・次の対応候補・詳細・コールスタックを出し、エラー終了を示す終了コードを返す場面で読む。

## Read this when
- 仕様側でエラー時の既定動作をそろえたいとき。
- エラー発生時に利用者へ何を出すか、どの時点で止めるか、終了状態をどう扱うかを確認したいとき。
- 個別仕様にエラー処理の上書き指示がなく、この共通規則を適用する必要があるとき。

## Do not read this when
- 個別仕様がエラー時の振る舞いを明示しているときは、そちらを先に読む。
- エラー内容の文面や詳細な報告項目を別途定義する具体仕様を確認したいときは、その仕様本文を読む。
- 正常系の処理手順だけを確認したいときは読む必要がない。

## hash
- bfaceea1701755cbe1f24db75ea9044ad4d4ed7dc98edef844bc94e39c3bbdf8

# `external_model_provider.md`

## Summary
- 本文が空のため、このファイル単体からは根拠のある routing entry を生成できない。

## Read this when
- このファイルに実仕様が追記され、外部 model provider の扱いが本文で明示されたとき。

## Do not read this when
- cmoc managed ollama の具体的な保証条件や手順だけを確認したいときは、より直接の正本である `{{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md` を読む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `indexing.md`

## Summary
- - `cmoc` による `INDEX.md` 自動配置と、その目次情報の生成・更新ルールを定める。
- - どのディレクトリとファイルを目次対象に含めるか、除外するかの判断基準を定める。
- - `INDEX.md` 生成時の処理順、差分の扱い、自動コミットの条件を定める。

## Read this when
- - `INDEX.md` を自動生成・再生成・更新する処理を実装または修正するとき。
- - あるディレクトリをインデックス対象に含めるか除外するかを判断するとき。
- - `INDEX.md` の生成タイミング、再帰順、差分処理、コミット単位を決めるとき。
- - インデクシング処理の正しさを確認するテストや検証を作るとき。

## Do not read this when
- - `INDEX.md` ではなく、個別機能の実装内容や利用者向け仕様を確認したいだけのとき。
- - 目次生成そのものではなく、別の `cmoc` 機能の設計や実装を扱うとき。
- - 手書きの `INDEX.md` 内容を考える作業で、自動配置や更新ルールが関係しないとき。
- - この仕様に含まれない具体的なハッシュ計算手順やコミット実装の細部だけを探したいとき。

## hash
- 61ab6318a773747ce71141f365f5aaf26fec36e326e42a08c8cb699b32cd199e

# `misc_spec.md`

## Summary
- cmoc の雑多な仕様を定義する oracle 文書。oracle file・realization file の列挙方法、work-root の前提、実行時カレントディレクトリ、タイムスタンプ形式、cmoc-managed-branch の対象範囲を扱う。misc 系仕様を確認する際の入口。

## Read this when
- oracle file または realization file の列挙方法を確認するとき
- work-root の前提や cmoc 実行時のカレントディレクトリを確認するとき
- タイムスタンプ形式を確認するとき
- cmoc-managed-branch 上の変更範囲の定義を確認するとき

## Do not read this when
- 特定の oracle file や realization file の実装内容を確認したいとき
- 開発環境、設計ルール、テストルールなど個別の開発手順を確認したいとき

## hash
- 35f26f304c23fb77c0a46fd13bc01989e8fc2629fc8ea3db7ee5dba90cdc5d3c

# `prompt_editor_input.md`

## Summary
- cmoc がユーザー入力用プロンプトをエディタで編集させる際の仕様を定義する。エディタの優先順位、`code --wait` の使用、初期プロンプトの配置、編集完了の扱い、コメント除去と前後空白の除去による入力読み出しを扱う。プロンプト編集フローの実装・確認時に参照する入口である。

## Read this when
- プロンプト入力用エディタの起動順序や起動オプションを変更・確認するとき
- 編集対象ファイルの場所、初期値、編集完了条件を変更・確認するとき
- エディタ入力から cmoc がプロンプトを読み出す処理を変更・確認するとき

## Do not read this when
- エディタ入力以外のプロンプト生成や AI Agent CLI/TUI の実行仕様を確認するとき
- 一般的なプロンプト設計や、編集対象ではない oracle file の内容を確認するとき

## hash
- c4d73b4fd42f632c93fe725969c1f42964015fdf716b054730177ab92a00e63c

# `prompt_standard.md`

## Summary
- cmoc の agent call 用プロンプトに関する正本仕様を定める oracle doc。プロンプトの動的構築元、realization 側での加工制約、Markdown・プレースホルダ・cmoc_block/cmoc_ref 記法、参照検証、使用言語の原則と例外を扱う。

## Read this when
- agent call に渡すプロンプトの構築方法や realization 側の加工可否を確認するとき
- プロンプトの Markdown 方言、プレースホルダ、cmoc_block/cmoc_ref の記法・検証を変更または実装するとき
- Codex CLI が扱う自然言語の使用言語や個別仕様による例外を確認するとき

## Do not read this when
- 具体的な oracle src の関数実装や動的プロンプト生成コードを直接変更・調査するときは、該当する oracle/src の実装を読む
- 一般的な agent 作業規則や oracle・realization の定義を確認するときは、リポジトリの共通規則を読む

## hash
- 9e3766aebf04cc43deaa8ca92d848217c208025881860ab522ff1882a870f126

# `run_isolation.md`

## Summary
- run の隔離作業を、fork から join または abandon までの lifecycle として定義する仕様文書。run とサブコマンドの関係、workload、専用 branch・linked worktree、成果物の merge または破棄、および run-root 外への書き込み例外を扱う。run の開始・終了、branch/worktree 管理、成果物の取り込み、cmoc 管理データの保存先を判断するための入口となる。

## Read this when
- run、fork、join、abandon の lifecycle を実装・レビューするとき
- run 用 branch、linked worktree、成果物の merge/破棄規則を確認するとき
- run-root 外への書き込み可否や cmoc 管理データの保存先を判断するとき
- 編集 run と read-only investigation/review、機械的更新、session join の conflict 解消の扱いを確認するとき

## Do not read this when
- run の隔離 lifecycle や branch/worktree 管理に関係しない機能を扱うとき
- 具体的な CLI 引数や個別 workload の詳細仕様を確認したいときは、対応する個別仕様を直接読むとき

## hash
- 2124abd2e172d2cbaafcebff6c722ffbcbe0f86611db40113fcc44a3dcbd292d

# `session_state.md`

## Summary
- cmoc workflow における session と、明示的な join を必要とする realization 編集 run の lifecycle を定義する JSON state file。session/run の最小スキーマ、各 field の意味、状態遷移、保存場所を正本として扱う。

## Read this when
- session の新規作成、fork、join、abandon、run 状態管理を実装・変更するとき
- session state JSON の schema、field の初期値・更新条件、run の状態遷移を確認するとき
- realization apply または realization refactor run と session の lifecycle の関係を確認するとき

## Do not read this when
- session/run の lifecycle や state JSON schema に関係しない機能を調査・変更するとき
- 具体的な CLI サブコマンドの実装詳細だけを確認したいときは、該当する realization implementation や test を直接読む

## hash
- 7501ed856adb909badee98dacd09f75e6d2d7330690f8bcea48ed841a11b7aa7

# `sub_command`

## Summary
- cmoc のサブコマンドおよび session・editing run lifecycle の正本仕様文書群を収めるディレクトリ。doctor、indexing、tui、oracle 操作、session 操作、realization apply/refactor、run lifecycle の実装・レビュー時の入口となる。

## Read this when
- cmoc のサブコマンドの実行条件、引数、処理手順、入出力、Codex CLI/TUI 起動仕様を確認するとき。
- session fork/join/abandon や editing run の fork/join/abandon lifecycle、state、branch、merge、cleanup、report を確認するとき。
- oracle 操作または realization apply/refactor の仕様を実装・変更・レビューするとき。

## Do not read this when
- 個別処理の内部実装やテスト詳細だけを確認したいとき。
- 共通 lifecycle や共通起動パラメータなど、本文から参照される専用の正本仕様を直接確認すべきとき。
- 対象サブコマンドと無関係な一般的な git 運用や Codex CLI の仕様だけを確認したいとき。

## hash
- fbb4bf5183262d937475144174e65e91b404ef1c28856015635f1a7b1a7d0cfe

# `subcommand_interruption.md`

## Summary
- 中断可能なサブコマンドにおけるユーザー中断要求（Ctrl+C）の対象範囲、共通処理、完了時の状態・report・終了 log、および中断後の run の扱いを定める仕様文書。該当サブコマンドの中断処理や再開可否を確認する入口。

## Read this when
- `cmoc realization refactor fork` または `cmoc oracle review` のユーザー中断処理を実装・変更・検証するとき
- Ctrl+C を正常系として扱う条件、部分結果の確定、state 更新、report・終了 log の要件を確認するとき
- 中断後の run を再開・join できるか判断するとき

## Do not read this when
- 中断可能サブコマンド以外の通常の CLI エラー処理や終了処理を扱うとき
- ユーザー中断や対象サブコマンドの run lifecycle と無関係な仕様・実装を調査するとき

## hash
- 78af86a4a5d1502db95696ef32c9b1a89a509acea0e398fd210537a50aecf86b

# `usage.md`

## Summary
- cmoc の基本的な利用手順を定義する文書。doctor、session fork/join、oracle の調査・編集・レビュー、realization apply/refactor、run の join/abandon までの標準 workflow と、各 workload の使い分けを案内する。

## Read this when
- cmoc の初回セットアップや標準 workflow を確認するとき
- oracle 変更の realization 反映方法や、apply と refactor の違いを確認するとき
- session・run の fork、join、abandon の手順を確認するとき

## Do not read this when
- 特定の oracle file の仕様内容を確認したいとき
- 実装やテストの詳細、個別コマンドの内部仕様を調べたいとき

## hash
- 224a77bd1f12361f99843cfc4d03a769350badf342f4dbcf41d8a73896002f96
