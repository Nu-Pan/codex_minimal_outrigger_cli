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

# `codex_exec_rule.md`

## Summary
- `codex exec` による Codex CLI 呼び出しの正本規約。agent call の path context、環境変数、preflight、argv 上書き、sandbox・権限、モデル・provider、prompt の渡し方、ログ保存、Structured Output、並列実行、失敗時の retry・待機・復旧方針を定める。Codex CLI 呼び出しや AgentCallParameter builder、prompt・sandbox・ログ・Structured Output 実装を変更・調査する際の入口となる。

## Read this when
- cmoc が Codex CLI を起動する方法や `codex exec` の argv・stdin・出力処理を変更するとき
- AgentCallParameter の cwd、path context、file access mode、model/provider、reasoning effort の扱いを確認するとき
- Codex CLI の sandbox、approval、permission profile、環境変数、preflight validation の実装を確認するとき
- Structured Output、prompt・stdout・stderr・output-last-message・call log の保存規約を確認するとき
- quota、rate limit、model capacity、一時障害、意味的失敗など Codex CLI 失敗時の retry・resume・待機処理を変更するとき

## Do not read this when
- Codex CLI 呼び出しや agent call 規約に関係しない cmoc 機能の実装・テストを調査するとき
- 一般的な Codex CLI の利用方法だけを確認したいときは、個別呼び出し仕様の正本である AgentCallParameter builder を直接読む
- モデル provider 固有の仕様だけを確認するときは、provider の正本文書を直接読む

## hash
- 374f98e35a94a3dd27c223879d6505a994a6d3b477d7e2eb6adf61cf398a37f5

# `codex_model_provider.md`

## Summary
- Codex CLI の model provider 設定仕様と、cmoc が担う責務境界を定義する正本文書。`CmocConfigCodex`、provider-local 設定、値の制約、secret 保存禁止、および provider 管理を行わない方針を確認する入口。

## Read this when
- Codex CLI 呼び出しの model/provider 設定、provider ID の検証、provider-local key の扱いを変更・確認するとき
- cmoc が model provider の管理・保証・自動起動を担うか判断するとき
- Codex 設定に保存できる値や secret の扱いを確認するとき

## Do not read this when
- model provider の argv への具体的な反映方法だけを確認したいときは、指定された codex_exec_rule.md を直接読む
- Codex CLI や provider 自体の稼働、認証、推論品質、model pull、cache 管理を調査するとき

## hash
- 928d25ace53f88c12fadd5a3b8fd311001343c040e43aa5dd25945d939bb0d82

# `console_and_file_log.md`

## Summary
- コンソール表示とサブコマンドログの正本仕様を定義する。時間・パスの表示形式、JSON Lines ログの保存先・イベント・flush 要件、Markdown 形式のコンソール通知、ステップ番号や Codex CLI 呼び出し情報、完了サマリーを扱う。出力形式やログ実装を変更・確認するときの入口となる。

## Read this when
- 時間表示、パス表示、コンソールログ、サブコマンドログの仕様を確認するとき
- サブコマンドのログ保存先、イベント記録、flush、ステップ通知、Codex CLI 通知、完了サマリーを実装・検証するとき

## Do not read this when
- コンソール出力やサブコマンドログに関係しない機能の実装・調査をするとき
- 具体的な実装構造やテスト手順だけを確認したいときは、対応する realization code や realization test を直接読む

## hash
- 0d394ef5255f04acc716ecb604b87e3e03aa9e25831c1cf4b41850d4a9992fab

# `doctor_preprocess.md`

## Summary
- doctor preprocess の責務、実行順序、共通前提の検証・修復、および修復不能時の終了条件を定義する正本文書。git 追跡状態、設定・refactor state の同期、修復内容と `cmoc run join` における同期時点を確認する入口。

## Read this when
- doctor preprocess の検証・修復仕様を確認するとき
- `.cmoc/gu`、`.agents`、`config.json`、refactor state の追跡状態や同期条件を変更・調査するとき
- `cmoc run join` における refactor state 同期のタイミングを確認するとき

## Do not read this when
- 個別サブコマンド固有の事前条件だけを確認するとき
- doctor preprocess と無関係な CLI 処理や実装詳細を調査するとき

## hash
- 489c8d13dcfb1d48f595820b7646abb2df6c6ab43097c531db338b9756163451

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
- cmoc の雑多な仕様を定める文書。oracle file・realization file の列挙方法、work-root の前提、cmoc 実行時のパス関係、タイムスタンプ形式、cmoc-managed-branch 上の変更範囲を扱う。これらの共通定義を確認するための入口。

## Read this when
- oracle file または realization file の列挙方法を確認するとき
- work-root、repo-root、run-root の前提や agent call の cwd の関係を確認するとき
- タイムスタンプ形式を実装・検証するとき
- cmoc-managed-branch 上の変更範囲や rename・削除ファイルの扱いを確認するとき

## Do not read this when
- 特定の oracle file や realization file の内容・責務を確認したいとき
- パスモデルの正本定義そのものを確認したいときは、参照先の path_model.py を直接読む

## hash
- f16f9bf6becc748adc0bbf8aef123a0e26ff5fd837224d4c65f73a765b69d935

# `prompt_editor_input.md`

## Summary
- cmoc がユーザーのプロンプトをエディタで入力・編集する際の仕様を定める。エディタ選択の優先順位、`code --wait` の要件、編集対象と初期値の出典、自動注入指示の扱い、編集完了判定、プロンプト読み出し時のコメント除去と空白除去を扱う。プロンプト編集フローやエディタ起動仕様を確認する際の入口となる。

## Read this when
- ユーザー入力用エディタの起動・選択・待機動作を変更または確認するとき
- エディタ入力ファイルの場所、初期値、自動注入指示、編集完了判定を確認するとき
- 編集後のプロンプトのコメント除去や前後空白除去の挙動を変更または確認するとき

## Do not read this when
- エディタを介さないプロンプト生成や、入力後のプロンプト処理だけを調べるとき
- エディタ入力の初期値を具体的に構築する実装を変更するときは、参照先の実装を直接読む

## hash
- b47670393941a74a64ff654dbc87f66c8cbc4d215130089c24b53b1f89b03284

# `prompt_standard.md`

## Summary
- cmoc が agent call に渡すプロンプトの構築規範を定める oracle doc。oracle src の builder 関数による動的生成、GFM と cmoc 固有記法、placeholder と参照ブロックの整合性検査、日本語を基本とする言語方針を扱う。

## Read this when
- agent call 用プロンプトの構築・変更・検証方法を確認するとき
- placeholder、cmoc_block、cmoc_ref の記法や整合性要件を確認するとき
- Codex CLI のプロンプト・レポート・INDEX.md などで使用する言語方針を確認するとき

## Do not read this when
- プロンプト構築以外の Python 実装規約を確認するときは、oracle src の実装対象や開発環境の文書を直接読む
- 一般的な Markdown の記法だけを確認したいとき
- 個別の agent 作業内容や対象ファイルの仕様を確認したいとき

## hash
- 68025ae63d5fc8e51868267a8c176cf65bba64d8f4aad41d38578f39493c4a10

# `run_isolation.md`

## Summary
- run の隔離作業における用語、fork から join または abandon までのライフサイクル、Git branch/worktree の扱い、および run-root 外への書き込み例外を定める仕様。run の開始・取り込み・破棄や、関連する branch、worktree、管理データの配置を理解するための入口。

## Read this when
- run の fork、join、abandon のライフサイクルを実装・確認するとき
- run branch、fork 時点の commit、linked worktree、session branch への merge 規則を扱うとき
- run-root 外への書き込み例外や cmoc 管理データの保存場所を確認するとき

## Do not read this when
- run の具体的な CLI 引数やサブコマンド実装だけを確認したいとき
- run 以外の workload の仕様や、個別の agent call path model の詳細を確認したいとき

## hash
- 000c7e1a1bd4461aa9f0229de21df744e6bb89d64940a3d3ce3bed99b82cf3ed

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
- cmoc のサブコマンド単位の正本仕様をまとめたディレクトリ。doctor、indexing、oracle/session/run の各 lifecycle、tui などの実行条件・手順・状態遷移・出力要件を扱い、サブコマンド仕様の実装・変更・レビュー時の入口となる。
- 共通 lifecycle や個別 workload の仕様を確認したい場合は、該当する文書へ進む。サブコマンド内部の実装、共通処理の詳細、入力パラメータ単体の仕様は、各文書から参照される対応先を直接読む。

## Read this when
- cmoc のサブコマンドの実行条件、引数、実行手順、状態遷移、終了処理を調査・変更するとき。
- session、editing run、oracle 操作、realization 操作、indexing、doctor、tui の正本仕様の入口を探すとき。
- 個別サブコマンドの仕様と、共通 lifecycle・workload 固有仕様の読むべき範囲を切り分けたいとき。

## Do not read this when
- サブコマンドに依存しない共通実装や、agent call・Codex CLI 起動など参照先の詳細仕様だけを確認したいとき。
- 具体的な realization 実装・テストの配置や開発環境の規則だけを確認したいとき。
- INDEX 自体の生成方法や、サブコマンドと無関係な仕様を調査するとき。

## hash
- 08c8f26210f4c027a0c387d8db393a2f77d14df795adea91c35d669a28613af2

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
- cmoc の基本的な呼び出し方法、初回準備、通常の session・oracle・realization の workflow、および apply と refactor の使い分けを説明する利用手順書。cmoc を使った開発 lifecycle の入口にあたる。

## Read this when
- cmoc の初回セットアップや基本的な呼び出し方法を確認するとき
- session fork/join、oracle 編集・レビュー、realization apply/refactor の手順を確認するとき
- realization apply と realization refactor の使い分けを判断するとき

## Do not read this when
- 特定の oracle file の仕様や編集内容を確認したいとき
- cmoc の内部実装や個別コマンドの詳細な技術仕様を調査するときは、対象コマンドまたは実装の文書を直接読む

## hash
- 67c1e11a5d4ebc3936273d706933419f4e789856bd1afb62c8baeed5896e0296
