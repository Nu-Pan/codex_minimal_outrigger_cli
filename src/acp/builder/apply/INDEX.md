# `__init__.py`

## Summary
- oracle 側の apply package への互換 import 経路を維持するための package 初期化ファイル。既存の acp.builder.apply.* 参照を正本側配置へつなぐ互換層として位置づけられ、参照がなくなれば削除可能な対象である。

## Read this when
- acp.builder.apply.* import の互換維持や削除可否を確認する。
- apply package の正本側配置と realization 側の import 経路の関係を確認する。

## Do not read this when
- apply の具体的な処理内容や仕様を確認したい場合は、正本側の apply package を読む。
- 新規機能の実装場所を探しているだけで、既存 import 互換に関係しない。

## hash
- cd3525acfac667a62268ceec2006db542a5aa39415a6a3f282225c5dacb5c290

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
