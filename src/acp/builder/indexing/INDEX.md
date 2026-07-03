# `__init__.py`

## Summary
- 正本側の indexing 実装を既存の公開名から参照できるようにする互換入口。実体は正本側に保ちつつ、既存利用者や realization 側に残る旧参照を成立させるための境界を示す。
- 互換コードを残す理由と削除条件を説明するだけの小さな入口であり、indexing の実処理や仕様本体はここには置かれない。

## Read this when
- 旧来の公開名から正本側の indexing 実装へ到達させる互換経路を確認したいとき。
- 互換入口を削除できるか判断するために、残存参照の有無や削除条件を確認したいとき。
- 正本側に実装を集約しながら、既存の利用者向け参照を壊さないための薄い公開面を調べるとき。

## Do not read this when
- indexing の具体的な生成処理、探索処理、データ構造、入出力仕様を確認したいとき。この入口ではなく正本側の実装を読む。
- 新しい indexing 機能を追加または変更したいとき。互換入口ではなく実体を持つ実装側を読む。
- 単にパッケージ配下の通常モジュール構成や汎用的な import 規約を調べたいとき。

## hash
- e4bcedd304d889b5a766dee3920c560154c0ad58215560788a4427d8835a1da8

# `index_entry.py`

## Summary
- oracle 側の indexing index entry builder を旧 acp.builder 名前空間から再公開する互換入口。
- 既存利用者が旧参照で build_indexing_index_entry_parameter を import し続けられるようにする薄い転送層。

## Read this when
- 旧 acp.builder.indexing.index_entry 参照の維持・削除条件を確認したいとき。
- indexing index entry builder の import 経路互換性を調べるとき。

## Do not read this when
- builder 本体の実装や引数構築ロジックを確認したいときは、再公開先を読む。
- 新規機能追加や index entry 生成仕様そのものを調べたいとき。

## hash
- 0942f373b620da2b885fbc99301d410e8eb54a141bea9edc93310c4ff55fbbeb
