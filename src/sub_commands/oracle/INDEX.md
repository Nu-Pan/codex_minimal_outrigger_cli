# `__init__.py`

## Summary
- oracle 系サブコマンドをまとめる package の境界を示す。oracle サブコマンド群への入口として扱う。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。

## Do not read this when
- 個別の oracle サブコマンド実装の詳細を確認するとき。

## hash
- 2c8110c7811042f7162e1264e7027bb2d801f4687eb66f48f1668402c8eeb0df

# `edit`

## Summary
- 編集関連の実装ファイルを含まない空のディレクトリです。現時点で下位要素へのルーティング先はありません。

## Read this when
- このディレクトリに編集関連ファイルが追加されたか確認するとき。

## Do not read this when
- Oracle サブコマンドの実装を調査するとき。親ディレクトリの実装ファイルを直接確認してください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `edit.py`

## Summary
- `cmoc oracle edit` サブコマンドの実行フローを担う実装。入力された oracle 編集指示を編集・抽出し、本命の oracle 編集 agent call と、成功後に続く仕様削減 agent call を順序どおり実行する。main worktree、active な cmoc session branch など本命起動前提の検証もここで行う。

## Read this when
- `cmoc oracle edit` の CLI 実行フロー、prompt 編集入力の収集、oracle 編集 agent call の起動条件や実行順序を確認するとき。
- 本命 agent call と仕様削減 agent call の状態報告、失敗時の扱い、subcommand step の進行を変更・調査するとき。
- oracle 編集処理が main worktree または active な cmoc session branch を要求する理由と検証箇所を確認するとき。

## Do not read this when
- oracle 編集 prompt の具体的な契約や最終状態の仕様を確認したいだけの場合は、参照コメントで示される oracle 編集仕様を直接読む。
- prompt 編集入力の予約・編集・抽出・確定処理の詳細だけを確認したい場合は、`commons.prompt_editor_input` の実装を直接読む。
- agent 起動パラメータの構築規則だけを確認したい場合は、`acp.builder.oracle.edit.launch_exec` の実装を直接読む。
- CLI 共通の実行制御、設定読込、セッション状態管理、報告更新の詳細だけを確認したい場合は、それぞれの `cmoc_runtime` または `commons` の実装を直接読む。

## hash
- 3fea2c4033a83d2e9495d8289341e4208205a0549b40ec929d9f7814d63989fe

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの read-only TUI 実行入口。oracle 調査指示の入力受付、完全な調査プロンプトの構築、設定済みの Codex TUI 起動までを CLI runtime 経由で調整する。oracle investigation の CLI フローやプロンプト編集・TUI 起動処理を確認するときの入口。

## Read this when
- `cmoc oracle investigation` の CLI 実行フローを変更・調査するとき
- oracle 調査指示の編集、プロンプト skeleton の生成、Codex TUI 起動の連携を確認するとき
- このサブコマンドの preflight、進捗段階、実行時設定の扱いを確認するとき

## Do not read this when
- oracle investigation の調査契約や prompt 内容そのものを確認したいとき
- TUI 起動パラメータの詳細実装を確認したいとき
- 共通の prompt editor 入出力処理だけを確認したいとき

## hash
- b3511825621dd0ec025ea9cd1f9a1cffc0cf67f11581636bb480c9d62cb3501a
