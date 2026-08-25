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
- refactor fork の変更差分を人間向けに要約する agent call の prompt と起動パラメータを構築する定義。差分を補助入力として完全 prompt に埋め込み、readonly・効率重視の実行条件と Structured Output schema を指定する。

## Read this when
- refactor fork の変更差分要約 agent call の prompt 内容、入力差分の渡し方、実行モデルや推論設定、作業ディレクトリ、読み取り専用条件を確認・変更するとき。

## Do not read this when
- 変更要約の出力形式そのものを確認するときは、対応する Structured Output schema を直接読む。
- refactor fork の実際の変更内容を確認するときは、この起動定義ではなく生成された raw git diff や対象の実装差分を直接読む。

## hash
- bc780d3ef3c3f1e9bee23801596aa74afa59f4c45e19bdc0ab6629272d98eec2

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
- refactor fork のファイル単位レビュー・修正用 AgentCallParameter を構築する定義。対象パスと実行用 worktree からパス文脈を作り、差分に依存しないレビュー・修正 prompt、各種 policy、構造化出力 schema、実行設定を組み立てる。レビュー対象の realization file と、それを起点に参照される prompt・oracle・path・構造化文書関連の実装へ進む入口となる。

## Read this when
- refactor fork のファイル単位レビュー・修正 agent call の prompt や実行パラメータを変更・調査するとき
- 対象 path、run worktree、ファイルアクセスモード、モデル・推論設定、preflight 実行の構築方法を確認するとき
- レビュー結果の realization policy、findings policy、routing policy、変更 path の事後条件がどこで prompt に組み込まれるか確認するとき
- 対応する Structured Output schema と builder の整合性を確認するとき

## Do not read this when
- レビュー・修正 agent call の一般的な実装詳細を直接調べる必要がなく、対象 realization file や対応 schema を直接読む方が目的に近いとき
- refactor fork 以外の agent call 種別の parameter builder を調査するとき
- prompt の共通生成処理そのものを調査するときは、この定義ではなく build_complete_prompt の実装を直接読むべきとき
- パス解決や構造化文書の markdown rendering の仕様だけを確認したいときは、各 oracle・実装を直接読むべき

## hash
- e258bae63612847e0bb508c912c8a6172b3bebf371d62279c1951a90de43134c
