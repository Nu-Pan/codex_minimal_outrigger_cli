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
- feedback report の issue 判定に使う repository 入力と candidate evidence をまとめ、保存済み判定の有効性、再確認履歴、修復の反復状態を扱う。
- 判定根拠の状態を管理し、issue の再評価が必要か判断する処理の入口。

## Read this when
- 前回の issue 判定を現在の状態に対して再利用できるか、再確認時に先行結果と変化をどう扱うか調べるとき。
- feedback 判定が参照する repository 入力や、再確認・再修正が同じ状態へ戻る場合の扱いを変更するとき。

## Do not read this when
- observation の受け入れ、候補の形成、利用者向け report の集約や表示だけを変更するときは、取込みと report 構築の責務を直接読む。
- agent による修復、wave の進行、commit・rollback、join、publication や recovery を変更するときは、run orchestration の責務を直接読む。
- checkpoint artifact の形式や永続化時の検証だけを変更するときは、artifact 検証と保存の責務を直接読む。

## hash
- 4cfa486a145314a5e622d36d92f56bb64f7b13a5b6b4f87590a8988d7f0041e0

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
- `feedback report` の run を開始・再開し、観測 wave ごとの issue 修復から checkpoint の確定、seal、自動 join、publication までを制御する。中断・失敗時の rollback や状態記録も扱う。
- 修復 agent の出力を実差分・verification と照合し、変更範囲と判定根拠を検証する。issue commit、join 後の整合性、publication 境界を追う際の入口となる。

## Read this when
- feedback report の wave 処理、issue ごとの修復・commit・rollback、seal、自動 join や run の再開がどう連携するかを調べるとき。
- 修復結果の検証や checkpoint を含む、run 全体の状態遷移と失敗時の扱いを確認するとき。

## Do not read this when
- 観測の集約、候補の構築、report の表示・publication の詳細だけを調べるときは `report.py` へ進む。
- 判定入力の作成、根拠 hash、履歴や再確認の判定方法だけを調べるときは `decision.py` へ進む。
- publication 後の cleanup や明示的な join・abandon の処理だけを調べるときは `recovery.py` へ進む。

## hash
- 803b35e0cdeb98ab236c719640503118c6ec04a06285b4c7408dde38b424b0dd

# `report.py`

## Summary
- 固定した feedback report cut の入力を検証・集約し、candidate の同一性正規化と machine observation の再発集計を行う。
- candidate の判定結果から正常 report と generation を publication するか、inconclusive を含む場合に incomplete 診断を生成する処理を担う。

## Read this when
- report cut の入力固定、observation の検証、candidate 集約・正規化、再発集計の動作を変更または調査するとき。
- 判定結果を report に描画し、generation や current pointer へ反映する publication の動作を変更または調査するとき。

## Do not read this when
- 修復 wave の進行、verification の実行、自動 join など run 全体の制御を調べるときは、その制御を担う実装へ進む。
- 判定根拠の比較や再確認履歴を調べるときは、その責務を担う判定実装へ進む。
- publication 後の cleanup や finalization recovery、明示的な join・abandon の境界を調べるときは、その責務を担う recovery 実装へ進む。

## hash
- f6c52c5fb1f6cbac676cd60598374d9621b9a2946e93f74ebc6b2062678b0ad8
