# `conflict_resolution.py`

## Summary
- session join の競合解消時に home worktree 上で呼び出す agent の起動定義。取り込む側と取り込み先の merge 前 commit、進行中の worktree、caller が確定した閲覧範囲を使って session join 固有の call parameter を組み立てる。
- 共通の競合解消 prompt 構築は共有 builder に委譲するため、session join 固有の起動設定と共通処理の接続点を確認する入口。

## Read this when
- session join の競合解消 call がどの commit と worktree を対象にし、どの閲覧範囲で起動するかを調べる、またはその起動設定を変更するとき。

## Do not read this when
- session join 全体の手順、state 更新、失敗時の動作を調べるときは、session join の仕様を読む。
- join 間で共有される競合解消 prompt や policy を調べるときは、共通 prompt builder と関連 policy を読む。
- run join の競合解消 call 固有の起動設定を調べるときは、その専用 builder へ進む。

## hash
- ef0fafa7009a94140fc7ace5794304efe1d29fbef367b22db2498ed350449351
