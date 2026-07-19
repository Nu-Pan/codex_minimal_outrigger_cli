# `__init__.py`

## Summary
- `cmoc oracle edit fork` 用の builder adapter。対象コマンドの fork 編集処理に関する adapter の入口。

## Read this when
- `cmoc oracle edit fork` の builder adapter の責務や実装入口を確認するとき。

## Do not read this when
- `cmoc oracle edit fork` 以外のコマンドや、builder adapter 以外の処理を確認するとき。

## hash
- c3bcc517bde2535db95df0ec1c9cba02cf62f8ed19805d6d8b83524d02f37df0

# `launch_exec.py`

## Summary
- oracle edit fork の launch_exec 用 builder を realization 側へ再公開する薄い adapter。元の builder を import し、公開対象を限定する。

## Read this when
- oracle edit fork の launch_exec パラメータ builder の realization 側エントリーや再公開経路を確認するとき。

## Do not read this when
- builder の正本仕様や実装詳細を確認したいときは、再公開元の oracle 側ファイルを直接読む。
- launch_exec 以外の builder や fork 処理を調べるとき。

## hash
- d4d9ea007e18526430ce29327b14db86b517198c283e3582591f14e2ac29ba4d
