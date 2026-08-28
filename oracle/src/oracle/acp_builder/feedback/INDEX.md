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
- 構造化済み observation と絞り込み済みの既存 issue candidate を比較し、feedback issue が既存 issue と同一か新規かを判断するための prompt と agent call パラメータを構築する。
- 入力以外のファイルや候補外 issue を参照せず、issue の同一性判断だけを行う処理への入口。

## Read this when
- feedback issue の同一性判定用 agent call の prompt、読み取り専用アクセス、入力データの埋め込み、または Structured Output の起動パラメータを確認するとき。
- 既存 issue candidate の ID と判定結果の整合性を保証する定義を確認するとき。

## Do not read this when
- issue の summary、impact、原因、現在性、actionability、human action、verification verdict、relation などの内容を生成・評価するとき。
- feedback observation の構造化や候補 issue の事前絞り込みを実装・確認するとき。

## hash
- cb1860f7b19eafebdda71b17a16444566f4f368f4025fe0379692bdefb48f092

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
- 人間向け feedback issue の検証用 agent call を構築する定義。report cut 時点で固定された参照と 1 件の issue candidate を入力し、検証担当向け prompt、読み取り専用アクセス、Structured Output schema、起動時の indexing 設定をまとめる。

## Read this when
- feedback issue candidate の検証 agent call の prompt 文面、参照範囲、読み取り専用制約、または起動パラメータを変更・確認するとき
- report cut reference だけを根拠に candidate を検証する処理の入口を確認するとき

## Do not read this when
- 検証結果の Structured Output の項目や JSON schema 自体を確認したいとき
- feedback issue の報告・観測送信や、candidate の生成・収集ロジックを直接確認したいとき
- prompt の共通構築規則だけを確認する場合は、prompt builder の定義を直接読むとき

## hash
- 326bd0555b76c69ddaeb61afece9fa3bdfd8c55426f476763614c74d5e2f1de7
