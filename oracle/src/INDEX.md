# `oracle`

## Summary
- `oracle/src/oracle` 配下の builder 系正本仕様断片を束ねる入口。`acp_builder` を起点に、agent call 周辺の用途別仕様、共通基盤、プロンプト構成補助をどこで読むかを絞るために使う。
- 配下の主対象は、ACP builder の領域分岐を案内する `acp_builder`、共通モデルと文書化・パス解決の基礎を扱う `other`、prompt 組み立ての部品群を扱う `prompt_builder`。

## Read this when
- builder 系のどの正本仕様断片を読むべきか、まず入口を絞りたい。
- apply / review / session / tui の各領域、共通部品、型定義、INDEX エントリー生成契約、設定やパス表現、prompt 構成のどれを確認すべきか整理したい。
- 個別領域へ進む前に、この階層で対象が builder 系か、共通基盤か、prompt 構成かを判断したい。

## Do not read this when
- 個別の実装詳細やテスト内容だけを確認したい。
- ACP builder 以外の正本仕様を探している。
- すでに読む下位領域が特定できており、この入口で再度絞り込みたくない。

## hash
- 090d5049f0da48008f81a34c47522a285afc305e7ce0be31e5f427f18ec0b708
