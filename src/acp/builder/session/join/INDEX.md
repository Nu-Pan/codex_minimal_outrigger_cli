# `__init__.py`

## Summary
- 既存の `acp.builder.session.join.*` import 経路を保つ互換パッケージの入口です。join 機能の処理自体は定義しません。

## Read this when
- この import 経路を維持する互換層の役割や、削除できる条件を確認するとき。

## Do not read this when
- session join の競合解決の処理を確認・変更するときは、その処理を定義する正本の実装を読んでください。

## hash
- 072255c777a758fe7fa412dab9c417d50fc420b5871fae782e550e97a8c1b483

# `conflict_resolution.py`

## Summary
- 従来の import 経路を維持するため、session join の merge conflict 解消用パラメータ構築関数を正規実装から再公開する互換層。
- prompt やポリシーの選択、パラメータの組み立ては行わず、正規実装に委譲する。

## Read this when
- 従来の import 経路を使う caller との互換性や、この層が再公開する関数の範囲を調べるとき。
- 互換経路の廃止や変更を検討し、既存 caller が残っているか確認するとき。

## Do not read this when
- conflict 解消用 prompt、ポリシー選択、パラメータ構築の内容を調べるときは、正規実装を読む。
- session join の競合列挙、呼び出し順序、実行時のエラー処理を調べるときは、サブコマンドの処理を読む。

## hash
- 80dd736d61e6995d92c4ad91df4c25fadaf86f51cec5a0fa7d97bcfdf01a96b5
