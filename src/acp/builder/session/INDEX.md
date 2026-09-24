# `__init__.py`

## Summary
- `acp.builder.session` 配下の既存 import 経路を保つ互換パッケージ宣言であり、session 機能の処理は実装しません。

## Read this when
- `acp.builder.session` パッケージ層の互換入口を維持するか、撤去できるかを確認するとき。

## Do not read this when
- 特定の session 機能の実装や挙動を変更するときは、その機能の実装元を直接確認してください。
- `acp.builder.session.join` の個別 import 内容や委譲先を調べるときは、該当する下位モジュールを直接確認してください。

## hash
- 1c24d1b1720d385b0f3388d0c70ebd4fa053c26df3a40f54e8cb91484c901dc8

# `join`

## Summary
- 既存の `acp.builder.session.join` 系 import を維持する互換パッケージで、競合解消用パラメータ構築関数を oracle 側の正本実装から再公開する。

## Read this when
- 既存の join 系 import の互換性や移行を確認するとき、またはその参照が残っているかを調べて互換経路の削除可否を判断するとき。

## Do not read this when
- 競合解消用 prompt、対象 path の解決、適用する政策、agent 起動パラメータの内容を調べたり変更したりするときは、oracle 側の正本実装を読む。
- 親の session 互換パッケージの役割だけを確認するときは、その親 package の定義を読む。

## hash
- b5b39442d76884d1539e2d24ee9aeafeaaa0abcd81bcc3cdda8e09ac6078bd2d
