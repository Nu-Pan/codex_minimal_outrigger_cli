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
- feedback observation と絞り込み済みの既存 issue 候補を比較し、同一 issue か新規 issue かを判断する prompt とエージェント起動パラメータを構築する関数。
- 入力外のファイルやログを参照せず、候補 issue の ID を用いた決定論的な同一性判断へ誘導する。関連する Structured Output schema と prompt 構築処理への入口となる。

## Read this when
- feedback issue の重複・同一性判定用 agent call の prompt 内容や起動設定を確認するとき
- 構造化 observation と既存 issue candidate を入力する feedback 正規化処理を追跡するとき

## Do not read this when
- feedback issue の summary、impact、原因、現在性、actionability、human action、verification、relation の生成仕様を確認したいとき
- Structured Output のフィールド定義そのものを確認したいときは、隣接する schema ファイルを直接読むとき

## hash
- 69cb83beff8477a42101a776bc451a1981fc221d00cd0f7f346aa2f32fc31d32

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
- feedback issue candidate の検証担当 agent call を構築する実装。report cut 時点で固定された参照と単一 candidate を埋め込み、読み取り専用・最大推論・routing policy 有効の検証パラメータを返す。
- 検証 prompt には参照範囲、変更禁止、candidate ID と evidence の決定論的条件を定義し、対応する Structured Output schema と実行時パスコンテキストを設定する。

## Read this when
- feedback issue candidate の検証 agent call の prompt、モデル設定、読み取り範囲、report cut reference の扱いを変更または確認するとき
- feedback 検証フローで返す AgentCallParameter の構築内容を追跡するとき

## Do not read this when
- feedback issue の報告・観測登録や別の candidate 処理の実装を直接確認するとき
- 検証結果の Structured Output 項目や型だけを確認したいときは、対応する schema を直接読むとき

## hash
- 1fe9f442f06cb28be74207276fb123757e4c3ac081bc3d2c5f074b4d24c97077
