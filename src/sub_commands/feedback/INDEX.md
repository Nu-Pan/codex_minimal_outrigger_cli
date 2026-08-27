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
- `cmoc feedback report` の publication／diagnostic pipeline を担う実装。固定済み report cut を起点に、raw observation の検証、agent・machine candidate の deterministic 集約、normalization と verification checkpoint の再利用、正常な generation/report publication、または incomplete 診断 report の保存までを一つの transaction として処理する。
- report cut では active state、current pointer、repository reference、raw observation の hash を固定し、処理再開時に入力と checkpoint の整合性を再検証する。publication 前後の current pointer 切替、generation artifact 保存、raw・checkpoint cleanup、割り込み・失敗・cleanup 未完了の状態記録もこの module が扱う。
- feedback report サブコマンドの実行入口は `cmoc_feedback_report_impl` で、共通 CLI runner と writer lock を介して事前条件確認から最終 `TerminalResult` までを制御する。candidate の issue identity 判定や verification の詳細は専用 builder・schema、永続 state と artifact 操作の契約は `commons` の runtime module が下位入口となる。

## Read this when
- `cmoc feedback report` の全体処理順序、report cut の固定、再開可能な checkpoint 処理を確認するとき。
- raw observation から issue candidate を作成・集約し、machine recurrence threshold や agent observation の同一性判定を確認するとき。
- verification 結果に基づく正常 publication、incomplete 診断、current pointer 切替、cleanup、割り込み・失敗時の状態遷移を確認するとき。

## Do not read this when
- feedback state の schema、generation・pointer・checkpoint の永続化契約そのものを確認したいときは、対応する `commons.runtime_feedback_state` と oracle 仕様を直接読む。
- normalization または verification agent の prompt、builder、Structured Output schema の詳細を確認したいときは、各 feedback builder と schema を直接読む。
- CLI 共通 runner、subcommand logger、primary report fields などの共通動作だけを確認したいときは、対応する runtime module を直接読む。

## hash
- c588820ada526aa1d88dae4e550b94560e56f46bda4c83c9908fc418176afc4a
