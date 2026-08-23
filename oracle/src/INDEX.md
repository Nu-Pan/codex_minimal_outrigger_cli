# `oracle`

## Summary
- `oracle/src/oracle` は、cmoc の正本仕様を参照しながら agent call、feedback、prompt 構築などの中核定義へ進むための上位入口です。用途別の agent call 構築定義、共通モデル、feedback 入力契約、prompt builder など、下位領域の責務を横断して確認する際の起点になります。

## Read this when
- agent call の起動条件や用途別パラメータ構築、feedback 入力契約、prompt の構成定義を横断して調査・変更するとき
- 配下で対象となる下位領域がまだ特定できず、agent call または prompt 関連の実装入口を選ぶとき

## Do not read this when
- 特定の用途別 agent call 構築定義、feedback の入力スキーマ、prompt builder の個別実装を直接調査するときは、対応する下位対象へ進むとき
- agent call の実行処理、CLI サブコマンド、TUI 表示、個別の oracle・realization file の内容だけを確認するとき

## hash
- cae9a9d0e2f0564935c768e14dbcbda7806968c84043fe865d3877af56253ccf
