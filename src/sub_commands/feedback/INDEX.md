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
- Feedback 判定の入力状態を固定し、検証結果と再確認履歴を結び付ける。
- tracked・未 ignore ファイルと oracle／realization ファイルを対象に、内容と Git mode のハッシュを作成する。
- Git metadata など判定根拠から除外する対象を判定し、過去 checkpoint との入力差分や非収束サイクルを検出する。

## Read this when
- Feedback の判定根拠に含める repository 入力、ファイルハッシュ、Git metadata の除外条件を確認するとき。
- 同じ candidate identity の checkpoint 履歴、再確認理由、過去結果、入力状態の変化を追跡するとき。
- remediation 後に同じ判定入力へ戻る循環や inconclusive 判定の根拠を確認するとき。

## Do not read this when
- Feedback の候補収集や MCP への報告方法だけを確認したいとき。
- run artifact の保存・読み出しや canonical JSON／SHA-256 の共通実装を直接確認すべきとき。
- 判定ロジックではなく、oracle／realization ファイルの所有 repository 分類そのものを確認したいとき。

## hash
- 7fd71b4bac5a2d74cb53e78434cd540fac99cd6331d2dc1dfc3d174fa05817dc

# `recovery.py`

## Summary
- feedback publication 後の finalization journal に基づく cleanup・状態遷移・隔離 run 資源回収を確定する処理と、手動終了時の report cut 破棄を扱う。
- feedback run について、自動 join 済みなら明示 join/abandon を拒否し、未 join の明示終了では監査記録を残して work artifact のみを破棄する境界を提供する。

## Read this when
- feedback report の publication 後に cleanup を再開・復旧する処理、finalization journal の検証、session/run 状態の ready/error 遷移を確認したいとき。
- feedback run の明示 join/abandon が許可される条件や、手動終了時に raw/current と監査用 checkpoint をどう扱うかを確認したいとき。

## Do not read this when
- feedback report の判定・remediation・publication そのものの仕様や処理を確認したいときは、対応する decision/remediation/publication の対象を直接読む。
- 一般的な run lifecycle や join 操作の共通実装だけを調べるときは、run lifecycle/join の共通対象を直接読む。

## hash
- 69e04af943a1db08bab64464419b23ec2fa9d39ad79a788ed3b8fbc4eddfe230

# `remediation.py`

## Summary
- feedback issue の逐次修復から自動 join、publication までを一続きの run 状態遷移として制御する。
- 観測の取り込み、wave ごとの候補判定、remediation agent の実差分検証・checkpoint 化、seal、merge、join 後検証、report publication と recovery を担う。

## Read this when
- feedback report の新規修復処理、自動 join、publication、SIGINT・例外時の recovery、または remediation checkpoint と判定根拠の整合性を確認・変更するとき。
- wave loop の収束条件、候補ごとの remediation 実行、正式 checkpoint の選択、sealed run の join 成功確認を追う必要があるとき。

## Do not read this when
- 観測の集約・表示や report 生成そのものの仕様・実装を確認したいときは report を読む。
- 永続的な feedback run artifact の形式・読み書き・checkpoint 検証だけを確認したいときは runtime_feedback_run_state を読む。
- 判定根拠の比較ロジックだけを確認したいときは decision を直接読む。

## hash
- 5cf2cee7a5c69ff765889b2c63e265919ea51cba7fac75e57ba1081403f08776

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
