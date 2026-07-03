# `__init__.py`

## Summary
- oracle.acp_builder.session.join 互換の package 初期化ファイル。既存の acp.builder.session.join.* import を維持するためだけに残る互換入口であり、実装本体は持たない。

## Read this when
- acp.builder.session.join 配下の import 互換性や公開面維持のために、この package が存在する理由を確認したいとき。
- oracle.acp_builder.session.join から realization 側への互換 package 配置を調べているとき。

## Do not read this when
- session join の具体的な処理内容や振る舞いを確認したいとき。
- 互換 import の利用箇所を探したいとき。
- realization 側と利用者向け公開面から参照がなくなったかを判断するために、実際の参照元を調査したいとき。

## hash
- 072255c777a758fe7fa412dab9c417d50fc420b5871fae782e550e97a8c1b483

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
