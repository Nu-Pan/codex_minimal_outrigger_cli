# `oracle`

## Summary
- AI コーディングエージェント呼び出しの共通設定、用途別 builder、prompt 構築、入力スキーマを扱う実装群への入口。
- quota probe、indexing、feedback、oracle・realization・session・TUI などの agent call 構築や、共通の prompt・Structured Output・作業環境設定を確認できる。

## Read this when
- agent call の共通パラメータ、アクセスモード、prompt、Structured Output、cwd、editor input handoff、または indexing preflight を調べるとき。
- 用途別の agent call builder や、agent 向け prompt・エディタ入力の構築経路を探すとき。

## Do not read this when
- 特定用途の prompt、出力契約、入力スキーマの詳細だけを確認したいときは、該当する下位対象を直接読む。
- Codex CLI の実行処理、フィードバック送信処理、oracle・realization の具体的な内容や編集手順を調べるとき。

## hash
- 38beea4879353cedd902bea8ee616ce2156e229752994451794d93df126b72d3
