# `__init__.py`

## Summary
- oracle.acp_builder.session との互換性を保つための package 初期化ファイル。既存の acp.builder.session.* import を維持するためだけに残されている。

## Read this when
- acp.builder.session.* import の互換維持経路を確認する。
- oracle.acp_builder.session 参照への移行や、互換 package を削除できる条件を確認する。

## Do not read this when
- session 実装の挙動や構成要素を確認したい場合。
- 新規機能の入口や通常の公開 API を探している場合。

## hash
- 1c24d1b1720d385b0f3388d0c70ebd4fa053c26df3a40f54e8cb91484c901dc8

# `join`

## Summary
- `acp.builder.session.join` 互換 package を収める案内用エントリー。ここには実装本体は置かれず、旧インポート経路を維持するための入口と、その周辺の互換公開面だけを案内する。
- `conflict_resolution` は、結合時の衝突解決パラメータを旧経路から参照している場合にだけ読む。正準実装へ移す判断や、削除条件の確認に使う。

## Read this when
- `acp.builder.session.join` 配下の互換 import や公開面の維持理由を確認したいとき。
- 旧経路を残している理由と、いつ削除できるかを判断したいとき。
- 互換 package 配置が必要かどうかを、`oracle.acp_builder.session.join` 側の定義との関係でたどりたいとき。

## Do not read this when
- session join の具体的な処理内容や振る舞いを確認したいとき。
- 互換 import の利用箇所そのものを探したいとき。
- 実際の参照元や移行状況を調べて、公開面から外せるか判断したいとき。
- 衝突解決パラメータの本体実装を確認したいとき。

## hash
- 759723a20930287ad6c97d49a165ac1f33346d79d900e482d6d9edc57603c625
