# `__init__.py`

## Summary
- oracle 側の ACP builder indexing パッケージと同じ入口を提供する互換パッケージである。
- 実処理や公開 API の定義ではなく、対応する oracle 名前空間との互換性を示す最小のパッケージ初期化部分である。

## Read this when
- ACP builder の indexing 領域で、oracle 側パッケージとの対応関係や import 経路の互換性を確認したいとき。
- この階層が実装本体ではなく互換パッケージ入口として置かれているかを確認したいとき。

## Do not read this when
- indexing の具体的な処理、データ構造、生成ロジックを調べたいとき。
- 個別機能の実装やテスト対象を探しており、互換パッケージ入口の確認が不要なとき。

## hash
- b4803c42ff491acfff068dded4c03d215e5e317aaec706174600a7bc037ff22b

# `index_entry.py`

## Summary
- index_entry に関する正本実装を realization 側へ公開する薄い再エクスポート入口。実体は oracle 側にあり、この対象自体は独自ロジックを持たず、同名モジュールの定義を src ツリーから参照できるようにする役割だけを担う。

## Read this when
- src 側から index_entry の公開定義を import できるか確認したいとき。
- realization 実装が oracle 側の index_entry 定義をそのまま公開しているかを確認したいとき。

## Do not read this when
- index_entry のデータ構造、関数、バリデーション、具体的な仕様や挙動を調べたいとき。この対象ではなく oracle 側の実体を読む。
- indexing 全体の生成処理や他モジュールとの連携を調べたいとき。この対象は再エクスポートのみで、制御フローや集約ロジックは持たない。

## hash
- 1088bec47c2ee7df235be7136604d0012f9eab602c63ce765e8935e617c7991b
