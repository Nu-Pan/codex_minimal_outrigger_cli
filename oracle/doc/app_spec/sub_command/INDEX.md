# `apply_abandon.md`

## Summary

- `cmoc apply abandon` は、現在の `<cmoc-session>` に紐づく未 join の apply run を破棄し、`<cmoc-apply-branch>` と `<cmoc-apply-worktree>` を片付けるサブコマンドの入口です。
- `<cmoc-session-branch>` やその commit、oracle 改訂内容は変更せず、`cmoc apply join` 済みの結果を取り消す rollback ではありません。
- 破棄前提条件、破棄対象、状態遷移、stdout への報告、cleanup 失敗時の扱いを整理するための目次です。

## Read this when

- 未 join の apply run を破棄する `cmoc apply abandon` の実装・修正・テスト・レビューを行うとき。
- `apply.state` が `running` / `completed` / `error` のときにどう破棄するか、また `ready` でない apply run の扱いを確認したいとき。
- `<cmoc-apply-branch>` と `<cmoc-apply-worktree>` の削除条件、`<cmoc-session-state-file>` の更新、warning の出し方や終了コードを確認したいとき。

## Do not read this when

- `cmoc apply fork` や `cmoc apply join` の作業フロー自体を確認したいとき。
- `cmoc session join` や `cmoc session abandon` など、apply 破棄以外の session 系仕様だけを確認したいとき。
- `INDEX.md` の生成規則や `oracle` 全体のルーティング方針だけを確認したいとき。

## hash

- 1d3d095e144d8770e47c629792206265fad1698d3e1db15313984de55c6946c3

# `apply_fork.md`

## Summary

- この文書は `cmoc apply fork` の入口であり、Codex CLI による apply ループ全体の仕様を案内します。
- `<cmoc-session-branch>` から隔離された `<cmoc-apply-branch>` と `<cmoc-apply-worktree>` 上で動作し、ベストエフォートで実装追従を進める前提をまとめます。
- 事前条件、反復回数、所見リスト生成と改善、修正作業、状態遷移、作業レポート、終了コードまでをたどるための目次です。

## Read this when

- `cmoc apply fork` の実装・修正・テスト・レビューを行い、全体の手順と責務境界を整理したいとき。
- 調査対象ファイルの列挙、所見リスト改善、所見 1 件ごとの修正、コミット、レポート作成までの流れを確認したいとき。
- `apply.state` の遷移、スコープモード、ダーティフラグ、編集禁止ディレクトリの扱いなど、`cmoc apply fork` 固有の制約を確認したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` など、apply 系の別サブコマンドの仕様を確認したいとき。
- `cmoc session fork` / `cmoc session join` / `cmoc review oracle` など、apply fork 以外のフローを確認したいとき。
- `run isolation` や `codex exec` の共通規則だけを確認したいときで、このサブコマンド固有の手順が不要なとき。

## hash

- 8f8a514b8ad9da0d77e83f535396fe87ff8422052f632eb375969056c7438cd3

# `apply_join.md`

## Summary

- `cmoc apply join` の仕様断片への入口で、`apply` で作成した成果物を session 側へ取り込む手順をまとめる。
- 位置引数はなく、`--force-resolve` の有無で想定外の差分の扱いが変わる。
- 事前条件、通常モードと強制モードの分岐、`apply.state = error` の扱い、`INDEX.md` のコンフリクト自動解決、使用済みブランチの削除条件を案内する。

## Read this when

- `<cmoc-apply-branch>` を `<cmoc-session-branch>` に取り込む `cmoc apply join` の入口を確認したいとき。
- `--force-resolve` の有無で、想定外の差分や revert の扱いがどう変わるかを確認したいとき。
- `apply.state = error` を許容して続行できる条件や、`INDEX.md` のコンフリクト自動解決方針、使用済みブランチと worktree の削除条件を確認したいとき。

## Do not read this when

- `cmoc apply fork` や `cmoc apply abandon` など、別の `apply` サブコマンドの仕様を確認したいとき。
- `cmoc apply join` の実行手順そのものを細かく追うより、他の共通仕様や上位の目次を先に確認したいとき。
- `INDEX.md` の生成・更新ルールや `oracle` 全体のルーティング方針だけを確認したいとき。

## hash

- 8cd2425c6a8ae9b88c0fef539076160d9f8bf341bc5cb40a607960ebaceb9c85

# `indexing.md`

## Summary

- `cmoc indexing` の仕様断片への入口で、現在の `<work-root>` に対するインデクシング手順をまとめた文書です。
- 引数なしで実行し、インデクシング結果は自動的に git commit される前提や、未コミット差分がある場合の失敗条件を扱います。
- インデクシングそのものの一般仕様は別紙の `<work-root>/oracle/docs/app_specs/indexing.md` に分かれており、このファイルはサブコマンド側の入口として機能します。

## Read this when

- `cmoc indexing` の実装・修正・テスト・レビューを行いたいとき。
- 現在の `<work-root>` に対してインデクシングを実行する条件や、インデクシング結果の自動コミット条件を確認したいとき。
- 未コミット差分がある場合のエラー挙動や、`indexing` の意味をサブコマンド仕様として確認したいとき。

## Do not read this when

- `cmoc indexing` 以外のサブコマンドの引数、処理手順、出力だけを確認したいとき。
- `INDEX.md` の配置ルール、Structured Output の扱い、目次生成の一般仕様を確認したいときは、このファイルではなく別の `indexing.md` を読むべきとき。
- 単に `oracle` 配下の他の仕様やルーティング文書をたどりたいだけで、`cmoc indexing` の仕様は不要なとき。

## hash

- 56dd83624b22d9f2e9219cb4fc720d730f72ace8968376b51b9cb29b70d96cca

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

# `review_oracle.md`

## Summary

- この `review_oracle.md` のルーティング文書で、`cmoc review oracle` の実行仕様への入口をまとめます。
- `--scope={session|full}`、run の隔離実行、所見の列挙・マージ・検証・採否判定、レポート出力の流れを辿るための目次です。
- 実装・修正・テスト・レビューの前に、`cmoc review oracle` の責務境界と反復ループを整理する起点です。

## Read this when

- `cmoc review oracle` の仕様全体を、引数・事前条件・実行手順・出力まで通して把握したいとき。
- `--scope={session|full}` による対象範囲の切り替えや、所見リストの反復ループ条件を確認したいとき。
- レポート保存先や、所見の列挙・マージ・検証・採否判定の責務分担を確認したいとき。

## Do not read this when

- `cmoc review oracle` 以外のサブコマンド仕様を確認したいとき。
- `INDEX.md` の生成・更新ルールだけを確認したいとき。
- 個別の実装ファイルやテストファイルを直接追いたいとき。

## hash

- df8019d8baa140e05925cec45090ae6a0b3b3e36fa029594bad66eddb64dd48b

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

- 08b0fe9b67e7874161819b90a1c7a51022ba373a9076aa74a4864597a7b8c098

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

- `cmoc session join` の仕様断片への入口であり、session を完了して `<cmoc-session-home-branch>` へ戻すための文書です。
- 現在の `<cmoc-session-branch>` を `<cmoc-session-home-branch>` に `git merge --no-ff` し、必要なら conflict 解消を Codex CLI に依頼する流れを案内します。
- 事前条件、`apply.state` の確認、`session.state` の更新、ブランチ削除までの後始末をたどるための目次です。

## Read this when

- 現在の session を home branch へ戻して完了させる `cmoc session join` の実装・修正・テスト・レビューを行うとき。
- 引数なし実行の前提条件や、`session.state=active` と `apply.state=ready` の確認条件を整理したいとき。
- `<cmoc-session-home-branch>` が先に進んでいた場合の扱い、merge conflict の解消依頼、後始末の条件を確認したいとき。
- `cmoc merge` という旧名の扱いも含めて、session join の仕様を素早く把握したいとき。

## Do not read this when

- `cmoc session fork`、`cmoc session abandon`、`cmoc apply` 系など、session join 以外のサブコマンドの手順だけを確認したいとき。
- 一般的な `git merge` の解説だけで足り、cmoc 固有の session 完了フローを確認する必要がないとき。
- `INDEX.md` の生成・更新ルールや、`oracle` 全体のルーティング方針だけを確認したいとき。

## hash

- 31ed0e990d33b60e8355e3bce347d1da6313cac817f7e0139e1e15910b71a41b
