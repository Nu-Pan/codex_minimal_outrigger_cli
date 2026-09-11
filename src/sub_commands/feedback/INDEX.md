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
- feedback issue の逐次修復から、自動 join、commit・rollback、finalization、publication、recovery までを同一 run の状態遷移として制御する実装。
- 観測の集約・表示、判定根拠の比較、永続 artifact の検査を下位モジュールへ委譲し、修復 checkpoint と merge 後の整合性を検証する。

## Read this when
- feedback report の実行経路、自動修復 wave、issue commit、run の join または publication を調べるとき。
- feedback run の中断・失敗・SIGINT、rollback、recovery、finalization の状態遷移を確認するとき。
- 修復結果の structured output、changed paths、decision basis、checkpoint、merge 後 tree の検証箇所を探すとき。

## Do not read this when
- 観測の読み取り・集約や表示ロジックだけを調べるときは report を直接読む。
- 判定根拠の比較・issue history・decision state の計算だけを調べるときは decision を直接読む。
- 永続 run artifact の形式や検証だけを調べるときは runtime_feedback_run_state を直接読む。
- feedback report 以外の一般的な run join、indexing、refactor state 同期の仕様だけを調べるとき。

## hash
- 1509d830c51a5b09daf1fe909a18dd59f95ffecb905de754bbbccf075a579aad

# `report.py`

## Summary
- feedback report サブコマンドの publication／diagnostic pipeline を担い、固定済み report cut に対する deterministic processing、candidate の normalization・verification、正常 publication、incomplete 診断、checkpoint 再開を一つの transaction として扱う実装。
- raw observation と current repository reference を固定入力として候補を構築し、machine recurrence 集約と agent observation の同一性判断を経て、active issue・generation・Markdown report・current pointer の整合した保存へ進む処理の入口。

## Read this when
- `cmoc feedback report` の処理全体、固定済み report cut、candidate の構築・同一性判断、normalization／remediation checkpoint、publication または incomplete 診断の挙動を調べるとき。
- feedback observation から active issue、generation artifact、current pointer、正常／診断 report までの transaction 境界や中断後の再開経路を確認するとき。

## Do not read this when
- raw observation の受付・保存や observation envelope の定義だけを調べるときは、feedback report の前段にある observation store／受付実装を直接読む。
- normalize／remediate agent に渡す個別 parameter や Structured Output schema の形式だけを確認するときは、それぞれの builder と schema を直接読む。
- generation state、pointer、checkpoint の共通データ構造だけを確認するときは、runtime feedback state／run state の実装を直接読む。

## hash
- db935f9fd7366038e7f168d68d65802d8f9d3f3631c2430b5a2d6b7fa4c65f79
