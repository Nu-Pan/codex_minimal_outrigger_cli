# `conflict_resolution.py`

## Summary
- `cmoc session join` の conflict marker 解消用のエージェント呼び出しパラメータを組み立てる処理を読む入口。`session join` で merge conflict の解消を扱うとき、対象パスの正規化、プロンプト組み立て、実行パラメータ設定の全体像を確認したい場合にここから入る。
- conflict 対象ファイルの列挙や、解消時に追加で許される編集範囲を確認したいときに読む。プロンプト本文の細部や共通 prompt 組み立ての他責務は、ここではなく関連する prompt builder 側を優先して読む。

## Read this when
- `cmoc session join` の conflict resolution 用パラメータ生成を変更・確認したい。
- conflict 対象パスの扱い、実行モデル、推論強度、repo write 前提の設定を確認したい。
- merge conflict 解消時に AI に渡す制約や追加ファイルアクセス条件を確認したい。

## Do not read this when
- 通常の `session join` の接続処理やセッション管理だけを見たい。
- 共通の prompt 生成ロジックや markdown 化の実装だけを見たい。
- conflict 解消以外のサブコマンド向けエージェントパラメータを探している。

## hash
- f6ae4a7d59acd24ac6b5921e784882991cd53c0f7f7eab6bcc2db4eb92d89107
