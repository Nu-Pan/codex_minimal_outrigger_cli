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
- `cmoc feedback report` の publication／diagnostic pipeline を一つの transaction として実装する module。固定済み report cut、raw observation と current reference の検証、deterministic candidate 集約、normalization／verification checkpoint の再利用、正常 publication または incomplete 診断を扱う。
- feedback report サブコマンドの状態機械と成果物処理の実装入口であり、report cut の作成・再開から generation、Markdown report、current pointer の publication、publication 後 cleanup までを確認する場合に読む。

## Read this when
- `cmoc feedback report` の全体フロー、report cut の固定・再開、checkpoint 付き normalization／verification、正常 publication または incomplete 診断の挙動を調べるとき。
- feedback observation と active feedback state から candidate・machine aggregate を生成し、current reference を検証して publication する処理を変更するとき。
- publication 前後の interruption、failure、cleanup、current pointer の状態遷移や subcommand log event を確認するとき。

## Do not read this when
- feedback state の正本スキーマやサブコマンドの詳細仕様を確認する場合は、対応する oracle file を直接読む。
- 個別の normalization／verification prompt builder、runtime state/store、report rendering helper の単独仕様を調べる場合は、該当する直接の実装または oracle file へ進む。

## hash
- 906cad8e8ce596929a9baa261753805a4dea9c28f9a35d83891cb4b15da9dd5e
