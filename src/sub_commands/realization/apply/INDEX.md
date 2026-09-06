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
- `cmoc realization apply fork` の実行入口として、realization apply 用の editing run を作成し、oracle 差分範囲を固定して追従 agent を実行する。
- agent の変更と生成された INDEX.md を検査・commit し、問題がなければ run を joinable として fork report に保存する。
- agent の異常終了、想定外差分、agent による commit、cleanup 失敗などを error state と report に記録し、join または abandon へ案内する。

## Read this when
- realization apply fork の実行手順、差分の始点 commit、agent 実行後の変更検査・commit、joinable/error run の状態遷移を確認するとき。
- fork report の内容、cleanup warning、accepted feedback observation の反映、agent commit や遅延 child の隔離処理を調べるとき。

## Do not read this when
- realization apply の agent 起動パラメータそのものを確認したいときは、launch_exec の対象へ直接進む。
- editing run の共通ライフサイクルや run の join/abandon 実装を確認したいときは、runtime_run_lifecycle などの共通実装へ直接進む。
- INDEX.md 生成の一般仕様や CLI の利用者向け仕様だけを確認したいときは、indexing または対応する app_spec 文書へ直接進む。

## hash
- 0fb56bca8d02ec46726835f1854370a90d49ced44af84e607cf75ffd0db3c47e
