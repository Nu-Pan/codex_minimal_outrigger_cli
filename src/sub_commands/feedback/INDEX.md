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
- `cmoc feedback report` の active-state publication pipeline を実装するサブコマンド本体。固定済み report cut を起点に、raw observation の検証、agent/machine candidate の deterministic 集約、normalization・verification checkpoint の再利用、report・generation artifact の生成、current pointer の切替、publication 後の cleanup までを一つの transaction として処理する。
- main worktree、active session branch、ready run state などの事前条件を検査し、writer lock 下で中断・失敗・publication 再開を含む状態遷移を管理する。raw observation や repository reference の hash、canonical JSON、schema、secret masking を検証して固定入力と成果物の整合性を保つ。
- agent observation の issue 同一性判定には normalization agent call、全 candidate の現況判定には verification agent call を用い、結果を正式な checkpoint として保存・再検証する。machine rule については recurrence window、日次 bucket、distinct scope/agent-call threshold に基づき集約する。
- 未解決 issue から active generation と Markdown feedback report を描画し、generation manifest・report・cleanup 情報を固定したうえで current pointer を publication する。ログ、CLI 表示、cleanup failure warning も担当する。

## Read this when
- `cmoc feedback report` の処理フロー、report cut、candidate 集約、normalization/verification、publication、resume/interruption の挙動を調べるとき
- feedback active state、current pointer、generation artifact、checkpoint、raw observation の整合性や hash 検証を確認するとき
- machine feedback rule の recurrence threshold や report の Markdown 出力内容を確認するとき

## Do not read this when
- feedback observation の保存・入力 envelope・secret masking など store 共通処理だけを調べるときは、feedback store の実装を直接読む
- issue normalization や verification の agent parameter・Structured Output schema の契約だけを調べるときは、対応する builder と oracle schema を直接読む
- active state や generation artifact の共通永続化 API の詳細だけを調べるときは、`runtime_feedback_state` を直接読む

## hash
- 89bf5186d85804891a2fbc92367bc5eb6731a3a32236778a0b8096d4accd2c32
