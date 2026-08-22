# `oracle`

## Summary
- cmoc の agent 呼び出し構築、feedback 入力契約、設定・パス・Markdown ノード、prompt 構築を扱う実装群へのルーティング入口。共通の AgentCallParameter 契約や用途別 builder、feedback の構造化、設定・root 解決、完全な agent prompt の生成を横断して確認できる。
- 下位の acp_builder、feedback、other、prompt_builder が、それぞれ agent call 設定、feedback 入力契約、設定・パス・文書ノード、prompt 構築の詳細実装への入口となる。

## Read this when
- cmoc の agent call 構築と prompt 構築を横断して調査するとき
- feedback 入力契約、設定・パスモデル、Markdown 文書ノードの実装の所在を確認するとき
- 用途別の下位実装へ進む前に、関連する oracle 実装群の構成を把握するとき

## Do not read this when
- 特定用途の prompt、builder、feedback 検証、設定モデルの詳細だけを確認したいときは、対応する下位対象を直接読む
- Codex CLI の実行処理や oracle の正本仕様を確認したいときは、実行側実装または oracle 文書を読む

## hash
- b2715544e3f87a7190e4cc4701f407d102318ca54c70bd46f9923054014081f6
