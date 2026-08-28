# `change_summary.json`

## Summary
- 対象は、realization refactor による変更差分を意味論的カテゴリへ分類し、人間向けの変更要約と根拠となる変更ファイルを対応付けて返す出力契約を定義する Structured Output schema です。
- 変更要約を作成・検証するときの出力形式の入口であり、変更の分類内容そのものや具体的な実装責務は定義しません。

## Read this when
- realization refactor の変更差分をカテゴリ別に要約する agent call の出力形式を確認するとき
- 各変更カテゴリに、人間向け要約と repository 相対の変更ファイル一覧を対応付ける必要があるとき

## Do not read this when
- 変更差分の実装内容や分類結果そのものを確認したいとき
- realization refactor 以外の出力形式や仕様を確認するとき

## hash
- 13d5ef8771340eda2ba02624ffcf0dac54739301c226e31d353d8ce465e5d401

# `change_summary.py`

## Summary
- refactor fork の作業差分を人間向けに要約する agent call の prompt と起動パラメータを構築する定義。
- 差分を補助情報として prompt に埋め込み、readonly の作業範囲、作業ディレクトリ、Structured Output schema、indexing preflight を指定する入口。

## Read this when
- refactor fork の変更要約 agent call の prompt 内容や起動パラメータを変更・確認するとき
- raw git diff の受け渡し、linked worktree の作業ディレクトリ、要約用 agent call のアクセスモードを確認するとき

## Do not read this when
- refactor fork の変更要約結果の schema や要約処理そのものだけを確認するとき
- refactor fork 以外の agent call 構築定義や、実際の refactor 実装差分を直接確認するとき

## hash
- e38bf155f8b84590a82476b2f75f5bbdd9a735eca013044f0f261d68d26ff18a

# `file_review_and_fix.json`

## Summary
- realization refactor のファイル単位レビュー・修正 agent call が、発見した所見、根拠、関連する oracle 要求、実装状況、対応結果を報告するための出力定義。レビュー結果の確認と、修正済み・未解消の対応状況を追跡する入口となる。

## Read this when
- realization refactor のファイル単位レビュー・修正 agent call の結果を確認するとき
- 所見の根拠、対応で生じた realization file の差分、oracle 要求との関係を追跡するとき
- レビューで発見された問題の修正済み・未解消の状態と検証結果を確認するとき

## Do not read this when
- realization の実装自体を調査・変更するとき
- oracle file の要求や設計上の責務を確認するときは、該当する oracle file を直接読むとき
- レビュー結果を扱わず、通常の agent call 入出力や別種の出力契約を確認するとき

## hash
- b7cbad24690341444e996dc6a9bc3a45ee16db64cba5ff2ae78125c1a95d0e4c

# `file_review_and_fix.py`

## Summary
- ファイル単位レビュー兼修正用の agent call パラメータを構築する定義です。
- 指定したレビュー対象 path と実行用 worktree から、レビュー・修正 prompt、アクセス範囲、Structured Output schema、実行時の作業ディレクトリをまとめた追従パラメータを生成します。

## Read this when
- ファイル単位で差分に依存しないレビュー・修正 agent call の入口を確認したいとき。
- レビュー対象を起点に oracle file と realization file を調査し、対応する realization file の修正まで行う prompt 構築規則を確認したいとき。

## Do not read this when
- レビュー対象の実装内容そのものを確認したいとき。
- レビュー結果の出力項目や JSON schema の詳細を確認したいとき。
- 実際の realization のレビュー・修正処理を直接調査したいとき。

## hash
- 0e411bfc7a3e9a8be6e838198582fe64854e1498226d51ec17ede9add2336ce0
