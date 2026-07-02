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
