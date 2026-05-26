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
- 調査・修正ループ、作業用ブランチと worktree、評価対象スナップショット、レポート境界をまとめています。

## Read this when

- `cmoc apply fork` の引数、事前条件、実行フロー、完了条件を確認したいとき。
- `<cmoc-apply-branch>` と `<cmoc-apply-worktree>` の生成・利用・削除ルールを確認したいとき。
- 開始時点の `<oracle-snapshot-commit>` に固定した調査・修正ループや、要修正点リストの Structured Output 仕様を確認したいとき。
- 部分適用モードと全体適用モードの違い、反復回数のデフォルト値、レポート内容を確認したいとき。

## Do not read this when

- `cmoc session fork` の作成条件や session metadata の保存だけを確認したいとき。
- `cmoc session join` の merge 手順、コンフリクト解決、session 終了処理だけを確認したいとき。
- `cmoc apply join` のマージ手順、差分検査、`--force-resolve` の挙動だけを確認したいとき。
- `cmoc apply abandon` の破棄手順や cleanup 挙動だけを確認したいとき。
- `cmoc eval-oracles` の評価モードや評価レポート仕様だけを確認したいとき。

## hash

- d2609b45513796846beb5a8bfc82fba45b907112c55399cfdfcfb8823419b130

# `apply_join.md`

## Summary

- `cmoc apply join` は、`apply fork` で作成された成果物をセッション本流へ取り込むコマンドの仕様を定義します。
- 処理は、ブランチの checkout、想定外の差分の記録または revert、`git merge --no-ff` による統合、セッション状態ファイルの更新、結果レポートで構成されます。
- マージコンフリクトは原則想定せず、発生した場合は解決せずにユーザーへ報告します。
- 一定条件を満たした場合にのみ、`<cmoc-apply-branch>` と `<cmoc-apply-worktree>` を削除できます。

## Read this when

- `cmoc apply join` の引数、事前条件、実行手順を確認したいとき
- `<cmoc-apply-branch>` を `<cmoc-session-branch>` にマージする処理を実装・修正したいとき
- 想定外の差分の検出、通常モード/強制モードの分岐、マージ後の state 更新を扱いたいとき
- 使用済みブランチと apply worktree の削除条件を確認したいとき

## Do not read this when

- `cmoc apply join` ではなく、`cmoc apply fork` の生成処理や調査・修正ループを確認したいとき
- セッション開始・終了、または `abandon` 系のフローだけを確認したいとき
- ブランチモデルや状態ファイルの基本仕様だけを確認したいとき

## hash

- 9920b25b80bed7bc2e7afa1e4f7745bc7784ff9712f46e4b14c638614dcf926e

# `eval_oracles.md`

## Summary

- `cmoc eval-oracles` の仕様断片への入口です。
- 現在の `<repo-root>/oracles` スナップショットに致命的な問題がないかを評価し、その結果を人間向けレポートとしてまとめる手順を扱います。
- 部分評価・全体評価モードの分岐、`codex exec` による 1 ファイル単位の評価、評価レポートの構成を確認するための文書です。

## Read this when

- `cmoc eval-oracles` の実装・修正・テスト・レビューを行うとき。
- `--full` による部分評価 / 全体評価の切り替え条件を確認したいとき。
- `codex exec` を使って `<repo-root>/oracles` の各ファイルを評価し、Structured Output のレポートをまとめる流れを確認したいとき。

## Do not read this when

- `cmoc eval-oracles` ではなく、`cmoc session` や `cmoc apply` など他サブコマンドの手順だけを確認したいとき。
- 実装コードやテストコードの作業だけで足りるとき。
- `INDEX.md` の生成・更新ルールや、`oracles` 全体の扱いだけを確認したいとき。

## hash

- 04dddafebf3feba523bb4be89a990dead4c7e4c5f698221e352ad45e8fd8f16e

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

- `cmoc session fork` の概要と、現在の local branch を起点に session branch を作る仕様をまとめた文書です。
- 引数なしで実行する前提と、detached HEAD・未コミット差分・既存 active session などのエラー条件を扱います。
- session start commit の取得、`.cmoc` の追跡対象外保証、session metadata 保存、標準出力への表示までの実行手順を扱います。
- `cmoc/session/<session-id>` の命名規則、任意 start point を受け取らない方針、`cmoc branch` のレガシー扱いを含みます。

## Read this when

- `cmoc session fork` の実装方針やテスト観点を確認したいとき
- 新しい session branch の作成条件や checkout 手順を把握したいとき
- session metadata の保存先やブランチ命名規則を確認したいとき
- `cmoc branch` という旧名やレガシー要素の扱いを確認したいとき

## Do not read this when

- `cmoc session fork` 以外のサブコマンド仕様を確認したいとき
- セッションの join・abandon・apply 系の挙動だけを調べたいとき
- branch モデル全体や一般的な使用法だけを確認したいとき

## hash

- 471fc0184da6ece904959ed74a6ae0bbae6c71ebd92ed2ff52c44a8c8576d946

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
