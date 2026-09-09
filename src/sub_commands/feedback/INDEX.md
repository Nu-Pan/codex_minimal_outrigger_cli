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
- Feedback 判定の根拠状態と再確認履歴を構築する実装。repository 入力の内容・mode をハッシュ化し、判定入力、過去 checkpoint、再確認時の変更点、循環状態、検証結果を後続処理へ結び付ける。

## Read this when
- Feedback の判定根拠が何を入力として固定・除外するか確認したいとき
- 判定結果の再確認、過去 checkpoint との比較、非収束サイクルの診断を調べるとき
- decision basis や canonical hash による入力状態の識別を変更・検証するとき

## Do not read this when
- Feedback の候補分類や結果分類そのものの仕様を確認したいときは、先に正本仕様を読むべき場合
- checkpoint の保存形式や manifest の管理処理だけを調べるとき
- Feedback 実行全体の CLI フローや remediation の適用処理を調べるとき

## hash
- 437ac190f3519c7047e08a5b4abbac2256a6fad3474ac017156108b11f26054e

# `recovery.py`

## Summary
- Feedback report の publication 後に、finalization journal を用いて cleanup、状態遷移、隔離資源回収を確定する処理。
- 中断後の finalization 再開と、report・session・run・join evidence の整合性検証を扱う。
- 自動 join 済み feedback run の明示 join/abandon を拒否し、明示終了時は監査記録を残して work artifact を破棄する入口。

## Read this when
- Feedback report の publication 後 cleanup、recovery、ready 遷移、run worktree 回収を確認したいとき。
- finalization journal の検証条件や、cleanup 失敗時の error 状態遷移を調べたいとき。
- feedback run に対する明示 join/abandon の可否、または手動終了時の後処理を確認したいとき。

## Do not read this when
- Feedback report の判定や正常 publication の内容を調べるとき。
- Feedback run の一般的な lifecycle、join 実装、または worktree 操作そのものを調べるとき。

## hash
- 0f934ef6ab4862779c72ca07f413807a9d4251f1ad9da0193fab9dfe4e85d020

# `remediation.py`

## Summary
- feedback issue の逐次修復を wave 単位で収束させ、正式 checkpoint の検証、自動 join、publication、同一 run の recovery までを一続きで制御する。

## Read this when
- feedback report の remediation 実行、issue ごとの実差分・verification・decision basis の照合、wave の再処理条件を確認したいとき。
- sealed な feedback run の merge 成功確認、join 後の到達可能性・最終 tree 検査、report publication または publication recovery の処理を確認したいとき。

## Do not read this when
- 観測の収集・候補生成・レポート表示の実装だけを確認したいときは report を直接読む。
- feedback run の永続 artifact の読み書き・検証だけを確認したいときは runtime_feedback_run_state を直接読む。
- 判定状態や decision basis の比較ロジックだけを確認したいときは decision を直接読む。

## hash
- 7d170960fb63ea7d64a7e20e441e315e35e3c0873b11fa325673b7bbcc80e57e

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
