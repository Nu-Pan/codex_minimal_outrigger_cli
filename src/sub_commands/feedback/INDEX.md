# `__init__.py`

## Summary
- feedback サブコマンド実装パッケージの説明で、配下全体の範囲を確認する入口です。個別の報告、判定、修復、回復の挙動はそれぞれの担当要素で確認します。

## Read this when
- feedback サブコマンド配下の実装範囲を把握し、調査先を選ぶとき。

## Do not read this when
- 報告の publication、判定根拠、修復と join、cleanup と回復の具体的な挙動を調べるときは、それぞれの担当要素へ直接進んでください。

## hash
- 314f863a7cbf0d8eb6a2e9f72ee941edfcbbfcc5768f529aed40f09e96968cb9

# `decision.py`

## Summary
- feedback の判定で比較するリポジトリ入力と候補の根拠を収集し、内容・実行属性と根拠から状態を識別します。判定に含めない生成物や Git metadata もここで扱います。
- 正式 checkpoint の履歴をたどって再確認の要否、前回からの変化、同じ状態へ戻る循環をまとめ、検査記録に結び付いた判定根拠を作成します。

## Read this when
- feedback 判定の入力範囲や変更検知を見直すとき。
- 過去の判定との照合、再確認、循環検出、判定根拠の保存形式を調べるとき。

## Do not read this when
- 候補の組み立て、agent call、修正・commit、report の封印や publication など、feedback remediation 全体の進行を調べるときは、呼び出し側の処理へ進んでください。
- checkpoint の構造や artifact の整合性検証を調べるときは、その検証処理へ進んでください。

## hash
- 9eb918f99fc41cdd7265ae270bf52adc7e2ad5c866fa886aec21234e5435cacc

# `recovery.py`

## Summary
- feedback report 公開後の finalization journal を検証し、中断後に cleanup と run の ready 遷移を再開する。
- 自動 join 済みの feedback run を手動 join/abandon から保護し、明示終了時には未公開の report cut を監査記録後に片付ける。

## Read this when
- feedback report 公開後に cleanup が中断し、journal や run state を照合して完了処理を再開する方法を調べるとき。
- feedback run の手動 join/abandon が許可される条件や、明示終了時の report cut の扱いを調べるとき。

## Do not read this when
- observation の収集、候補の修復、join 判定など report の実行フロー自体を調べるときは、そのフローの実装へ進む。
- report の候補作成、証拠処理、本文描画、publication の内容を調べるときは、それらを担う report 処理へ進む。

## hash
- 82c9bc8ca34a2d26169c8f2010d33da72b95c8edbe73990a8921a584743ddd64

# `remediation.py`

## Summary
- feedback report の制御を担い、wave ごとの観測取込み、issue 修復の実差分検証と checkpoint、自動 join、公開までを一連の run 状態遷移として進める。
- 候補の集約や判定根拠の算出そのものではなく、それらを呼び出して修復の順序と run の整合を保つ処理を確認する入口。

## Read this when
- 観測を wave に取り込んでから issue を修復し、差分検証・commit・checkpoint・自動 join へ進む制御を変更または調査するとき。
- 自動 join・公開の回復や、中断・失敗時の run 状態と進捗記録の扱いを変更または調査するとき。

## Do not read this when
- 観測の検証・候補集約・レポート内容の生成や公開処理そのものが主題なら、それらを担う処理から確認するとき。
- 判定根拠の内容、入力変更の検出、再確認条件そのものが主題なら、判定ロジックから確認するとき。
- 公開後の cleanup や明示的な join・abandon の扱いそのものが主題なら、その終了処理から確認するとき。

## hash
- 8348e183bd3a45453ddbf84f708c80841415b5c6f1df637a4046e8134da340bb

# `report.py`

## Summary
- feedback report の raw observation と current state を report cut の固定入力へまとめ、candidate・machine aggregate・evidence reference を構築する。
- 固定入力から正常 report または incomplete 診断を描画し、artifact の整合性を確認して generation と current pointer を publication する。CLI entry point も担うが、修復 run の反復、join、recovery の制御は別の処理に委ねる。

## Read this when
- feedback observation や current evidence の固定・candidate 化・machine aggregate 処理を変更または調査するとき。
- 正常 report と incomplete 診断の内容、publication の再開、artifact 検証、current pointer 切り替えを変更または調査するとき。

## Do not read this when
- 修復 agent の反復実行、run の開始・join・finalization・recovery の流れが主題なら、run orchestration 側から確認するとき。
- observation の共通保存形式や feedback state artifact の共通検証・永続化が主題なら、共通 runtime 側から確認するとき。

## hash
- db935f9fd7366038e7f168d68d65802d8f9d3f3631c2430b5a2d6b7fa4c65f79
