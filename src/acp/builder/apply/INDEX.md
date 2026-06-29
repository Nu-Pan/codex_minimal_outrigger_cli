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
- `cmoc apply fork` の各 agent 呼び出しに渡す parameter と prompt を組み立てる realization builder 群への入口。所見列挙、所見適用、変更要約の各フェーズについて、model class、reasoning effort、file access mode、構造化出力 schema、oracle prompt 断片の取り込み方を扱う。
- apply fork 系 builder が oracle src を import するための共通補助処理と、レビュー結果・変更要約を機械可読に返すための出力契約も同じ責務範囲に含む。

## Read this when
- `cmoc apply fork` で、所見列挙・所見適用・変更要約 agent の呼び出し設定や prompt 構築を確認または変更したいとき。
- apply fork 系 builder が repo root を解決し、oracle src の正本 prompt 断片や構造化 markdown renderer を import して利用する流れを追いたいとき。
- 差分適用後の変更要約や実装レビュー所見を、どの schema 契約で agent に返させるか確認したいとき。
- apply fork の builder 層が読み取り専用・書き込み可などの file access mode、model class、reasoning effort を各フェーズへどう割り当てるか調べたいとき。

## Do not read this when
- fork 作成、作業ディレクトリ管理、git 操作、レポート保存など、`cmoc apply fork` 全体の実行制御を調べたいとき。
- oracle 側の正本仕様断片、prompt builder、review standard、path model の内容そのものを確認または変更したいとき。
- agent が返した所見や変更要約を実際に解釈・表示・永続化する処理を追いたいとき。
- 個別の差分検出アルゴリズム、パッチ適用手順、CLI 入出力全体の整形だけを確認したいとき。

## hash
- 6cb3fb94bf71ec735bd4c699bc64114ff883e9c9f0d781e49a27e3b2e814cdb4
