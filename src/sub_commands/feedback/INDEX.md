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
- `cmoc feedback report` の report cut 処理を一つの transaction として実装するサブコマンド固有の状態機械。
- pending observation と active state、repository reference を deterministic に固定し、normalization・全 candidate verification・正常 publication・incomplete 診断・中断再開を処理する。
- feedback state、checkpoint、generation artifact、current pointer、Markdown report、cleanup、および subcommand log の整合性を hash と schema で検証する実行経路の入口。

## Read this when
- `cmoc feedback report` の publication、incomplete 診断、中断・再開、checkpoint 再利用、cleanup、current pointer 切替の挙動を確認または変更するとき。
- feedback observation の validation、agent observation の issue 集約、machine rule の recurrence 集約、issue verification の参照制約を調査するとき。
- feedback report の report cut manifest、generation artifact、active issue、Markdown 出力、primary report fields、publication log の連携を追跡するとき。

## Do not read this when
- feedback observation の envelope や raw store の一般仕様だけを確認する場合は、対応する state/store の実装または oracle を直接読む。
- issue normalization agent や verification agent の prompt・Structured Output schema だけを確認する場合は、対応する builder と schema を直接読む。
- feedback state のデータ構造・artifact 操作・lock・pointer の共通実装だけを確認する場合は、`runtime_feedback_state` を直接読む。
- 他のサブコマンドの実装や通常の Markdown report 描画だけを確認する場合は、この report pipeline ではなく対象モジュールを直接読む。

## hash
- 349007565bcb66666699528be92a8a95b7674ed2b80c21403411db3852d8789f
