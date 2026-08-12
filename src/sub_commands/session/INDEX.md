# `__init__.py`

## Summary
- session サブコマンドの実装パッケージ。session サブコマンドに関する実装を確認する際の入口となる。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。

## hash
- bfd8539ef9776e0e27e2e2e0d6365626dc832eb3abf90403affec4b29f1f8364

# `abandon.py`

## Summary
- `cmoc session abandon` サブコマンドの実装。active session を検証し、home branch へ切り替えた後に session branch と state を abandoned としてクリーンアップする。失敗時は state・branch を可能な限りロールバックし、結果または cleanup error を表示する。

## Read this when
- `cmoc session abandon` の事前条件、branch 切り替え・削除、state 更新、cleanup 失敗時の復旧処理を変更・調査するとき。

## Do not read this when
- session の開始・継続・完了など、abandon 処理以外の session サブコマンドを変更・調査するときは、各サブコマンドの実装を直接読む。

## hash
- 4409f62cddd5b057e30bd1769b75c2bbddcfdcb40636b89b68e7075effa1c815

# `fork.py`

## Summary
- 現在の local branch から cmoc 管理対象の session branch と state file を作成する CLI 実装。active session の重複確認、clean worktree 検証、session-id 衝突回避、branch/state 作成、結果表示を担う。作成途中の失敗時には branch と state file をロールバックし、復旧情報を含むエラーを報告する。

## Read this when
- `cmoc session fork` の branch 作成、session state 保存、session-id 生成、競合制御、失敗時ロールバックの挙動を変更・調査するとき。

## Do not read this when
- session の join・abandon など、fork 実行以外のライフサイクル処理を確認するとき。
- session state のデータ構造や共通 runtime 関数の仕様を直接確認する必要があるとき。

## hash
- 9f402913f831a35fc4e90001691620f8eed657cda8878eeb7ae91320860736e7

# `join.py`

## Summary
- `cmoc session join` の CLI 実装本体。active な session branch の事前条件を検証し、session home branch へ merge した後、状態を joined に更新して session branch を安全条件付きで削除し、結果と警告を表示する。
- merge conflict 発生時は、conflict 対象の列挙、Codex による解消依頼、対象外差分と marker 外変更の拒否、marker 残存確認、stage、merge commit までを管理する。Git path の NUL framing、conflict context の保持、path fingerprint による変更検査など、conflict 解消の安全境界も定義する。

## Read this when
- `cmoc session join` の実行条件、merge 先、session 状態更新、branch 削除条件、完了時の出力を確認するとき
- session join の merge conflict 解消フロー、Codex 呼び出しの許可範囲、不要な差分の拒否条件を調査・変更するとき
- session join に関する CLI runtime、Git 操作、状態永続化、エラーレポート先の挙動を確認するとき

## Do not read this when
- session の作成・開始・離脱など、session join の merge 処理を直接扱わない subcommand を調査するとき
- conflict resolution parameter の生成規則そのものを確認したいときは、conflict resolution builder または prompt 定義を直接読む
- 共通の Git status、runtime 結果、状態管理 API の仕様だけを確認する場合は、該当する共通実装・仕様を直接読む

## hash
- f4ed6fa516be3047aec6c46fcc0d1b30fc5679ab80198c0927c2e49f89cb7975
