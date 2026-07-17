# `launch_tui.py`

## Summary
- `cmoc oracle edit` 用の TUI 起動パラメータを構築する実装。ユーザー指示を含む完全プロンプトを生成し、cmoc 管理下の TUI ログへ保存したうえで、固定モデル・推論強度・ファイルアクセスモード・実行前インデックス作成設定を持つ `AgentCallParameter` を返す。

## Read this when
- `cmoc oracle edit` の TUI 起動条件、プロンプト生成、ユーザー指示の組み込み、起動パラメータの固定値を変更・確認するとき。
- 完全プロンプトの保存先や `oracle` 専用ファイルアクセス設定との連携を確認するとき。

## Do not read this when
- `cmoc oracle edit` の編集プロンプト本文や oracle 編集規則そのものを確認したいときは、プロンプト生成元や関連する oracle 定義を直接読む。
- TUI 起動以外の agent call パラメータ構築や一般的な prompt builder の挙動だけを調べるとき。

## hash
- 82be60b4ba26dbf5fdaa9c5bebc73f26f2d8faf5a4b6a1134225d3637defe248
