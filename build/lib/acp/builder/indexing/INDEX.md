# `__init__.py`

## Summary
- oracle 側の indexing 実装を既存の acp.builder.indexing 参照から利用できるようにする互換入口。正本は oracle 配下に保ち、公開面から旧参照が消えるまで残すための薄い公開モジュールとして位置づけられる。

## Read this when
- acp.builder.indexing 経由の参照がどこで成立しているか確認したいとき。
- oracle 側の indexing 実装と realization 側の既存公開面の互換関係を調べるとき。
- acp.builder.indexing 参照の削除可否や互換入口の削除条件を確認するとき。

## Do not read this when
- indexing の正本仕様や本体実装を確認したいときは、oracle 側の対応する実装を直接読む。
- 互換入口ではなく、新しい公開 API や出力仕様を設計したいとき。
- acp.builder.indexing 以外の builder 領域や indexing と無関係な import 経路を調べるとき。

## hash
- e4bcedd304d889b5a766dee3920c560154c0ad58215560788a4427d8835a1da8

# `index_entry.py`

## Summary
- oracle 側の index entry 実装を、旧来の builder パッケージ経路から参照できるようにする互換入口。
- 公開面や realization 側に残る旧経路参照を維持するための薄い再公開であり、独自の index entry ロジックは持たない。

## Read this when
- 旧来の builder パッケージ経路から index entry 関連 API が参照される理由を確認したいとき。
- oracle 側の実装へ移った index entry API の互換入口や削除条件を確認したいとき。
- 旧経路参照を削除できるか判断するため、互換層の残存理由を確認したいとき。

## Do not read this when
- index entry の実体定義や生成ロジックを確認したいとき。その場合は oracle 側の実装を読む。
- INDEX.md エントリーの記述基準やルーティング規則を確認したいとき。その場合は対応する oracle doc を読む。
- 新しい index entry API を追加・変更したいとき。この互換入口ではなく、正本となる oracle 側の実装を確認する。

## hash
- f40922bbff39f2f514b174dfbb7ba079bdcf376ff8108a6e5a8bfc9f329f189c
