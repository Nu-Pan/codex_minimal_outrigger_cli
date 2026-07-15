# `oracle`

## Summary
- oracle の共通ソース入口。ACP builder の agent 呼び出し設定・用途別 Structured Output 契約、設定／パス／構造化文書基盤、規範文面を prompt に組み込む処理を扱う。下位の acp_builder、other、prompt_builder から詳細領域へ進む。

## Read this when
- agent 呼び出しパラメータや用途別 Structured Output の正本を確認・変更するとき。
- cmoc の設定モデル、ルートパス解決、構造化 markdown の正本を確認するとき。
- oracle・realization standard、ファイルアクセス規則、INDEX ルーティング規則を prompt に組み込む正本を確認するとき。

## Do not read this when
- サブコマンドの実行フロー、CLI 入出力、差分適用や conflict 解消の realization 実装を調査するとき。
- prompt の合成順序や個別の実行制御だけを調査するとき。
- 個別の oracle file や realization 側の実装・テスト本文だけを確認するとき。

## hash
- 4a9e8229899b83d63563907a81c307314d13558fa3f2fa142846b327b71be24a
