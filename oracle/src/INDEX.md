# `oracle`

## Summary
- AI 呼び出し契約、プロンプト構築、共有補助モデルを実装形式で記述する正本仕様断片群への入口。論理的なモデル区分・reasoning effort・ファイルアクセスモード、用途別の AgentCallParameter、完全プロンプトの組み立て、設定・パス・規範・構造化 Markdown の基礎モデルを扱う。
- この領域の本文はプログラム言語や JSON schema で書かれた oracle src であり、自然言語ドキュメントの本文仕様そのものではなく、cmoc が AI agent に渡す契約や正本仕様を生成・表現するための型と構築規則を確認する起点になる。

## Read this when
- AI コーディングエージェント呼び出しに渡す論理パラメータ、prompt、Structured Output schema、モデル品質区分、ファイルアクセス制約の正本仕様断片を探すとき。
- indexing、oracle review、apply fork、session join、TUI 実行パラメータ解決など、用途別の AI 呼び出しがどの role・summary・goal・標準プロンプト・schema を使うか確認したいとき。
- 完全プロンプトの構成順、静的・動的プロンプトの分離、標準規範プロンプト注入フラグの依存関係、プレースホルダ定義の扱いを調べるとき。
- cmoc 全体で共有される永続設定、root path placeholder と実パス解決、oracle standard などの規範データ構造、階層化文書の Markdown レンダリング helper を確認するとき。

## Do not read this when
- 利用者向け CLI サブコマンドの実行フロー、状態ファイル、git 操作、外部プロセス起動、画面操作、バックエンド CLI への実パラメータ変換だけを調べたいとき。
- 自然言語で書かれた oracle doc の要求本文や、oracle test の検証内容そのものを読みたいとき。
- realization implementation や realization test の現在の実装・修正対象を探しており、正本仕様断片としての型・構築規則・AI 呼び出し契約を確認する必要がないとき。
- 特定の用途別 prompt、schema、設定モデル、パスモデル、規範モデルなど読むべき本文がすでに分かっており、その対象へ直接進めばよいとき。

## hash
- 7f095959aaee8f9f8d406260d66b82781e71fb994119c5cde8879125aff72806
