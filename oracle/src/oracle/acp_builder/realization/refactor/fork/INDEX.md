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
- refactor fork の run branch 差分を人間向けに要約する agent call の prompt と起動パラメータを構築する入口。
- 差分本文、linked worktree の作業コンテキスト、readonly 権限、変更要約用の実行条件をまとめて AgentCallParameter に変換する。

## Read this when
- refactor fork の変更差分要約処理を追加・変更・調査するとき。
- run branch の差分を入力にした agent call の prompt 構成、作業ディレクトリ、readonly 実行条件、indexing preflight の設定を確認するとき。

## Do not read this when
- 変更要約 agent の出力内容や出力形式そのものを確認したいとき。
- refactor fork 以外の agent call 構築や、差分生成・適用の処理を確認したいとき。

## hash
- c68ab8c4910f4000666585fbc7b22832c6233114efe3182086389dcb99bf6d28

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
- refactor fork におけるファイル単位のレビュー・修正用 AgentCallParameter の構築定義。指定した oracle または realization file を起点に調査対象と対応する realization file を特定し、レビュー・修正 prompt と実行条件を組み立てる。

## Read this when
- refactor fork のファイル単位レビュー・修正 agent call の prompt、対象範囲、realization 書き込み権限、構造化出力、実行前 indexing 設定を確認するとき。
- 差分に依存しない追従レビュー用パラメータの生成経路を調査するとき。

## Do not read this when
- レビュー・修正対象の具体的な realization file の内容や個別所見を確認したいとき。
- refactor fork 以外の agent call 構築定義、または共通 prompt 生成処理そのものを直接調査するとき。

## hash
- 8819b72b73854e978dd9b8ee00639c047de37c61468e1c0fa6c9860977ec2709
