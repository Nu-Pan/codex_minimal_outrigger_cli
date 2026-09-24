# `conflict_resolution.py`

## Summary
- session join の merge 競合時に使う agent call の固有設定を組み立てる。対象 commit、home worktree、編集アクセス範囲、preflight の扱いを session join に合わせ、共通 prompt の構築は共通要素に委譲するため、この call の固有設定を調べる入口となる。

## Read this when
- session join の競合解消 call の起動条件や、共通 prompt 構築との責務境界を確認・変更するとき。
- 対象 commit、作業 worktree、編集アクセス範囲、preflight の設定を追うとき。

## Do not read this when
- session join の実行手順、state 更新、branch cleanup を調べるときは、session join の仕様へ進む。
- join 間で共通する競合解消 prompt や policy 自体を調べる・変更するときは、共通 prompt builder、policy、または競合解消の仕様へ進む。

## hash
- 99dbe0e5be70c445fe13eee24816ab6806de4d3f3124dbe3b3897b19bc642d3c
