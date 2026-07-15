# `join`

## Summary
- `cmoc session join` の merge conflict 解消用 AI 呼び出しを組み立てる入口。衝突ファイル一覧を受け取り、解消対象の範囲・編集許可・高優先度実行条件を決める内容を読むときの案内先。
- session join の conflict 解消時に、対象ファイルの渡し方、編集許可の範囲、呼び出し条件や推論強度の設定を確認・変更したいときに進む。

## Read this when
- `cmoc session join` の conflict 解消用プロンプト内容、対象ファイルの渡し方、呼び出しパラメータの設定を確認したいとき。
- session join の conflict 解消時に、どこまで編集を許すか、どのモデル・推論強度で呼び出すかを変えたいとき。

## Do not read this when
- 一般的なプロンプト組み立て規則だけを見たいときは、より汎用の prompt builder 側を読む。
- merge conflict 解消以外の session join 挙動を知りたいときは、このファイルではなく該当サブコマンドの実装を読む。

## hash
- e3d325a17e362bec618d1339a0a3f8f41b3b2a414313fc7ebf45c49b0beb5bac
