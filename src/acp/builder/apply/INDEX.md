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
- apply fork 向けの ACP builder 実装群を収めるディレクトリ。各 builder は repo root 解決、oracle builder の import 準備、oracle 側 parameter 生成への委譲、realization 側公開型への変換を担い、互換 package の入口も含む。

## Read this when
- apply fork の agent call parameter 構築経路を確認・変更したいとき。
- apply fork の各 agent 用 builder が oracle 側 builder をどのように呼び出し、戻り値を realization 側の公開型へ適合させているか確認したいとき。
- packaged layout と開発 tree layout の両方で oracle builder を import 可能にする共通処理を確認したいとき。
- apply fork 互換 package の存在理由や、package 自体が処理本体ではなく互換用入口であることを確認したいとき。

## Do not read this when
- apply fork コマンド全体の実行フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理を調べたいときは、上位の apply fork 実装へ進む。
- agent prompt、出力条件、parameter 生成内容、人間意図などの正本仕様を確認したいときは、対応する oracle 側 builder を読む。
- ACP parameter のデータ構造や公開型そのものを確認したいときは、基本型定義へ進む。
- apply fork 以外の ACP builder や汎用 git 操作 helper、path model を調べたいだけのときは、それぞれの共通実装へ進む。

## hash
- 252aa75f38436d8dbdd65ec89af91cb1f5a89d5fe495a8527a2ebbab03b6db96
