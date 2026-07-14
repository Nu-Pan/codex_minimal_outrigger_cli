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
- セッション結合の衝突解決パラメータを、互換性のために旧インポート経路から公開している薄い中継層。実装の本体ではなく、呼び出し元がまだ旧経路を使っている間だけ参照する。

## Read this when
- `session.join` の衝突解決パラメータをどこから公開しているかを確認したいとき。
- 旧経路を維持している理由と、削除してよい条件を確認したいとき。
- このモジュールを本体として直すのではなく、呼び出し元を正準の実装へ移すべきか判断したいとき。

## Do not read this when
- 衝突解決パラメータの本体実装や振る舞いを確認したいときは、正準の oracle 側の実装を見る。
- `session.join` の他の機能や、互換 import 以外の公開経路を探したいとき。
- このファイルを新しい実装の置き場として扱いたいとき。

## hash
- 9898c72f7a30b418dedee6e47c62149173a0820d92f73593fe987891300a1b10
