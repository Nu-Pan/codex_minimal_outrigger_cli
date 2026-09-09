# `__init__.py`

## Summary
- oracle.acp_builder.session との互換性を保つための package 初期化ファイル。既存の acp.builder.session.* import を維持するためだけに残されている。

## Read this when
- acp.builder.session.* import の互換維持経路を確認する。
- oracle.acp_builder.session 参照への移行や、互換 package を削除できる条件を確認する。

## Do not read this when
- session 実装の挙動や構成要素を確認したい場合。
- 新規機能の入口や通常の公開 API を探している場合。

## hash
- 1c24d1b1720d385b0f3388d0c70ebd4fa053c26df3a40f54e8cb91484c901dc8

# `join`

## Summary
- `acp.builder.session.join` の互換 package と、session join の conflict resolution を canonical 実装へ委譲する import 経路を案内する。具体的な処理内容ではなく、互換性維持のための入口として読む対象。

## Read this when
- 既存の `acp.builder.session.join.*` import を維持する理由や、session join の conflict resolution が canonical 実装へ委譲される関係を確認するとき。
- realization 側の利用者向け公開面から互換参照を削除できる条件を調査するとき。

## Do not read this when
- session join の conflict resolution の仕様・具体的な振る舞い・実装を確認したいとき。
- 互換 import の実際の利用箇所を調べたいときは、参照元を直接検索する。

## hash
- b5b39442d76884d1539e2d24ee9aeafeaaa0abcd81bcc3cdda8e09ac6078bd2d
