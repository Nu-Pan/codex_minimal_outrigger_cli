# `__init__.py`

## Summary
- `oracle.acp_builder.session.join` と互換の package であることだけを示す package 初期化対象。

## Read this when
- `oracle.acp_builder.session.join` 互換 package の存在確認や import 経路の確認をする。
- この package 自体が担う公開上の位置づけを確認する。

## Do not read this when
- join session の具体的な処理内容や実装詳細を調べたい。
- 互換 package ではなく、実際の機能定義・制御ロジック・テストを調べたい。

## hash
- b0d15cb786f4514211487ee0127714fafa93fe6b3674ae0b61f53efd3bd9602c

# `conflict_resolution.py`

## Summary
- セッション join の conflict resolution について、旧 import 経路を正本側の実装へ橋渡しする互換モジュール。実体は持たず、canonical oracle path から再エクスポートするだけの入口として置かれている。

## Read this when
- 旧 import 経路から conflict resolution を参照している呼び出し元との互換性を確認する。
- canonical oracle path への移行が完了しているか、またはこの互換モジュールを削除できる条件を判断する。
- セッション join の conflict resolution で、実装本体ではなく import 経路の差し替えや再エクスポートだけを確認する。

## Do not read this when
- conflict resolution の仕様や実装内容そのものを確認したい場合は、正本側の実装を読む。
- 新しい conflict resolution の挙動を追加・変更したい場合は、この互換層ではなく canonical 側を読む。
- 旧 import 経路の維持や削除条件に関係しない作業では読む必要はない。

## hash
- 308ba3143561e535d1701917f783244cc6d376a665220a955c4dee24d183bb76
