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
- apply fork 用の agent call parameter builder 群をまとめる実装ディレクトリ。各 builder は realization 側の入口として、repo root 解決、oracle 側 builder の import 準備、oracle builder への委譲、realization 側 parameter 型への適合を担う。
- この階層は、変更要約、ファイル単位所見列挙、所見適用といった `cmoc apply fork` の個別 agent 呼び出し準備と、それらが共有する oracle 連携 helper への入口である。

## Read this when
- `cmoc apply fork` で agent call parameter をどの builder が組み立てるか確認したいとき。
- realization 側 apply fork builder が oracle 側 builder をどのように import 可能にし、委譲結果を realization 側型へ変換しているか確認したいとき。
- 変更要約、ファイル単位所見列挙、所見適用のいずれかの agent 呼び出し準備を調査・変更したいとき。
- apply fork builder 群に共通する repo root 解決、oracle src import 経路補正、ACP parameter 型境界を確認したいとき。

## Do not read this when
- `cmoc apply fork` コマンド全体の制御フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理を調べたいときは、上位の apply fork 実装や CLI 側へ進む。
- agent prompt、出力条件、変更要約や所見処理の正本仕様を確認したいときは、委譲先の oracle 側 builder や正本仕様断片を読む。
- 汎用 git 操作 helper、path model、ACP 共通型そのものを調べたいだけなら、それぞれの共通実装や基本型定義へ進む。
- package 初期化 docstring だけを確認したい場合を除き、互換 package の存在確認だけで個別 builder の処理内容まで読む必要がないとき。

## hash
- b61afcbe59a8921889d4655a9d05a907c43f8ec6b2d43238acc56489c3b9cb2d
