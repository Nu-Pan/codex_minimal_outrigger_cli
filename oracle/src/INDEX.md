# `oracle`

## Summary
- AIエージェント呼び出しに使う prompt、Structured Output schema、モデル、推論強度、ファイルアクセスモード、cwd、preflight などの起動パラメータを、cmoc の処理単位ごとに定義する領域です。直下の共通データモデルから、indexing、feedback、oracle、realization、session、tui、quota probe など用途別の呼び出し定義へ進むための入口になります。

## Read this when
- 特定の cmoc 機能が起動する AI エージェントについて、prompt と Structured Output schema の対応や起動パラメータを調べるとき。
- 共通の AgentCallParameter と用途別の agent call builder の責務分担を確認してから、個別の処理定義へ進むとき。
- oracle review、feedback issue 判定、realization の apply/refactor、session join、TUI、quota probe の呼び出し定義を探すとき。

## Do not read this when
- AIエージェント呼び出しの実行処理、共通 prompt 生成規則、パス解決、ACP 基本型の実装だけを調べるとき。
- レビュー対象の oracle file、realization file、feedback issue の具体的内容を確認するとき。
- Structured Output schema の一般仕様や、個別の所見・issue の原因と重要度だけを調べるとき。

## hash
- c3f8abbd4a7d21d9c1953c142dbf098c93f610785227ee0a86797bed3dfc1119
