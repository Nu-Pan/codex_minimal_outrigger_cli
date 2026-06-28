# `__init__.py`

## Summary
- oracle 側の apply builder package と対応する互換 package であることだけを示す package 初期化要素。実処理や公開 API の定義ではなく、同領域を package として扱うための入口に位置づけられる。

## Read this when
- apply builder 領域が oracle 側の package 構造と対応しているかを確認したいとき。
- package 初期化部分に実装意図や互換性メモがあるかを確認したいとき。

## Do not read this when
- apply builder の具体的な処理、変換、適用ロジックを調べたいとき。その場合は同 package 内の実装本体を読む。
- 公開関数、クラス、入出力仕様、エラー処理を確認したいとき。この対象にはそれらの定義は含まれない。

## hash
- a6df93a5897c266e6f48287739c8bf8192733ea9fb19e2f6eb05a302f4165b06

# `fork`

## Summary
- apply fork 系の agent call parameter builder と、その隣接 JSON schema、共通 helper をまとめる領域。`cmoc apply fork` の所見列挙、所見適用、変更要約に関するプロンプト構築、出力契約、リポジトリルート解決を確認する入口になる。
- oracle 側の正本仕様断片に追従しつつ realization 側で runtime import する場合としない場合の境界、読み書き制約や INDEX.md ルーティング指示を各 agent へ渡す実装が含まれる。

## Read this when
- `cmoc apply fork` がレビュー・修正・変更要約用 agent を呼ぶための parameter 構築処理を探すとき。
- apply fork 周辺で使う所見列挙や変更要約の JSON schema を確認し、生成結果の機械可読な契約を検証したいとき。
- apply fork 配下の builder が共有するリポジトリルート解決 helper や、oracle src との互換 import 経路の扱いを確認したいとき。
- 修正担当 agent に渡す読み書き範囲、作業禁止事項、INDEX.md 利用方針、差分や所見本文の prompt への埋め込み方を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の fork 作成、git branch 操作、commit 操作、作業ディレクトリ管理、レポート保存などの制御フローを追いたいとき。
- 個別 realization file の実装修正内容や、修正担当 agent が実際に編集するコードを調べたいとき。
- oracle file にある正本 prompt、レビュー基準、path model などの仕様断片そのものを確認したいとき。
- apply fork 以外の apply 系処理、CLI 出力全体の表示整形、または git 操作一般の実行ロジックを確認したいとき。

## hash
- d28dce9fa0aa69f7a2e715a0e4d1cacdbc61dbacfe853d6acce78a96a8a2b852
