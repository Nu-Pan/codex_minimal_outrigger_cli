# `conflict_resolution.py`

## Summary
- run join の競合解消を担当する agent call を構築する。自動 join で封印済みの feedback report cut が渡された場合は、その結果を保つための追加指示も組み込む。

## Read this when
- run の競合解消 call の入力、編集範囲、作業場所や起動条件を調べるとき。
- 自動 feedback join で封印済み結果を引き継ぎ、競合解消後に維持する流れを調べるとき。

## Do not read this when
- run と session に共通する競合解消 prompt の構築を変更するときは、共通の prompt 構築定義へ進む。
- session を home に統合する join の call 構築を調べるときは、session join 専用の定義へ進む。
- 競合解消や封印済み結果の規範的な要件を確認するときは、対応する正本仕様を参照する。

## hash
- 4c9d7c42bb7430e25c163acbb12693c2bf418658c27047bcec493a6ea77f3070
