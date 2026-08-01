# `apply`

## Summary
- `cmoc realization apply fork` 実行時に使う `codex exec` 用 AgentCallParameter の正本コード。prompt、権限、oracle 差分、実行用 worktree、commit 範囲、モデル設定を組み立てる。

## Read this when
- `cmoc realization apply fork` の AgentCallParameter 生成や prompt 構成を変更・検証するとき。
- oracle 差分の渡し方、実行用 worktree、commit 範囲、モデル設定を調査するとき。

## Do not read this when
- 通常の realization 実装・テストを調査するとき。
- `cmoc realization apply fork` 以外の agent call 起動処理を調査するとき。
- oracle 変更に追従する realization 実装そのものを調査するとき。

## hash
- 1e237c12628442cd8f02b41ab9dc080c0d2b6cdf9b766868ba1048ff36c9840f

# `refactor`

## Summary
- refactor fork の変更要約と単一ファイルレビュー・修正に関する Structured Output schema、およびそれらを利用する AgentCallParameter 構築の正本実装を扱う。変更要約、レビュー対象 path の解決、prompt、権限、モデル設定、作業ディレクトリの確認・変更に進むための入口となる。

## Read this when
- refactor fork の変更要約 agent の出力形式、差分カテゴリ、要約、根拠 path を確認するとき
- 単一ファイルのレビュー・修正 agent の prompt、対象 path、権限、検証条件、git 操作制約を確認するとき
- 配下の変更要約またはファイルレビュー・修正の schema や AgentCallParameter 構築実装を確認・変更するとき

## Do not read this when
- レビュー対象ファイル自体の実装内容や個別の oracle/realization file の仕様を調査するとき
- 変更要約またはファイルレビュー・修正の Structured Output schema の詳細だけを確認したいとき
- 一般的な prompt 構築、path 解決、構造化文書レンダリングの実装だけを調査するとき

## hash
- f1ada39671e97d2728b0770519c14810a6fa95681b2ba97f0ee60e6fd531ece8
