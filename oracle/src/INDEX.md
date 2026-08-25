# `oracle`

## Summary
- oracle 関連の agent call 構築、feedback 入力契約、設定・パス・構造化文書の補助モデル、prompt と policy の生成定義をまとめた領域です。
- agent call の共通パラメータや目的別の起動設定を確認する場合は `acp_builder`、feedback issue の入力・検証契約を確認する場合は `feedback`、設定・パス解決・Markdown レンダリングを確認する場合は `other`、prompt の統合や oracle／realization・routing policy を確認する場合は `prompt_builder` へ進みます。

## Read this when
- oracle や realization を扱う agent call の構築責務と、目的別の prompt・Structured Output schema の入口を探すとき
- feedback、indexing、oracle review、realization、session、quota probe、TUI に関する agent call 設定を調査するとき
- prompt の組み立て、アクセス規定、routing、oracle／realization の policy を確認または変更するとき
- cmoc の設定モデル、agent call のパス境界、構造化文書の Markdown 化を確認するとき

## Do not read this when
- Codex CLI の実際の起動処理や backend モデル名への変換を確認したいとき
- oracle や realization の正本仕様本文、実装本文、feedback state、INDEX.md の内容を直接確認したいとき
- agent call と無関係な CLI 挙動や、別領域の仕様・テストだけを調査するとき

## hash
- ab0d3833563fdf0ecba76b4e1c4ac19273d5e8504ff36b95ca5738caaf7ef8c2
