# `__init__.py`

## Summary
- `cmoc oracle edit` サブコマンドの main worktree 向け TUI 起動処理を担当する実装。プロンプト編集入力の収集、oracle 編集用 TUI パラメータ構築、indexing preflight、Codex TUI 起動までをオーケストレーションする。
- 起動前に main worktree、active な `cmoc/session/` branch、active session、clean worktree を検証するため、oracle edit の CLI 実行経路や TUI 起動条件を確認する際の入口となる。

## Read this when
- `cmoc oracle edit` の CLI runtime、TUI 起動、プロンプト入力、起動前提条件を変更・調査するとき
- main worktree と session branch の検証、oracle 編集 instruction の受け渡しを確認するとき

## Do not read this when
- oracle 編集対象の選択・編集ロジック自体を調査するときは、oracle edit 用の builder や対象側の実装を直接読む
- 共通 CLI runtime、git 状態検証、runtime state の詳細だけを調査するときは、それぞれの共通モジュールを直接読む

## hash
- 34626c438ec6e03563f6a3c961b665d563a901b1c12514f8047b0ad33eddc235
