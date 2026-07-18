# `cli_auto_completion.md`

## Summary
- `_CMOC_COMPLETE` が存在する呼び出しを通常実行と区別し、自動補完プローブとして扱うための CLI 規則を定義する。補完処理より前に通常実行向けの前処理・検査・副作用を行わないこと、および補完に不要な stdout/stderr 出力を混在させないことを定める。

## Read this when
- CLI の自動補完、`_CMOC_COMPLETE` 環境変数、補完プローブと通常実行の処理分岐を変更・レビューするとき。
- 自動補完時の副作用、実行前検査、ログ・INDEX 更新、エラー出力、標準出力または標準エラー出力の扱いを確認するとき。

## Do not read this when
- 通常のサブコマンド実行や、自動補完と無関係な CLI 処理だけを変更・調査するとき。
- 自動補完の具体的な CLI ライブラリ実装を直接確認する必要があり、この規則の適用判断を要しないとき。

## hash
- 9633af8d389e9b14415c7904f464d7269ed51e6117204d2904e894ac491c02b2

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
- cmoc から `codex exec` を呼び出す際の正本規約。CODEX_HOME の解決と preflight、argv による設定上書き、sandbox・権限・モデル指定、stdin 経由のプロンプト渡し、ログ・Structured Output・並列数・失敗時リトライを定める。Codex CLI 呼び出し実装やその設定を変更・検証する際の入口となる。

## Read this when
- cmoc の Codex CLI 呼び出し、AgentCallParameter の設定反映、sandbox や CODEX_HOME の扱いを変更・確認するとき
- Codex CLI のログ保存、Structured Output、リトライ、quota・一時障害時の復旧動作を確認するとき

## Do not read this when
- Codex CLI 呼び出しや cmoc の実行規約に関係しない機能を変更・調査するとき
- AgentCallParameter builder の具体的な設定値や実装責務を確認する場合は、先に指定された oracle/src/oracle/acp_builder ツリーを直接読むとき

## hash
- e7c51f221739cd9ea62c33fb53d84ced387b5a21e57b7235b9de41328841f242

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
- cmoc の各サブコマンド実行前に、リポジトリの追跡状態や managed ollama の利用可能性を検証し、可能な範囲で修復したうえで、発生した差分を git commit する共通前処理を定義する。修復困難な場合のエラー終了条件と、各対象の検証・修復手順を扱う。

## Read this when
- cmoc のサブコマンド共通の事前検証・修復処理を変更または調査するとき
- `.cmoc/gu`、`.agents`、設定ファイル、refactor state の git 追跡状態や修復条件を確認するとき
- doctor preprocess の失敗条件、state JSON の妥当性、managed ollama の利用可能性を確認するとき

## Do not read this when
- 個別サブコマンド固有の事前条件や本命処理だけを変更・調査するとき
- doctor preprocess と無関係な git 管理、refactor state 仕様、managed ollama の詳細仕様を確認するときは、それぞれ参照先の仕様を直接読む

## hash
- a8b8e2b8086a3aa33c0dd7c16f92036e68119f2721a99e23fc5ddb93f0ef8a66

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
- cmoc サブコマンドの run を git branch と worktree で隔離する規則を定義する仕様文書。run の前提、ブランチ作成・マージ、worktree checkout、run-root 外への書き込み例外を扱い、サブコマンド実行環境の構成や書き込み先を判断する入口となる。

## Read this when
- cmoc サブコマンド実行時の run、branch、worktree の関係を確認するとき
- run 作業の開始時点、作業場所、ブランチ作成またはマージ規則を確認するとき
- run-root 外へのファイル書き込みが許可される例外を確認するとき

## Do not read this when
- サブコマンド実行環境の隔離以外の仕様を確認したいとき
- 個別サブコマンドの具体的な処理内容や、隔離後の作業そのものの仕様だけを確認したいとき

## hash
- 40d9fd3dc022d579a5d853584035e8e5be6bd0dda79038b7140407d60ede811c

# `session_state.md`

## Summary
- cmoc workflow における session と realization run の fork・join・abandon を管理する永続 JSON state の正本仕様。session 状態、run 状態、branch、commit、oracle snapshot の意味と状態遷移を定義する。

## Read this when
- session state の JSON スキーマ、各フィールドの初期値・更新条件・意味を確認するとき
- realization apply/refactor の fork、join、abandon、状態遷移の仕様を確認するとき

## Do not read this when
- session や realization run の具体的な CLI 実装を調査するとき
- git branch・merge 操作の一般的な実装詳細や、他の状態ファイルの仕様だけを確認するとき

## hash
- 36ef0e4821b2f17605da7fdd957a8c8b2b1813ed3a40058b72076a3dd14b9f3c

# `sub_command`

## Summary
- cmoc の主要サブコマンド仕様をまとめた oracle doc ディレクトリ。doctor・indexing・oracle 操作・realization run・session 管理・tui の実行条件、処理フロー、状態遷移、エラー処理、Codex CLI 起動規則への入口を提供する。

## Read this when
- cmoc のサブコマンドの実装、仕様確認、テスト、エラー処理を行うとき。
- doctor、indexing、oracle、realization、session、tui のいずれかの実行条件や処理フローを確認するとき。
- realization apply/refactor や session の fork・join・abandon における共通状態管理・cleanup・report の仕様を確認するとき。

## Do not read this when
- 特定サブコマンドの内部処理、入力エディタ、Codex CLI 起動パラメータなど、本文で参照されるより具体的な正本仕様だけを確認したいとき。
- インデクシングそのもの、oracle file の内容、realization file の網羅的な追従方針など、各サブコマンドが委譲する詳細仕様だけを調べるとき。
- サブコマンドと無関係な共通開発環境や一般的な git 運用を確認したいとき。

## hash
- c6b03259281e69e654fdb742ce820a1d0bef42dc3b8095844a184444547dd576

# `subcommand_interruption.md`

## Summary
- 中断可能なサブコマンドにおける Ctrl+C のユーザー中断処理を定義する仕様。対象サブコマンド、共通の完了・状態更新・レポート・終了ログの扱い、および再開可否を確認するための入口。

## Read this when
- 中断可能なサブコマンドへの追加・変更を検討するとき
- Ctrl+C による中断、部分結果の確定、正常系完了、終了ログやレポートの扱いを実装・確認するとき
- 中断後の再開や checkpoint 保存の要否を判断するとき

## Do not read this when
- 中断処理を含まないサブコマンドの通常動作だけを変更・確認するとき
- 個別サブコマンドの詳細な処理仕様や Codex CLI 呼び出し規則を確認したいときは、対応する個別仕様や codex 実行規則を直接読む

## hash
- cddbcb965d0e7dc98587ee8398df96bd0b60a62c8a5b6cf3149aefc73ee3d907

# `usage.md`

## Summary
- cmoc のエンドユーザー向け利用方法を定義する文書。初回 doctor 実行、session fork から oracle 変更・review・commit・realization apply/refactor、session join までの標準 workflow と、apply/refactor の使い分けを案内する。

## Read this when
- cmoc の初回セットアップ方法を確認するとき
- cmoc session、oracle、realization の標準的な作業手順を確認するとき
- realization apply と realization refactor の使い分けを判断するとき

## Do not read this when
- cmoc の内部実装や責務境界を調査するとき
- oracle file の具体的な仕様や realization code の実装詳細を確認するとき

## hash
- aaefa10a40b003b249441da59877f82058794fb27cbcf6d93dcc477c616627da
