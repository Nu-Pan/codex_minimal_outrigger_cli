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
- `cmoc oracle edit` の実行本体として、編集指示の入力・抽出、編集前 indexing、main worktree と active session branch の事前条件確認、同一設定を共有した 2 回の Codex exec 実行、各呼び出し状態の報告、終了処理を統括する。

## Read this when
- `cmoc oracle edit` がどの順序で入力を受け取り、事前検証を行い、oracle 編集 agent call を 2 回起動するか確認したいとき。
- oracle 編集の起動条件（main worktree、`cmoc/session/` branch、active session）や agent call の成功・失敗報告の実装を確認したいとき。

## Do not read this when
- 編集 prompt の内容や oracle 編集契約そのものを確認したいときは、`oracle_edit.md` または prompt builder の実装を直接読む。
- CLI の全体ルーティングや共通サブコマンド実行基盤を確認したいときは、対応する親コマンド・runtime 実装を直接読む。

## hash
- 0035f443b392d1e180a728c0465a73fa363d82007faba70ecbac2214cb5b15c5

# `investigation.py`

## Summary
- `cmoc oracle investigation` の CLI 実行入口と本体を提供する。indexing 前処理と実行状態を設定し、oracle 調査指示の入力編集・収集を経て、read-only の Codex TUI を起動する。
- oracle investigation の実行フローを確認する際の realization implementation 側の入口であり、TUI 起動パラメータの具体的な構築規則は専用 builder 実装へ引き渡す。

## Read this when
- `cmoc oracle investigation` の CLI 起動条件、実行手順、prompt skeleton の準備、エディタ入力の保存・収集、または Codex TUI 起動までの流れを確認・変更するとき。
- oracle investigation における indexing 前処理、実行ステップ管理、設定読込、通知用コマンド名などの呼び出し構成を調べるとき。

## Do not read this when
- oracle investigation の完全な prompt 文面、oracle file の読み取り範囲、または TUI 起動パラメータの固定規則だけを確認したいときは、oracle 側の専用 builder 実装を直接読む。
- oracle investigation の正本仕様を確認・変更するときは、`oracle/doc/app_spec/sub_command/oracle_investigation.md` を直接読む。
- TUI 自体の表示・操作、共通ランタイム、または prompt エディタ共通処理の一般仕様だけを調べるときは、それぞれの専用実装を直接読む。

## hash
- 3146ae750632ef1edd6f7fc67328141eec9370cc679b8a454be3b0635146690a
