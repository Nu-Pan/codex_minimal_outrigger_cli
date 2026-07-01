# `__init__.py`

## Summary
- apply サブコマンド実装を束ねるパッケージ入口であり、この階層の下位要素が apply 処理を担当することだけを示す。
- この対象自体は詳細な処理や公開 API を定義せず、apply 関連実装へ進むための最小限の位置づけを持つ。

## Read this when
- apply サブコマンド実装の配置単位を確認したいとき。
- apply 関連の下位実装へ進む前に、この階層が apply 用であることだけを確認したいとき。

## Do not read this when
- apply サブコマンドの具体的な引数処理、実行手順、入出力、エラー処理を確認したいとき。
- apply 以外のサブコマンド実装を探しているとき。
- 詳細な実装責務を判断するために、下位の実装ファイルを直接読む方が適切なとき。

## hash
- e5354bb58c94a87f51093db4681c6f341202c07abf4b77772fb37b788f40b7b1

# `_runtime.py`

## Summary
- apply 実行時の linked worktree 特定、apply process pid file の保存・読取・削除、Codex subprocess 追跡環境の一時設定、apply abandon 用の process/group 停止処理を担う。
- pid reuse を避けるため start time と pidfd を使って process 同一性を確認し、壊れた pid file や stale pid を停止対象から外す制御を含む。

## Read this when
- apply branch から managed worktree を復元する処理、または session branch が checkout された linked worktree の探索処理を確認・変更したいとき。
- apply 実行中の pid file の形式、保存場所、lock、cleanup、壊れた内容の扱いを確認・変更したいとき。
- apply abandon が実行中 apply process や Codex subprocess group をどの順序・条件で停止するかを確認・変更したいとき。
- pidfd、process start time、process group、Linux /proc、zombie process の扱いに関係する停止安全性を調査するとき。

## Do not read this when
- apply の CLI 引数、出力 schema、session state 全体の構造を調べたいだけなら、より上位の command 実装や状態定義を読む。
- Codex subprocess の起動方法や実作業内容を調べたいだけなら、subprocess を開始する側の実装を読む。
- git worktree の一般的な作成・削除フローを調べたいだけなら、worktree 管理を担当する実装を読む。

## hash
- 25625f4e91acd37a8ef3835a54cfb3b03718bb4b8ecb56db40212f4f3f026937

# `abandon.py`

## Summary
- 未 join の active apply run を破棄し、apply state を ready に戻す CLI 実行処理を担う。
- session branch または apply branch 上での実行確認、session state の検証、running apply process の停止、apply worktree と apply branch の削除、process id file の削除、state 更新、結果表示までを扱う。
- apply abandon の外部挙動、破棄時の cleanup、warning 出力、session/apply branch 間の扱いを確認するための入口になる。

## Read this when
- apply abandon コマンドの実行条件、失敗条件、cleanup 手順、出力内容を確認または変更したいとき。
- active apply run を ready に戻す処理、running apply process の停止、apply worktree や apply branch の削除に関する挙動を追うとき。
- session branch から実行した場合と apply branch から実行した場合の作業ディレクトリ・対象 branch 判定を確認したいとき。

## Do not read this when
- apply run の開始、join、状態生成など、abandon 以外の apply サブコマンドを調べたいとき。
- worktree 削除、branch 削除、process 停止、state 読み書きの低レベル実装そのものを確認したいとき。
- apply abandon のテスト観点や fixture を確認したいだけで、実行処理本文を読む必要がないとき。

## hash
- 8cf68cbbea7c3a9377b922b36715768d1c71aea6dc037c1b20400f7f5834da66

# `fork.py`

## Summary
- apply fork の実行制御を担う実装。session branch 上で apply 用 branch/worktree を作り、scope に応じた対象列挙、Codex による finding 列挙・適用、差分 commit、report 出力、apply state 更新、失敗時 report/state 更新までを一つの apply run として扱う。
- apply fork の orchestration 全体を追う入口であり、対象正規化、再キュー、commit subject 生成、直近 join 済み apply merge commit の解決も同じ apply loop の復旧条件に関わる処理として含む。

## Read this when
- apply fork の開始条件、scope ごとの対象列挙、apply 用 worktree/branch 作成、apply state の running/completed/error 遷移を確認したいとき。
- Codex による finding 列挙・適用 loop、変更後の再キュー、commit 作成、収束/未収束時の戻り値や report path 出力を調べるとき。
- apply fork の失敗時に process id、state、error report、stdout へ渡される report path がどう扱われるか確認したいとき。
- apply 対象から除外される領域、oracle を含めるかどうか、git ignore・INDEX/AGENTS 除外などの対象正規化条件を変更するとき。

## Do not read this when
- apply fork report の具体的なファイル内容や書き込み形式だけを確認したい場合は、report 生成側を直接読む。
- Codex に渡す finding 列挙・finding 適用プロンプトや parameter 構築の詳細だけを確認したい場合は、builder 側を直接読む。
- apply process id の保存形式や tracking helper の実装だけを確認したい場合は、apply runtime 側を直接読む。
- apply join や他の apply サブコマンドの利用者向け挙動を確認したいだけなら、そのサブコマンド実装または対応する仕様を読む。

## hash
- 5df4bc5c860a258c6b78a92eac6b0ee37c45e24b27440ca2e0148d387c9f8cc8

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を、Markdown と YAML frontmatter を持つ作業レポートとして生成する処理を担う。
- apply fork の差分を fork commit 以降の管理対象変更、未コミット変更、ステージ済み変更、未追跡ファイルから集め、Codex による構造化要約または path 一覧の fallback 要約へ変換する。
- レポート本文には終了結果、所見数の推移、変更内容要約、session/apply branch や commit/worktree の識別情報をまとめる。

## Read this when
- apply fork の作業レポートの生成場所、frontmatter、本文構成、終了結果ラベルの表示文言を確認または変更したいとき。
- apply fork の変更要約がどの git diff 範囲、未追跡ファイル、rename/delete filter を対象にしているか確認したいとき。
- 変更要約生成に失敗した場合や空要約の場合の fallback 表示、変更 path の集約方法を確認したいとき。

## Do not read this when
- apply fork のループ制御、所見列挙、収束判定そのものを調べたいとき。
- Codex に渡す変更要約生成 prompt や Structured Output の詳細を調べたいとき。
- session state、report directory、git 実行 wrapper、timestamp などの共通 runtime 処理を調べたいとき。

## hash
- c7226e131c37868e9bca44b61ec1b05a65e0caa1a2babf58e134693e5e858595

# `join.py`

## Summary
- apply run の完了またはエラー後に、apply branch を session branch へ join する CLI 実行本体を扱う。
- join 可否の state 検証、想定外差分の検出と force-resolve、merge conflict 処理、state 更新、report 作成、apply worktree/branch cleanup までを担う。
- apply/session branch で許可される変更範囲や、INDEX.md conflict の機械解決など、apply join 固有の制御ロジックへの入口になる。

## Read this when
- apply join の実行条件、失敗条件、force-resolve の挙動、cleanup の挙動を確認または変更したいとき。
- apply branch と session branch の差分分類、想定外差分 report、merge conflict report の生成内容を調べたいとき。
- apply join 後の session state 更新、last joined oracle snapshot commit、apply state 初期化、apply worktree/branch 削除の流れを追いたいとき。
- INDEX.md の merge conflict だけを自動解決する処理や、削除・rename を含む managed branch 差分判定を確認したいとき。

## Do not read this when
- apply run の開始、apply branch/worktree の作成、または apply 中の agent 実行制御を調べたいだけのとき。
- session state のデータ構造や永続化 format そのものを確認したいとき。
- git worktree 探索 helper や cmoc runtime 共通関数の詳細実装を確認したいとき。
- apply join 以外のサブコマンドの CLI 入口やルーティングだけを調べたいとき。

## hash
- fff7ab6917b17a245a6a01863838ed827e5fe02fffaba951e76fddb05210aabf
