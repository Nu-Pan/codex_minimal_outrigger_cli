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
- feedback issue の逐次修復を wave 単位で収束させ、各 issue の実差分・検証結果・判定根拠を checkpoint と commit に確定する。
- 修復済み run の join、merge 成功の recovery、最終 tree の整合性検査、report publication までを一続きの finalization として制御する。
- SIGINT・例外・中断時の run state、進捗 report、rollback、確定済み artifact を管理し、未確定の修復や不正な入力を publication 前に拒否する。

## Read this when
- feedback report の自動修復処理、wave の再実行条件、issue remediation の commit/checkpoint 化を確認するとき。
- feedback run の seal・join・merge・publication、または join 後 recovery の状態遷移と整合性検査を追うとき。
- 修復 agent の structured output、変更 path、verification、decision basis、checkpoint artifact の照合仕様を調べるとき。
- 中断・失敗時の rollback、error 状態、進捗記録、確定済み merge を保持する例外境界を確認するとき。

## Do not read this when
- 観測の集約・候補生成・表示ロジックだけを調べる場合は report を直接読む。
- 判定根拠の比較や issue history、decision state の計算だけを調べる場合は decision を直接読む。
- run artifact の永続化・checkpoint 検証や run join の汎用処理だけを調べる場合は runtime_feedback_run_state、runtime_run_join などの委譲先を直接読む。

## hash
- a081c9101876c2cc278adecaf7d1351e8679a2dd4ee3f0d2fed47407f6b85097

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
