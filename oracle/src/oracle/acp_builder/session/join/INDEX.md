# `conflict_resolution.py`

## Summary
- session branch を home branch に統合する際の競合解消用 agent call を構築し、統合先 worktree と編集範囲を設定する。

## Read this when
- session join 中に merge conflict が発生し、競合解消 call の起動設定を確認・変更するとき。
- 競合解消 call が merge 中の作業場所や indexing preflight をどう扱うか調べるとき。

## Do not read this when
- run の成果を session に統合する競合解消 call を調べるときは、その処理専用の構築定義へ進む。
- 競合の判断基準や解消結果の受理・報告に関する意味仕様を確認するときは、共通の merge 競合解消仕様へ進む。

## hash
- 99dbe0e5be70c445fe13eee24816ab6806de4d3f3124dbe3b3897b19bc642d3c
