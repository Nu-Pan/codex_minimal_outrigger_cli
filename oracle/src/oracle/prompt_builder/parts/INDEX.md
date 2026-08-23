# `oracle_and_realization_basic.py`

## Summary
- oracle と realization の基本概念を説明する prompt builder の part。oracle file・realization file・uncategorised file の役割、下位分類、分類条件を、root 定義に基づくパス付き説明として構築する。oracle/realization の区別や、対象ファイルの分類規則を含むプロンプトを作成・変更・確認するときの入口であり、分類文面の正本である misc_spec 自体や、具体的な oracle/realization ファイルの実装責務を確認する場合は、それぞれの直接の対象へ進む。

## Read this when
- oracle と realization の基本的な役割・下位概念・分類条件を prompt に組み込む処理を調べるとき
- oracle file、realization file、uncategorised file の分類説明を生成する part の責務を確認するとき
- root の work-root 定義を call-scoped context から取得して説明文中の placeholder に渡す処理を確認するとき

## Do not read this when
- oracle/realization の分類文面そのものの正本仕様を確認・変更するとき
- 個別の oracle doc、oracle src、oracle test、realization implementation、realization test の具体的な責務や実装を調べるとき
- prompt builder の共通構造や PlaceholderMap、SDHeader の一般的な仕様だけを確認するときは、該当する定義へ直接進む

## hash
- f4153ed94db3fe3edad69a8637668c5779ed5148f0eca0137903b133f72b5f8b
