# `join`

## Summary
- session join 中の merge conflict 解消に使う、join 固有の agent call を組み立てる。
- source・target commit と home worktree を共通 prompt builder に渡し、この call のアクセス範囲や起動設定を決める。

## Read this when
- session join の競合解消 call がどの commit と worktree を使うか確認・変更するとき。
- この call のアクセス範囲、prompt builder への引き渡し、indexing preflight などの起動設定を確認・変更するとき。

## Do not read this when
- session join 全体の手順、state 遷移、report、失敗時の動作を調べるときは、session join の仕様へ進む。
- 競合解消の判断基準や共通 prompt の内容を調べるときは、競合解消の仕様または共通 prompt builder へ進む。
- session join の競合解消 call 以外の session call の起動設定を調べるときは、その call を定義する対象へ進む。

## hash
- 80369de4088bc3f5bb5de1ff7d969437a64a6a12c3b3bc7c7bb36cd1d60d9381
