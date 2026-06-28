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
- apply fork 系の ACP builder をまとめる領域。共通の実行環境解決、変更要約・所見列挙・所見適用の agent call parameter 構築、各 builder が返す structured output schema への入口を持つ。
- `cmoc apply fork` の各フェーズで、oracle 側の prompt builder と schema を使って agent 呼び出し設定を組み立てる realization implementation 群を探す起点になる。

## Read this when
- `cmoc apply fork` が変更要約、実装所見列挙、所見適用の各 agent をどの model・reasoning effort・file access mode・schema・prompt で呼ぶか確認したいとき。
- apply fork 系 builder が repo root を解決し、oracle src を import 可能にして、oracle 側の prompt 断片を render する流れを確認したいとき。
- 差分適用後のレビュー用出力や所見出力の structured output schema と、それを使う builder 実装の対応関係を追いたいとき。
- apply fork builder 群に共通する helper と、個別フェーズ向け builder のどちらへ進むべきかを切り分けたいとき。

## Do not read this when
- `cmoc apply fork` 全体の fork 作成、git 操作、作業ディレクトリ管理、レポート保存などの実行制御を調べたいとき。
- oracle 側の正本 prompt 断片、review standard、realization standard、path model の定義そのものを確認・変更したいとき。
- 生成された変更要約や所見の内容そのものを読みたいだけで、agent call parameter の構築処理や schema 契約を確認する必要がないとき。
- apply fork 以外の builder、CLI サブコマンドルーティング、または package 初期化 docstring 以外の公開 API を探しているとき。

## hash
- d704c7b82c36af134c6e396064b91b05ec36ca83889da729c45ea94281a38749
