# `join`

## Summary
- run の変更を session worktree に統合する競合解消 call を、run 固有の編集範囲と文書検索範囲に合わせて組み立てる。
- feedback の自動 join で封印済み結果が渡された場合は、採用結果の維持に必要な調整と検証の指示を追加する。

## Read this when
- run join の競合解消 call に適用する作業場所・編集範囲・文書検索範囲や、その構築方法を調べるとき。
- feedback 自動 join で封印済み結果を参照し、採用結果を維持するための調整を調べるとき。

## Do not read this when
- run と session の両方に共通する競合解消の指示や方針を調べるときは、共通の競合解消 prompt 定義または正本仕様へ進む。
- session を home に統合する call 固有の構築を調べるときは、session join 側の定義へ進む。
- run の join 制御や feedback report の受付・分類・封印処理を調べるときは、それぞれの処理を定める仕様へ進む。

## hash
- dc207e3c58d26de6c3d0af401797a51ca650434ef1d8e5539ff54a2e1c707745
