# `oracle`

## Summary
- cmoc の oracle 層に属する agent call builder、prompt builder、入力スキーマ、設定・パス・構造化文書の基盤をまとめた実装群。oracle の編集・調査、realization 追従、feedback 処理、session join、TUI・quota probe、INDEX エントリー生成へ進む入口を提供する。

## Read this when
- oracle 関連の agent call 構築、prompt・policy、Structured Output schema、または共通のパス・設定・文書モデルを横断して確認するとき。
- oracle file の編集・調査や realization への反映、feedback issue の処理など、cmoc の各機能が agent call をどう構成するかを調べるとき。
- 下位の個別 builder・policy・schema のどこから読み始めるべきか判断するとき。

## Do not read this when
- 特定の agent call の詳細な prompt、schema、結果処理だけを確認したいときは、該当する acp_builder、prompt_builder、feedback、または editor_input_handoff の下位要素を直接読む。
- 共通の実行処理、Codex CLI 呼び出し、設定の永続化、Git 差分処理など、oracle 層の定義を利用する処理だけを調べたいとき。
- 実際の oracle file や realization file の内容、正本仕様そのもの、または INDEX.md の既存エントリーを確認したいとき。

## hash
- e2de1bf2fbc25c3af9fea650b81a6fb3eff25950fd81166b4a9e37e686678f7d
