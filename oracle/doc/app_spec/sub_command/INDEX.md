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
- Codex CLI による apply ループを実行するサブコマンドの正本仕様断片。セッション状態、ブランチ・作業コピーの扱い、調査待ちファイルリスト、agent call による所見列挙と修正反映、レポート生成、終了結果区分を定義する。
- 実装を正本仕様断片へ近づけるためのベストエフォートな反復処理を扱い、目標達成を保証しない責務境界や、回数上限到達を正常系として人間判断に委ねる方針も示す。

## Read this when
- apply 系サブコマンドのうち、Codex CLI に修正反映を依頼して実装品質や正本仕様との一致を改善する処理を実装・変更・検証するとき。
- apply 実行前のエラー条件、セッション状態ファイルの状態遷移、未コミット差分や編集禁止領域の扱いを確認するとき。
- 調査待ちファイルリストの初期化スコープ、重複除去、所見が残った場合の再調査、差分発生ファイルの再投入など、apply ループの制御ロジックを確認するとき。
- apply 用 agent call の役割分担、所見列挙、所見適用、変更要約生成のどこでどの仕様を正本として参照するかを確認するとき。
- apply 実行後に保存する作業レポートの必須メタデータ、本文に含める結果区分・所見数推移・変更要約、標準出力へ流す内容を確認するとき。
- 収束・未収束・エラーを区別する終了結果や、回数上限到達時の扱いを実装・テストするとき。

## Do not read this when
- apply ループではなく、run の隔離実行そのものの詳細仕様だけを確認したいときは、隔離実行を扱う仕様を直接読む。
- 所見列挙、所見適用、変更要約生成の agent call パラメータの詳細だけを確認したいときは、それぞれの正本となる builder 仕様や実装を直接読む。
- oracle file と realization file の一般定義や、正本仕様断片としての基本原則だけを確認したいときは、基礎概念や標準を扱う文書を読む。
- apply 以外のサブコマンドの引数、事前条件、状態遷移、レポート形式を調べるときは、そのサブコマンドの仕様へ進む。
- 実装コードの配置、関数分割、テスト構成だけを調べたい場合で、apply の外部挙動や責務境界を確認する必要がないとき。

## hash
- 7af9d118609d8b45432b105b30c5c833746c6a1c7c577ef68f9e47bc224c0b14

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
- 作業可能なリポジトリ状態を作る初期化サブコマンドの正本仕様断片。引数を取らないこと、作業用メタディレクトリを git 追跡対象外にすること、その過程の差分を commit することを定める。
- 作業用メタディレクトリを追跡対象外にするための ignore 追加、既存 tracked ファイルの追跡解除、完了判定に使う git コマンド条件を確認する入口になる。

## Read this when
- 初期化サブコマンドの挙動、引数、事前条件、実行順序を確認したいとき。
- 作業用メタディレクトリを git 管理から外す実装やテストを扱うとき。
- ignore ルール追加、tracked ファイルの追跡解除、追跡対象外保証の完了判定を確認したいとき。
- 初期化処理でどの差分を commit すべきか、または初期化処理が commit を行うかを確認したいとき。

## Do not read this when
- 初期化以外のサブコマンド仕様を確認したいとき。
- パスキーワードそのものの定義や意味を確認したいとき。
- 作業用メタディレクトリ配下に保存される状態ファイルの内容やライフサイクルを確認したいとき。
- git ignore 判定や git コマンド実行の一般的な共通実装だけを確認したいとき。

## hash
- 6d71cfacaa1ab032d05af4ff7b18af7bbc0253443ba913121aee66734520d342

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
- ユーザー入力プロンプトと自動生成プロンプトを組み合わせ、AI Agent CLI/TUI を起動するサブコマンドの正本仕様断片。
- エディタによるオリジナルプロンプト入力、agent call によるパラメータ解決、完全プロンプト生成、Codex CLI 起動時に持ち込む実行規則とプロンプト渡しの境界を扱う。

## Read this when
- AI Agent CLI/TUI を、cmoc の規則・規範を注入した状態で起動するサブコマンドの挙動を確認・実装・テストする。
- ユーザーが入力するオリジナルプロンプトの編集方法、保存先、初期文面、コメント除去、空白除去の仕様を確認する。
- agent call で決定するパラメータと、agent call に委ねず固定するモデル種別・推論強度の境界を確認する。
- オリジナルプロンプトを完全プロンプトへ注入する方法や、Markdown 見出しの有無による変換規則を確認する。
- Codex CLI を起動する際のコマンド種別、完全プロンプトの保存、初期プロンプトの渡し方、codex exec rule から持ち込む要素を確認する。

## Do not read this when
- AI Agent CLI/TUI 起動ではないサブコマンドの引数・実行手順・外部挙動を確認したい。
- Codex CLI 全般の実行規則、環境変数、preflight validation、profile、ファイルアクセス制限そのものを確認したいだけで、このサブコマンドからの利用方法には関心がない。
- agent call の詳細な入力 schema やパラメータ構築関数の正本仕様だけを確認したい。
- パスキーワードや work-root、repo-root、cmoc-root の定義を確認したいだけで、このサブコマンド固有のログ保存・起動処理には関心がない。

## hash
- 969da73489da8d7eec6d14430542ac1a20aeefe412cddc35137e4f963f68d08c
