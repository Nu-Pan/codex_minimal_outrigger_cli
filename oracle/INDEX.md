# `doc`

## Summary
- `app_spec` は cmoc の実行仕様をまとめる oracle/doc 配下の上位入口で、CLI 起動前後の共通規則、出力、ログ、エラー処理、run 隔離、状態管理、外部 model provider 境界、補完、利用手順を横断して確認するときに使う。
- 個別サブコマンドへ進む前に読むルーティング用の文書で、cmoc 全体の挙動を把握したいときにここから sub_command 配下へ分岐する。

## Read this when
- cmoc 全体の実行仕様を横断して把握したいとき。
- CLI 補完、ログ、エラー処理、run 隔離、状態管理、prompt、外部 model provider との責務分担をまたいで確認したいとき。
- どの個別サブコマンド仕様へ進むべきか判断したいときの入口として使うとき。

## Do not read this when
- 個別サブコマンドの挙動だけを確認したいときは、対応する sub_command 側を直接読む。
- oracle file と realization file の一般的な役割分担や編集規則だけを確認したいとき。
- この配下にない別領域の仕様や実装を調べたいとき。

## hash
- eba2cbcbec6eaf0769411bcd4e779c153e303366af81a7408f6234ba26b1596b

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
