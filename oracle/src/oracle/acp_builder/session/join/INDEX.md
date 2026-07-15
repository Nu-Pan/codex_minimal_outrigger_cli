# `conflict_resolution.py`

## Summary
- `cmoc session join` の merge conflict marker 解消用 AI 呼び出しパラメータを組み立てる入口。衝突ファイル一覧を受け取り、解消対象の範囲・編集許可・高優先度実行条件をまとめて返す。

## Read this when
- `cmoc session join` の conflict 解消用プロンプト内容、対象ファイルの渡し方、呼び出しパラメータの設定を確認したいとき。
- session join の conflict 解消時に、どこまで編集を許すか、どのモデル・推論強度で呼び出すかを変えたいとき。

## Do not read this when
- 一般的なプロンプト組み立て規則だけを見たいときは、より汎用の prompt builder 側を読む。
- merge conflict 解消以外の session join 挙動を知りたいときは、このファイルではなく該当サブコマンドの実装を読む。

## hash
- 0d683ed9bde30e17c0907a0fabb464ea213e0aa4d5214db62c6ab5a35ab373c7
