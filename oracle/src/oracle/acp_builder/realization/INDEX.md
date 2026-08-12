# `apply`

## Summary
- `cmoc realization apply fork` における差分追従用の AgentCallParameter を構築する対象。commit 範囲と oracle file の raw git diff を prompt に組み込み、realization file への反映条件と単一 agent call の起動設定をまとめる。

## Read this when
- `cmoc realization apply fork` の oracle file 差分追従処理を確認・変更するとき
- commit 範囲や oracle diff の prompt 組み込み方法を調査するとき
- 差分追従 agent call のモデル、推論強度、ファイルアクセス、linked worktree、実行前 indexing などの設定を変更するとき

## Do not read this when
- 通常の realization 実装やテストの挙動を確認するとき
- 一般的な prompt 生成や共通の AgentCallParameter 構築規則を確認するとき
- `cmoc realization apply fork` 以外の起動経路を調査するとき

## hash
- 7147dbd62af417a0061881af4e4556cadcf74648d6e421f49500339e7290f4db

# `refactor`

## Summary
- refactor fork における変更要約と、ファイル単位のレビュー・修正を行う agent call の定義および Structured Output スキーマを扱う領域。変更差分の意味的要約、oracle と realization の調査、対応する realization file の修正、修正後の検証に関する入口を提供する。
- 変更要約の出力契約だけを確認する場合は change_summary.json、レビュー結果の項目や対応状態だけを確認する場合は file_review_and_fix.json を読む。agent call の prompt、権限、パス解決、実行条件を確認・変更する場合は対応する Python 定義へ進む。

## Read this when
- refactor fork の変更差分を構造化して要約したいとき
- ファイル単位のレビュー・修正 agent の呼び出し条件、調査範囲、修正権限、検証規則を確認・変更するとき
- 変更要約またはレビュー・修正結果の出力契約を確認するとき

## Do not read this when
- 個別のレビュー対象ファイルの実装内容や具体的なレビュー所見を調査するとき
- 変更要約またはレビュー結果の項目・型・形式だけを確認するときは、対応する JSON スキーマへ直接進む
- 共通の prompt 構築処理や path 解決処理だけを確認したいときは、共通実装へ直接進む

## hash
- e9b6113a6311bc212d33254d89e828dde914cc3839e3dd941677061f8dc1b399
