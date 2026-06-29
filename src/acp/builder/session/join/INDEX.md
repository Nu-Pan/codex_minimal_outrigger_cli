# `__init__.py`

## Summary
- ACP builder の session join 領域を、oracle 側の対応するモジュール構成と互換にするための package 入口を示す。
- 実処理ではなく package としての存在および互換境界を担うだけの薄い初期化対象である。

## Read this when
- ACP builder の session join 領域で、package 階層や import 経路の互換性を確認するとき。
- oracle 側の対応領域と realization 側の package 構成が対応しているかを調べるとき。
- session join 配下の実装へ進む前に、この階層が package として成立している理由だけを確認したいとき。

## Do not read this when
- session join の具体的な処理内容、関数、クラス、入出力仕様を調べたいとき。
- ACP builder 全体の設計や session join 以外の領域を調べたいとき。
- oracle 側の正本仕様そのものを確認したいとき。

## hash
- b0d15cb786f4514211487ee0127714fafa93fe6b3674ae0b61f53efd3bd9602c

# `conflict_resolution.py`

## Summary
- session join conflict resolution の旧 import 経路を維持するための互換モジュール。実体は正本側の実装を再 export しており、この場所自体には衝突解決ロジックを持たない。
- 旧経路を使う呼び出し元が残っている間だけ存在する移行用入口であり、呼び出し元が正本側を直接参照するようになったら削除対象になる。

## Read this when
- session join conflict resolution が旧 import 経路から参照されている理由を確認したいとき。
- 旧 import 経路を使う呼び出し元の移行、互換 import の削除可否、または再 export の存在理由を確認したいとき。
- 同名の正本側実装ではなく、この場所にモジュールが残っている理由だけを確認したいとき。

## Do not read this when
- session join conflict resolution の挙動、API、判定内容、実装詳細を確認・変更したいときは、正本側の実装を読む。
- 新しい衝突解決ロジックやテスト対象の仕様を探しているときは、この互換入口ではなく実体を持つ実装へ進む。
- 旧 import 経路の利用有無や移行状況に関係しない作業では読む必要はない。

## hash
- 308ba3143561e535d1701917f783244cc6d376a665220a955c4dee24d183bb76
