# `normalize_issue.json`

## Summary
- feedback issue の同一性判断を返す出力スキーマ。入力された既存 issue candidate と同一か新規かの判断結果を定義し、feedback 同一性判断処理の出力契約への入口となる。

## Read this when
- feedback issue が既存候補と同一か、新しい issue かを判定する agent call の出力形式を確認するとき
- 同一 issue の ID を返す場合と、新規 issue として null を返す場合の契約を確認するとき

## Do not read this when
- feedback issue の内容や同一性判定ロジック自体を確認したいとき
- agent call の入力形式や issue candidate の生成・保存処理を確認したいとき

## hash
- 2b30dfd42f9d1f751aca7b061bfe811dbe8d7fcfa85788fea6e1a1cfc647764f

# `normalize_issue.py`

## Summary
- feedback issue の同一性を判断する agent call の prompt と起動パラメータを構築する。
- 構造化済み observation と絞り込み済みの既存 issue candidate だけを比較し、既存 issue または新規 issue の判定へ進む入口を提供する。

## Read this when
- feedback observation と既存 issue candidate の同一性だけを判定したいとき。
- 同一性判定の入力範囲、候補外探索の禁止、同一 issue と判定した場合の issue ID の一致制約を確認したいとき。

## Do not read this when
- issue の summary、impact、原因、現在性、actionability、human action、verification verdict、relation を生成または評価したいとき。
- 候補 issue の絞り込み、raw log・過去の Codex session・feedback state の調査、または候補外 issue の探索を行いたいとき。

## hash
- cc5ca8c7b9f7ad5b716b9d51a0a97a80423a68b563ee308c72778b7382595be7

# `verify_issue.json`

## Summary
- feedback issue の verification agent call が返す検証結果のスキーマ。candidate の現在状態を evidence で示し、unresolved・resolved・not_actionable・inconclusive の verdict と、それに応じた人間対応または判定理由を表現する。feedback issue の検証結果契約や verdict 別の出力要件を確認するときの入口。

## Read this when
- feedback issue の verification 結果を生成、検証、解釈するとき
- candidate の現在状態、report cut reference に基づく evidence、verdict 別の human action と reason の扱いを確認するとき
- unresolved・resolved・not_actionable・inconclusive のいずれかに応じた出力構造を確認するとき

## Do not read this when
- feedback issue の検出や candidate の生成条件を確認したいとき
- verification agent call の実装フローや実行方法を確認したいとき
- verdict の根拠となる report cut reference や candidate の実データを直接確認したいとき
- 検証結果のスキーマではなく、別の ACP builder 出力契約を確認したいとき

## hash
- 3fc48fb37c197aa9005dfc81984d850e34881c5d05adab44e4d58f032fd665f4

# `verify_issue.py`

## Summary
- report cut 時点で固定された参照だけを根拠に、1 件の issue candidate を検証する prompt と起動パラメータを構築する。candidate ID の一致、参照 ID の限定、検証結果の根拠条件など、Structured Output の決定論的事後条件も prompt に組み込む。

## Read this when
- feedback issue candidate の検証処理や、その検証用 prompt・起動パラメータを変更または確認するとき。
- candidate と report cut reference だけに作業範囲を限定する検証フローの入口を確認するとき。

## Do not read this when
- feedback issue の候補生成、report cut 参照の作成、または検証結果の Structured Output schema 自体を直接確認するとき。
- candidate 外の問題探索や live repository、raw log、過去の session・feedback state を扱う必要があるとき。

## hash
- 669241fa12ef4fc2a0b1444e98de2d01d1401fdebf53f10b8a95aa50e8bded7e
