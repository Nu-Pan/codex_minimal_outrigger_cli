# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消タスクを AI エージェントへ依頼するための呼び出しパラメータ構築を担う領域。
- conflict 対象パスを work root 基準の実パスへ解決し、解消対象ファイル一覧、作業制限、oracle file 例外編集ルール、git add・git commit 禁止を含む complete prompt と AgentCallParameter を組み立てる。

## Read this when
- `cmoc session join` 中に検出済みの merge conflict marker を解消するエージェント呼び出し内容を確認・変更したいとき。
- conflict marker 解消担当へ渡す role、summary、goal、補助 prompt、対象ファイル一覧の文面や構成を調整したいとき。
- conflicted paths を実パスへ解決し、編集対象パスとして AgentCallParameter に渡す流れを確認したいとき。
- merge conflict marker 解消時だけ oracle file の必要最小限の編集を許可する例外ルールや、git add・git commit を禁止する制御を確認したいとき。
- conflict 解消タスクで使うモデル種別、推論強度、ファイルアクセスモード、complete prompt rendering の設定箇所を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の orchestration、branch 操作、merge 実行、conflict 検出の流れを調べたいだけのとき。
- merge conflict marker の有無を検出する処理や、実際に marker を解析して内容を選択・削除するアルゴリズムを探しているとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode の定義や共通仕様を確認したいとき。
- complete prompt の共通構築規則、oracle/realization 標準 prompt の詳細、StructDoc の markdown rendering を調べたいとき。
- 通常の realization write 権限や oracle file 編集禁止ルールそのものの基本定義を確認したいとき。

## hash
- ed515ca206fe710cabb674682f420631db8fcba97058c5dfc68d14acef9149a6
