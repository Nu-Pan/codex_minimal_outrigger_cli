# `doc`

## Summary
- `app_spec` 配下の正本仕様断片群への入口。CLI の起動前処理、補完、実行呼び出し、ログ、事前検証、エラー処理、model provider 境界、索引更新、prompt 標準、run 隔離、session 状態、利用手順のような横断仕様を確認するときに進む。

## Read this when
- cmoc の CLI 全体に関わる横断仕様を確認・実装・修正・テストするとき。
- 補完、`codex exec` 呼び出し、ログ出力、doctor preprocess、エラー処理、indexing、session/apply 状態、run 隔離、外部 model provider 境界のどれを読むべきか切り分けたいとき。
- 利用手順や prompt 標準のように、個別コマンドの細部ではなく共通の起動・出力・状態管理の規則を確認したいとき。

## Do not read this when
- 個別サブコマンド仕様を直接知りたいときは、`sub_command` 配下の該当仕様を先に読む。
- この階層ではなく、個別の CLI 引数や状態フィールドの細部だけを確認したいとき。
- oracle file と realization file の一般論や、INDEX.md エントリー作成ルールそのものを調べたいとき。

## hash
- f5f6357fd57dca315cc37eb5dfb45da49846f8595076a48eae725db41550e2dd

# `src`

## Summary
- `oracle/src` 配下の正本仕様断片への入口。`acp_builder` を起点に、builder 系の用途別仕様、共通基盤、prompt 構成補助のどこを読むかを絞るために使う。
- 主に案内する対象は、ACP builder の領域分岐を担う `acp_builder`、共通モデルと文書化・パス解決の基礎を扱う `other`、prompt 組み立ての部品群を扱う `prompt_builder`。

## Read this when
- builder 系のどの正本仕様断片を読むべきか、まず入口を絞りたいとき。
- apply / review / session / tui の各領域、共通部品、型定義、INDEX エントリー生成契約、設定やパス表現、prompt 構成のどれを確認すべきか整理したいとき。
- 個別領域へ進む前に、この階層で対象が builder 系か、共通基盤か、prompt 構成かを判断したいとき。

## Do not read this when
- 個別の実装詳細やテスト内容だけを確認したいとき。
- ACP builder 以外の正本仕様を探しているとき。
- すでに読む下位領域が特定できており、この入口で再度絞り込みたくないとき。

## hash
- e683a5491cf65253cb901798c4111e77e159b2719a4bad1b10face6280bf90b7
