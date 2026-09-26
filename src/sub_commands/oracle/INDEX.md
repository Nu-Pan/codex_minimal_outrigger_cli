# `__init__.py`

## Summary
- oracle 系サブコマンドをまとめる Python package の境界を示す初期化モジュールです。

## Read this when
- oracle 系サブコマンド群の package としての位置づけを確認するとき。

## Do not read this when
- oracle edit や oracle investigation の処理や起動動作を調べるときは、各サブコマンドの実装を直接読んでください。

## hash
- 2c8110c7811042f7162e1264e7027bb2d801f4687eb66f48f1668402c8eeb0df

# `edit`

## Summary
- このサブ階層には現在、独立した Oracle 編集処理がありません。編集コマンドの挙動を調べる入口は、実処理を担う Oracle 編集コマンド実装です。

## Read this when
- このサブ階層に固有の実装責務があるかを確認するとき。現時点では、ここに独立した処理は置かれていません。

## Do not read this when
- Oracle 編集コマンドの挙動を調べる場合は、実処理を担うコマンド実装へ直接進んでください。
- 他の Oracle サブコマンドの挙動を調べる場合は、それぞれのコマンド実装へ直接進んでください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `edit.py`

## Summary
- `cmoc oracle edit` の CLI 実行を制御し、編集指示と起動条件を確定してから、共通の設定と起動パラメータで Codex exec を2回実行する。各呼び出しの成否を primary report に反映する。

## Read this when
- `cmoc oracle edit` の入力から実行までの流れや、2回の編集呼び出しで入力・設定・起動パラメータを共用する制御を調べるとき。
- 編集起動に必要な main worktree、cmoc session branch、active session の条件を調べるとき。

## Do not read this when
- 編集 agent の prompt やアクセス境界を変更するときは、prompt を構築する oracle 側の共通 builder を読む。
- エディタ用入力の予約、検証、起動、handoff の共通動作を変更するときは、共有 editor-input の実装を読む。
- read-only の oracle investigation が TUI を起動する流れを調べるときは、そのコマンドの実装を読む。

## hash
- 66ad9c312a541becae6d0e387f2962aa8dea6cd2a5ac7b466ced332ad1a4f143

# `investigation.py`

## Summary
- `cmoc oracle investigation` の CLI 実行層として、oracle 文書の検索範囲を設定し、エディタでの指示入力から read-only Codex TUI の起動までをつなぐ。
- このコマンドの前処理、実行ステップ、worktree 設定の読み込みを担い、調査用の完全な prompt と起動パラメータの内容は専用 builder に委ねる。

## Read this when
- oracle 調査コマンドの指示入力、実行前処理、検索範囲の指定、または TUI 起動までの流れを追う・変更する場合。
- このコマンドの runtime 設定や、指示を TUI に渡す統合方法を確認する場合。

## Do not read this when
- 完全 prompt の文面、oracle file の参照制約、handoff の指示、または TUI 起動パラメータの選択を変更する場合は、調査用 TUI parameter builder を直接確認する。
- エディタ入力の予約・編集・回収の共通動作を変更する場合は、prompt-editor 入力の共通実装を直接確認する。
- 共有 CLI runtime の実行管理や TUI 起動処理そのものを変更する場合は、該当する runtime 実装を直接確認する。

## hash
- 768ef39e345a27881f4cce4b0330cb761ef18db3c85a7339215b13796b036755
