# `oracle`

## Summary
- `cmoc review oracle` に関する AI 呼び出しパラメータと Structured Output schema の正本をまとめるディレクトリ。
- レビュー対象 oracle file からの新規所見列挙、所見の擁護・反証理由の追加調査、採否判定、重複・矛盾する所見の整理という review oracle フローの各境界へ進む入口になる。
- 各処理について、prompt に渡す役割・目標・補助文脈・標準類・モデル設定・file access mode と、対応する応答 schema の意味的な契約を確認できる。

## Read this when
- `cmoc review oracle` の所見生成、所見検証、採否判定、所見整理に関する prompt builder や応答契約の読む先を選びたいとき。
- oracle file を根拠にしたレビュー所見について、新規所見、擁護理由、反証理由、採否結果、整理操作のどれを確認すべきか切り分けたいとき。
- review oracle 系の AI 呼び出しで、既知理由・既知所見との重複排除、補助文脈の渡し方、Structured Output schema との接続を追いたいとき。
- oracle 標準および review oracle 標準を組み込んだ prompt 構築が、レビュー工程ごとにどう分かれているか把握したいとき。

## Do not read this when
- oracle file や realization file の一般定義、パスキーワード、oracle 標準そのものを確認したいだけのとき。
- `cmoc review oracle` 以外のサブコマンド、通常の実装担当 agent 向け prompt、INDEX.md 生成 prompt を調べたいとき。
- レビュー後の CLI 表示、永続化、集約、実行制御など、AI 呼び出しパラメータや応答 schema 以外の実装詳細を確認したいとき。
- 個別の oracle file 本文を読んで具体的な仕様上の問題を判断したいとき。

## hash
- da391888efa47b3e5ed93fd4c44f5ef7ac12e80550728b003cff6d4e94809b94
