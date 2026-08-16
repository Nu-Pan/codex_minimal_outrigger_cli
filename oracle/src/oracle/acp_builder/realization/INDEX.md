# `apply`

## Summary
- `realization apply fork` の追従 agent 用 AgentCallParameter を構築する起動処理。commit 範囲と oracle file の raw git diff を完全 prompt に組み込み、run worktree、アクセス権、各種 policy、モデル・推論設定を指定する。

## Read this when
- `realization apply fork` の prompt、作業範囲、完了条件、run worktree、起動パラメータを変更または確認するとき。
- oracle file の変更を realization file 全体へ反映する agent call と、commit 範囲・raw git diff の prompt 埋め込みを調査するとき。

## Do not read this when
- `realization apply fork` 以外の apply 処理を調査するとき。
- 完全 prompt の共通生成規則を調査するときは、共通 prompt builder を直接読むとき。
- AgentCallParameter の共通データ構造や列挙値だけを調査するときは、基礎定義を直接読むとき。
- 個別の oracle file、realization implementation、realization test の仕様や挙動を確認するときは、対象ファイルを直接読むとき。

## hash
- 0547d2589048a2ea7c63b3d1920147e554738899a1bfd82d6fa0481fd20d132b

# `refactor`

## Summary
- refactor fork における変更差分の構造化要約と、ファイル単位のレビュー・修正を行う agent call の定義および出力契約をまとめた入口です。
- 変更要約の prompt、起動パラメータ、差分分類用 Structured Output schema を扱います。
- ファイルレビュー・修正の prompt、権限、対象 path 解決、検証方針、所見と変更 path の整合条件、および出力 schema を扱います。

## Read this when
- refactor fork の変更差分を意味論的カテゴリへ整理する agent call の prompt、実行設定、linked worktree、または出力形式を確認・変更するとき。
- ファイル単位のレビュー・修正 agent call の調査範囲、修正権限、oracle・realization 参照方針、検証条件、または所見出力契約を確認・変更するとき。

## Do not read this when
- 実際の refactor 差分、レビュー対象の実装、個別の oracle file や realization file の内容を調査するとき。
- 共通 prompt 生成処理や refactor fork 以外の agent call builder を確認・変更するとき。

## hash
- 66aba6dd17746b7a435681b9b653636acae9d44c28d1b1ddde0dc51baa23dfc4
