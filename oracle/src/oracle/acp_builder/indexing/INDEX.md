# `index_entry.json`

## Summary
- INDEX.md エントリーを生成するための Structured Output schema を定義する。
- 対象本文は、エントリーに含める人間向け要約、読むべき条件、読まなくてよい条件の3要素を必須にし、余分な項目を許可しないことで、ルーティング情報の出力契約を固定する。

## Read this when
- INDEX.md エントリー生成の出力形式を確認したいとき。
- ルーティング文書作成担当が、エントリーに含めるべき情報の単位や必須項目を確認したいとき。
- INDEX.md エントリー生成結果を検証する実装やテストで、期待する JSON 構造を確認したいとき。

## Do not read this when
- 個別のファイルやディレクトリについて、実際にどのような要約や読む条件を書くべきかを判断したいとき。
- INDEX.md のルーティング方針やエントリーの記述品質基準を確認したいとき。
- 対象ファイルの内容理解ではなく、cmoc の実装・テスト・CLI 挙動を確認したいとき。

## hash
- ae0ec45ebc0afcd5c1e83a5a01655b75075b0d0da3ce141b4e0913339ba56494

# `index_entry.py`

## Summary
- `cmoc indexing` の INDEX.md で、目次情報生成用の agent 呼び出しパラメータ構築を読むための入口。
- この対象は、プロンプト組み立てと `AgentCallParameter` の固定値をまとめているため、indexing の呼び出し設定や入出力の根拠を確認したいときに読む。
- `resolve_real_path` による `<target-path>` 展開や、`index_entry_standard` を有効にする理由を追うときの参照先。

## Read this when
- indexing 用の prompt 正本から、どのモデル・推論設定・アクセス権で呼び出すかを確認したい。
- `<target-path>` と `target_content` をどう prompt に埋め込むか、また `INDEX.md` 用エントリー生成規則をどう渡しているかを見たい。
- 目次情報生成の preflight 呼び出しがどの固定値で構成されているかを確認したい。

## Do not read this when
- 目次情報生成そのものの文言仕様だけを知りたい場合は、ここではなく prompt 組み立て側の正本を読む。
- `INDEX.md` の個々の記述内容やルーティング方針を知りたい場合は、この構築関数ではなく対象となる本文を読む。
- `AgentCallParameter` や関連型の定義自体を知りたい場合は、このファイルではなく型定義側を読む。

## hash
- aa84ff8862d099d364aba94542163ebdba8132cecf3cc2dafe810a53001d2c43
