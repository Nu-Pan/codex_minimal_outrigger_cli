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
- Codex CLI による apply ループのサブコマンド仕様。セッション状態と git 状態を前提条件として確認し、隔離された作業先で所見調査と修正依頼を繰り返し、結果を状態遷移・コミット・レポート・終了コードとして扱う責務境界を定義する。
- apply ループの調査対象スコープ、調査待ちリストの更新規則、所見列挙・修正適用・変更要約の agent call 連携、回数上限到達時の未収束扱い、作業レポートに含める情報を確認する入口になる。

## Read this when
- apply ループを実行するサブコマンドの仕様、前提条件、状態遷移、終了区分、レポート生成を実装または検証するとき。
- ローリング・セッション・フルの各スコープで、どのファイルを調査待ちリストの初期値にするかを確認するとき。
- 所見列挙、所見に対する修正適用、変更内容要約を Codex CLI へ依頼する agent call の呼び出しタイミングや副作用を確認するとき。
- apply 用ブランチ、作業用コピー、セッション状態ファイル、隔離実行、git commit の関係を確認するとき。
- 作業結果が収束・未収束・エラーのどれに分類され、標準出力・レポート・終了コードでどう扱われるべきかを確認するとき。

## Do not read this when
- apply ループではなく、review 系やその他のサブコマンドの外部仕様を確認したいとき。
- agent call に渡すパラメータの詳細 schema やプロンプト仕様そのものを確認したいときは、ここではなく各 builder の正本仕様へ進む。
- run 隔離実行の一般仕様だけを確認したいときは、隔離実行を定義する文書へ進む。
- oracle file と realization file の一般定義や品質基準だけを確認したいときは、基本概念や標準を扱う文書へ進む。
- 特定の実装モジュールやテストの現在のコード構造を調べたいだけのときは、対応する realization 側のルーティングへ進む。

## hash
- 7185b2407e571a30711be4e4439b61b87eead12e43ddb12b914cc5019526fa43

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

# `init.md`

## Summary
- `cmoc init` による初期化の正本仕様断片。作業可能化のために、作業用メタ領域を git 追跡対象外にし、agent 用領域を git 追跡対象として用意し、その差分を commit する流れを定義している。
- 引数なしで実行される初期化コマンドについて、ignore 設定、既存追跡ファイルの追跡解除、agent 用領域の作成・保持、完了判定に使う git コマンド条件を確認する入口になる。

## Read this when
- 初期化サブコマンドの挙動、引数、事前条件、実行順序を確認したいとき。
- 作業用メタ領域を git 追跡対象外にする処理、または将来作成ファイルまで ignore されることの判定条件を実装・検証するとき。
- agent 用領域を初期化時に作成し、空の場合も git 追跡対象として保持する理由や必要操作を確認するとき。
- 初期化処理の最後に、初期化で発生した差分を commit する必要があるかを確認するとき。

## Do not read this when
- 初期化以外のサブコマンドの CLI 仕様や実行手順を調べたいとき。
- パスプレースホルダ全般の意味や、作業ルート・リポジトリルートの概念定義だけを確認したいとき。
- agent 操作禁止領域の一般ルールだけを確認したいとき。
- git ignore や git 追跡状態を扱わない実装内部の整理、共通 helper の分割方針、テスト構成だけを検討するとき。

## hash
- 96c03604e2136c25cc176229f1eb007a2fbee2a3a0626ad28b19c47ce8956c80

# `review_oracle.md`

## Summary
- `cmoc review oracle` サブコマンドの正本仕様断片。現在の作業対象の oracle file をレビューし、致命的・軽微な所見を人間向けレポートとして提示する処理の責務、事前条件、ループ構造、agent call 境界、レポート構成を定義する。
- レビュー対象の列挙、所見の列挙・マージ・検証・採否判定、隔離実行、レポート保存と stdout への提示までの流れを扱う。

## Read this when
- oracle file の問題検出を行うレビュー用サブコマンドの仕様を確認・実装・テストする。
- レビューのスコープ、事前条件、git 未コミット差分の扱い、セッション状態との関係を確認する。
- 所見リストの列挙、マージ、検証、採否判定の各ループや、対応する agent call の責務境界を確認する。
- レビュー結果レポートの frontmatter、本文セクション、所見の並び順、保存先、stdout 出力の仕様を確認する。
- レビュー処理が oracle file だけを対象とし、実装ファイルや自動生成ファイルをレビュー対象にしない境界を確認する。

## Do not read this when
- oracle file の一般的な定義、realization file との関係、正本仕様断片としての原則だけを確認したい。
- run の隔離実行そのものの共通仕様を確認したい場合は、隔離実行を扱う共通仕様を読む。
- 個別 agent call に渡すパラメータの詳細仕様だけを確認したい場合は、対応する parameter builder の正本を読む。
- 通常の実装ファイルを交えたコードレビュー、設計改善提案、過去の oracle file 差分調査の仕様を探している。
- 自動生成されるルーティング文書のレビューや生成規則を確認したい。

## hash
- df8019d8baa140e05925cec45090ae6a0b3b3e36fa029594bad66eddb64dd48b

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
- 現在 checkout しているローカルブランチを session の home branch とし、その HEAD から active session branch を作成するサブコマンドの正本仕様断片。
- 実行可能な checkout 状態、未コミット差分や既存 active session の禁止、session branch と状態ファイルの作成、標準出力に出す branch 名の扱いを定める。
- repository default branch を特別扱いしないこと、任意 start point を受け取らないこと、旧 branch 形式や旧サブコマンドの互換性を残さないことも境界として示す。

## Read this when
- session を開始するサブコマンドの実装・テスト・CLI 挙動を確認または変更するとき。
- home branch、session branch、fork commit、session id、状態ファイル保存の関係を確認したいとき。
- detached HEAD、remote-tracking branch、commit hash、cmoc 管理 branch、未コミット差分、既存 active session などのエラー条件を扱うとき。
- session branch の命名規則、active session は home branch ごとに高々 1 つという原則、旧仕様の削除範囲を判断するとき。

## Do not read this when
- session の終了、merge、apply、一覧表示など、session 作成以外のサブコマンドだけを扱うとき。
- path keyword や root model の定義そのものを確認したいとき。
- 実装ファイルの分割方針、テスト構成、補助スクリプトなど、正本仕様ではなく realization 側の設計だけを調べるとき。
- 旧 branch 形式や旧サブコマンドを実装互換対象として復活させる目的のとき。

## hash
- 7c6bbb2121f0e62abea69d96f955068bed6ff201353f4f3296bcd23411c39e16

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
- ユーザーがエディタで入力したオリジナルプロンプトと cmoc 側の自動生成プロンプトを用いて、AI Agent CLI/TUI を起動するサブコマンドの正本仕様断片。
- 引数なしで実行され、git 追跡除外の保証、プロンプト入力用ファイルの作成と読み出し、agent call による起動パラメータ決定、バックエンド別の TUI 起動条件を扱う。

## Read this when
- 任意のユーザープロンプトを cmoc の規則・規範の上で実行するサブコマンドの挙動を確認・実装・テストする。
- エディタ起動順、`code --wait`、プロンプト初期文面、コメント除去と `strip` によるオリジナルプロンプト読み出しを確認する。
- TUI 起動前に agent call で決定するパラメータと、agent call に委ねない固定パラメータを確認する。
- AI Agent CLI/TUI 起動パラメータ、または Codex CLI バックエンドで持ち込む `$CODEX_HOME`、preflight validation、codex profile の扱いを確認する。

## Do not read this when
- TUI 起動ではなく、非対話実行や別サブコマンド固有の CLI 挙動だけを確認したい。
- agent call の詳細な parameter schema そのものを確認したい場合は、参照先の parameter builder 仕様を直接読む方が適切である。
- Codex CLI の preflight validation や codex profile の詳細仕様だけを確認したい場合は、それらを定義する参照元仕様を直接読む方が適切である。
- oracle file や realization file の一般原則、INDEX.md エントリー作成規則、またはパスモデルの定義だけを確認したい。

## hash
- 32f5c6ae5e38803d7063ee32abe5978afa645f09fcb982a528d04ffe63d1f987
