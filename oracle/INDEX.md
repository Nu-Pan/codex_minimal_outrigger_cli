# `doc`

## Summary
- cmoc の正本ドキュメント群を集約するディレクトリ。アプリケーション仕様、branch・commit・worktree モデル、採用しなかった設計案、Python 開発規約・実装配置・環境・テスト規則を扱い、目的に応じた下位文書への入口となる。

## Read this when
- cmoc のアプリケーション挙動、session/run lifecycle、branch・worktree の関係、または開発・実装・テスト規約を確認するとき
- 複数の正本文書にまたがる仕様・設計・開発手順の確認先を判断するとき
- 採用されなかった設計案とその理由を調査するとき

## Do not read this when
- 特定機能の詳細仕様、具体的な実装責務、テスト実行手順、Python 環境操作など、対応する下位文書を直接読めば足りるとき
- raw observation、feedback state、Structured Output schema、prompt 構築など個別資料の具体的内容だけを確認するとき
- realization file の実装詳細や、本文書群に含まれない将来用途・一般的なコード品質を調べるとき

## hash
- 6646a0efecbccd4b98dec878a6288675e672c46861044c7d2a15a6f66d4a981b

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
