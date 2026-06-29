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
- `cmoc indexing` の目次情報生成に使う AI エージェント呼び出しパラメータを構築する正本仕様断片。対象パスと対象内容を受け取り、読み取り専用の complete prompt、効率重視モデル、低 reasoning、構造化出力先を組み合わせて返す責務を持つ。
- ルーティング文書作成担当としての role、対象の `INDEX.md` 用エントリー生成という summary/goal、既存 `INDEX.md` を根拠にしない生成規則、対象内容の埋め込み、`<target-path>` の実パス解決を一体で定義する入口。

## Read this when
- `cmoc indexing` における `INDEX.md` 用エントリー生成の prompt 内容、補助文書、プレースホルダー、対象内容の渡し方を確認または変更するとき。
- 目次情報生成用の AI 呼び出しで使うモデルクラス、reasoning effort、ファイルアクセスモード、出力 schema path の正本仕様を確認するとき。
- 既存 `INDEX.md` を読ませず、対象本文を根拠に structured output を返させる制約がどこで組み立てられているかを調べるとき。

## Do not read this when
- `INDEX.md` エントリーの個別対象本文そのものや、生成結果の日本語文面だけを確認したいとき。
- path keyword や実パス解決の一般仕様を知りたいだけの場合は、path model の定義を直接読む方がよい。
- complete prompt の汎用構築処理、構造化 markdown の描画処理、または AgentCallParameter 自体のデータ構造を調べたい場合は、それぞれの定義元を直接読む方がよい。

## hash
- b700d4d32d1442f6c130f4a14239ff09202788fcb071a19e010f5eba0a7e4b3e
