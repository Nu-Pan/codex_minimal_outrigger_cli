# `oracle`

## Summary
- `oracle` は cmoc の agent call、プロンプト、パス・設定モデル、Structured Markdown、feedback、indexing、oracle review、realization などの正本となる Python 定義と Structured Output schema をまとめる領域です。
- agent call の共通契約は `acp_builder`、完全 prompt の構築規則は `prompt_builder`、設定・パス解決・文書レンダリングの共通モデルは `other`、feedback 入力契約は `feedback` から確認します。

## Read this when
- cmoc の agent call パラメータ、モデル・推論設定、ファイルアクセス、cwd、Structured Output の構築を調査・変更するとき
- 完全 prompt の統合規則、prompt policy、placeholder、oracle・realization 関連の指示を確認するとき
- work root・repository root・run root のパス解決、cmoc 設定、構造化 Markdown のモデルやレンダリングを確認するとき
- feedback issue の入力契約、検証・同一性判断、または indexing のエントリー生成を確認するとき
- oracle review や realization など、下位機能の agent call builder と schema の入口を探すとき

## Do not read this when
- Codex CLI の実行制御、サブコマンドの通常フロー、または agent call の終了結果処理だけを調査するときは、対応する呼び出し側・実行処理を直接読む
- 個別の prompt policy、Structured Output schema、feedback reporter の保存・集約処理だけを確認したいときは、対応する下位要素を直接読む
- cmoc の正本仕様や開発・テスト手順だけを確認したいときは、対応する oracle 文書を直接読む

## hash
- 07834b7e08d1f253c3bac34277ea95804a14774ba3e23995c643d4b158f73b15
