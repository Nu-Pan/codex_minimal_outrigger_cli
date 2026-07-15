# `__init__.py`

## Summary
- `acp.builder.apply` 系の既存 import を保つための互換パッケージ。実処理は正本側の apply 実装へ進める入口として扱う。

## Read this when
- `acp.builder.apply` 配下の実装を探していて、既存の import 経路を壊さずに正本側の実装へ進みたいとき。

## Do not read this when
- 新しい apply 実装の正本を探したいときは、互換層ではなく `oracle/src/oracle/acp_builder/apply` 側を見る。
- この互換層の内部に実処理や仕様本体がある前提で読むべきではない。

## hash
- 484f419d6ff82058c68a8e19540e3837fc6e40e96b976026d61532af98ae9bfb

# `fork`

## Summary
- `cmoc apply fork` の realization 側 builder package。正本側 builder への委譲入口と、repo root・oracle import 解決などの共通処理を扱い、ファイル単位レビュー・修正および変更要約の agent call parameter を構築する。

## Read this when
- `cmoc apply fork` の realization 側 builder の責務や、正本 builder への委譲経路を確認するとき。
- fork 系 builder の repo root 解決、oracle import、ACP parameter の受け渡しを変更するとき。
- ファイル単位レビュー・修正または変更要約の parameter 構築入口を変更するとき。

## Do not read this when
- `cmoc apply fork` のループ制御、再投入、commit、state 遷移を調べたいとき。
- レビュー・修正や変更要約の prompt・schema など、正本仕様そのものを確認したいとき。
- `cmoc apply fork` 以外のサブコマンドの実装や、fork builder と無関係な import 解決を変更したいとき。

## hash
- a54a5a0855c60c8416edffeb93bfae4bdd9f7c780aec7743f8eb4d75eda73e06
