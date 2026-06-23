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
- `cmoc indexing` の目次情報生成で使う AI エージェント呼び出しパラメータを構築する実装。対象パスと対象本文を受け取り、INDEX.md エントリー生成用の完全な prompt、読み取り専用のファイルアクセスモード、効率重視モデル、構造化出力先を組み合わせて返す。
- エントリー生成規則と対象本文を prompt に埋め込み、既存の目次ではなくオリジナル本文を根拠にする制約を呼び出しパラメータへ反映する入口になっている。

## Read this when
- `cmoc indexing` が目次エントリー生成用にどの role、summary、goal、補助 prompt、ファイルアクセスモードを AI に渡すか確認したいとき。
- INDEX.md エントリー生成 prompt の文面、対象本文の埋め込み方、既存 INDEX.md を読ませない制約の扱いを変更したいとき。
- 目次情報生成用の AgentCallParameter で使うモデル種別、reasoning effort、出力 JSON パス、完全 prompt の組み立てを追うとき。

## Do not read this when
- 生成された INDEX.md エントリーそのものの内容やルーティング品質だけを確認したいとき。
- path keyword の意味、実パス解決の詳細、AgentCallParameter や FileAccessMode の型定義を調べたいとき。
- `cmoc indexing` 全体のファイル走査、INDEX.md の読み書き、サブコマンド実行フローを調べたいとき。

## hash
- 787b01be0b3ef7a9faad4724e2b71b4c98c19d21d28dedb4c4ed10a4e644c3ea
