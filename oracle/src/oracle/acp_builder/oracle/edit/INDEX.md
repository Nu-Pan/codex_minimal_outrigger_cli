# `launch_tui.py`

## Summary
- `cmoc oracle edit` の TUI 起動パラメータを構築する oracle src。ユーザー指示を埋め込んだ完全プロンプトを生成・ログ保存し、固定のモデル・権限・実行設定で Codex CLI を起動するための入力を返す。

## Read this when
- `cmoc oracle edit` の TUI 起動処理、完全プロンプトの構成、起動時のモデル・推論強度・ファイルアクセス設定を変更または確認するとき。
- ユーザー指示を含む editor_input ログの保存方法や、TUI 起動用 AgentCallParameter の生成を確認するとき。

## Do not read this when
- oracle file の編集内容そのものや編集担当 agent のプロンプト仕様を変更するときは、関連する prompt builder または oracle 編集処理を直接読む。
- 一般的な ACP パラメータ定義やパス解決の仕様だけを確認するときは、各共有モジュールを直接読む。

## hash
- 58d9240405468082816e1ce919b2afbb2ce1fd09794409fd43b1d1a414359efa
