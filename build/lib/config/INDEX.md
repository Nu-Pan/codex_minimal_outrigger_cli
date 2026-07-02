# `__init__.py`

## Summary
- oracle src の cmoc_config を正本にしたまま、既存の config 名前空間からの参照を成立させる互換 import 入口。
- config.* 参照が realization 側や利用者向け公開面に残っている間だけ必要な橋渡しを担う。

## Read this when
- config.* 参照がどの正本設定へつながるかを確認したいとき。
- oracle src の設定定義を移動・改名せずに既存 import 互換性を保つ理由を確認したいとき。
- config.* 参照を削除できる条件や、この互換入口の存続理由を確認したいとき。

## Do not read this when
- cmoc_config の正本内容そのものを確認したいときは、oracle 側の設定定義を直接読む。
- 新しい設定仕様や設定値の意味を調べたいだけで、config.* 互換 import の扱いに関係しないとき。
- realization 側の具体的な config.* 利用箇所を探したいときは、利用元の実装を直接読む。

## hash
- 991b20cfe981e7da47b9fb4f45010bb926ac60ed1f2f88ce102a246827f26742

# `cmoc_config.py`

## Summary
- oracle 側の設定定義を複製せずに公開するための再公開層。既存の `config.cmoc_config` 参照を維持する互換入口として残されており、正本の設定内容そのものは持たない。

## Read this when
- realization 側や利用者向け公開面で `config.cmoc_config` 参照を維持する理由を確認したいとき。
- oracle 側の設定定義をコピーせず参照するための互換層を調べるとき。
- この再公開層を削除できる条件を確認したいとき。

## Do not read this when
- 設定定義の正本内容を確認したいとき。この対象は再公開だけを担うため、oracle 側の設定定義を読む。
- 新しい設定項目や設定処理の実装場所を探しているとき。この対象には独自の設定ロジックはない。
- `config.cmoc_config` 参照の互換維持や削除可否に関係しない作業をしているとき。

## hash
- 96661a3576725931d1a746eafcb745029a6db9b11df02841355452ad56759809
