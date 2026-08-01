# `change_summary.json`

## Summary
- 変更要約生成エージェントの構造化出力スキーマを定義し、変更内容をカテゴリ別の要約と根拠ファイル一覧として返せるようにする。

## Read this when
- refactor fork の変更要約出力形式や、要約結果の検証項目を確認するとき

## Do not read this when
- ファイル単位レビュー・修正の出力形式を確認したいときは、対応するレビュー用スキーマを直接読む

## hash
- dc922a0d0f2d939d57f9fe06e94599cbe8166bdbfd52c2ff17cd5c65882b6eda

# `change_summary.py`

## Summary
- refactor fork の変更差分を要約する agent call 用パラメータを構築する。差分を動的 prompt に埋め込み、読み取り専用の linked worktree を対象として、効率重視のモデル設定と Structured Output schema を指定する。

## Read this when
- refactor fork の run branch 差分を人間向けに要約する prompt 構築や、その agent call の実行条件を確認するとき。

## Do not read this when
- refactor fork の実際の変更内容を調査するときは、生成された差分や対象実装を直接読む。
- 変更要約の出力形式そのものを確認するときは、対応する Structured Output schema を直接読む。

## hash
- e8ae11e0b02d60a1916d306796b879d5a57e176398051e2aa648ff069224d985

# `file_review_and_fix.json`

## Summary
- 対象ファイルは所見を記録するための Structured Output schema であり、内容上の要修正点は確認できません。

## Read this when
- この schema のレビュー結果を確認するとき

## Do not read this when
- 実装ファイルの挙動や修正内容を調査するとき

## hash
- 0510d3855b5b99e1f3cfbcdfb863e34e58dc00054954c748b0b6ccf8129677cc

# `file_review_and_fix.py`

## Summary
- `cmoc realization refactor fork` のファイル単位レビュー・修正用 AgentCallParameter を構築する。対象ファイルと実行用 worktree を受け取り、パス文脈、完全なレビュー・修正プロンプト、モデル設定、構造化出力 schema、cwd、事前 indexing をまとめて返す。レビュー対象の oracle/realization file を起点に、調査・修正・検証まで行う agent call の設定入口である。

## Read this when
- ファイル単位の realization review・fix agent call のプロンプト内容、権限、検証要件を変更または確認するとき
- レビュー対象 path と linked worktree の解決、モデル・推論設定、structured output schema の指定を変更するとき
- refactor fork 系の agent call parameter 構築処理を調査するとき

## Do not read this when
- レビュー・修正 prompt の詳細ではなく、実際のレビュー処理や realization code の実装を調査するとき
- 構造化出力の具体的な schema 定義だけを確認するときは、対応する schema file を直接読む
- 他の agent call 種別の prompt 構築規則だけを調査するとき

## hash
- cb92108ab52a21f75bf7203e62fef63cd2a0dff36e5d2d53ab96d7b0cbef1d70
