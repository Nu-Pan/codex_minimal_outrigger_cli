# `fork`

## Summary
- `cmoc apply fork` の fork 適用工程で使う、AI エージェント呼び出しパラメータと Structured Output schema の正本断片をまとめる領域。
- 適用後差分の人間向け変更要約、realization file の要修正所見列挙、検出済み所見への修正依頼という、fork 適用時のレビュー・報告・修正支援に関わる入出力契約と prompt 構成を扱う。
- 実際の branch 操作や patch 適用そのものではなく、fork 適用フロー内で AI に何を読ませ、どの role・goal・制約・出力 schema で呼び出すかを確認する入口となる。

## Read this when
- `cmoc apply fork` で、適用後差分の変更要約、実装調査の所見列挙、所見対応修正依頼に使う AI 呼び出しの構成を確認したいとき。
- fork 適用後のレビューや作業レポートで、差分要約や所見リストの Structured Output schema と prompt 側の対応を確認したいとき。
- oracle file、realization file、起点パス、差分テキスト、検出済み所見を、AI エージェント呼び出しへどう渡すかを調べたいとき。
- apply review standard や realization standard を含む読み取り専用調査、または修正作業用のファイルアクセス権・モデル種別・推論努力量の指定を確認したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、branch 作成、git 操作、差分取得、patch 適用などの実行フロー本体を調べたいとき。
- 個別ファイルの patch 内容そのものや、実際に realization file をどう修正するかという修正ロジックを探しているとき。
- oracle standard、realization standard、apply review standard、path 語彙、共通 prompt 部品、AgentCallParameter 型定義そのものを確認したいとき。
- INDEX.md 用エントリーや一般的なルーティング文書の書き方を確認したいとき。

## hash
- 6d2ed36f7a330d8c896d29c4da21078be177d47dca877ac73064e3f8d2d1fae9
