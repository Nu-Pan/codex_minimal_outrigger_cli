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
- cmoc が `cmoc` provider 用の Ollama サービスを準備・検証・再利用する必要があるときに読む。サービス管理、永続化資源、GPU 推論の成立確認、Codex CLI への接続条件が主題で、モデル利用だけを扱う実装や一般的な CLI 入口より直接的である。
- 本番実行とテストで共通の `cmoc managed ollama` をどう維持するかを確認したいときに読む。終了処理で停止や削除をしないこと、既存資源を再利用すること、必要時のみ新規構築・修復することが判断材料になる。
- `CodexModelSpec.model_provider=="cmoc"` の前提で、agent call 開始前に満たすべき利用可能性条件を確認したいときに読む。GPU 推論の確認、127.0.0.1:11434 の提供元確認、モデル要求一致、リクエスト疎通の修復方針が必要になる場合に進む。

## Read this when
- cmoc がローカル SLM を `cmoc managed ollama` で提供する構成を扱うとき。
- doctor preprocess でサービスの利用可能性を保証する処理を実装・修正するとき。
- Ollama の取得、配置、モデル pull、永続資源の扱い、GPU 推論の検証条件を確認するとき。
- Codex CLI へ渡す `cmoc managed ollama` 用の provider 設定や実行引数を調整するとき。

## Do not read this when
- 単に cmoc の他のサブコマンドや一般的な設定項目を扱うだけで、Ollama サービスや `cmoc` provider を使わないとき。
- サービス起動の内部手順ではなく、別のモデル provider や別の実行基盤の仕様を探しているとき。
- `--profile` や組み込み provider ID の一般的な使い方だけを知りたいときで、`cmoc managed ollama` 固有の制約が不要なとき。

## hash
- 229d722c09503b9b563c54a23ee8e4a850d5e057b76739987c78848a3acb3c56

# `codex_exec_rule.md`

## Summary
- `codex exec` を cmoc から呼び出すときの引数・環境変数・事前検証・ログ保存・Structured Output の扱いを決めるルールを読むための入口。実際に `codex exec` の起動方法や出力保存方法を実装・変更するときに読む。
- ファイルアクセス制限やモデル設定、プロンプト本文の渡し方、失敗時の再試行や待機の条件を確認したいときに読む。個別の builder 実装や呼び出し処理の調整は、その仕様の根拠としてここを見る。

## Read this when
- cmoc から Codex CLI を起動する処理を追加・変更するとき
- `CODEX_HOME` の解決、preflight validation、`--model` や `--config` による上書き、`--json` や `--output-last-message` の保存先を扱うとき
- プロンプトを stdin で渡す方法、Structured Output の schema 保存、失敗時の再実行や quota 待機の扱いを確認したいとき

## Do not read this when
- `codex exec` 以外の cmoc 実装や一般的な CLI 仕様だけを見たいとき
- ファイル分類としての oracle / realization の境界だけを確認したいとき。これは別の oracle で扱う
- Codex CLI の個別 parameter builder の詳細実装だけを追いたいとき。まずはここで方針を確認し、必要なら正本側の builder 定義へ進む

## hash
- eb7b8c3503c2eadeae5ce0fdcd3010170b2aea7e1759f003f025810508076b60

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
- cmoc の各サブコマンド起動前に共通で走る事前検証と修復、特に `.cmoc/gu` の追跡除外、`.agents` と `.cmoc/gt/ar/config.json` の追跡保証、必要時の cmoc managed ollama 準備、そして失敗時の即時終了方針を定める。

## Read this when
- サブコマンド本体より前に実行される共通の検証・修復の責務を確認したいとき。
- `.cmoc/gu` の ignore 化、`.agents` の追跡可能化、`.cmoc/gt/ar/config.json` の追跡保証のどれかを実装・修正するとき。
- cmoc managed ollama を doctor preprocess から使う条件や前提を確認したいとき。

## Do not read this when
- 個別サブコマンド固有の事前条件や本命処理を確認したいときは、各サブコマンドの仕様を読む。
- cmoc managed ollama の具体的な扱いだけを確認したいときは、`cmoc_managed_ollama.md` を直接読む。
- 共通の入出力やエラー体系だけを確認したいときは、より一般的な app_spec の別文書を読む。

## hash
- adfd851d3fe719b82990d8e00020d3b5d36be4f1304fe71acb8c7a0c5d924b62

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
- `cmoc apply abandon` の正本仕様断片。未 join の apply run を破棄し、apply 側の cleanup と session state の復帰を扱う入口。
- `cmoc apply fork` の成果物を取り消したいとき、または session 破棄前に active / completed / error の apply run を先に片付けたいときに読む。
- 破棄ではなく merge をしたい場合や、session 本体の破棄・apply 実行ループ・join 側後処理を扱いたい場合は別の対象を読む。

## Read this when
- 現在の session に紐づく未 join の apply run を破棄する挙動を実装・確認するとき。
- `{{cmoc-apply-branch}}` と `{{cmoc-apply-worktree}}` を削除する正規手順と、その前提条件・警告・終了コードを確認したいとき。
- `cmoc apply fork` の結果を取り消したいが、`cmoc apply join` は行わず、session 本体は維持したいとき。
- `cmoc session abandon` の前に、残っている apply run を先に片付ける必要があるか確認したいとき。

## Do not read this when
- apply 成果物を `{{cmoc-session-branch}}` に取り込む処理を知りたいときは `cmoc apply join` を読む。
- session 自体を破棄したいときは `cmoc session abandon` を読む。
- apply の実行や探索、差分反映のループを知りたいときは `cmoc apply fork` を読む。
- report 保存や merge 後のブランチ削除など、join 側の後処理を知りたいときは `cmoc apply join` を読む。

## hash
- 388262110d7981d764e4e46050e6a297da39dbbc8eca9bd0e953be3630212fa9

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
