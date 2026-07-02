# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消を AI エージェントへ依頼するための agent call parameter 構築を扱う。conflict 対象パスの実パス解決、対象ファイル一覧、追加アクセス規則、oracle/realization 標準を含む prompt、model・reasoning・file access mode の指定を確認する入口。

## Read this when
- `cmoc session join` で conflict marker 解消用エージェントを呼び出す prompt や role、summary、goal の内容を確認したいとき。
- conflict 解消時に oracle file の最小編集を例外的に許可する条件や、git add・git commit を禁止するアクセス規則を確認したいとき。
- conflicted_paths から prompt に提示する対象ファイル一覧を作る処理や、生成される AgentCallParameter の model・reasoning・file access mode を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、merge 実行、conflict 検出、解消結果の取り込みを確認したいとき。
- merge conflict marker の具体的な解消アルゴリズムや、個別ファイル内容をどうマージするかを確認したいとき。
- agent call parameter の基礎データ構造、prompt builder、パスモデルの定義を確認したいとき。

## hash
- 9803e965cc01c506fe77d4e2f9f430849a3392f7abe9bcf41c35c075884061da
