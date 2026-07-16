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
- cmoc がリポジトリ全体に対して前提として置く運用規則をまとめた案内。実装ファイルの列挙方法、作業時のカレントディレクトリ前提、タイムスタンプ形式、`cmoc-managed-branch` の解釈を確認したいときに読む。
- この文書は個別機能の仕様ではなく、cmoc が他の文書や実装を読む前に共有すべき共通前提を定義する。作業対象の範囲判定や、時刻・ブランチ・列挙ルールの解釈を揃える役割を持つ。

## Read this when
- リポジトリ全体をまたぐ cmoc の作業前提を確認したいとき。
- ファイル列挙、作業ディレクトリ、タイムスタンプ、ブランチ解釈の基準を揃えたいとき。
- 個別の実装や機能仕様ではなく、cmoc 共通の運用ルールを先に確認したいとき。

## Do not read this when
- 個別機能の入出力や挙動を知りたいときは、より直接の仕様文書を読む。
- 既に作業前提が確定していて、ファイル選定や時刻・ブランチ解釈の確認が不要なとき。
- `INDEX.md` のルーティング先として、より具体的な下位文書が明らかなとき。

## hash
- 71b43ecc5c13c5360c32cd86aa230e0b1570780c5ebf75bda47569998a58599a

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
- `cmoc` の各 run が、共有される `{{repo-root}}` と衝突しないように、実行中の作業場所と変更の記録先をどう分けるかを扱う。branch と worktree の両方の隔離規則、そして例外的に `{{repo-root}}` 側へ書き込む条件が必要なときに読む。
- サブコマンドごとの run 開始時の作業環境作成、run 中の作業先の固定、完了後の session への反映方法を決めるときの入口にする。

## Read this when
- run をどのブランチと worktree で実行すべきかを判断したい。
- run の開始・実行中・完了後で、どの作業場所に何を書いてよいかを確認したい。
- 共有リポジトリと run 用作業領域の境界、または例外的に共有側へ書ける条件を確認したい。

## Do not read this when
- run の具体的なマージ手順や各サブコマンド固有の実装詳細を知りたいだけなら、より下位のサブコマンド仕様を読む。
- run の中で扱う個別のログや状態ファイルの内容仕様を知りたいだけなら、該当ファイルの仕様を直接読む。

## hash
- 32259835b5cceab7790965ad988769f48ca3b8844a41418d379f29edae1b3c71

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
- cmoc のサブコマンドごとの正本仕様断片をまとめたディレクトリ。apply、session、doctor、indexing、review、tui などの実行条件・状態遷移・入出力・失敗時挙動を扱い、各サブコマンド仕様への入口となる。

## Read this when
- cmoc の特定サブコマンドの実装・テスト・挙動を確認するとき。
- サブコマンドの引数、事前条件、状態遷移、終了処理、エラーや中断時の扱いを調べるとき。
- apply、session、doctor、indexing、review、tui のどの正本仕様を読むべきか選ぶとき。

## Do not read this when
- サブコマンド共通基盤、run isolation、agent call parameter などの共通仕様だけを調べるときは、それぞれの共通仕様を直接読む。
- 特定サブコマンドの仕様ではなく、INDEX.md の生成やルーティング情報だけを更新するとき。
- git、branch、state file など基礎概念の一般仕様だけを確認したいときは、対応する基礎仕様を直接読む。

## hash
- ef52981d6f947db52fd10ee8302e3d8353ccc9cadda8d42e7c560614fffbcdc4

# `subcommand_interruption.md`

## Summary
- 実行中の `cmoc` をユーザーが `Ctrl+C` で中断したときの扱いを定める仕様断片。中断を正常系として完了させる条件、確定済み結果の保持、終了ログやレポートで中断完了を判別できることを確認したいときに読む。
- `cmoc apply fork` と `cmoc review oracle` のような中断可能サブコマンドを追加・変更するときに読む。中断要求の受付、通常完了処理への引き継ぎ、再開なしの制約が論点になる。

## Read this when
- 実行中のサブコマンドに対する `Ctrl+C` をユーザー中断要求として扱う必要がある。
- 中断をエラーではなく正常完了として記録・出力したい。
- 中断後も確定済みの部分結果を残したまま終了処理を行う必要がある。
- 中断可能サブコマンドを新規追加する、または既存の中断挙動を変更する。

## Do not read this when
- 単純な通常終了や失敗終了の仕様だけを確認したい。
- `Ctrl+C` 以外の入力を中断として扱うかを決めたい。そこは未定義なので、この文書だけでは確定しない。
- 中断からの再開 checkpoint を設計したい。再開機能は提供しない。
- サブコマンド固有の処理内容や詳細なエラーハンドリングだけを確認したい。

## hash
- fe0f3e04336f5c5cf846558298ec39d78fdb650eae19bf49cd3cb3271190508a

# `usage.md`

## Summary
- cmoc の利用手順全体をまとめた入口。初回の準備、session fork / review oracle / apply fork / apply join / session join の流れを追いたいときに読む。

## Read this when
- cmoc をどう呼び出すか、作業開始から終了までの標準的な進め方を確認したいときに読む。
- どのサブコマンドをどの順で使うか、oracle の更新と実装追従の役割分担を確認したいときに読む。

## Do not read this when
- 特定のサブコマンドの詳細仕様や個別の制約を知りたいときは、そのサブコマンドの説明を直接読む。
- 実装やエラー処理、状態管理の細部を知りたいときは、この全体案内ではなく該当する機能別の文書を読む。

## hash
- fe7509350bf677016679ba49878e301fbc712e3375ea1ebbd876b1ffcd68f9eb
