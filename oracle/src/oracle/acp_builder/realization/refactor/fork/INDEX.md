# `change_summary.json`

## Summary
- refactor fork が指定するコミット範囲の変更を、人間向けに意味論で分類・要約する agent call の出力契約を定める。
- ファイル単位のレビュー所見や修正結果ではなく、範囲全体の変更要約を扱う。

## Read this when
- 指定コミット範囲の変更要約について、出力契約や意味論的な分類の要件を確認・改訂するとき。

## Do not read this when
- 変更要約 agent call の prompt、差分取得、コミット範囲、起動パラメータを調べるときは、呼び出し構築定義へ進む。
- ファイル単位のレビュー所見や修正・検証結果の出力契約を扱うときは、その agent call の出力仕様へ進む。

## hash
- 13d5ef8771340eda2ba02624ffcf0dac54739301c226e31d353d8ce465e5d401

# `change_summary.py`

## Summary
- 指定された run fork commit から要約確定時点の HEAD までの tree 差分を Git から取得し、人間向けに要約する read-only 呼び出しを構築する。
- 呼び出し元が決めた閲覧範囲と linked worktree を引き継ぎ、プロンプトや構造化出力先を含むパラメータを組み立てる。

## Read this when
- refactor fork の変更全体を要約する呼び出しの範囲や、比較対象の commit を固定する条件を確認するとき。
- 差分を取得できなかった場合の扱いや、この呼び出しの閲覧・書き込み制約を確認するとき。

## Do not read this when
- 個別ファイルの調査や修正の手順を確認するときは、同階層のファイル単位レビュー・修正用定義を読む。
- 構造化出力の項目や形式を確認するときは、その出力定義を読む。

## hash
- 21ce1da8a51622edef86b9676a87f8ff319af5691ac28a2f451d2b6d9a25f3c6

# `file_review_and_fix.json`

## Summary
- oracle または realization file を起点に行う realization refactor の所見調査・修正 call の出力契約を定める。調査の根拠と修正・検証の結果を、実際の realization file の変更申告に結びつけて返す。

## Read this when
- この call の結果を作成または解釈するときに、所見報告の出力条件を確認する場合。
- 報告された対応結果と realization file の変更申告が、call 内の修正・検証に対応しているか確認する場合。

## Do not read this when
- agent call の指示文、調査範囲、修正方針、起動パラメータを確認するときは、対応する prompt builder を読む。
- コミット範囲の変更を人間向けに要約するときは、変更要約用の出力契約を読む。

## hash
- b7cbad24690341444e996dc6a9bc3a45ee16db64cba5ff2ae78125c1a95d0e4c

# `file_review_and_fix.py`

## Summary
- refactor fork で、特定ファイルを起点にレビューと修正を行う agent call の prompt と起動パラメータを構築する。

## Read this when
- ファイル単位の調査、realization file の修正、修正後の確認を一つの agent call で行う処理の prompt や実行条件を変更・調査するとき。

## Do not read this when
- 指定 commit 範囲の差分全体を要約する処理を変更するときは、変更要約用の構築定義を読む。

## hash
- b79c0910b6d7e77e87c1ffb910367af03ba4be434133b751a6854e387c6ea146
