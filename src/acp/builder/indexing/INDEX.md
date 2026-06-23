# `index_entry.json`

## Summary
- `index_entry` 生成用の Structured Output schema を定義する JSON Schema。INDEX.md エントリーに必要な要約、読む条件、読まない条件の3要素と、それぞれが文字列配列であることを固定する。
- ルーティング文書生成処理が、生成結果の形を検証したり、エントリーに含める意味情報の最小単位を確認したりする入口になる。

## Read this when
- INDEX.md エントリー生成の出力 schema を確認する必要があるとき。
- 生成結果に含めるべきトップレベル項目や必須項目を確認するとき。
- summary、read_this_when、do_not_read_this_when がどのような役割の文章を持つべきかを確認するとき。

## Do not read this when
- 個別ファイルやディレクトリのルーティング文そのものを作成するだけで、schema の形を確認する必要がないとき。
- INDEX.md の探索順、読み進め方、oracle file と realization file の関係など、ルーティング運用や仕様体系の規則を確認したいとき。
- 生成されたエントリーをどこに保存するか、どのコマンドで生成するかなど、schema 以外の実装や運用手順を調べたいとき。

## hash
- ae0ec45ebc0afcd5c1e83a5a01655b75075b0d0da3ce141b4e0913339ba56494

# `index_entry.py`

## Summary
- `cmoc indexing` で目次エントリー生成用の AI 呼び出しパラメータを組み立てる実装。対象パスと対象本文を受け取り、読み取り専用の完全プロンプト、低コスト寄りのモデル設定、構造化出力 schema の保存先を含む `AgentCallParameter` を返す。
- エントリー生成時に、既存の目次を根拠にせず対象本文を根拠にする制約、対象外文書を必要に応じて参照できる制約、対象本文をコードブロックとして埋め込む構成を定義している。

## Read this when
- `cmoc indexing` の目次エントリー生成で、AI に渡す role・summary・goal・補助プロンプト・読み取り専用モードの内容を確認または変更したいとき。
- 目次エントリー生成の呼び出しで使うモデルクラス、reasoning effort、ファイルアクセスモード、構造化出力 schema の指定方法を追うとき。
- 対象パスの実パス解決や、対象本文を完全プロンプトへ埋め込む処理の入口を確認したいとき。

## Do not read this when
- 生成済みの目次エントリー本文そのものや、個別ディレクトリのルーティング内容を確認したいだけのとき。
- 完全プロンプト全体の共通構築規則、Markdown レンダリング、構造化ドキュメント部品の詳細を調べたいとき。
- 実際の indexing サブコマンドの CLI 引数処理、ファイル走査、INDEX.md の読み書き処理を調べたいとき。

## hash
- ee5f46b207126cb432c31d6ef4dd229f97479d2fe667c46f7677d5212fa83711
