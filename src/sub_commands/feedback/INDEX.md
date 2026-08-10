# `__init__.py`

## Summary
- feedback サブコマンドの実装を担う。feedback サブコマンドの処理を確認・変更するときの入口。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。

## hash
- 314f863a7cbf0d8eb6a2e9f72ee941edfcbbfcc5768f529aed40f09e96968cb9

# `report.py`

## Summary
- `cmoc feedback report` の active-state publication pipeline を実装するサブコマンドモジュール。固定済み report cut を入力として、raw observation の検証、agent／machine candidate の deterministic 集約、必要な normalization と全 candidate の verification、generation・Markdown report の生成、current pointer の切替、publication 後の cleanup までを一つの再開可能な transaction として扱う。
- report cut manifest、processing／publication 状態、normalization・verification checkpoint、current state と repository reference の hash を用いて、中断・失敗・再開時の入力固定と成果物整合性を検証する。machine rule には 30 日 window、日次 bucket、bounded digest、allowlist threshold を適用し、agent observation には candidate identity normalization を適用する。
- このファイルは `cmoc feedback report` の CLI 実行フローと report publication の責務を確認するときの入口であり、candidate の normalization／verification parameter の詳細は対応する builder と Structured Output schema、active state・artifact 操作の詳細は `commons.runtime_feedback_state`、raw observation の保存・検証の詳細は `commons.runtime_feedback_store` を読む。

## Read this when
- `cmoc feedback report` の実行前提、report cut の固定、checkpoint 再利用、candidate 集約、verification、generation／report publication、current pointer 切替の挙動を確認・変更するとき。
- feedback report の中断・失敗・再開時に、どの入力と成果物を hash／reference で固定するかを確認するとき。
- machine feedback rule の recurrence 集約や agent observation の issue identity normalization の処理入口を調べるとき。

## Do not read this when
- normalization agent に渡す parameter やその Structured Output 契約だけを確認したい場合は、対応する feedback normalization builder／schema を直接読む。
- verification agent の parameter、出力 schema、postcondition 契約だけを確認したい場合は、対応する feedback verification builder／schema を直接読む。
- active state、generation artifact、pointer、cleanup の共通データ操作だけを確認したい場合は、`commons.runtime_feedback_state` を直接読む。
- raw observation の保存、canonical JSON、path、masking、publication lock の共通処理だけを確認したい場合は、`commons.runtime_feedback_store` を直接読む。

## hash
- 7885c875f38a1b0f8cc72996603e79887e466ce9887eecc8d98b882f96bc7652
