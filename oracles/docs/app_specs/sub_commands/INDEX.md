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

- `cmoc apply fork` の開始から完了レポートまでを扱うサブコマンド仕様です。
- 調査・修正ループ、作業用ブランチと worktree、評価対象スナップショットをまとめています。
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

- 5a7b8fb2701115b1466b61ed94b8cd34faed802a305f72675ed45d18fe881a7c

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

# `init.md`

## Summary

- `cmoc init` は `<repo-root>` を cmoc による作業が可能な状態に初期化するサブコマンドである。

## Read this when

- `cmoc init` の実装・修正・テスト・レビューを行うとき。
- `<repo-root>/.cmoc` を git 追跡対象外にする処理や、`.gitignore` 更新、`git ls-files` / `git check-ignore` による確認仕様を扱うとき。
- 初期化後に続く session/apply 系コマンドの前提条件として、リポジトリ初期化の振る舞いを確認したいとき。

## Do not read this when

- `cmoc init` 以外のサブコマンドや、その周辺の実装・テストだけを扱っているとき。
- `.cmoc` の git ignore 追加や tracked ファイルの追跡解除が論点に含まれないとき。
- 初期化後の session/apply の運用仕様だけを確認したいとき。

## hash

- b3b7cca844c91f7ba5a4e8d4592f0c2fb5510aa4ab31fbb1c114b7fd62574175

# `review_oracles.md`

## Summary

- `cmoc review oracles` の仕様入口で、`<repo-root>/oracles` のスナップショットを評価して人間にレポートする手順をまとめた文書です。
- `review_oracles.md` の実装・修正・レビュー時に、どの仕様断片へ進むべきかを素早く判断するための目次です。
- 部分評価・全体評価のモード分岐、評価対象の選定、レポート形式、致命的問題の定義を案内します。

## Read this when

- 現在の `<repo-root>/oracles` スナップショットに致命的な問題がないかを評価し、人間へレポートする入口を確認したいとき。
- 部分評価モード・全体評価モードの切り替え条件や、`--full` の扱い、評価対象 `oracle` ファイルの列挙方法を確認したいとき。
- 評価レポートの構成、`fatal` / `inconclusive` / `warning` の判定基準、出力先や参照ファイル一覧の仕様を確認したいとき。

## Do not read this when

- `cmoc review oracles` 以外の `cmoc` サブコマンドの手順や引数だけを確認したいとき。
- `oracles` 配下の個別仕様ファイルを直接確認したいとき。
- `INDEX.md` の生成・更新ルールや、`oracles` 全体のルーティング方針だけを確認したいとき。

## hash

- 3e9a7e2782585d528db7b4dfa50c2333b9ee44517efb93de41360913de145e02

# `session_abandon.md`

## Summary

- `cmoc session abandon` は、現在の `<cmoc-session-branch>` を `<cmoc-session-home-branch>` に merge せず破棄するサブコマンドです。
- session の成果物を本流へ取り込まず、`cmoc session join` 済み結果の rollback でもありません。
- 実行には session が active であること、apply が ready であること、未コミット差分がないことなどの前提があります。

## Read this when

- 現在の `cmoc-session-branch` を `merge` せずに破棄したいとき。
- `session.state` や `apply.state` の前提条件、破棄対象、状態遷移を確認したいとき。
- `cmoc session abandon` を実装・修正・テストするとき。

## Do not read this when

- `cmoc session fork` の仕様だけを確認したいとき。
- `cmoc session join` の仕様や、session を merge して完了させる流れだけを確認したいとき。
- `cmoc apply abandon` など、apply run の破棄仕様だけを確認したいとき。

## hash

- bcb79ab68e9293890ddbe24d146e34e8b5bbff528ac21f015290f00e16a2d954

# `session_fork.md`

## Summary

- `cmoc session fork` は、現在 checkout している local branch を session home branch とし、その HEAD から session branch を作成する手順を定める文書です。
- 引数なし実行を前提に、detached HEAD、未コミット差分、既存 active session、managed branch 上での実行などのエラー条件を扱います。
- session start commit の取得、`.cmoc` の追跡対象外保証、session metadata の保存、標準出力への表示、`cmoc/session/<session-id>` の命名規則を扱います。

## Read this when

- `cmoc session fork` の実装方針やテスト観点を確認したいとき
- 新しい session branch の作成条件や checkout 手順を把握したいとき
- session metadata の保存先やブランチ命名規則を確認したいとき
- `cmoc branch` という旧名やレガシー要素の扱いを確認したいとき

## Do not read this when

- `cmoc session join`、`cmoc session abandon`、`cmoc apply` 系の挙動だけを確認したいとき
- branch モデル全体や一般的な使い方だけを確認したいとき
- セッション開始ではなく、終了・破棄・統合の手順だけを確認したいとき

## hash

- 758a51bc67aeb9f3b5951c7e5fe4c2426113fad8b592cfe6b4f9092c89cbf566

# `session_join.md`

## Summary

- `cmoc session join` の仕様断片への入口で、現在の `<cmoc-session-branch>` を session metadata に記録された `<cmoc-session-home-branch>` へ `git merge --no-ff` して session を完了する手順を定めます。
- 引数はなく、現在ブランチ・state file の存在・`session.state=active`・`apply.state=ready`・home branch の特定可否・未コミット差分なしを事前条件とします。
- 実行は事前検証、`.cmoc` の非追跡保証、`git switch` と `git merge --no-ff`、conflict 時の Codex CLI 依頼、`session.state` の更新とブランチ削除の後始末で構成されます。
- home branch が session 作成後に進んでいてもエラーにはせず、その時点の HEAD に merge します。merge conflict は通常の conflict として扱い、`cmoc merge` は旧名として後方互換を保ちません。

## Read this when

- `cmoc session join` が何をするコマンドか、入力なしでどう session を完了させるか確認したいとき。
- session branch を home branch へ戻す前提条件や、`apply.state` の確認基準を実装・レビューしたいとき。
- home branch が先に進んでいた場合の扱い、conflict 解消時の Codex CLI 依頼、後始末の条件を確認したいとき。
- `cmoc merge` という旧名の扱いを整理したいとき。

## Do not read this when

- `session fork` / `session abandon` の手順だけを確認したいときは、それぞれの仕様文書を読むべきです。
- `apply` 系コマンドの実行条件や破棄手順だけを確認したいときは、この文書は適しません。
- 一般的な git merge の解説だけで足りるときは、この文書を読む必要はありません。

## hash

- 428466eab6eb5bbb48cf36c26eb649f9159375e2f63a555739d5146a999407a7
