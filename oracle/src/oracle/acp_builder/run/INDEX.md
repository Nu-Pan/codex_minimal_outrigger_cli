# `join`

## Summary
- run の変更を session に統合する競合解消 call を組み立て、run 固有の作業条件を共通の merge 指示に渡す。
- feedback の自動 join で封印済み report cut がある場合は、その採用結果を保つための追加指示と検証条件も組み込む。

## Read this when
- run と session の統合 call の作業条件、または封印済み feedback 結果を保つための追加指示を変更するとき。

## Do not read this when
- 両 join に共通する競合確認・統合・検証の指示を変更するときは、共通の merge prompt 定義を直接読む。
- session の変更を home に統合する call を変更するときは、session join 側の構築定義を読む。

## hash
- d2638ea587b10c0618069a49c7f79d13b9597b50b6fa1a120931fc102944fbfb
