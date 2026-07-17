# `oracle`

## Summary
- `cmoc oracle edit` の TUI 起動パラメータを構築する実装。ユーザー指示を組み込んだ完全プロンプトを保存し、固定のモデル・推論強度・ファイルアクセス・実行前インデックス設定を持つ `AgentCallParameter` を返す。

## Read this when
- `cmoc oracle edit` の TUI 起動条件、プロンプト生成、ユーザー指示の組み込み、起動パラメータの固定値を変更・確認するとき。
- 完全プロンプトの保存先や oracle 専用ファイルアクセス設定との連携を確認するとき。

## Do not read this when
- `cmoc oracle edit` の編集プロンプト本文や oracle 編集規則そのものを確認したいとき。
- TUI 起動以外の agent call パラメータ構築や一般的な prompt builder の挙動だけを調べるとき。

## hash
- 25c98afd0d9508fbe8e1f4fafff2eed65ab69b8d6444eec977d70ea72bbc6f0f
