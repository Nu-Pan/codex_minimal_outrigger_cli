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
- refactor fork の作業差分を人間向けに要約する AgentCallParameter を構築する正本実装。差分を補助入力として prompt、読み取り専用の実行条件、効率重視のモデル設定、Structured Output schema の参照先をまとめる。

## Read this when
- refactor fork の変更差分を要約する prompt 構築処理や、その AgentCallParameter の実行条件を確認・変更するとき。

## Do not read this when
- refactor fork の変更内容そのものや要約結果の形式だけを確認したいとき。差分入力や Structured Output schema の定義を直接確認する場合は、対応する入力元・schema を読む。

## hash
- af7d317b4f642b2960d33444e913d1f38c4f4a6e05ecc93c5f2844e52253b36a

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
- `cmoc realization refactor fork` における、単一ファイルを起点としたレビュー・修正用の AgentCallParameter を構築する oracle src。対象 path と実行 worktree を受け取り、完全なレビュー・修正 prompt、ファイルアクセス権限、モデル設定、構造化出力 schema、作業ディレクトリをまとめて返す。
- 対象ファイルを起点に、必要な oracle file・realization file の調査、所見への修正、修正後検証、テスト通過を agent に要求する prompt を組み立てる。差分推測の禁止、git add/commit の禁止、変更と findings の対応付けなどの作業上の制約も prompt に含める。
- レビュー対象 path は `AgentCallPathContext` と `resolve_real_path` で prompt 用の実パスへ変換し、`build_complete_prompt` と `render_as_markdown` を通じて最終 prompt 化する。実装本体ではなく、ファイル単位レビュー・修正 agent の呼び出しパラメータ生成を担う入口である。

## Read this when
- ファイル単位の realization refactor fork レビュー・修正 agent の起動条件、prompt 構成、対象 path の扱いを確認するとき。
- AgentCallParameter のモデルクラス、推論強度、realization write 権限、構造化出力 schema、agent call の作業ディレクトリ設定を変更・調査するとき。
- レビュー結果に求める findings/resolution、修正・検証・git 操作に関する制約を確認するとき。

## Do not read this when
- レビュー対象ファイルそのものの実装内容や、個別の oracle/realization file の仕様・実装を調査するときは、それぞれの対象ファイルを直接読む。
- レビュー結果の structured output schema の詳細だけを確認するときは、指定された schema ファイルを直接読む。
- 一般的な prompt 構築処理、path 解決、構造化文書のレンダリングの実装を確認するときは、対応する import 元のモジュールを直接読む。

## hash
- 0cc296fcb605b459776af995cf3befc7643a27a71e1204ee44c5f7f50a3816dd
