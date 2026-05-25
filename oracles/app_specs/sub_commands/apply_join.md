# `cmoc apply join`

## 概要

- `cmo apply fork` によってキックされた処理の成果物をセッション本流にマージする
- 言い換えると `<cmoc-apply-branch>` を `<cmoc-session-branch>` にマージするということ

## 引数

- 位置引数なし
- オプション引数 `--force-resolve` を受け取る

## 事前条件

以下の場合はエラー終了する

- 現在のブランチが `<cmoc-session-branch>`, `<cmoc-apply-branch>` のいずれでもない
- 対応する `<cmoc-session-state-file>` が存在しない
- 対応する `<cmoc-session-state-file>` の `session.state` が `active` ではない
- 対応する `<cmoc-session-state-file>` の `apply.state` が `completed` ではない
- git 未コミット差分が存在する

## モード分岐

- 想定外の差分に対する対する対応方法がモードによって異なる
- 想定外の差分とは
    - apply の実行中にユーザーが `<cmoc-session-branch>` 上で編集するのは oracles ファイルだけという想定
    - `<cmoc-apply-branch>` 上で cmoc が積み上げる変更対象は実装ファイルだけという想定
    - これら想定に違反した差分のことを指す
- 通常モード
    - 特に指定がない場合はこちら
    - 想定外の差分があったことをレポートして処理を中止する
- 強制モード
    - オプション引数 `--force`, `-f` が渡された場合はこちら
    - 想定外の差分を revert して処理を続行する

## 実行作業

1. `<cmoc-apply-branch>` 前準備
    1. `<cmoc-apply-branch>` を checkout
    2. `<cmoc-apply-branch>` 上の想定外の差分を…
        - 通常モード : レポート用に記録
        - 強制モード : revert して、その事をレポート用に記録
2. `<cmoc-session-branch>` 前準備
    1. `<cmoc-session-branch>` を checkout
    2. `<oracle-snapshot-commit>` から `<cmoc-session-branch>` HEAD までの間にあった (i.e. apply 実行中にユーザーが発生させた) 想定外の差分を…
        - 通常モード : レポート用に記録
        - 強制モード : rever して、その事をレポート用に記録
3. 通常モード : レポート用の変更の有無が記録されている場合、それらをレポートしてコマンド終了
4. `<cmoc-session-branch>` 上で `git merge --no-ff <cmoc-apply-branch>` を実行する。
5. `<cmoc-session-state-file>` を更新する (e.g. `apply.state` を `ready` に遷移)
6. 結果をレポート

## merge conflict 

- 想定外の差分がなければ、マージコンフリクトは発生しないはずである
- 通常モードでは想定外の差分が有る場合、処理を中断するのでマージまでたどり着かない
- 強制モードでは revert によって無理やり想定内の差分に収める
- よって、マージコンフリとは発生しないはずである
- 万が一発生した場合、cmoc が解決を試みることはせず、最後のレポートの一部としてユーザーに報告する

## 使用済みブランチの削除

- 以下の条件を満たす場合 cmoc は `<cmoc-apply-branch>` と `<apply-worktree>` を削除してよい
    - 対応する `<cmoc-session-state-file>` の `apply.state` が `ready` である
    - `<cmoc-apply-branch>` の HEAD が `<cmoc-session-branch>` から到達可能である
    - レポートが保存済みである
    - `<cmoc-session-state-file>` に結果が保存済みである
- 確認に失敗した場合はブランチを削除せず、warning として報告する。
