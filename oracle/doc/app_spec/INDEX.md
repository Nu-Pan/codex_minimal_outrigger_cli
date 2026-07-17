# `cli_auto_completion.md`

## Summary
- `_CMOC_COMPLETE` を伴う呼び出しを通常実行から切り分け、自動補完用プローブでは cmoc 固有の前処理・検査・副作用を補完処理より先に走らせないための規則を扱う。補完時に余計な標準出力や標準エラー出力を混ぜない条件を確認したいときに読む。

## Read this when
- `_CMOC_COMPLETE` の有無で CLI の分岐を実装・変更したいとき。
- 補完候補の生成前に、サブコマンド未指定判定・カレントディレクトリ変更・session/apply 状態検査・`.cmoc` ログ作成・INDEX 更新・cmoc 形式のエラーレポート出力を抑止すべきか確認したいとき。
- 補完処理の標準出力や標準エラー出力に、補完ライブラリ以外の文言が混ざらないことを確認したいとき。

## Do not read this when
- 通常のコマンド実行時のサブコマンド処理全般を知りたいだけのときは、CLI の通常実行ルールの文書を先に読む。
- session 状態や apply 状態そのものの仕様を知りたいだけのときは、それぞれの状態仕様の文書を読む。
- エラー表示全般の形式やログ出力全般の仕様を知りたいだけのときは、個別のエラーハンドリングやログの文書を読む。

## hash
- 480051b6d39bcaaf30039ef43ae1a8853e51bcadc27cd83c7c39a44cf76ef3c4

# `cmoc_managed_ollama.md`

## Summary
- cmoc がユーザー空間で管理するローカル SLM サービスの正本仕様。サービスのライフサイクル、永続ダウンロード資源、preflight のプロセス間排他、GPU 推論を含む利用可能性保証、Codex CLI からの接続方法を定める。cmoc managed ollama の構築・修復・利用条件や関連実装の入口となる。

## Read this when
- cmoc managed ollama の準備・起動・サービス管理・モデル pull・資源永続化を実装または確認するとき
- cmoc の doctor preprocess、利用可能性保証、GPU 推論確認、エラー終了条件を実装または検証するとき
- 同一ユーザーの cmoc process 間の preflight 排他やサービスのライフサイクルを扱うとき
- Codex CLI の model provider、argv、base URL、provider 設定を変更または確認するとき

## Do not read this when
- cmoc managed ollama に関係しない一般的な CLI、Codex agent 呼び出し、または別の model provider の実装を扱うとき
- ollama 自体の一般的な仕様や、cmoc が管理しないサービスの運用を調べるとき

## hash
- fc1659cd049f2f1c59c7cf92837719fdcc9e04cc663865acdb131b7f4b9f522b

# `codex_exec_rule.md`

## Summary
- Codex CLI の `codex exec` 呼び出しに関する正本仕様断片。環境変数、preflight validation、argv による設定上書き、sandbox、permission profile 禁止、モデル・推論設定、プロンプト・ログ・Structured Output の受け渡し、並列実行、失敗時の再試行・待機・復帰方針を定める。Codex CLI 呼び出し処理や AgentCallParameter builder の仕様を確認する際の入口。

## Read this when
- cmoc または AgentCallParameter による Codex CLI 呼び出しを実装・変更・レビューするとき
- Codex CLI の sandbox、承認設定、モデル、reasoning effort、Structured Output、ログ保存方法を確認するとき
- Codex CLI の quota 枯渇、レートリミット、サーバー一時障害などの失敗時処理を確認するとき

## Do not read this when
- Codex CLI 呼び出しやその周辺仕様を扱わず、別の機能領域だけを調査するとき
- AgentCallParameter builder の具体的な個別設定値だけを確認する場合は、対応する builder の正本仕様を直接読むとき

## hash
- a38c37009467d95f2fe561bcdeae11572051847b304d1f4e0fca74a1a9217463

# `console_and_file_log.md`

## Summary
- コンソール表示とサブコマンド実行ログの出し方を定める正本断片です。時間表記、パス表記、サブコマンドログの保存先と必須イベント、コンソールの見出し付き出力、完了時サマリーの要件を確認したいときに読む対象です。

## Read this when
- 時間表示やパス表示の見え方を合わせたいとき。
- サブコマンド実行中の記録をどこに、どの粒度で残すかを決めたいとき。
- コンソールに出す進行通知や完了サマリーの内容を実装・修正したいとき。

## Do not read this when
- CLI の引数設計やサブコマンド分割そのものを決めたいときは、より上位のコマンド仕様を先に読むべきです。
- ログの内部保存形式やイベント項目の細部が既に確定していて、表示・保存ルールを変更しない作業なら、ここを読む必要はありません。

## hash
- eb26e061fe01f68d53bfb90f687d37fa59850c633b0887fe776704f5d901f267

# `doctor_preprocess.md`

## Summary
- `doctor preprocess` の責務を読む入口。`cmoc` の実行前に共通で行う事前検証と修復、特に ignore 状態・初期ディレクトリ準備・追跡対象の保証・必要時のコミットという流れを確認したいときに進む。

## Read this when
- `cmoc` の起動前に共通前処理として何を保証するか知りたいとき。
- `.cmoc/gu` を追跡対象外にする、`.agents` を追跡対象として用意する、`.cmoc/gt/ar/config.json` を追跡対象にする、のいずれかの要件を確認したいとき。
- 修復可能ならその場で直し、困難ならエラー終了する条件を確認したいとき。

## Do not read this when
- 個別サブコマンド固有の事前条件を確認したいとき。まず `doctor preprocess` 後に読むべき対象を探す。
- `cmoc managed ollama` の可用性保証の詳細だけを知りたいとき。そこから先は専用の仕様断片を読む。
- 既存の `INDEX.md` エントリー一覧やルーティング全体を把握したいだけのとき。

## hash
- 456a872269e84de215902aa521fb1f4095a8a7af7366b23fba5692d0accff503

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

# `prompt_standard.md`

## Summary
- cmoc が agent call に渡すプロンプトの共通規範を定める。Markdown 方言、`{{...}}` プレースホルダ、`<cmoc_block>` / `<cmoc_ref>` の参照記法、構築時の整合性検査、自然言語部分の言語方針を確認したいときに読む。プロンプトの動的構築や参照整合性の実装方針を決める入口であり、個別サブコマンド仕様ではなくプロンプト基盤の約束事を読む対象。

## Read this when
- agent call 用プロンプトの生成・レンダリング・検査ルールを決めたいとき。
- プロンプト中の参照ブロックやプレースホルダの表記を統一したいとき。
- プロンプト本文の言語方針や、oracle src で構築された内容をそのまま使うべきかを確認したいとき。

## Do not read this when
- 個別コマンドの入出力や振る舞いを確認したいとき。
- プロンプト基盤ではなく、CLI 仕様・エラー処理・セッション管理など別の app spec を見たいとき。
- `build_*_parameter` の実装詳細そのものや、構築済みプロンプトの具体的な文面だけを確認したいとき。

## hash
- 2c29e51d5d2ffd5edb8fc0759db046a91d6ec2dfcded91e0d7ae8bc5d703ce59

# `run_isolation.md`

## Summary
- cmoc サブコマンドごとの run を、人間の操作や他の run と衝突しないよう git branch と worktree で隔離する規則を定義する。run 開始時の branch 作成、作業 worktree、完了後のマージ規則、および run-root 外への書き込み例外を確認するための仕様入口。

## Read this when
- サブコマンド実行時の run、branch、worktree の作成・checkout・マージ規則を確認するとき
- run-root と repo-root のアクセス範囲や、.cmoc への書き込み例外を確認するとき

## Do not read this when
- 個別サブコマンドの具体的な実装や、branch 名・worktree 名の確定値だけを確認したいとき
- run の隔離と無関係なアプリケーション仕様を調べるとき

## hash
- d5d7b420980d6f635e03a1a6384bd040e76679e5a8fab777e87c365f16b2ba61

# `session_state.md`

## Summary
- cmoc の fork/join で共有するセッション状態の永続化仕様を確認したいときに読む。どの情報を状態として残し、どの値をその場で解決する前提かを判断する入口であり、個々のコマンド実装や保存先の細部を追う前にここを確認する。

## Read this when
- session の状態遷移や、apply と session の整合を保つために永続化すべき値を決めたいとき。
- fork 後にどの branch / commit を session 側に記録するか、join 後にどの参照 commit を更新するかを確認したいとき。
- 状態ファイルに何を保持し、何を保持しないかの境界を知りたいとき。

## Do not read this when
- cmoc のコマンド一覧や使い方を知りたいだけのときは、より上位の usage 仕様を読む。
- fork/join の具体的な実行手順やエラー処理の詳細だけを追いたいときは、各サブコマンドや error_handling の仕様を先に読む。
- 状態保存の場所だけを確認したいときは、ここではなく保存先や branch model を扱う文書を読む。

## hash
- c26d92ba2c2bbdc16a14881700c67a47096e38f93287cfd2bb3cc6a941d90144

# `sub_command`

## Summary
- cmoc のサブコマンド仕様をまとめた正本文書群。apply、session、doctor、indexing、oracle review、TUI などの実行条件・状態遷移・後処理・責務境界を確認する入口であり、個別サブコマンドの仕様調査時に対象文書へ進む。

## Read this when
- cmoc のサブコマンドの実装・変更・検証で、実行条件、状態遷移、終了処理、cleanup、merge、レビュー、TUI 起動フローの正本仕様を確認するとき。
- apply または session の fork、join、abandon の処理境界や相互の前提条件を調べるとき。
- サブコマンド入口の仕様と、個別処理・agent call の詳細仕様を切り分けて読む対象を選ぶとき。

## Do not read this when
- サブコマンドに共通する開発環境・設計・テスト規則を確認したいとき。
- 個別サブコマンド内部の realization 実装や、run isolation・parameter などの詳細正本だけを調べたいときは、対応するより直接の文書を読む。
- 一般的な git 操作や CLI 設計を調べるだけで、cmoc サブコマンドの正本仕様が関係しないとき。

## hash
- e67ee954c143d861c9b55025ad11a775e7e66c088d97c7eed92e928a66100547

# `subcommand_interruption.md`

## Summary
- 長時間実行中の `cmoc apply fork` と `cmoc oracle review` における、Ctrl+C によるユーザー中断の正規動作を定義する仕様。中断受付後の処理停止、確定済み結果の保持、通常の完了処理、正常系としての扱い、再開不可の条件を扱う。中断可能サブコマンドの追加条件と、個別仕様での明記要件も定める。

## Read this when
- 中断可能なサブコマンドの Ctrl+C 対応や、ユーザー中断時の状態更新・レポート・終了ログの挙動を実装または検証するとき。
- ユーザー中断を正常系として扱うか、処理単位の確定・破棄や再開機能の要否を判断するとき。
- `cmoc apply fork` または `cmoc oracle review` の中断仕様を確認するとき。

## Do not read this when
- 中断処理ではなく、通常のサブコマンド固有の処理内容や Codex CLI 呼び出し規則だけを確認するときは、各サブコマンドの仕様を直接読む。
- 中断とは無関係な一般的なエラー処理、CLI 入力、レポート形式の詳細を確認するときは、それぞれの専用仕様を読む。
- 中断済み run の途中位置からの再開機能だけを調べるときは、再開や run 管理を直接定義する対象を読む。

## hash
- 1543ca6f7dd0c898ccf9c84db8bd3a65ae7aac0ea134afce8f174d0ebd873e17

# `usage.md`

## Summary
- cmoc のエンドユーザー向け利用手順を定義する文書。PATH 設定と初回準備、セッション fork、oracle の記述・レビュー・commit、apply fork/join、session join までの標準ワークフローを示す。cmoc の基本的な呼び出し方と、各ブランチ・スナップショットの役割を確認する入口となる。

## Read this when
- cmoc の初回セットアップ方法を確認するとき
- session fork から oracle の反映、セッション終了までの標準手順を確認するとき
- cmoc の各コマンドを実行する順序やブランチ運用を確認するとき

## Do not read this when
- cmoc の内部実装やコマンド仕様の詳細を調査するとき
- oracle の設計原則や開発環境・テスト規則を確認するとき
- 特定の apply 処理やセッション処理の実装を変更するとき

## hash
- 110f1757462ca73f72f5111eb4164464c38fb14990a4f9429e5801a87235316d
