# `apply_abandon.md`

## Summary
- `cmoc apply abandon` の正本仕様断片。現在の session に紐づく未 join の active apply run を、Codex CLI を呼ばず機械的に破棄し、apply 状態を `ready` に戻す cleanup コマンドの挙動を定義する。
- 破棄対象と保護対象、事前条件、状態遷移、cleanup 失敗時の扱い、stdout report、終了コードを扱う。

## Read this when
- 未 join の apply run を破棄する処理を実装・修正・検証するとき。
- apply worktree、apply branch、session state の cleanup 境界を確認するとき。
- `running`、`completed`、`error` の apply 状態から `ready` へ戻す状態遷移を扱うとき。
- apply abandon の stdout 表示内容、warning、終了コードを確認するとき。

## Do not read this when
- apply 成果物を session branch へ取り込む処理を扱うときは、join 側の仕様を読む。
- apply run を開始・実行する処理を扱うときは、run 側の仕様を読む。
- join 済み結果の rollback 仕様を探しているとき。この対象は rollback コマンドを定義しない。
- oracle 改訂内容や session branch の commit を変更する処理を扱うとき。この対象ではそれらを保護対象として扱う。

## hash
- d8cc18d3e8ed2a18a61d9ea5261d5cc9a7c50571eb6879746501b3ee0190eaa4

# `apply_fork.md`

## Summary
- `cmoc apply fork` の実行責務と境界を定める正本仕様断片。事前条件、`--scope` の初期調査対象、apply ループの流れ、状態遷移、レポート出力までを確認したいときに読む。

## Read this when
- `cmoc apply fork` の挙動や終了条件を実装・修正したいとき。
- apply 対象ファイルの初期化条件、重複除去、再調査の扱いを確認したいとき。
- セッション状態ファイルの `apply` 状態遷移や、作業レポートの保存・出力要件を確認したいとき。

## Do not read this when
- `run` の隔離実行そのものの詳細だけを知りたいときは、参照先の `run_isolation` の仕様断片を読む。
- `build_apply_fork_file_finding_enumeration_parameter` や `build_apply_fork_finding_application_parameter` の入出力の詳細だけを確認したいときは、それぞれの正本仕様断片を読む。
- `cmoc apply fork` 以外のサブコマンドの一般仕様を探しているとき。

## hash
- 4b83469f170f1c66c5ebd6079c936da72d4e14ffc7e62d31d94ab622fe525306

# `apply_join.md`

## Summary
- `apply fork` の成果物をセッション本流へ取り込む `cmoc apply join` の正本仕様断片。事前条件、通常モードと `--force-resolve` の差分処理、merge conflict の扱い、状態更新、使用済み apply branch/worktree の削除条件を定義する。

## Read this when
- `cmoc apply join` の CLI 引数、実行順序、終了条件、レポート内容、状態遷移を確認または実装する。
- apply 実行中に発生した想定外の差分を、通常モードでは中止、強制モードでは revert する境界を確認する。
- `INDEX.md` の merge conflict 自動解決、または自動解決対象外 conflict の報告方針を確認する。
- apply 完了後に apply branch/worktree を削除してよい条件を確認する。

## Do not read this when
- `apply join` 以外の apply 系サブコマンドの起動、実行、状態作成を確認したい。
- path placeholder、branch 名、session state file などの用語定義そのものを確認したい。
- 実装ファイルの責務分割、内部 helper、git コマンド実行 wrapper の詳細だけを確認したい。

## hash
- e8e8a871e1b6833cd1b3d74a7bcaa03f4bf162fc355e453dafa3e2361a7f24de

# `doctor.md`

## Summary
- cmoc の実行可能性を検証し、可能な範囲で修復するために doctor preprocess を明示実行するサブコマンド仕様。引数を取らず、固有の事前条件も持たない単純な起動口として位置づけられる。

## Read this when
- 利用者が明示的にリポジトリ状態の検証・修復を起動するサブコマンドの挙動を確認したいとき。
- doctor preprocess を CLI から呼び出す入口の引数、事前条件、実行手順を確認したいとき。
- 引数なしで実行される診断系サブコマンドの仕様に合わせて実装やテストを書くとき。

## Do not read this when
- doctor preprocess 自体が何を検証・修復するかを詳しく確認したいとき。
- 通常のコマンド実行時に暗黙で行われる前処理の適用条件や順序を確認したいとき。
- リポジトリパスや作業ルートなどのパス概念そのものを確認したいとき。

## hash
- 7e91b86ad01bbeb36bc4e965ac92b894e817234344a580d86fb46694185d690f

# `indexing.md`

## Summary
- 現在の作業ツリーに対してインデクシングを実行するサブコマンドの仕様断片。引数を取らず、未コミット差分がある場合はエラー終了し、doctor preprocess、明示的なインデクシング、発生差分の git commit を順に行う。

## Read this when
- インデクシング実行用サブコマンドの外部仕様、事前条件、実行順序を確認したいとき。
- インデクシング結果を自動的に git commit する挙動を実装またはテストするとき。
- 未コミット差分がある状態でのエラー終了条件を確認したいとき。

## Do not read this when
- インデクシングそのものの対象、生成内容、更新規則を確認したいとき。
- doctor preprocess の詳細な仕様や個別の処理内容を確認したいとき。
- 他のサブコマンドの引数、事前条件、実行手順を確認したいとき。

## hash
- a35701932f19171b593632055592a5d0a46367d438f2be544655e7001f8c413d

# `review_oracle.md`

## Summary
- `cmoc review oracle` のルーティング用エントリー。`oracle` 配下のスナップショットをレビューし、所見を集約して Markdown レポートを出すコマンドに進むための入口を示す。
- この対象は、`--scope` によるレビュー範囲、事前条件、所見の列挙・検証・判定の流れ、最終レポートの保存先を扱う。実装本体ではなく、レビューの責務境界と出力物の確認が必要なときに読む。

## Read this when
- `oracle` ツリーの内容に対するレビュー仕様、処理手順、出力レポート形式を確認したいとき。
- レビュー対象の範囲や前提条件、所見の集約順序、レポート保存先を知りたいとき。
- `cmoc review oracle` が何を責務とし、何を責務外とするかを確認したいとき。

## Do not read this when
- 実装ファイルや一般的なコマンド実行手順を知りたいだけのとき。
- 自動生成ファイルや別コマンドの仕様を探しているとき。
- 所見の個別内容そのものではなく、`oracle` 配下の別文書や実装詳細を直接読むべきとき。

## hash
- 026f8af4331413ebc3759bb25643694e8176d2b35e8862d0e8c6b917b445ab0f

# `session_abandon.md`

## Summary
- 現在の session branch を home branch に取り込まず破棄するサブコマンドの仕様。実行可能な状態、破棄してよい対象と破棄してはいけない対象、状態更新、失敗時の再実行可能性を定める。
- session の成果物を本流へ反映する join ではなく、管理下の active session を安全に abandon 状態へ移すための境界を示す。

## Read this when
- session を merge せず終了する挙動を実装または検証する。
- active session の破棄前検証、apply run が残っている場合の扱い、未コミット差分の拒否条件を確認する。
- session branch 削除、state file 更新、home branch への切り替え、abandoned 状態への遷移を扱う。
- クリーンアップ途中の失敗時に、ロールバックと再実行可能性をどう扱うか確認する。

## Do not read this when
- session の成果物を home branch へ取り込む完了処理を確認したい場合は、join の仕様を読む。
- join 済み結果を取り消す rollback 挙動を探している場合は、この対象ではない。
- apply run 自体の破棄方法を確認したい場合は、apply abandon の仕様を読む。
- session を新規作成する fork の条件や挙動だけを確認したい場合は、fork の仕様を読む。

## hash
- 170436dbc12899d7540fccb0c26d04f0663f5a359fc7865c77c8e7f82577c8ba

# `session_fork.md`

## Summary
- `cmoc session fork` を読むべき条件を、現在のローカルブランチから session 用ブランチを新規作成する処理、事前条件の検証、session 状態保存、旧 `cmoc branch` / `cmoc_<time-stamp>` 系の非互換方針に絞って案内する。
- この文書は、分岐元を変えたい場合の start point 指定ではなく、既に目的のローカルブランチへ移動したうえで fork する流れを確認したいときに読む。
- `doctor preprocess` の呼び出し、active な session の重複禁止、作成ブランチ名と home branch 名の出力仕様を確認したいときの入口に置く。

## Read this when
- 現在 checkout しているローカルブランチを起点に `cmoc session fork` がどう session ブランチを作るか確認したいとき。
- 実行前の失敗条件として、detached HEAD、remote-tracking branch や commit hash からの実行、`cmoc/session/...` や `cmoc/apply/...` 上での実行、未コミット差分、既存 active session の有無を確認したいとき。
- session ID 生成、branch 作成と checkout、`/.cmoc/gu/ar/session/<session-id>.json` への状態保存、標準出力への表示内容を確認したいとき。
- 旧 `cmoc branch` や `cmoc_<time-stamp>` 形式を実装・テストから排除すべきか判断したいとき。

## Do not read this when
- 任意の start point を受け取る fork 挙動を確認したいときは、この文書ではなく、start point を扱う別の仕様を読むべき。
- session の開始後にどう join するか、あるいは abandon するかを確認したいときは、この文書ではなく該当する別のサブコマンド仕様を読むべき。
- branch 命名以外の session 状態全般や CLI 共通規則だけを確認したいときは、より上位の一般仕様を読むべき。
- 旧 `cmoc branch` への後方互換を前提にした実装を探したいときは、この文書ではなく、非互換方針を含む他の仕様を確認すべき。

## hash
- dc02c6bd4c55ff5d696db81813820583de05785e5a19c854e03c41bab2e9ff71

# `session_join.md`

## Summary
- session を完了し、現在の session branch を session home branch に merge して join 済み状態へ遷移させるコマンド仕様。
- 引数なしで動作し、state file・branch 状態・未コミット差分・apply ready 状態などの事前条件、merge 手順、conflict 解消 agent call、後始末、managed branch 削除条件を定める。
- legacy 名の互換維持を不要とし、旧名の実装・テスト痕跡を残さない境界も扱う。

## Read this when
- session 完了時に session branch を home branch へ取り込むコマンドの挙動を確認・実装・テストする。
- join 実行前の state file 条件、active/ready 判定、home branch 特定、未コミット差分の扱いを確認する。
- home branch が session 作成後に進んだ場合の merge 基準や conflict 発生時の扱いを確認する。
- merge conflict 発生時に conflict 対象列挙、agent call、marker 検査、git add、unmerged path 検査、merge commit 作成の流れを扱う。
- conflict 解消時だけ oracle file 編集禁止や差分検査の規則を例外扱いする必要がある。
- join 後に session state を joined にする処理や、session branch を安全確認できる場合だけ削除する処理を扱う。
- 旧名コマンドの後方互換性を残すべきか、または既存の旧名実装・テストを削除すべきか判断する。

## Do not read this when
- 通常の git branch 同士を任意に merge する汎用 wrapper の仕様を探している。
- repository default branch を特別扱いする処理の仕様を探している。
- session の作成、apply ready へ至る処理、state file の一般的な形式など、join 実行前の別フェーズを主に扱う。
- conflict 解消 agent call の詳細な parameter 構築仕様そのものを確認したい場合は、その正本定義を直接読む。
- legacy 名の互換実装を新たに追加する目的で読もうとしている。

## hash
- 6c1ed51eb5eea52942ca8984857198e485152c992c65aeed3301afc2d7f528cc

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの起動経路を扱う。ユーザーのオリジナルプロンプトをエディタ入力で受け取り、agent call で必要パラメータを決め、AI Agent CLI/TUI を起動する流れを確認したいときに読む。
- この対象は、入力エディタの起動順序と初期テンプレート、入力読み出し時の整形、TUI 起動時に参照すべき正本仕様、Codex CLI 起動時に持ち込む追加要素を定める。
- 実装の内部分割や agent call の詳細、TUI 起動パラメータの細部はここでは追わず、対応する正本仕様へ進む。

## Read this when
- `cmoc tui` の全体フロー、特に入力取得から TUI 起動までの接続を確認したいとき。
- ユーザー入力用エディタの選定順、初期プロンプト雛形、読み出し時の整形条件を確認したいとき。
- Codex CLI バックエンドで起動するときの追加条件や持ち込み要素を確認したいとき。

## Do not read this when
- agent call のパラメータ解決の個別仕様だけを見たいときは、そちらの正本仕様を直接読む。
- TUI 起動パラメータの詳細だけを確認したいときは、起動パラメータの正本仕様を直接読む。
- エディタ起動やプロンプト入力を伴わない別サブコマンドの流れを見たいとき。

## hash
- d150cc09cab57f12ffc1074eec9e261fc79875b029efe97e01c5d7d9b48d9f6a
