# `oracle`

## Summary
- `oracle/src/oracle` は cmoc の agent call 構築と、その prompt・Structured Output・設定モデルを定義する oracle ソースの入口です。共通の AgentCallParameter、論理モデル、推論強度、ファイルアクセスモード、cwd、indexing preflight を基盤に、個別の agent call 構築へ進みます。
- agent call の具体的な prompt と schema は `acp_builder`、prompt の合成と policy は `prompt_builder`、feedback 入力契約は `feedback`、設定・パス解決・構造化文書モデルは `other` が担当します。

## Read this when
- cmoc の agent call 構築全体の責務や、共通パラメータから個別処理への入口を確認するとき
- feedback、indexing、oracle、realization、session、TUI、quota probe の agent call 構築を調査・変更するときは `acp_builder` から対応する下位対象へ進む
- prompt の統合順序、policy、placeholder、oracle／realization の共通概念を確認するときは `prompt_builder` から対応する下位対象へ進む
- feedback reporter の入力項目と検証契約を確認するときは `feedback` を読む
- 設定値、モデル変換に使う設定モデル、agent call のパスコンテキスト、構造化文書の Markdown 化を確認するときは `other` を読む

## Do not read this when
- 実際の Codex CLI 呼び出し、sandbox 制約、共通 prompt の実行基盤、またはパス解決の利用側の挙動だけを確認したいときは、担当する realization 実装や共通仕様を直接読む
- 個別の Structured Output schema の項目・型・形式だけを確認したいときは、`acp_builder` 配下の該当 schema を直接読む
- 個別の oracle 文書、realization 実装・テスト、feedback state の保存・集約、または CLI サブコマンドの実装挙動だけを確認したいときは、それぞれの担当対象を直接読む
- 既存の INDEX.md のルーティング内容だけを確認したいとき

## hash
- 60bdd76541d024a5fdfd9c522a1f943ceaeca99f0519631c18584f9b8b0d945d
