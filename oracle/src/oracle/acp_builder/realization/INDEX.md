# `apply`

## Summary
- `cmoc realization apply fork` 用の agent call prompt と起動パラメータを構築し、作業用 worktree、呼び出し元が確定した文書検索範囲、指定 commit 範囲を結び付ける。
- Git 差分から oracle file の変更を追って realization file に反映する作業指示、完了条件、差分の取得規則、関連ポリシーを構成する。

## Read this when
- `cmoc realization apply fork` の作業指示、完了条件、commit 差分の取得や rename の扱いを調べたり変更したりするとき。
- この call の worktree や文書検索範囲、realization file への書き込み設定など、起動パラメータを調べたり変更したりするとき。

## Do not read this when
- 複数の call に共通する完全 prompt の組み立てやポリシー合成を変更するときは、共通 prompt builder の定義から確認する。
- 差分を起点にしない realization refactor の個別ファイル調査・レビュー・修正の指示や起動定義を扱うときは、その workflow の定義から確認する。

## hash
- 8c54dce1b26d82bfb670c52d6fab8a043f6b08a0e106b951117c7bbe2cad47dc

# `refactor`

## Summary
- realization refactor の fork 用 agent call を構築する定義群です。確定した commit 間差分の読み取り専用要約と、指定ファイルを起点にした所見調査・realization 修正を扱います。
- 各 call の prompt、起動パラメータ、出力契約を確認する入口です。

## Read this when
- refactor fork の変更要約で、比較範囲や読み取り条件、要約の出力契約を調べる・変更するとき。
- refactor fork のファイル単位レビュー・修正で、調査範囲や修正条件、所見の出力契約を調べる・変更するとき。

## Do not read this when
- commit 間の oracle 変更をリポジトリ全体の realization に反映する apply 作業を調べるときは、その作業の起動定義を参照してください。
- どの agent call 設定が実行時に選ばれるかだけを調べるときは、呼び出し側の設定を参照してください。

## hash
- ef733025bc70e1600e0151d3fad4c1d0b8c73072946f04f1815d76d482d5a671
