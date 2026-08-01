# `oracle`

## Summary
- AIエージェント呼び出し用パラメータを構築する正本ソースを扱うディレクトリ。共通パラメータ、INDEX.md生成、oracle操作、realization適用、session競合解消、TUI起動に関する下位領域への入口を提供する。
- 設定・パスモデル・規範構造・Markdown構造化文書を扱うPythonモジュール群。リポジトリ固有設定、agent callのパス解決、Standard/Requirementの変換、StructDocのレンダリングを調査・変更するときに読む。
- プロンプトビルダーの中核実装を扱うディレクトリ。placeholder型、agent callプロンプトの構築、エディタ初期文面、oracle／realization／INDEXなどの規範部品を確認・変更するときの入口を提供する。

## Read this when
- agent callの共通パラメータ、INDEX.md生成、oracle操作、realization適用、session joinの競合解消、TUI起動を調査・変更するとき
- CmocConfig、agent callのパスモデル、Standard/Requirement、StructDocのMarkdownレンダリングを調査・変更するとき
- agent callに渡す完全なプロンプト、プロンプト入力エディタの初期文面、規範注入、placeholder型を調査・変更するとき

## Do not read this when
- oracle fileやrealization fileの具体的な仕様・実装内容だけを確認するとき
- 一般的なprompt構築、path解決、構造化文書レンダリングなど、別の共通実装を調査するとき
- CLI実行フロー、設定ファイル生成・同期、個別の規範本文、ModelClass・ReasoningEffort自体の定義だけを調査するとき
- 個別のプロンプトパーツ本文、CLI、パスモデル、構造化文書機構、プロダクト機能を調査するとき

## hash
- f45c9b8c9373fdef3550954dfa322543859290c173d1e9a1a4eda9c8d0dfee6b
