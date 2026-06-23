# `__init__.py`

## Summary

- `commons` package marker です。
- cmoc の shared runtime helper 群を `src/commons` 配下へ置くための package 初期化ファイルです。

## Read this when

- `commons` package の存在理由や import 境界を確認したいとき。
- shared helper の配置規則に関する package 構造を確認したいとき。

## Do not read this when

- runtime helper の実装内容を確認したいとき。
- CLI command callback や subcommand implementation の処理を追いたいとき。

## hash

- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary

- CLI 実行時の git 操作、最小 session state schema と後方互換読み込み、`.cmoc` ignore 保証、config 永続化、エラー整形、INDEX ハッシュ補助をまとめる shared runtime 実装ファイルです。
- `src/main.py` や `src/sub_commands/` から呼ばれる副作用のある処理と、テストしやすい純粋寄りの helper を置いています。
- session/apply 状態ファイルの読み書きや共通の事前条件確認を追う入口です。

## Read this when

- CLI サブコマンドの git 事前条件や状態ファイル形式を確認したいとき。
- `.cmoc` を git 追跡対象外にする処理、`.cmoc/config.json` の読み書き、structured markdown error の生成を確認したいとき。
- `src/main.py` や `src/sub_commands/` から呼ばれる共通処理を調べたいとき。

## Do not read this when

- Typer のコマンド登録や stdout の文面だけを確認したいとき。
- prompt builder や oracle/src に対応する純粋な仕様断片だけを確認したいとき。
- 個別の config 既定値や path model API だけを直接追いたいとき。

## hash

- bf40bf55cbab549545d9769272a675971c84b7811dc4bc9e7a5237c5e0bfc8bd
