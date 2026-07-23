# `__init__.py`

## Summary
- `cmoc oracle edit` サブコマンドの実行入口。入力された oracle 編集指示を受け取り、起動条件を検証したうえで Codex TUI を main worktree から起動する。

## Read this when
- `cmoc oracle edit` の CLI 起動経路、入力収集、TUI 起動パラメータ、起動前検証を変更・調査するとき。

## Do not read this when
- oracle 編集指示の具体的な仕様や TUI パラメータ生成処理だけを確認したいときは、参照されている oracle 仕様または `launch_tui` 実装を直接読む。

## hash
- 476a738e23265d2f782dbf5646861067f56b647d0f4ad96cdba6ff6e2e541c57
