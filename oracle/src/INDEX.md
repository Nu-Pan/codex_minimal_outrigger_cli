# `oracle`

## Summary
- AI コーディングエージェント呼び出しのパラメータ、ファイルアクセスモード、パスコンテキスト、設定モデルを構成する oracle 基盤モジュール群への入口。
- agent call 用 prompt、Structured Output 入力契約、用途別 builder、oracle・realization・feedback・indexing・session・TUI の下位構成を確認する起点。

## Read this when
- agent call の共通パラメータ、アクセス制御、cwd、パス解決、設定構造を確認または変更するとき。
- agent call の prompt 構築、editor input handoff、feedback 入力、または Structured Output 契約の入口を探すとき。
- quota probe、indexing、feedback、oracle、realization、session、TUI など用途別の builder 構成を確認するとき。

## Do not read this when
- 特定の用途の prompt、出力契約、起動処理、編集・レビュー手順の詳細だけを確認したいときは、該当する下位対象を直接読む。
- oracle・realization file の具体的な内容や保存・編集手順だけを確認したいとき。
- Codex CLI の実際の実行挙動や、agent call 共通処理の実装だけを調査したいとき。

## hash
- 317ad582e36e51a72f0df315fffb3d02df0c4370fc87d11f0461201782f999b2
