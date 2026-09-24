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
- refactor fork の変更要約 agent call を構築し、指定された commit 範囲の tree 差分を Git から取得して要約する prompt と起動パラメータを定める。commit 範囲や prompt、アクセス方式など、この call の組み立てを変更する際の実装上の入口。
- 同じ fork 配下のファイル単位の所見調査・修正 call は別の builder が扱う。

## Read this when
- fork report 向け変更要約 call の prompt や、要約対象の commit 範囲の渡し方を変更するとき。
- この call のアクセス方式、作業ディレクトリ、preflight などの起動パラメータを変更するとき。

## Do not read this when
- 変更要約を生成する条件や、空差分・中断・エラー時の report 上の扱いだけを確認するとき。refactor fork の正本仕様を読む。
- ファイル単位の所見調査・修正 call の prompt や動作を変更するとき。同階層の別 builder を読む。
- この call の出力データ構造だけを変更するときは対応する Structured Output schema を、model provider や reasoning 設定を変更するときは agent call 設定を読む。

## hash
- 8ce6ede01b04ca8b537c53b595aab7743ffa6d50dec7b009314136714ac4547f

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
- refactor fork で指定された oracle／realization file を起点に所見を調査し、対応する realization file の修正・検証を行う agent call の prompt と起動パラメータを構築する。

## Read this when
- ファイルを起点とする refactor fork の調査・修正で、対象範囲や書き込み方針、完了条件、起動時の振る舞いを確認・変更するとき。

## Do not read this when
- 指定 commit 範囲の変更内容を人間向けに要約するだけなら、差分要約用 builder を読む。
- commit 差分の oracle 変更をリポジトリ全体の realization file に適用する作業なら、差分駆動の追従用 builder を読む。

## hash
- 8819b72b73854e978dd9b8ee00639c047de37c61468e1c0fa6c9860977ec2709
