# `apply_abandon.md`

## Summary
- 現在の session に紐づく未 join の apply run を、session 側の commit や oracle 改訂内容を保ったまま機械的に破棄するサブコマンド仕様。
- 破棄対象となる apply 用 branch/worktree、session state の更新、事前条件、許可される破棄範囲、失敗時の扱い、stdout に出す結果情報を定める。
- join 済み結果の rollback ではなく、active apply run の成果物を正規手順で捨てて apply.state を ready に戻す処理の入口となる。

## Read this when
- 未 join の apply run を破棄する CLI 挙動を実装・修正・テストする。
- apply.state が running、completed、error の状態から ready へ戻す状態遷移を確認する。
- apply 用 branch/worktree の強制削除、削除済み対象の warning 扱い、session 側 worktree の未コミット差分チェックを扱う。
- Codex CLI を呼ばない機械的 cleanup としての apply 破棄処理、または専用 markdown report を作らず stdout に結果を出す方針を確認する。

## Do not read this when
- apply 成果物を session 側へ取り込む join 処理の仕様を確認したい。
- join 済み結果を取り消す rollback 仕様を探している。
- 新しい apply run の開始、Codex CLI 呼び出し、AI による修正・整理・conflict 解消・report 作成の仕様を確認したい。
- session branch や session home branch の作成・管理など、apply run 破棄以外の session ライフサイクルを調べたい。

## hash
- 1d3d095e144d8770e47c629792206265fad1698d3e1db15313984de55c6946c3

# `apply_fork.md`

## Summary
- Codex CLI による apply ループを実行するサブコマンドの正本仕様断片。セッション状態・git 差分・scope に基づき調査対象を選び、所見列挙、修正依頼、コミット、状態遷移、作業レポート生成までの責務境界を定める。
- このサブコマンドは `<cmoc-session-branch>` と元の作業コピーを直接汚さず、apply 用ブランチと隔離 worktree 上でベストエフォートに実装品質と oracle 一致へ近づけるものとして扱う。

## Read this when
- apply ループの開始条件、終了条件、回数上限到達時の扱い、収束・未収束・エラーの区別を確認したいとき。
- rolling、session、full の各 scope が調査待ちファイルリストをどう初期化するかを実装またはテストしたいとき。
- 所見列挙 agent call、所見反映 agent call、変更要約 agent call の呼び出しタイミングや結果の扱いを確認したいとき。
- apply 実行中のセッション状態ファイル更新、apply 用ブランチへのコミット、作業レポート保存、標準出力、終了コードを扱うとき。
- run 隔離実行と組み合わせた apply 作業の責務境界を確認したいとき。

## Do not read this when
- run 隔離実行そのものの詳細仕様を確認したいだけの場合は、隔離実行の仕様を直接読む。
- 所見列挙、所見反映、変更要約の各 agent call parameter の詳細なプロンプトや Structured Output を確認したい場合は、それぞれの builder 定義を直接読む。
- apply 以外のサブコマンドの引数、状態遷移、レポート仕様を確認したい場合は、そのサブコマンドの仕様を読む。
- oracle file、realization file、パスプレースホルダなどの横断的な定義を確認したいだけの場合は、それらを定義する共通仕様を読む。

## hash
- 26e4695c1716e10fb02586d2898d41fc4fd74d87c98e9490ea22839d44033847

# `apply_join.md`

## Summary
- `cmoc apply join` が、fork された apply 処理の成果をセッション本流へ取り込むための正本仕様断片。セッションブランチと apply ブランチの事前条件、想定外差分の扱い、通常モードと強制モード、merge conflict の自動解決範囲、状態更新、使用済みブランチと worktree の削除条件を定める。
- apply 処理の成果物をセッション側へマージする制御フロー、失敗時の中断条件、`--force-resolve` による差分 revert 方針、`apply.state = error` でも join を継続できる境界を確認する入口となる。

## Read this when
- `cmoc apply join` の実装、テスト、CLI 挙動、状態遷移、またはレポート内容を扱うとき。
- apply ブランチからセッションブランチへの merge 手順、merge 前の checkout 順序、未コミット差分や想定外差分の検出・revert・報告方針を確認したいとき。
- `--force-resolve` の意味、通常モードで中断すべき条件、強制モードで処理を続行してよい条件を判断するとき。
- `INDEX.md` の merge conflict を自動解決してよい範囲や、それ以外の conflict をユーザー報告へ回す条件を確認するとき。
- join 完了後に session state を更新する条件、apply ブランチや apply worktree を削除してよい条件、削除できない場合の warning 扱いを確認するとき。

## Do not read this when
- apply 処理を開始して apply ブランチや worktree を作る側の仕様だけを確認したいとき。
- セッション作成、セッション終了、または apply 以外のサブコマンドの CLI 引数や状態遷移を調べたいとき。
- oracle file、realization file、パスモデルなど、cmoc 全体の基本概念や用語定義だけを確認したいとき。
- 実装ファイルやテストファイルの配置、コード構造、既存 helper の詳細を確認したいだけで、join の正本仕様を参照する必要がないとき。

## hash
- 8cd2425c6a8ae9b88c0fef539076160d9f8bf341bc5cb40a607960ebaceb9c85

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
- 現在の作業ルートに対してインデクシングを実行するサブコマンドの仕様断片。引数を取らないこと、未コミット差分がある場合のエラー終了、実行後に発生した差分を自動でコミットする流れを扱う。
- インデクシングそのものの詳細仕様ではなく、サブコマンドとしていつ何を実行し、どの前提条件を満たす必要があるかを確認する入口となる。

## Read this when
- 現在の作業ルートを対象にインデクシングを明示実行する CLI 挙動を確認・実装・テストする。
- インデクシング実行前に未コミット差分をどう扱うか、また実行後の差分を git commit するかを確認したい。
- このサブコマンドが引数を受け取るかどうか、また処理手順の外部挙動を確認したい。

## Do not read this when
- インデクシングで何を生成・更新するかという処理内容そのものを確認したい場合は、インデクシング全体の仕様を直接読む。
- 別のサブコマンドの引数、事前条件、実行手順を確認したい場合は、そのサブコマンドの仕様へ進む。
- git 操作一般、パスモデル、または実装内部の helper 分割方針だけを調べたい場合は、より直接その責務を持つ仕様または実装を読む。

## hash
- 56dd83624b22d9f2e9219cb4fc720d730f72ace8968376b51b9cb29b70d96cca

# `review_oracle.md`

## Summary
- `cmoc review oracle` サブコマンドの仕様。現在の oracle file を対象に致命的または軽微な所見を Codex CLI による複数段の列挙・マージ・検証・判定で抽出し、人間向け Markdown レポートとして保存してそのパスを出力する流れを定義している。
- セッション状態・ブランチ・未コミット差分に関する事前条件、`--scope` によるレビュー対象範囲、run 隔離実行、所見 ID とダーティフラグ管理、レポート frontmatter と本文構成を扱う。

## Read this when
- `cmoc review oracle` の CLI 引数、事前条件、終了時の出力、またはレポート保存先を確認したいとき。
- oracle file レビューの対象範囲を `session` と `full` でどう切り替えるか確認したいとき。
- 所見リストの列挙・マージ・検証・採用判定の制御フロー、ループ上限、ダーティフラグ更新規則を実装またはテストしたいとき。
- `cmoc review oracle` が何をレビュー対象に含め、何を責務外とするか確認したいとき。
- レビュー結果 Markdown の frontmatter、本文セクション、所見の表示順、`result` の判定を確認したいとき。

## Do not read this when
- 個別 agent call の prompt やパラメータ詳細だけを確認したいとき。対応する `build_review_oracle_*_parameter()` の定義を読む方が直接的。
- run 隔離実行そのものの汎用仕様を確認したいとき。run isolation の仕様を読む方が直接的。
- oracle file や realization file の一般定義、または oracle 標準全体を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドの引数、実行手順、レポート仕様を確認したいとき。

## hash
- 0dcdad4b5ac6720f32a78b727d3298a1566dbfb3d9c71f68edc9c8840cd6f43f

# `session_abandon.md`

## Summary
- 現在の session branch を home branch に取り込まず破棄するサブコマンドの正本仕様断片。join との違い、rollback ではないこと、手作業での branch 削除ではなく cmoc 管理下で破棄する位置づけを示す。
- 引数なしで実行され、実行可能な branch・state file・session/apply state・home branch・未コミット差分に関する事前条件を定める。
- 破棄してよい対象と破棄してはいけない対象、home branch への切り替え、session state の abandoned 更新、branch 強制削除、途中失敗時の rollback と再実行可能性を扱う。

## Read this when
- session を本流へ merge せず中止・破棄する挙動、実装、テスト、CLI 出力、状態更新を確認したいとき。
- session branch、session home branch、session state file、apply state、未コミット差分の検証条件を実装または検証したいとき。
- session abandon が削除してよいものと保持すべきものの境界を確認したいとき。
- abandoned になった session の扱い、active session からの除外、新しい session fork の可否を確認したいとき。
- 破棄処理の途中失敗時に rollback し、ユーザーへ手動解決と再実行を促すべき場面を扱うとき。

## Do not read this when
- session の成果物を home branch へ取り込んで完了する通常の join 処理を知りたいとき。
- join 済みの結果を取り消す rollback 機能を探しているとき。
- active、completed、error などの apply run 自体を破棄する手順を知りたいとき。
- session の作成、fork、report 保存、oracle 改訂や実装修正そのものの仕様を調べたいとき。

## hash
- 08b0fe9b67e7874161819b90a1c7a51022ba373a9076aa74a4864597a7b8c098

# `session_fork.md`

## Summary
- 現在のローカルブランチから session を開始するサブコマンドの正本仕様断片。分岐元・merge 先となる home branch、作成される session branch、保存される session 情報、標準出力、実行可能な checkout 状態、未コミット差分や既存 active session のエラー条件を扱う。
- repository default branch を特別扱いしないこと、任意 start point を受け取らないこと、旧 branch 形式や旧サブコマンドの互換実装を残さないことを明示する。

## Read this when
- 現在 checkout 中のローカルブランチから session branch を作成する処理、CLI 出力、session 情報保存、branch 命名、gitignore 対象の確保を実装・検証する。
- detached HEAD、remote tracking branch、commit hash、managed branch、未コミット差分、既存 active session がある場合のエラー終了条件を確認する。
- session home branch と session branch の関係、1 home branch あたり active session を高々 1 つにする制約を確認する。
- 旧 branch 形式や旧サブコマンド名への後方互換性を削除・禁止してよいか判断する。

## Do not read this when
- session の作成ではなく、既存 session の merge、apply、終了、一覧表示など別操作の仕様を確認したい。
- branch 作成の外部挙動ではなく、内部 helper の分割、実装上の関数名、テスト fixture の置き方だけを判断したい。
- path placeholder の一般定義、managed branch 全体の分類、session 情報ファイルの共通 schema など、この仕様断片で定義されていない横断概念を確認したい。

## hash
- 9ed112129e33d4ad4e9633f88c0188b43039369d51764e0dccb27ef660ea240b

# `session_join.md`

## Summary
- session を完了させるため、現在の session branch を対応する home branch へ merge して joined 状態へ移行するサブコマンドの仕様断片。
- 引数を受け取らないこと、実行前に必要な状態・branch・worktree 条件、merge と conflict 解消、状態更新、session branch 削除条件、旧 merge サブコマンドを残さない境界を扱う。

## Read this when
- session 完了処理、session branch から home branch への merge、または joined 状態への遷移を実装・変更・検証するとき。
- session join 実行前に active/ready 状態、対応する状態ファイル、home branch 特定、未コミット差分なしをどう検証するか確認するとき。
- session 作成後に home branch が進んでいた場合の扱い、merge conflict 発生時の agent call、conflict marker 解消後の add と merge commit 作成手順を確認するとき。
- session 完了後の状態ファイル更新、session branch を削除してよい条件、削除できない場合の warning 継続を確認するとき。
- 旧 merge サブコマンド互換を実装やテストに残してよいか判断するとき。

## Do not read this when
- session の作成、apply 準備、状態ファイル形式そのものなど、join 以外の session lifecycle を確認したいとき。
- 通常の git branch 同士を汎用的に merge する機能を探しているとき。
- repository default branch の特別扱いを前提にした挙動を確認したいとき。
- conflict 解消 agent call のパラメータ詳細そのものを確認したいときは、その正本となる builder 仕様を直接読む。

## hash
- 31ed0e990d33b60e8355e3bce347d1da6313cac817f7e0139e1e15910b71a41b

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの正本仕様断片。ユーザーがエディタで入力したオリジナルプロンプトと cmoc の自動生成プロンプトを注入し、AI Agent CLI/TUI を起動する流れを定義している。
- 引数なし・事前条件なしのコマンドとして、`.cmoc` の git 追跡対象外保証、エディタ入力、agent call による必要パラメータ決定、TUI 起動までの実行手順を扱う。
- エディタ選択順、編集対象ファイル、初期 Markdown 文面、コメント除去と strip による読み出し、固定するモデル種別・推論強度、Codex CLI 起動時に持ち込む要素を確認する入口になる。

## Read this when
- `cmoc tui` の実装、テスト、または挙動確認を行うとき。
- ユーザー入力プロンプトの作成場所、初期内容、エディタ起動順、入力完了判定、読み出し時の整形規則を確認したいとき。
- TUI 起動前に agent call へ委ねるパラメータと固定値の境界を確認したいとき。
- Codex CLI を TUI バックエンドとして起動する際のコマンド名や、codex exec rule から持ち込む要素を確認したいとき。

## Do not read this when
- `cmoc tui` 以外のサブコマンド仕様を確認したいとき。
- agent call の詳細なパラメータ仕様そのものを確認したいときは、ここではなく対応する `build_tui_resolve_parameter_parameter` の正本を読む。
- TUI 起動パラメータの詳細そのものを確認したいときは、ここではなく対応する `build_tui_launch_tui_parameter` の正本を読む。
- Codex CLI の preflight validation、`$CODEX_HOME`、codex profile の詳細を確認したいときは、ここではなく codex exec rule の正本を読む。

## hash
- bf9e56d62773457f35ea256e938a9e9c6f17712b545de2ea129e5b3ed3c5e1ac
