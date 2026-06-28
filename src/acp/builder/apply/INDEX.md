# `__init__.py`

## Summary
- oracle 側の apply builder package と対応する互換 package であることだけを示す package 初期化要素。実処理や公開 API の定義ではなく、同領域を package として扱うための入口に位置づけられる。

## Read this when
- apply builder 領域が oracle 側の package 構造と対応しているかを確認したいとき。
- package 初期化部分に実装意図や互換性メモがあるかを確認したいとき。

## Do not read this when
- apply builder の具体的な処理、変換、適用ロジックを調べたいとき。その場合は同 package 内の実装本体を読む。
- 公開関数、クラス、入出力仕様、エラー処理を確認したいとき。この対象にはそれらの定義は含まれない。

## hash
- a6df93a5897c266e6f48287739c8bf8192733ea9fb19e2f6eb05a302f4165b06

# `fork`

## Summary
- fork 適用領域の realization 側入口をまとめる package。内容は互換 package 初期化と、change summary、file finding enumeration、finding application などの公開 API を oracle 側実装へ接続する薄い再エクスポートで構成される。
- この階層自体は処理本体や正本仕様ではなく、src 側の import 経路から oracle 側の実体へ到達するための接続点として位置づく。

## Read this when
- realization 側から fork 適用関連の公開名がどの oracle 側実装へ委譲されているか確認したいとき。
- fork 適用領域で、src 側 import 経路の互換 package や再エクスポートの入口だけを確認したいとき。
- 具体的な処理本文を読む前に、この階層が実装本体ではなく oracle 側実装への接続層であることを確認したいとき。

## Do not read this when
- fork 適用処理の具体的な関数、型、データ構造、分岐条件、入出力を調べたいとき。その場合は委譲先の oracle 側本文を読む。
- fork 適用処理全体の流れや、change summary、file finding enumeration、finding application 以外の責務を調べたいとき。その場合はより上位または隣接する対象を読む。
- oracle 側の正本仕様断片そのものを確認したいとき。この階層は realization 側の接続層であり、正本仕様ではない。

## hash
- b5b20a45eea2923fef6770bf0e47c4657670c7b5696373c788cfe7c265ac3e59
