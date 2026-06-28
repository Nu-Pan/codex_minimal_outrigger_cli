# `__init__.py`

## Summary
- ACP builder の session join 領域を、oracle 側の対応するモジュール構成と互換にするための package 入口を示す。
- 実処理ではなく package としての存在および互換境界を担うだけの薄い初期化対象である。

## Read this when
- ACP builder の session join 領域で、package 階層や import 経路の互換性を確認するとき。
- oracle 側の対応領域と realization 側の package 構成が対応しているかを調べるとき。
- session join 配下の実装へ進む前に、この階層が package として成立している理由だけを確認したいとき。

## Do not read this when
- session join の具体的な処理内容、関数、クラス、入出力仕様を調べたいとき。
- ACP builder 全体の設計や session join 以外の領域を調べたいとき。
- oracle 側の正本仕様そのものを確認したいとき。

## hash
- b0d15cb786f4514211487ee0127714fafa93fe6b3674ae0b61f53efd3bd9602c

# `conflict_resolution.py`

## Summary
- セッション join 時の競合解決ロジックの realization 側入口であり、正本側の同名実装をそのまま再公開する薄い委譲モジュール。競合解決の実体は正本側に集約され、この対象自体は実装差を持たない。

## Read this when
- realization 側からセッション join の競合解決機能がどの正本実装へ接続されているかを確認したいとき。
- 競合解決ロジックの import 経路や公開名のつながりを、realization 実装側の入口として確認したいとき。

## Do not read this when
- 競合解決の具体的な判定条件、分岐、データ構造を知りたいとき。この対象は委譲だけなので、正本側の対応実装を読む。
- セッション join 全体の構成や他の join 処理を調べたいとき。この対象は競合解決入口だけを扱うため、より上位または隣接する join 関連対象を読む。

## hash
- 567e04ccfa10d6cdad9ae8687b6f955d32d2f76999e359d8b1ff184e838f2bab
