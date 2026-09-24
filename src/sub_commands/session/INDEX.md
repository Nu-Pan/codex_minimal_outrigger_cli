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
- 現在の session branch を記録済み home branch に merge し、session の完了と安全な branch cleanup まで行う CLI 処理を担う。
- join 固有の競合解消呼び出しも含むため、merge、session state 更新、完了後 cleanup の実装を調べる入口となる。

## Read this when
- active session を home branch に取り込んで完了するコマンドの動作や変更箇所を確認するとき。
- session join 中の競合解消、joined state への更新、条件付き branch cleanup を調べるとき。

## Do not read this when
- session branch の新規作成と state 初期化を調べるときは、fork の処理へ進む。
- home branch に merge せず session を破棄する動作を調べるときは、abandon の処理へ進む。
- session lifecycle を介さない一般的な Git merge の動作を調べるとき。

## hash
- 3d6413b6e1023842a5a07d50f4a24357af4c697fa6e2db14f327bdd35546c614
