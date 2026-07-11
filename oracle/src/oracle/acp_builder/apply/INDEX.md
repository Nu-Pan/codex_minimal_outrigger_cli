# `fork`

## Summary
- `cmoc apply fork` の差分要約・所見列挙・所見適用のための prompt/agent 呼び出し条件をまとめる領域。作業レポート用の要約、file 単位の所見リスト、所見本文からの適用処理に分かれ、個別の出力契約と呼び出し方針を確認するときの入口になる。
- 変更要約だけを見たいときは `change_summary.*`、file 単位の所見抽出だけを見たいときは `file_finding_enumeration.*`、所見本文から適用用の呼び出し条件を見たいときは `finding_application.py` を読む。

## Read this when
- `cmoc apply fork` で fork 後の差分を人間向けに要約・分類して出力する仕様を確認したいとき。
- file 単位の所見を列挙する入力条件、読ませる範囲、出力の形を確認したいとき。
- 所見本文から修正作業用の agent 呼び出し条件や prompt 構成を確認したいとき。
- 差分要約、所見列挙、所見適用のどれか一つの契約だけを追いたいとき。

## Do not read this when
- fork の作成、branch 操作、diff 取得、保存などの実行フロー全体を追いたいとき。
- 個別の所見内容や実装修正そのものを確認したいときは、対象の oracle file または realization file を読むべきで、ここは出力契約と呼び出し条件の入口に留まる。
- `cmoc apply fork` 以外のサブコマンドの prompt や agent call 条件を探しているとき。

## hash
- 687bde67bff25f93a489725dbb0812965d7b905c9191b12cf4adc215aee64ae5
