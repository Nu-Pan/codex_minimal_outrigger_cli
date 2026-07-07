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
- Codex CLI による apply ループを実行するサブコマンドの正本仕様断片。セッション状態・git 差分・隔離作業ツリーを前提に、調査対象ファイルの選定、所見列挙、修正依頼、自動コミット、状態遷移、作業レポート生成までの責務境界を定める。

## Read this when
- apply ループを実行するサブコマンドの CLI 引数、事前条件、終了状態、終了コードを確認したいとき。
- セッション状態ファイルの apply セクションをいつ running、completed、error に遷移させるか確認したいとき。
- rolling、session、full の各スコープで調査待ちファイルリストをどう初期化するか確認したいとき。
- 所見列挙、所見反映、変更要約の agent call をどのタイミングで呼び、結果を調査待ちリストやコミットへどう反映するか確認したいとき。
- apply 作業レポートの保存先、Front Matter、本文に含める内容、標準出力へ流す値を実装またはテストしたいとき。

## Do not read this when
- run の隔離実行そのものの詳細仕様を確認したいときは、隔離実行の仕様を直接読む。
- agent call パラメータの詳細なプロンプトや Structured Output を確認したいときは、対応するパラメータ生成仕様を直接読む。
- apply 以外のサブコマンドの引数、状態遷移、レポート仕様を調べたいときは、そのサブコマンドの仕様へ進む。
- oracle file、realization file、パスプレースホルダの一般定義だけを確認したいときは、用語やパスモデルの仕様を読む。

## hash
- ed0ad23eb49a444f0b0bffd7b03ed03353a215afa9096aaf8d518725533d633e

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
- `cmoc review oracle` の正本仕様断片。現在の oracle file のスナップショットを対象に、致命的または軽微な問題の所見を agent call で列挙・マージ・検証・判定し、人間向けの Markdown レポートとして保存・提示するサブコマンドの責務、前提条件、実行手順、ループ制御、レポート形式を定める。

## Read this when
- oracle file をレビューするサブコマンドの挙動、責務境界、対象範囲、またはスコープ指定を確認したいとき。
- レビュー所見の列挙、マージ、検証、採用判定に関わる agent call の呼び出し順序や反復条件を確認したいとき。
- レビュー対象となる oracle file の選び方、ダーティーフラグ、ループ回数上限、隔離実行の扱いを確認したいとき。
- レビュー結果として保存・標準出力へ提示される Markdown レポートの構成、frontmatter、本文セクション、所見表示順を実装またはテストしたいとき。

## Do not read this when
- oracle file の内容そのものを修正する作業で、レビューサブコマンドの挙動を確認する必要がないとき。
- 実装ファイルや生成物を交えた総合レビュー、または過去の oracle file の変更履歴レビューを扱うとき。
- 個別 agent call のプロンプトやパラメータ構造だけを確認したいときは、対応する builder 定義を直接読む方が適切。
- run の隔離実行そのものの一般仕様を確認したいときは、隔離実行の仕様を直接読む方が適切。

## hash
- 305ad4b3715f3fc13c345e7ccff3c81a13daf2acf2c62a9c2669fc2782a09824

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
- 現在 checkout しているローカルブランチを session の分岐元兼 merge 先として扱い、そこから session 用 managed branch と local session 状態を作成するサブコマンドの正本仕様断片。
- 実行可能な checkout 状態、未コミット差分や既存 active session によるエラー条件、作成する branch と session 状態、標準出力に出す情報の境界を定める。
- 任意 start point、repository default branch の特別扱い、旧 branch 命名、旧サブコマンド互換を現行対象外として切り分ける。

## Read this when
- session を開始するサブコマンドの実装、CLI ルーティング、標準出力、状態ファイル作成、または git branch 作成処理を変更する。
- session 開始時に許可する checkout 状態、managed branch 上での実行可否、未コミット差分、active session 重複の扱いを確認する。
- session branch の命名、session id の生成、home branch と fork commit の保存内容、doctor preprocess の呼び出し有無を確認する。
- 旧 branch 形式や旧サブコマンド名への互換実装・テストを残してよいか判断する。

## Do not read this when
- session の merge、apply、終了、削除など、開始後の session 操作だけを扱う。
- path placeholder の意味、managed branch 全般の分類、または doctor preprocess 自体の詳細仕様を確認したい。
- INDEX.md エントリー生成規則や oracle file と realization file の責務境界を確認したい。

## hash
- 700e5f0b4083ac19c029f1aa024dbdd477552bc4e26f5b87e049889aa0437c5e

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
- ユーザーがエディタで入力したオリジナルプロンプトと cmoc 側の自動生成プロンプトを使って、AI Agent CLI/TUI を起動するサブコマンドの正本仕様断片。
- doctor preprocess、エディタ入力、agent call による起動パラメータ決定、TUI 起動までの実行順序と、Codex CLI 起動時に持ち込む規則の境界を扱う。

## Read this when
- 任意のプロンプトを cmoc の規則・規範の上で AI Agent CLI/TUI に渡す起動フローを確認・実装・テストする。
- ユーザー入力用エディタの選択順、待機条件、初期テンプレート、コメント除去と空白除去の扱いを確認する。
- TUI 起動前に agent call へ委ねるパラメータと、固定する model class・reasoning effort の境界を確認する。
- Codex CLI を TUI として起動する場合のコマンド種別や、既存の Codex 実行規則から持ち込む要素を確認する。

## Do not read this when
- doctor preprocess 自体の詳細仕様だけを確認したい。
- agent call に渡すパラメータ構造の詳細だけを確認したい。
- TUI 起動パラメータの構造や出力形式の詳細だけを確認したい。
- Codex 実行規則全般、環境変数、preflight validation、profile の詳細だけを確認したい。

## hash
- ede49ccc7f4139b7099aa7726ed5dfc93c7ca3077e0404f3bd330b9c4bbfdc2f
