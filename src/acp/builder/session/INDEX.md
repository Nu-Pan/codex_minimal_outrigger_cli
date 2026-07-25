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
- oracle.acp_builder.session.join 互換の package 初期化ファイル。既存の acp.builder.session.join.* import を維持するための互換入口で、実装本体は持たない。
- session join の競合解決パラメータ生成関数を旧来の import 経路へ提供する互換モジュール。canonical 実装呼び出し後、競合ファイル一覧を code fence を保護して prompt に追加する。

## Read this when
- acp.builder.session.join の import 互換性や公開面維持を確認するとき。
- oracle 側の session join から realization 側への互換配置、または競合 path prompt 生成の互換経路を調べるとき。

## Do not read this when
- session join の具体的な処理仕様や canonical 実装を確認したいとき。
- 互換 import の利用箇所や、互換経路を削除できるかを実際の参照元から判断したいとき。

## hash
- 4ce7051bdd408e58ebb58322b1cbc07c051365db6dd3043bb08413fa9acf7d09
