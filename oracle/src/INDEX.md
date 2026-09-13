# `oracle`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータとファイルアクセスモードを定義する基盤。
- quota probe、INDEX.md エントリー生成、feedback issue の正規化・修正、oracle 調査・編集、realization 追従、session join の conflict 解消、TUI 起動に関する agent call 構築処理への入口。
- agent call ごとの prompt、対象範囲、起動 cwd、Structured Output、editor input handoff、indexing preflight の設定を扱う。

## Read this when
- agent call の共通パラメータ、論理ファイルアクセスモード、または起動設定を確認するとき。
- cmoc の個別サブコマンドに対応する agent call の prompt、権限、対象範囲、Structured Output 設定を調べるとき。
- quota、indexing、feedback、oracle、realization、session join、TUI の下位処理へ進む入口を判断するとき。

## Do not read this when
- ファイルアクセスモードの正本上の意味や Codex CLI sandbox への対応を確認したいとき。
- agent call の実際の実行処理、prompt 共通構造、path context、構造化文書のレンダリングを直接調べたいとき。
- feedback の受付・候補 issue 管理、oracle file や realization file の具体的内容、または通常の Git 差分処理そのものを調べたいとき。

## hash
- cf42c0c1bc25a5598cb3a6eac062ad18110772b29f8f24ce997698b59713fcf6
