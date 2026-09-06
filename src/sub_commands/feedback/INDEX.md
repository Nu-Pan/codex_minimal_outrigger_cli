# `__init__.py`

## Summary
- feedback サブコマンドの実装を担う。feedback サブコマンドの処理を確認・変更するときの入口。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。

## hash
- 314f863a7cbf0d8eb6a2e9f72ee941edfcbbfcc5768f529aed40f09e96968cb9

# `decision.py`

## Summary
- Feedback 判定の再確認に使う repository 入力の固定、判定状態ハッシュ、正式 checkpoint 履歴、循環検知、判定根拠の記録を担う。
- 依存 path の申告に限定せず、読める repository 入力全体を保守的な検証条件として扱う判定処理への入口。

## Read this when
- Feedback の判定根拠をどの入力から構成するか確認したいとき。
- 再確認時の差分、過去 checkpoint の参照、同一判定入力へ戻る循環の検知を調べるとき。
- 判定直後の verification・current evidence と入力状態を、後続処理から独立して記録する方法を確認したいとき。

## Do not read this when
- Feedback の結果分類や利用者向け仕様を確認したいだけで、判定根拠の保存・再確認履歴を扱わないとき。
- 実行状態 artifact の読み書きや Git 入力列挙の個別実装を直接調べる必要があるときは、それぞれの runtime artifact・store・Git 共通処理の対象へ進むとき。

## hash
- 806899c5d09fab6e5b6bec975e51a34631c7f5ccfa119b846c3b60add9600dea

# `recovery.py`

## Summary
- Feedback report の publication 後に、recovery journal を用いて cleanup・session の ready 遷移・隔離 run 資源回収を再開する処理と、明示的な join/abandon による終了との境界を扱う。

## Read this when
- feedback report の正常完了後に cleanup が中断し、同じ report と join tree から finalization を再開・検証したいとき
- feedback run を明示的な join または abandon の対象にしてよいか、その状態遷移と制約を確認したいとき

## Do not read this when
- feedback report の判定・remediation・publication 本体の仕様や実装を確認したいときは、それぞれの decision、remediation、publication 関連対象を直接読む
- feedback state のデータ構造や一般的な report cut 操作だけを確認したいとき

## hash
- f773aa1d190f88c1f8ee6bf1316dea8d5b7dedb83deb678e061d38b31243a712

# `remediation.py`

## Summary
- Feedback observation の issue 修復 wave を実行し、remediation checkpoint と commit を確定する処理を担う。
- 封印済み run の join 成功を recovery し、最終 tree・判定根拠・差分 hash を検証して publication へ渡す。
- commit、rollback、SIGINT 保留、run state 更新など、同一 feedback run の finalization 境界を確認する入口である。

## Read this when
- feedback report の自動修復、wave の再処理、issue ごとの agent 出力と実差分の照合を調べるとき。
- remediation checkpoint、sealed・merged・completion artifact の整合性、join 後の tree 検証を確認するとき。
- feedback run の中断・失敗・publication recovery や、自動 join から report publication までの状態遷移を追うとき。

## Do not read this when
- 観測の収集・集約・表示や report cut の候補生成を調べるときは report を直接読む。
- feedback run artifact の読み書き・形式検証だけを調べるときは runtime_feedback_run_state を読む。
- 判定状態、判定根拠、履歴比較のロジックだけを調べるときは decision を直接読む。

## hash
- f266bff1dbb4e5dcd4db85a94da4d54edeb411a38d994bb097389098df005c2b

# `report.py`

## Summary
- feedback observation を固定済み report cut として検証・正規化・機械集約し、candidate の同一性判断と remediation verification を経て正常 report または incomplete 診断を publication する、`cmoc feedback report` の transaction 実装。
- raw observation、active issue、current repository reference、処理 version、checkpoint、generation、pointer、cleanup を hash 付きで管理し、中断・再開と secret-safe な evidence materialization まで担う。

## Read this when
- `cmoc feedback report` の report cut、candidate 集約、normalization/remediation checkpoint、publication、incomplete 診断、中断復旧の挙動を実装または調査するとき。
- feedback state の current generation、machine aggregate、raw observation、report artifact の整合性や hash、canonical JSON、repository reference の扱いを確認するとき。

## Do not read this when
- feedback observation の受付・envelope 検証だけを調べる場合は、観測保存や受付を直接担うモジュールを読む。
- issue normalization や remediation agent の prompt/schema の詳細だけを調べる場合は、それぞれの builder、schema、agent 実装を直接読む。
- 一般的な report 表示形式や共通 logging、generation state の仕様だけを確認する場合は、対応する oracle または共通 state モジュールを直接読む。

## hash
- 6e78fafac18b91b082c663a6dd08c450255e3afd980cebecaab9c994cce61a84
