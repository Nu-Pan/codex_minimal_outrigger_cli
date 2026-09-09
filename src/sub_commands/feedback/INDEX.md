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
- Feedback report の publication 後に、finalization journal を根拠として work artifact、session state、join 済み run の隔離資源を整合的かつ再実行可能に cleanup する処理。
- 自動 join 済みの feedback run を明示的な join/abandon で終了させない境界と、明示終了された未 publication run の監査記録・work cleanup を扱う下位処理への入口。

## Read this when
- feedback publication 後の cleanup、finalization journal の検証・recovery、または session/run/worktree の整合性確認が必要なとき。
- feedback run が自動 join 済みか、明示 join/abandon を許可できる状態かを判定したいとき。

## Do not read this when
- feedback report の生成、remediation、decision、または publication 前の report cut 処理そのものを調べたいとき。
- feedback run 以外の一般的な run lifecycle の join/abandon 処理を調べたいとき。

## hash
- c9708faad6582446fddd44536620cd42da92118571ca2cc4fd3a752c01242bc2

# `remediation.py`

## Summary
- feedback report の run 全体を制御し、観測の wave 処理から issue remediation、checkpoint 確定、自動 join、publication までを一続きに扱う実行入口。
- remediation agent の出力・実差分・verification・判定根拠を照合し、commit と immutable checkpoint を確定する責務を持つ。
- sealed、merged、completion の run artifact と session tree の整合性を検査し、中断・失敗時の rollback、error 化、join recovery、publication recovery を扱う。

## Read this when
- feedback report の新規実行、wave の再処理、high watermark に基づく観測取り込み、候補ごとの remediation の流れを確認するとき
- remediation 出力の issue ID・変更パス・status・verification と実際の worktree 差分を照合する処理を調べるとき
- remediation checkpoint の選択、判定根拠の再検証、sealed run の自動 join、join 後の publication または recovery を追跡するとき
- SIGINT、中断、例外、未確定 checkpoint の rollback、run state の error 化、進捗記録の復元を確認するとき

## Do not read this when
- 観測の正規化・集約・表示や publication レポートの詳細な生成規則だけを調べるときは report を直接読む
- run artifact の schema、保存・読出し、checkpoint の低レベル検証だけを調べるときは runtime_feedback_run_state を直接読む
- issue の候補化、判定状態、decision basis の比較規則だけを調べるときは decision を直接読む
- 一般的な run join の merge 手順や editing run lifecycle の共通実装だけを調べるときは run lifecycle 側の対象を直接読む

## hash
- 64ec051c43e400457b2e1d68b7399b6092e998e13867c27212e5e5eb4818dd42

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
