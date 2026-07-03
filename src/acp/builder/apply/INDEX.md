# `__init__.py`

## Summary
- oracle.acp_builder.apply と互換の package として、既存の acp.builder.apply.* import を維持するための入口。実体ではなく互換層であり、realization 側と公開面から同参照が消えた後に削除できる。

## Read this when
- 既存コードや利用者向け公開面で acp.builder.apply.* import が残っている理由を確認したいとき。
- oracle.acp_builder.apply 側への移行に伴い、この互換 package を削除できる条件を判断したいとき。

## Do not read this when
- apply 機能の実装詳細や挙動を確認したいときは、実装本体へ進む。
- 新しい import 経路や公開 API を追加する場所を探しているとき。

## hash
- 3b7b28a47bd63cc192d8e90c21680ef7b23035187cf7a0ead5fabeef8e509a4c

# `fork`

## Summary
- apply fork 向け agent call parameter builder 群を収める package。各 builder は realization 側の薄い入口として、repo root 解決、oracle builder import 準備、oracle 側生成結果から realization 側公開型への変換を担う。
- 旧来の apply fork 系 import 互換を維持するための package 境界も含み、互換公開面を残す理由と削除判断の入口になる。

## Read this when
- `cmoc apply fork` の変更要約、ファイル単位所見列挙、所見適用に関する agent call parameter 構築経路を確認・変更したいとき。
- apply fork の realization 側 builder が oracle 側 builder をどう呼び出し、戻り値を realization 側 `AgentCallParameter` に適合させるか確認したいとき。
- apply fork 用 ACP builder 共通の repo root 解決、oracle src import 準備、oracle parameter 受け渡し境界を確認したいとき。
- 旧来の apply fork 系 import 互換 package を維持または削除できるか判断したいとき。

## Do not read this when
- `cmoc apply fork` 全体の実行フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理を調べたいときは、上位の apply fork 実装や呼び出し元を読む。
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいときは、対応する oracle 側 builder を読む。
- ACP parameter のデータ構造、公開型そのもの、汎用 git helper、path model を調べたいだけなら、それぞれの共通実装や型定義を読む。
- apply fork 以外の ACP builder の個別ロジックを確認したいとき。

## hash
- aa780174e29dd5732bd1c16b52ac8021bcb036497590175d985fe4d9b4e7c86a
