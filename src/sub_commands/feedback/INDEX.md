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
- Feedback issue の逐次修復から wave の収束、自動 join、publication までを同一 run の状態遷移として制御する実行入口。
- 修復 agent の実差分・structured output・verification を照合し、issue ごとの commit と remediation checkpoint を確定する。
- 封印済み候補の判定根拠、join 後の commit 到達可能性、最終 tree、publication recovery を検証する。
- 観測の集約・表示は report、永続 artifact の検査は runtime_feedback_run_state、判定根拠の比較は decision に委譲する。

## Read this when
- feedback report の新規実行、wave の追加取得と収束条件、自動 join、publication、または中断・失敗後の recovery を調べるとき。
- feedback issue の remediation call、実差分と出力の整合性検証、rollback、commit、checkpoint 保存を追うとき。
- sealed run の join 前後で、採用候補、判定根拠、commit 到達可能性、最終 realization tree の整合性を確認するとき。

## Do not read this when
- 観測の集約・表示や report cut の入力生成だけを調べる場合は report を直接読む。
- 判定状態や判定根拠の比較規則だけを調べる場合は decision を直接読む。
- 永続 run artifact の形式、読み書き、checkpoint の検証だけを調べる場合は runtime_feedback_run_state を直接読む。
- 一般的な run lifecycle、join、indexing、refactor state 同期の実装だけを調べる場合は、それぞれの委譲先を直接読む。

## hash
- 3d7922563fd8777d6682849433fad81558878b457a8738edccc7df8e61a9d7cd

# `report.py`

## Summary
- `cmoc feedback report` の report cut を起点に、raw observation の検証、candidate 集約、issue identity の正規化、machine recurrence の集約、remediation verification、publication または incomplete 診断までを一つの transaction として処理する。
- current active state と固定済み reference、checkpoint、generation、report、pointer の hash・状態整合性を管理し、中断後の再開と安全な publication を担う。

## Read this when
- `cmoc feedback report` の raw observation から active issue、machine aggregate、report cut、checkpoint、generation、current pointer までの処理経路を確認するとき。
- feedback report の issue 同一性判定、reference の固定、verification、正常 publication、incomplete 診断、中断・再開時の状態遷移を変更または調査するとき。

## Do not read this when
- feedback observation の受付や envelope 検証そのものを確認したいときは、観測保存・受付を担当する対象を先に読む。
- normalize issue や remediate issue の agent prompt、Structured Output schema、個別の remediation 判定規則だけを確認したいときは、それぞれの builder・schema・判定対象を直接読む。
- feedback state の共通 path、pointer、generation artifact の形式だけを確認したいときは、共通 state 管理対象を直接読む。

## hash
- eb94d66c031f52e22303f2941e8cad6d9244a088145b458f81812a44962ada0e
