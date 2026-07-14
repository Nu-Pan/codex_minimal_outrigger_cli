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
- `cmoc apply fork` の互換公開面と、その下で各 builder が oracle 実装へ委譲する薄い入口群をまとめる。ここでは実処理の詳細ではなく、どの入口が何の変換責務を持つかだけを案内する。
- 互換 package の削除可否を確認したい場合と、fork 系 builder から oracle 側の正本実装へ渡す前処理を追いたい場合に読む。

## Read this when
- 旧来の `cmoc apply fork` 系 import の互換性を維持すべきか判断したいとき。
- fork 系 builder で使う共通の repo root 解決や import 調整、oracle 側の parameter をそのまま受け渡す経路を確認したいとき。
- 変更要約、所見列挙、所見適用のいずれかの入口を個別に探していて、まずどのモジュールを読むべきか判断したいとき。

## Do not read this when
- `cmoc apply fork` の実処理や判定ロジックの詳細を知りたいときは、対応する oracle 側の正本実装を読む。
- 互換 import の維持可否ではなく、現行の制御ロジックや入出力変換そのものを変更したいとき。
- `cmoc apply fork` 以外のサブコマンドや、別系統の公開面を追いたいとき。

## hash
- 5d778304413e09362af156dacc97b5bf881792cfe1abff9ad0691fac4fc23cdf
