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
- フィードバック判定の根拠状態を識別し、過去の処理履歴との比較から再確認に関する情報を組み立てる。

## Read this when
- 判定根拠の状態比較や、過去の判定を再確認する条件を調べるとき。

## Do not read this when
- 再確認を含む remediation の処理順序や実行制御を変更するときは、remediation の処理を担う対象から確認する。
- 実行 artifact の形式や検証規則だけを変更するときは、その形式と検証を担う対象から確認する。

## hash
- 7fd71b4bac5a2d74cb53e78434cd540fac99cd6331d2dc1dfc3d174fa05817dc

# `recovery.py`

## Summary
- Feedback report の publication 後に、finalization journal と join evidence を照合し、cleanup と session/run の終了状態を再開可能な形で確定する。
- Feedback report run の明示 join/abandon を自動 publication と調整し、手動終了時の記録と未公開 work の破棄を担う。

## Read this when
- report の公開後に cleanup が中断し、同じ report cut と join 状態から recovery を追うとき。
- feedback report run に対する明示 join/abandon の制約や、手動終了時の記録・work cleanup を確認するとき。

## Do not read this when
- report の生成、修復、正規化、候補検証の手順を調べるときは、report pipeline または remediation coordinator を読む。
- 通常の run join/abandon の merge、worktree、branch cleanup を調べるときは、run lifecycle 側を読む。

## hash
- 69e04af943a1db08bab64464419b23ec2fa9d39ad79a788ed3b8fbc4eddfe230

# `remediation.py`

## Summary
- feedback の修復 run を制御し、観測を wave 単位で取り込みながら issue ごとの修復、差分検証、commit、checkpoint を進める。
- run の成果を封印して join と publication へ渡し、中断・失敗時の rollback、recovery、進捗確定も扱う。集計・レポート処理と判定根拠の比較は、それぞれの専用処理へ委譲する。

## Read this when
- feedback report の wave intake から issue 修復・checkpoint までの進行や収束条件を変更・調査するとき。
- 修復成果の join、join 後の検査、publication への受け渡し、または中断・失敗時の run 状態回復を扱うとき。

## Do not read this when
- CLI の起動処理、観測の集計、正規化、レポート内容や publication の内部だけを扱うときは、該当する report 処理から確認する。
- 判定入力の hash、根拠の有効性、再確認履歴だけを扱うときは、判定処理から確認する。
- run artifact の読み書きや形式検証だけを扱うときは、artifact 状態管理の処理から確認する。

## hash
- 3cff3fece0363dc0fe5e24d429b5a3a7f442e17a443268e093b105ec4f6ba794

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
