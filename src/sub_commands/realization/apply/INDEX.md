# `__init__.py`

## Summary
- realization の apply 処理に関する workload を扱うモジュール。apply workload の実装を確認する入口となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。

## hash
- d6d2ca470e50cfd6872e3d6ceaaf3a134b7f0dc8205826c843ca70d79352d5f7

# `fork.py`

## Summary
- `cmoc realization apply fork` の実行を統括し、editing run の作成から realization apply agent の実行、差分検査、commit、joinable/error state 更新、fork report 保存までを担う。
- agent の commit、想定外ファイル変更、遅延 Codex child の書き込みを検出・清掃し、成功時は joinable な成果物として公開し、失敗時は差分を rollback して error report を保存する。
- realization apply fork の CLI runtime と、apply 固有の差分始点・accepted feedback observation・cleanup warning の report 反映を確認する入口である。

## Read this when
- `cmoc realization apply fork` の処理順序、成功・失敗時の run state、差分の許可範囲、commit/rollback、fork report の内容を確認または変更するとき。
- realization apply agent が作成した差分を joinable run として公開する経路や、agent commit・想定外変更・遅延 child を扱う cleanup を調査するとき。

## Do not read this when
- realization apply の仕様や共通 editing run の契約を確認する場合は、対応する oracle/specification または共通 runtime 実装を直接読む。
- fork 以外の realization apply サブコマンドの固有処理だけを確認する場合は、各サブコマンドの実装を直接読む。

## hash
- cbb2acf1b2ac3b46a4b142ee18c71b0e4a5828e445e1ccb18e226b360061d868
