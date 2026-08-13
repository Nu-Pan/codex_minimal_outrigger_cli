# `oracle`

## Summary
- cmoc の oracle 実装パッケージ。agent call のパラメータ構築、prompt と Structured Output schema の定義、設定・パス・構造化文書モデル、feedback 入力契約を提供する。
- agent call の用途別定義は acp_builder、共通 prompt の組み立ては prompt_builder、設定・パス・文書モデルは other、feedback reporter の入力契約は feedback へ進む入口になる。

## Read this when
- cmoc の oracle 層で、agent 呼び出し定義、prompt 構築、Structured Output schema、設定モデル、パスモデル、構造化文書、feedback 入力契約を調査・変更するとき。
- 下位領域のどこから調査を始めるべきかを判断するとき。

## Do not read this when
- 実際の agent call 実行、CLI バックエンド、業務ロジック、状態保存、realization 実装を直接調べるときは、対応する実行側・状態管理側・realization 側へ進む。
- 個別の prompt、schema、設定型、パス型、構造化文書型だけを確認するときは、該当する下位領域へ直接進む。

## hash
- b02d95edeb7a1b6294433a524f7c332d056a84f5a8d95c0eba2e58ae309b59fc
