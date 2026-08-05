# `apply`

## Summary
- `cmoc realization apply fork` 用の codex exec 起動パラメータを構築する実装。oracle file の差分、commit 範囲、linked worktree を prompt に組み込み、FLAGSHIP モデルへ realization file の差分追従を委譲する入口。

## Read this when
- oracle file の変更を realization file へ追従させる AgentCallParameter を構築・変更するとき
- realization apply fork の prompt、作業範囲、差分参照、モデル設定、worktree 設定を確認するとき
- 差分追従の完了条件や realization write の委譲方法を調査するとき

## Do not read this when
- realization apply fork の差分適用ロジックやテストだけを調べるとき
- 一般的な prompt 構築処理を調べるとき
- AgentCallParameter や path context の共通定義を調べるとき

## hash
- 132f46ba2d4207e8b13105a02aa0265cc1bd78a348aa3c925878926a52fbe27c

# `refactor`

## Summary
- refactor fork の変更差分要約とファイル単位レビュー・修正を扱う構造化出力スキーマおよび AgentCallParameter 構築実装の入口です。
- 変更要約では、差分を意味論的カテゴリに分類し、概要と根拠となる変更パスを返す契約と、そのための READONLY prompt・モデル設定・事前インデックス処理を確認できます。
- ファイルレビュー・修正では、所見の根拠、変更パス、oracle 要求、実装状況、理由、対応結果を返す契約と、対象パス解決、REALIZATION_WRITE 権限、レビュー・修正用 prompt、検証条件の構築経路を確認できます。

## Read this when
- refactor 差分の変更要約に必要な出力項目や分類単位を確認するとき。
- 変更要約用 AgentCallParameter の prompt、入力差分、モデル・推論設定、構造化出力スキーマ、事前インデックス処理を変更・調査するとき。
- ファイル単位レビュー・修正の所見契約、根拠位置、変更パス、対応状態を確認するとき。
- ファイルレビュー・修正呼び出しの対象パス、アクセス権、prompt の事後条件、oracle・realization 参照規則、検証条件を変更・調査するとき。

## Do not read this when
- 変更差分の内容そのものを確認するときは、変更要約の出力契約や prompt 構築実装ではなく、差分入力元を直接読む。
- 対象ファイルの実装内容や個別仕様への適合性を調査するときは、ファイルレビュー・修正の契約ではなく、対象 realization file と対応する oracle file を直接読む。
- 構造化出力のフィールド定義だけを確認するときは、AgentCallParameter 構築実装ではなく、対応する JSON スキーマを読む。
- refactor fork 以外の agent call の prompt 生成や出力契約を調査するときは、このディレクトリを読まない。

## hash
- 8ef051073a3eeb089840bf555fe319e7ed1ca057dcc1e717f3168222d1b43e6a
