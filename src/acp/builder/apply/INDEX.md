# `fork`

## Summary
- `cmoc apply fork` の適用・レビュー工程で使う AI 呼び出しパラメータ群と、その入出力に使う構造化スキーマをまとめる領域。ファイル単位の所見列挙、所見リストの整理、所見に基づく realization file 修正、作業後の差分要約という一連のエージェント呼び出し条件を確認する入口になる。
- 各呼び出しでは、対象パスや git diff、所見リスト、個別所見を補助プロンプトに埋め込み、参照する標準、ファイルアクセス権限、モデルクラス、reasoning effort、Structured Output schema の選択を組み立てる。

## Read this when
- `cmoc apply fork` のレビュー・修正・レポート生成で、AI エージェントに渡す role、summary、goal、補助プロンプト、参照標準、ファイルアクセスモードを確認または変更したいとき。
- ファイル単位の所見列挙、集約済み所見リストの改善、個別所見への修正作業、git diff からの変更要約という各段階の呼び出し条件を追いたいとき。
- apply fork の所見一覧や変更要約が、どの Structured Output schema に従い、どの粒度の情報を保持するかを確認したいとき。
- レビュー所見を重複・矛盾・False-Positive の除去を経て作業可能な順序に整理する prompt、または所見本文を修正担当エージェントへ渡す prompt を調整したいとき。

## Do not read this when
- `cmoc apply fork` のサブコマンド登録、CLI 引数解析、branch 作成、git コマンド実行、差分取得などの実行フロー本体を調べたいとき。
- 完全プロンプトの共通組み立て処理、構造化 markdown の描画、path keyword の定義、AgentCallParameter やモデル種別などの共通型定義を変更したいとき。
- oracle file、realization file、各種 standard の本文そのものを確認したいとき。
- 実際の変更対象ファイルの内容、個別の修正コード、またはテスト実装を調べたいとき。

## hash
- 0ed564517d58e1b085ac871c393c280e05e8a352e88aa23747519fd22ab75d93
