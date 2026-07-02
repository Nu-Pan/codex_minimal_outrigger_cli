# `index_entry.json`

## Summary
- INDEX.md 用エントリーを表す JSON オブジェクトの構造を定義する schema。
- エントリーに必要な要約、読む条件、読まない条件を必須項目として持たせ、各項目を文字列配列として扱う。

## Read this when
- INDEX.md エントリー生成結果の必須項目や値の型を確認したいとき。
- ルーティング文書作成処理が返す Structured Output の形を検証したいとき。

## Do not read this when
- 特定ファイルの実際のルーティング文言を知りたいとき。
- INDEX.md の生成方針や、エントリー本文の品質基準を確認したいとき。

## hash
- ae0ec45ebc0afcd5c1e83a5a01655b75075b0d0da3ce141b4e0913339ba56494

# `index_entry.py`

## Summary
- `cmoc indexing` の目次情報生成用に、対象ファイルまたはディレクトリの内容から AI エージェント呼び出しパラメータを組み立てる実装。
- ルーティング文書作成担当としての役割、Structured Output 返却、既存目次を読まない制約、対象内容の提示、目次エントリー基準を含む完全 prompt を生成し、効率重視の低推論設定で返す。

## Read this when
- `cmoc indexing` で目次エントリー生成用の agent call parameter がどう作られるかを確認したいとき。
- 目次エントリー生成 prompt に渡す役割、目的、読み取り専用制約、対象本文の埋め込み、placeholder の解決方法を変更したいとき。
- 生成される parameter の model class、reasoning effort、file access mode、出力 schema path を確認または調整したいとき。

## Do not read this when
- 実際の目次エントリー本文の品質基準や書き方だけを確認したいときは、その基準を定義している文書を直接読む。
- path placeholder の意味や実パス解決の仕様を調べたいだけなら、path model 側を読む。
- agent call parameter の共通データ構造や enum 定義そのものを確認したいだけなら、builder の基本定義を読む。

## hash
- b700d4d32d1442f6c130f4a14239ff09202788fcb071a19e010f5eba0a7e4b3e
