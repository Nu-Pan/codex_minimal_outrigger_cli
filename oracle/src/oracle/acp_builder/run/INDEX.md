# `join`

## Summary
- run branch の成果を session worktree に統合する競合解消 call を構築し、編集範囲、実行 cwd、indexing preflight の設定を担う。
- feedback 自動 join では封印済み report cut を参照入力に加え、採用結果を維持するための調整・検証指示を追加する。

## Read this when
- run join の競合解消 call の構築設定や、feedback 自動 join で封印済み結果を引き継ぐ処理を調査・変更するとき。

## Do not read this when
- run join と session join に共通する競合調査・統合・検証の指示を変更するときは、共通の競合解消 prompt 構築定義を読む。
- session の変更を home に取り込む join call の設定を調べるときは、session join 側の構築定義を読む。
- 競合解消や封印後のマージ調整に関する規範要件を確認・改訂するときは、正本仕様を読む。

## hash
- d2638ea587b10c0618069a49c7f79d13b9597b50b6fa1a120931fc102944fbfb
