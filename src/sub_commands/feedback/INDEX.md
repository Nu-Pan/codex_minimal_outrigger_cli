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
- `cmoc feedback report` サブコマンドの publication／diagnostic pipeline を実装するモジュール。固定した report cut に対して raw observation の検証、candidate の deterministic 集約・normalization、全 candidate の verification、正常な active generation／Markdown report の publication、または incomplete 診断 report の保存までを一つの transaction として扱う。中断・失敗時の checkpoint 再開、current pointer の整合性確認、artifact の hash 検証、publication 後 cleanup、ログ記録も担う。feedback report の処理順序や checkpoint／publication の実装を確認する入口であり、feedback state のデータ契約そのものを確認する場合は対応する state 仕様、agent 入出力契約を確認する場合は normalize／verify builder と schema を読む。

## Read this when
- `cmoc feedback report` の実行フロー、report cut、normalization、verification、publication、incomplete 診断の挙動を変更・調査するとき
- feedback report の中断再開、checkpoint の再利用、current pointer の切替、artifact cleanup、hash 整合性を確認するとき
- raw observation や active issue がどのように candidate・generation・Markdown report へ変換されるかを確認するとき

## Do not read this when
- feedback state の正本データ構造や永続化契約だけを確認する場合は、先に対応する feedback state 仕様を読む
- normalization／verification agent の prompt、Structured Output schema、builder の契約だけを確認する場合は、それぞれの builder・schema を直接読む
- report の表示形式だけを確認する場合は、render 関数または対応する仕様を直接読む

## hash
- 84be1c92fe983a23839f545240e0a21ce5ac19b443c79c59b8231780d088c260
