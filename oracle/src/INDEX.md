# `oracle`

## Summary
- エディタ入力上書きツールが受け取る対象識別値と書き込み内容の JSON Schema。
- フィードバック問題報告の分類、影響、未解消制約、原因、根拠、継続状態を表す入力 JSON Schema。
- AI コーディングエージェント呼び出しの共通パラメータ型と、quota probe・indexing・feedback・TUI など用途別の起動設定を構築する入口。
- cmoc の設定、Codex CLI 呼び出し設定、agent call のルートパス導出、パスプレースホルダー、構造化文書の保持・Markdown レンダリングを扱う基盤。
- agent call 用の完全 prompt、エディタ初期入力、ファイルアクセスや oracle・realization・routing などの policy 部品を構築する入口。

## Read this when
- エディタ入力上書きの入力項目と形式を確認するとき。
- cmoc_feedback.submit_observation に渡す問題報告の契約を確認するとき。
- agent call の共通パラメータ、用途別 builder、prompt、Structured Output、cwd、アクセスモードの構成を確認するとき。
- cmoc の設定、Codex CLI 設定、パスコンテキスト、ルートプレースホルダー、構造化文書の処理を確認するとき。
- 完全 prompt の組み立て、policy の注入、placeholder の統合、エディタ初期入力の生成を確認するとき。

## Do not read this when
- 特定の agent call の個別 prompt、入力、結果分類、検証条件だけを確認したい場合は、acp_builder 配下の対応する領域を直接読む。
- エディタ入力上書きの実装や呼び出し手順だけを確認したい場合は、対応する処理実装を直接読む。
- フィードバック報告の送信処理、collector、issue 同一性判定、remediation の実装を確認したい場合は、対応する実装を直接読む。
- Codex CLI sandbox のアクセスモードの正本仕様や、Structured Output schema の機械的受理条件だけを確認したい場合は、各正本・JSON schema を直接読む。
- 個別の CLI 機能、MCP tool、realization file の具体的な挙動だけを確認したい場合は、該当する実装または仕様を直接読む。

## hash
- c3658c331f1dfe061b823537bd02494e62b2571c6667043f7d66db82082e51dd
