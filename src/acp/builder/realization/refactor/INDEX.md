# `__init__.py`

## Summary
- realization refactor 用 builder adapter 群の package marker。個別の builder adapter に進む前に、この群の位置づけを確認する入口。

## Read this when
- realization refactor の builder adapter 群が担う範囲を確認するとき。

## Do not read this when
- 個別 builder の提供内容やパラメータ構築を調べるときは、該当する adapter または oracle builder を直接読む。

## hash
- 4c331bccb54a9842893b30e509c994292dd25afbf1159ad4b7929ebffb3a311d

# `fork`

## Summary
- fork 用 builder adapter として、変更要約とファイル単位のレビュー・修正の builder を正本定義から再公開する。
- 変更要約は指定された commit 範囲の差分を読み取り専用で要約し、レビュー・修正は commit 差分に依存せず対象ファイルを調査して修正する作業向け。

## Read this when
- fork の変更要約またはファイル単位レビュー・修正で使う builder の呼び出し口を調べるとき。

## Do not read this when
- prompt の内容、builder の構築処理、出力形式の詳細を変更・確認するときは、正本定義と対応する出力スキーマを直接読む。

## hash
- a7abf8a243b9633a083c8790886337faeceed4b98c00a1439f7f1a0213de4855
