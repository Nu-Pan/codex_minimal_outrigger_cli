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
- fork 適用領域のうち、作業レポート向け変更要約の出力契約と agent call parameter builder、および oracle 側実装へ委譲する互換入口をまとめる実装パッケージ。
- 差分適用後の変更要約生成では、隣接 schema と builder が主な入口になり、file finding enumeration や finding application の実体確認では oracle 側へ進むための再エクスポート接続点になる。

## Read this when
- fork 適用後の作業レポートに含める変更要約を、どの schema と agent 呼び出し設定で生成するか確認したいとき。
- 変更要約担当 agent に渡す raw git diff、プロンプト、読み取り専用アクセス、reasoning、モデル設定の組み立て箇所を探したいとき。
- realization 側の fork 適用関連 import 経路が、oracle 側の file finding enumeration や finding application 定義へどう接続しているか確認したいとき。
- このパッケージ自体が互換入口なのか、具体的な処理本体を持つ実装なのかを切り分けたいとき。

## Do not read this when
- fork 作成、差分適用、git 操作、作業レポート保存など、適用処理全体の制御フローを追いたいときは、より上位の apply/fork 実装へ進む。
- file finding enumeration や finding application の具体的な仕様、型、関数、挙動を確認したいときは、再エクスポート先の oracle 側本文を読む。
- agent call parameter の共通データ構造、モデル種別、reasoning、ファイルアクセスモードそのものを確認したいときは、共通 ACP 定義を読む。
- 変更要約の表示文面や CLI 出力全体の整形だけを調べたいときは、出力やレポート表示を担う領域を読む。

## hash
- 735609bdf382ea49e7774085a08a124842a12b175667f11e967216de3b1b0a7d
