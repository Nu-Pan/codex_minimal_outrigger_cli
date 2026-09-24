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
- `cmoc oracle edit` の CLI 実行を制御し、編集指示の入力、事前 indexing、active session branch の確認、2 回の Codex exec 起動と状態記録をつなぐ。
- oracle 調査の TUI 実行経路とは異なり、編集用 exec の実行順序と前提条件を調べる際の入口となる。

## Read this when
- `cmoc oracle edit` の指示入力から exec 起動までの手順や順序を変更・確認するとき。
- main worktree と active session branch の検証、または indexing の事前処理を調べるとき。
- 2 回の agent call で共有する設定や起動パラメータ、各 call の状態記録を変更・確認するとき。

## Do not read this when
- 編集 agent に渡す prompt の契約や内容、exec 起動パラメータの構築を変更するときは、oracle の正本仕様または builder の担当箇所から確認する。
- prompt editor の予約・編集・保存・抽出の共通動作を変更するときは、その共通処理の担当箇所から確認する。
- コマンドの登録・振り分け、共通の実行 lifecycle やレポート描画、oracle 調査の TUI 動作を変更するときは、それぞれの担当箇所から確認する。

## hash
- 0035f443b392d1e180a728c0465a73fa363d82007faba70ecbac2214cb5b15c5

# `investigation.py`

## Summary
- `cmoc oracle investigation` の入力受付から Codex TUI 起動までを組み立てる CLI 実行層です。
- 調査用プロンプトと起動パラメータの内容は専用 builder に委譲し、editor 入力と runtime の処理をつなぎます。

## Read this when
- `cmoc oracle investigation` の指示入力、起動前処理、または TUI 起動までの流れを確認するとき。
- 調査用の完全プロンプトを editor に渡し、入力された指示で TUI を起動する連携を追うとき。

## Do not read this when
- 調査の意味上の範囲や正確な prompt 文面、起動パラメータの決め方を確認するときは、専用 builder または調査コマンドの正本仕様を直接読む。
- oracle file の編集フローを確認するときは `cmoc oracle edit` の実装や正本仕様へ進む。
- 共通の editor 入力処理や CLI runtime の内部動作が目的なら、それぞれの共通実装を直接読む。

## hash
- 3146ae750632ef1edd6f7fc67328141eec9370cc679b8a454be3b0635146690a
