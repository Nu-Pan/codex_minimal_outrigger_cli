# `doc`

## Summary
- cmoc の正本文書を、アプリケーション仕様と開発規約に分けて案内するディレクトリ。`app_spec` では実行契約、状態管理、サブコマンド、workflow、prompt、feedback、通知などの利用・挙動仕様へ進み、`dev_rule` では Python 実装、CLI 配置、環境、テスト要件、品質検査の規約へ進む。`branch_model` や `considered_alternative` ではブランチ設計や不採用案の背景を確認できる。

## Read this when
- cmoc の正本文書群から、アプリケーションの挙動仕様と開発規約のどちらを確認すべきか判断するとき
- 実行・状態管理・サブコマンドなどの利用契約、または Python 実装・CLI 配置・環境・テストの規約を対応する下位文書へ振り分けるとき
- branch、commit、worktree の関係や、採用しなかった設計案の背景を確認するとき

## Do not read this when
- 特定のアプリケーション機能、開発規約、branch model、不採用案の詳細を確認する場合は、対応する下位文書を直接読むとき
- 具体的な実装ファイル、テスト実行結果、既存 INDEX.md の内容を調べるとき

## hash
- 14a6716425bc4ff6d8f3c784e1edc417152871205534d8137df7e11ce405efef

# `src`

## Summary
- oracle 配下の agent call 構築、prompt・policy の生成、feedback 入力契約、設定・パス解決・構造化文書の補助モデルを実装する領域です。
- agent call の共通パラメータや目的別起動処理を調べる場合は `acp_builder`、prompt の統合や oracle／realization・routing・feedback の規定を調べる場合は `prompt_builder`、設定・パス解決・構造化文書のモデルとレンダリングを調べる場合は `other`、feedback reporter の入力契約を調べる場合は `feedback` へ進みます。

## Read this when
- agent call のモデル、reasoning effort、ファイルアクセス、作業ディレクトリ、Structured Output schema、indexing preflight の構築を確認または変更するとき
- prompt の統合、placeholder、oracle／realization の基本定義、ファイルアクセス、routing、feedback、review、conflict resolution の policy を確認または変更するとき
- agent call に使う root path の解決、パス境界、設定モデル、Structured Document の Markdown レンダリングを確認するとき
- feedback observation の入力項目・分類・重要度・根拠・継続状態の契約を確認するとき

## Do not read this when
- Codex CLI の実際の実行、backend へのモデル名変換、または外部プロセス起動の実装だけを確認したいとき
- oracle／realization の正本仕様本文や、realization 側の実装・テストを直接確認したいとき
- INDEX.md の既存ルーティング内容を確認したいとき
- agent call、prompt、feedback、設定、パス解決、構造化文書に関係しない CLI 挙動や別領域の仕様・テストだけを調査するとき

## hash
- c3273e05e2785c83946120d4cb928499a9a956fb6a749f806fbe103a4e762849
