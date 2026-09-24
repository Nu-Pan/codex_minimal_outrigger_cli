# `__init__.py`

## Summary
- session subcommand 群の Python package 宣言で、内容は説明 docstring のみです。各操作の処理は `fork.py`、`join.py`、`abandon.py` にあり、CLI command tree の確認は `main.py` が対象です。

## Read this when
- `sub_commands.session` の package 宣言や import 境界を確認するとき。

## Do not read this when
- session の fork・join・abandon の動作を調べるときは、該当する操作モジュールを直接読む。
- CLI command tree への登録を調べるときは、`main.py` を読む。

## hash
- bfd8539ef9776e0e27e2e2e0d6365626dc832eb3abf90403affec4b29f1f8364

# `abandon.py`

## Summary
- `cmoc session abandon` を実行し、active session を home branch に取り込まず破棄する処理を担う。
- 事前条件の確認、home branch への切替、session state と branch の cleanup、失敗時の rollback、および primary report の更新を扱う。

## Read this when
- session abandon の事前条件・状態遷移・cleanup・rollback の実装や障害を調べるとき。
- abandon の実行結果や primary report への反映を追うとき。

## Do not read this when
- session の新規作成や home branch への join が主題なら、それぞれ fork または join の処理を読む。
- 未 join の編集 run だけを破棄するなら、run abandon の処理を読む。

## hash
- 1f77a2d356b51d2ef653868dbaf4661146a20bf1ab74457ee31e8c353871cde9

# `fork.py`

## Summary
- 現在の通常の local branch を起点に session branch と active state を作成する、session lifecycle の開始処理です。作成前提の確認と、失敗時の後始末も扱います。

## Read this when
- 通常の local branch から新しい session を開始する作業や、fork の作成条件・失敗時の処理を確認するとき。

## Do not read this when
- 既存 session の home branch への統合や破棄を扱うときは、それぞれ join または abandon の実装を直接確認してください。

## hash
- fa5f8734a893ac8545c67fa88c0fb50107b2e37a49b4b542812966d365dfad2e

# `join.py`

## Summary
- 現在の active session branch を、session state が示す home branch に merge して session を完了する処理を担う。
- merge conflict の解消依頼と結果確認、session state の更新、安全性を確認した session branch cleanup までを扱う。

## Read this when
- `cmoc session join` の実際の処理、競合時の解消、完了後の状態や cleanup を確認・変更するとき。

## Do not read this when
- session join の正本仕様を確認・変更するときは、その仕様を直接読む。
- session branch の作成や破棄を扱うときは、`cmoc session fork` または `cmoc session abandon` の処理へ進む。
- 編集 run の取り込みを扱うときは、別の `cmoc run join` の処理へ進む。

## hash
- f5e66b3bd1eddafe6db63d5dc50c2382e13e25be362483fda5d765d0148c3e3e
