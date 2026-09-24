# `cmoc`

## Summary
- CLI のシェル起動境界を担い、プロジェクト内 Python の利用可否を確認してから CLI 本体へ引数を渡す。起動失敗の報告と補完要求の分岐も扱う。

## Read this when
- cmoc の起動可否、実行環境の確認、起動失敗の報告、通常起動と補完要求のシェル側の分岐を調べるとき。

## Do not read this when
- コマンド一覧、引数解釈、help や parse error の処理、各コマンドの実行内容を調べるときは、CLI 本体や該当コマンド実装へ直接進む。

## hash
- 1b63a1dcdef93f11792004773f0fe325678464587246e67f24d6975fb716bec4
