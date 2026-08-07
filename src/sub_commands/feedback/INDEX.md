# `__init__.py`

## Summary
- feedback サブコマンドの実装を担う。feedback サブコマンドの処理を確認・変更するときの入口。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。

## hash
- 314f863a7cbf0d8eb6a2e9f72ee941edfcbbfcc5768f529aed40f09e96968cb9

# `report.py`

## Summary
- feedback report コマンドの中核状態機械。raw observation の snapshot 固定、未処理 observation の validation と増分 normalization、machine/agent issue 統合、checkpoint 再利用、unit 単位の commit/rollback、assessment 再評価、前回 report との差分計算、可視化条件の適用、Markdown report と tracked report record の保存までを一つの中断可能な transaction として扱う。
- feedback normalization の ingestion・issue identity・revision・occurrence・assessment・report record を生成し、確定済み unit の commit ID、deferred/invalid 件数、再発・再検証・disposition 変更などを最終 report に反映する。
- feedback report の CLI 実行入口と、session branch・run state・clean worktree・tracked feedback state の事前条件検査も担う。

## Read this when
- `cmoc feedback report` の実行順序、状態遷移、snapshot、deferred observation、partial/interrupted 処理を調べるとき。
- feedback observation を machine rule または agent report の issue に正規化・統合する処理を変更または確認するとき。
- normalization checkpoint、unit commit/rollback、tracked feedback record、assessment の再評価を調べるとき。
- 前回正常 report との差分、既定表示と `--all` 表示、再発 issue・再検証要求・human disposition 変更の判定を調べるとき。
- feedback report の出力 Markdown、front matter、可視 issue の evidence/reference 表示、report record 保存を変更または確認するとき。

## Do not read this when
- feedback observation の envelope/schema や issue record のデータ構造そのものだけを調べるときは、先に `commons.runtime_feedback_state` などの直接の定義を読む。
- feedback normalization agent の prompt/Structured Output parameter の生成だけを調べるときは、`acp.builder.feedback.normalize_issue` を直接読む。
- 一般的な CLI runtime、git 操作、ログ、パス、report directory の共通実装だけを調べるときは、それぞれの `cmoc_runtime`、`commons.runtime_logging`、`commons.runtime_paths`、`commons.runtime_results` の定義を直接読む。
- feedback report の正本仕様や利用者向け挙動を確認するときは、対応する oracle 文書を先に読む。

## hash
- c2e07c0ded18d88fffc5d4a161cc9aa7de7349d27163b699d9d5c495dbe91ad9
