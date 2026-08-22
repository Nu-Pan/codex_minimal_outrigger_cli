# `doc`

## Summary
- `oracle/doc` は、cmoc の正本仕様・設計・開発ルールを機能別に参照するための上位入口。アプリケーション仕様、branch model、採用しなかった代替案、開発ルールへ進み、実装・テスト・環境・運用上の判断に必要な根拠を探すために使う。

## Read this when
- cmoc の正本仕様や設計・開発ルールの入口を探すとき
- アプリケーションの挙動、session/run と branch の関係、採用しなかった設計案、Python 実装・環境・テストの規約を確認するとき
- 個別の仕様書や開発ルール文書へ進む先を判断するとき

## Do not read this when
- 特定機能の詳細仕様や具体的な実装・テスト手順だけを確認する場合は、対応する下位文書を直接読む
- 実行時に生成された report やその他の生成物の具体的内容だけを調査する場合は、該当する生成物を直接調べる

## hash
- aa7e5f3d1f73847735d33a8a381558edd4b8a8d23395f5527b7cc6707d3f5d97

# `src`

## Summary
- cmoc の agent call に関する正本実装を配置するソースディレクトリ。AgentCallParameter と利用モデル・推論強度・ファイルアクセスの論理定義、quota probe、プロンプト構築、設定・パス・構造化文書モデル、feedback 入力検証を扱う。
- agent call の起動パラメータや quota 確認は `oracle/acp_builder`、完全プロンプトと用途別 policy は `oracle/prompt_builder`、設定・パス・構造化文書モデルは `oracle/other`、feedback 入力契約は `oracle/feedback` を入口にする。

## Read this when
- agent call の論理パラメータ、モデル・推論強度・ファイルアクセスモード、cwd、preflight、Structured Output の構築を確認または変更するとき
- agent call に渡す完全プロンプト、placeholder、oracle／realization／routing などの policy 構築を確認または変更するとき
- cmoc 設定、Codex provider 設定、パスコンテキスト、構造化文書モデルを確認または変更するとき
- feedback reporter に渡す入力形式や入力検証を確認または変更するとき
- oracle/src 配下で、目的に応じて acp_builder・prompt_builder・other・feedback のどこを読むべきか判断するとき

## Do not read this when
- 具体的な realization・oracle・TUI の実装やテストを確認したいときは、それぞれの対象を直接読む
- 個別の正本仕様や既存の INDEX.md の内容を確認したいときは、その対象を直接読む
- collector 側の feedback 保存・集約・重複判定や、問題検出後の継続判断だけを確認したいとき
- 実際に保存された設定ファイルの内容や TUI の画面表示だけを確認したいとき

## hash
- d8615d01db16a1ca9c2ae80d9cc3dc4fdb36497447ca1044d766262ff951410d
