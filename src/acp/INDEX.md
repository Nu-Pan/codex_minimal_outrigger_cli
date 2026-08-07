# `__init__.py`

## Summary
- `acp` 互換の公開入口を扱う。`acp.*` を利用している既存参照を、`oracle.*` または実体モジュールへ移す必要があるときに読む。

## Read this when
- `acp` という公開名を残すべきか、削除できるかを判断したいとき。
- 既存の利用者向け参照を壊さずに、`oracle` 側の実体へ切り替える導線を確認したいとき。

## Do not read this when
- `acp` 配下の具体的な実装内容や移行先の詳細を知りたいだけなら、直接その実体モジュールを読む。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変えたいだけならここではない。

## hash
- fe0939ab61e919bfb5ae35264e02859ee36efb102a15498d95fcbd45f9670e76

# `builder`

## Summary
- ACP builder の realization package。既存の `acp.builder.*` import 経路を維持する互換入口と、oracle 側の canonical builder へ委譲する各種 adapter をまとめる。
- 共通の Markdown code fence 保護、feedback・indexing・session・TUI・quota probe、oracle command、realization apply/refactor など、用途別の builder 接続点を下位要素から辿る起点となる。

## Read this when
- ACP builder の realization package 全体の構成、互換 import 経路、canonical builder への委譲関係を確認するとき。
- 特定の builder 用途に対応する下位 adapter の入口を選ぶとき。
- prompt の動的 section 保護や、oracle・realization command の builder 接続経路を調査するとき。

## Do not read this when
- canonical な builder の仕様、prompt 本文、モデル設定、実装詳細を確認したいとき。対応する oracle 側の対象を直接読む。
- 特定の用途の builder 実装を変更・調査するとき。該当する下位ディレクトリまたはモジュールを直接読む。
- ACP builder の利用箇所や利用者向け公開面を調査するとき。各参照元を直接読む。

## hash
- 2ac96fcb8cb677cefba4ff05a700955577260a4694c0d555072d3d1d5f58a737
