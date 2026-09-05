# `__init__.py`

## Summary
- feedback サブコマンドの実装を担う。feedback サブコマンドの処理を確認・変更するときの入口。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。

## hash
- 314f863a7cbf0d8eb6a2e9f72ee941edfcbbfcc5768f529aed40f09e96968cb9

# `recovery.py`

## Summary
- Feedback report publication 後の finalization journal に基づく cleanup・recovery と、feedback run の自動 join 済み状態を明示 join/abandon から保護する境界を扱う。
- feedback run を明示的に終了した場合の監査記録、report cut の checkpoint 回収、work artifact 破棄を扱う。

## Read this when
- feedback report の publication 後に cleanup や finalization journal の recovery 処理を確認するとき
- feedback run の自動 join と、明示 join/abandon を許可する条件の境界を変更・確認するとき
- 明示終了した feedback run の監査記録や report cut cleanup の挙動を確認するとき

## Do not read this when
- feedback report の判定・remediation・publication 自体の処理を確認するとき
- feedback 以外の run の join/abandon や一般的な run lifecycle を変更するとき
- 通常の feedback state 構造や report artifact の形式だけを確認するとき

## hash
- eef1664e3984df8f96491c8a0e73e5a6855c7e0991d8d75b697d7a563e2260bb

# `remediation.py`

## Summary
- feedback issue の逐次 remediation wave、run の seal・自動 join、join 後の recovery、publication を一貫した境界で制御する。
- agent の実差分、structured output、verification、checkpoint、commit 到達可能性を検証し、正式な issue 修復結果だけを session tree と report publication へ渡す。
- feedback workflow における中断・エラー・SIGINT 保留、進捗記録、merge 成功後の publication recovery を扱う。

## Read this when
- feedback report の remediation wave、issue 単位の commit/checkpoint、automatic join、publication の順序や失敗回復を変更・調査するとき。
- feedback run の seal、high watermark、checkpoint、merge 後の tree/hash 検証がどのように連携するか確認するとき。
- feedback remediation agent の出力と実際の変更 path・verification を照合する処理を確認するとき。

## Do not read this when
- 観測の集約・表示や report の候補生成そのものを変更・調査するときは、feedback report 実装を直接読む。
- 永続化された feedback artifact の形式・読み書き・検査規則だけを確認するときは、runtime_feedback_run_state などの artifact 管理対象を直接読む。
- 一般的な run lifecycle、Git join、state 管理の共通仕様だけを確認するときは、対応する共通 runtime 実装を直接読む。

## hash
- c3eaa004c03556abcc89fc26f974b208069bf705e11a48ab39bce446884b3b62

# `report.py`

## Summary
- `cmoc feedback report` の report cut を固定入力として、observation の検証・正規化・machine recurrence 集約・candidate verification・publication または incomplete 診断までを一つの transaction として扱う実装。
- active issue、raw observation、repository reference、checkpoint、generation、report、current pointer の整合性と hash を確認し、中断・再開や異常時の durable state を管理する feedback report pipeline の入口。

## Read this when
- `cmoc feedback report` の report cut、candidate の同一性判定、machine rule の recurrence threshold、verification 結果、正常 publication または incomplete 診断の処理を変更・調査するとき。
- feedback state と report cut の checkpoint、artifact hash、generation／pointer 切替、観測値や repository evidence の保存範囲を確認するとき。
- feedback report の Markdown 出力、publication／diagnostic の transaction、interrupt・resume・cleanup・subcommand log の記録経路を追うとき。

## Do not read this when
- feedback observation の受付・envelope 検証や raw store への保存処理だけを調査するときは、まず observation intake／store の実装を読む。
- normalize／remediate agent に渡す parameter や Structured Output schema の内容だけを確認するときは、対応する builder と schema を直接読む。
- feedback state の永続化 API、run state の wave／join 管理、generation artifact の一般的な形式だけを調査するときは、対応する commons または remediation／recovery 実装を直接読む。
- 通常の別サブコマンドの report 生成や、feedback report と無関係な Markdown／logging 処理を調査するとき。

## hash
- 755215736453938bf0404e4b8dddf20a284111c7dc1d10b60d1b808c25a776a5
