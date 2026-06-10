# `apply_abandon.md`

## Summary

- `cmoc apply abandon` の仕様断片への入口です。
- 未 join の apply run を安全に破棄する手順と前提条件、破棄対象、状態遷移、出力内容をまとめています。

## Read this when

- 現在の session に紐づく未 join の apply run を破棄したいとき。
- `<cmoc-apply-branch>` と `<cmoc-apply-worktree>` の削除条件、`apply.state` の更新、cleanup 時の warning を確認したいとき。
- `cmoc apply abandon` の実装・修正・テスト・レビューを行いたいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループ開始や要修正点リストアップの仕様だけを確認したいとき。
- `cmoc apply join` のマージ手順、想定外の差分の処理、`--force-resolve` の挙動だけを確認したいとき。
- `cmoc session abandon` や `cmoc session join` など、session 側の終了・破棄手順だけを確認したいとき。

## hash

- 65a56fe5bb8b38e641adf42fd80069b16cca0e2d78c698aecf00f015f9a2789a

# `apply_fork.md`

## Summary

- このファイルは `cmoc apply fork` の開始から完了レポートまでを扱うサブコマンド仕様です。
- 調査・修正ループ、作業用ブランチと worktree、評価対象スナップショットの扱いを定めます。
- `apply.state` の遷移、要修正点リストの Structured Output、レポート境界を案内します。

## Read this when

- `cmoc apply fork` の引数、事前条件、実行フロー、完了条件を確認したいとき。
- `<cmoc-apply-branch>` と `<cmoc-apply-worktree>` の生成・利用・削除ルールを確認したいとき。
- 開始時点の `<oracle-snapshot-commit>` に固定した調査・修正ループや、要修正点リストの Structured Output 仕様を確認したいとき。
- 部分適用モードと全体適用モードの違い、反復回数のデフォルト値、レポート内容を確認したいとき。

## Do not read this when

- `cmoc apply join` のマージ手順や `--force-resolve` の扱いだけを確認したいとき。
- `cmoc apply abandon` の破棄手順や cleanup の扱いだけを確認したいとき。
- `cmoc session fork` や `cmoc session join` など、session 側の開始・終了・統合だけを確認したいとき。
- `cmoc review oracles` の評価モードやレポート仕様だけを確認したいとき。

## hash

- 54860088428871af19ce47baa212d3c7f8a6f533d1aa29c8373dc1000d649cbf

# `apply_join.md`

## Summary

- `cmoc apply join` の仕様断片への入口で、`apply` で作成した成果物を session 側へ取り込む手順をまとめた文書です。
- 位置引数なしで実行し、`--force-resolve` によって想定外の差分の扱いが変わる点を案内します。
- 事前条件、通常モードと強制モードの分岐、`apply.state = error` の扱い、`INDEX.md` のコンフリクト自動解決、使用済みブランチの削除条件までを扱います。

## Read this when

- `<cmoc-apply-branch>` を `<cmoc-session-branch>` に取り込む流れを確認したいとき。
- `--force-resolve` の有無で、想定外の差分をどう扱うかを知りたいとき。
- `apply.state = error` を許容して続行できる条件や、マージコンフリクト時の `INDEX.md` 自動解決を確認したいとき。
- 処理後に `<cmoc-apply-branch>` と `<cmoc-apply-worktree>` を削除してよい条件を確認したいとき。

## Do not read this when

- `cmoc apply join` の実行手順や引数の詳細を確認したいだけのとき。
- `cmoc apply fork` や `cmoc apply abandon` など、別の `apply` サブコマンドの仕様を探しているとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。

## hash

- 08d097e56ecd4ed0c02fc21fd6c88a252fb2d166a9a683297f31e54ff5081c3f

# `indexing.md`

## Summary

- `cmoc indexing` の仕様断片で、現在の `<work-root>` に対してインデクシングを実行する手順を定める。
- 引数はなく、インデクシング結果は自動的に git commit される。
- 未コミット差分がある場合はエラー終了し、実際のインデクシングの意味は別紙の `oracles/docs/app_specs/indexing.md` を参照する。

## Read this when

- `cmoc indexing` の実装・修正・テスト・レビューを行うとき。
- 現在の `<work-root>` に対してインデクシングを明示的に実行する条件や、自動コミットの扱いを確認したいとき。
- 未コミット差分があるときにどう失敗するか、また `indexing` という語の意味を一般仕様から追いたいとき。

## Do not read this when

- `cmoc indexing` 以外のサブコマンドの手順や入出力だけを確認したいとき。
- インデクシングの一般仕様、`INDEX.md` の配置・生成ルール、Structured Output の扱いを確認したいときは、別の `indexing.md` を読むべきとき。
- 単に `oracles` 配下の他の仕様やルーティング文書をたどりたいだけのとき。

## hash

- 000c7f787bedd7230e77b80f5a06484638dd5302b521dc97be65f3f364c178ad

# `init.md`

## Summary

- `cmoc init` は `<repo-root>` を cmoc による作業が可能な状態に初期化するサブコマンドの仕様入口です。
- `.cmoc` を git 追跡対象外にする扱い、`.gitignore` 更新、`git ls-files` / `git check-ignore` による確認手順をまとめています。
- 初期化後に続く session/apply 系コマンドの前提条件として、初期化の振る舞いを確認するための文書です。

## Read this when

- `cmoc init` の実装・修正・テスト・レビューを行うとき。
- `<repo-root>/.cmoc` を git 追跡対象外にする処理や、`.gitignore` 更新、`git ls-files` / `git check-ignore` による確認仕様を扱うとき。
- 初期化後に続く session/apply 系コマンドの前提条件として、リポジトリ初期化の振る舞いを確認したいとき。

## Do not read this when

- `cmoc init` 以外のサブコマンドの仕様だけを確認したいとき。
- `.cmoc` の git ignore 追加や tracked ファイルの追跡解除が論点に含まれないとき。
- 初期化後の session/apply の運用仕様だけを確認したいとき。

## hash

- d7d79ec30c118e067dbee08ca5840d7aa23501c4d6f1a1030b3bc85886c7bfdb

# `review_oracles.md`

## Summary

- `cmoc review oracles` の仕様入口で、`<repo-root>/oracles` のスナップショットを評価して人間にレポートする手順をまとめた文書です。
- 部分評価・全体評価のモード分岐、所見の列挙・マージ・検証・判定ループ、レポート形式を案内します。
- 致命的問題と単純な問題の定義、および `codex exec` に渡す Structured Output の使い方を扱います。

## Read this when

- `cmoc review oracles` の実装・修正・レビュー時に、どの仕様断片へ進むべきかを素早く判断したいとき。
- 現在の `<repo-root>/oracles` スナップショットに致命的な問題がないかを評価し、人間へレポートする入口を確認したいとき。
- 部分評価モード・全体評価モードの切り替え条件や、`--scope` の扱い、評価対象 `oracle` ファイルの列挙方法を確認したいとき。
- 評価レポートの構成、`fatal` / `minor` の判定基準、出力先や参照ファイル一覧の仕様を確認したいとき。

## Do not read this when

- `cmoc review oracles` 以外の `cmoc` サブコマンドの手順や引数だけを確認したいとき。
- `oracles` 配下の個別仕様ファイルを直接確認したいとき。
- `INDEX.md` の生成・更新ルールや、`oracles` 全体のルーティング方針だけを確認したいとき。

## hash

- 84a327d125bc7ee83eb336a11c2f9ec81fdc75c1f2337c7cf0aeec85bccbcdba

# `session_abandon.md`

## Summary

- `cmoc session abandon` の仕様断片への入口です。
- 現在の `<cmoc-session-branch>` を `<cmoc-session-home-branch>` へ merge せずに破棄する手順、前提条件、破棄対象をまとめています。
- `session.state` を `abandoned` に更新し、未コミット差分なし・`apply.state = ready` などの条件を確認します。

## Read this when

- 現在の session branch を本流へ戻さずに破棄したいとき。
- `session.state`、`apply.state`、未コミット差分、home branch 存在の前提条件を確認したいとき。
- `cmoc session abandon` の実装・修正・テスト・レビューを行いたいとき。

## Do not read this when

- `cmoc session fork` だけを確認したいとき。
- `cmoc session join` による merge 完了の流れだけを確認したいとき。
- `cmoc apply abandon` など、apply run の破棄仕様だけを確認したいとき。

## hash

- 772b40b00c253d8508bf1ec3cd041089c008e57df5ee6f408aafa93e6f679cbb

# `session_fork.md`

## Summary

- `cmoc session fork` は、現在 checkout している local branch を session home branch とし、その HEAD から session branch を作成する手順を定める文書です。
- 引数なし実行を前提に、detached HEAD、未コミット差分、既存 active session、managed branch 上での実行などのエラー条件を扱います。
- session start commit の取得、`.cmoc` の追跡対象外保証、session metadata の保存、標準出力への表示、`cmoc/session/<session-id>` の命名規則を扱います。

## Read this when

- `cmoc session fork` の実装方針やテスト観点を確認したいとき。
- 新しい session branch の作成条件や checkout 手順を把握したいとき。
- session metadata の保存先やブランチ命名規則を確認したいとき。
- `cmoc branch` という旧名やレガシー要素の扱いを確認したいとき。

## Do not read this when

- `cmoc session join`、`cmoc session abandon`、`cmoc apply` 系の挙動だけを確認したいとき。
- branch モデル全体や一般的な使い方だけを確認したいとき。
- セッション開始ではなく、終了・破棄・統合の手順だけを確認したいとき。

## hash

- 7c6bbb2121f0e62abea69d96f955068bed6ff201353f4f3296bcd23411c39e16

# `session_join.md`

## Summary

- `cmoc session join` の仕様断片への入口です。
- 引数なしで現在の `<cmoc-session-branch>` を `<cmoc-session-home-branch>` へ `git merge --no-ff` して session を完了する流れを案内します。
- 事前条件、`apply.state` の確認、conflict 時の Codex CLI 依頼、終了後の `session.state` 更新とブランチ削除までをたどるための目次です。

## Read this when

- 現在の session を home branch へ戻して完了させる `cmoc session join` の実装・修正・テスト・レビューを行うとき。
- 引数なし実行の前提条件や、`session.state=active` / `apply.state=ready` の確認条件を整理したいとき。
- `<cmoc-session-home-branch>` が先に進んでいた場合の扱い、merge conflict の解消依頼、後始末の条件を確認したいとき。
- `cmoc merge` という旧名の扱いを含めて、session join の仕様を素早く把握したいとき。

## Do not read this when

- `cmoc session fork`、`cmoc session abandon`、`cmoc apply` 系など、他のサブコマンドの手順だけを確認したいとき。
- 一般的な git merge の解説だけで足りるとき。
- `INDEX.md` の生成・更新ルールや `oracles` 全体のルーティング方針だけを確認したいとき。

## hash

- 666aedaa7021a6bbcc4b03c6a3e3d2921cb0557b1dbbdf7c42600619adc377bd
