# `doc`

## Summary
- cmoc のアプリケーション挙動仕様を集約する正本文書群。CLI 自動補完、Codex 呼び出し、ログ・エラー処理、doctor preprocess、feedback、prompt、session/run、サブコマンド、通知などの個別仕様への入口として、対象機能に対応する下位仕様へ進むために読む。

## Read this when
- cmoc の利用者向け挙動仕様、共通実行契約、サブコマンド lifecycle、feedback、prompt、session/run、通知の正本を探すとき
- 複数のアプリケーション仕様にまたがる責務境界や、適切な下位仕様の入口を確認するとき

## Do not read this when
- 特定機能の詳細仕様が明らかな場合は、このディレクトリ全体ではなく対応する個別仕様を直接読むとき
- 実装コード、realization の具体的挙動、テスト実行手順、開発環境の規則だけを確認するとき

## hash
- a27226caa4dcfe973a9e71577f14e02662f7f12767b62902c6d99ac13ba0a595

# `src`

## Summary
- cmocのagent call起動定義とprompt構築実装の入口。共通のAgentCallParameterや実行設定、用途別の起動パラメータ、prompt部品、Structured Output schema、パス・標準文書などを扱う。
- agent callの用途別実装はacp_builder、promptの組み立てと規範部品はprompt_builder、共通モデルや設定・構造化文書はotherへ進むための上位ルーティング対象。

## Read this when
- oracle、realization、feedback、indexing、session join、TUIなど、複数用途にまたがるagent call構築の責務や配置を確認するとき。
- 特定用途の起動定義、prompt構築、Structured Output schema、共通設定のいずれを読むべきか判断するとき。

## Do not read this when
- 特定用途のagent call起動処理を調査する場合はacp_builder配下を直接読むとき。
- promptの共通部品や用途別Standardを調査する場合はprompt_builder配下を直接読むとき。
- AgentCallParameter、モデル・推論設定、パス解決、構造化文書などの共通定義だけを確認する場合はother配下を直接読むとき。
- oracleやrealizationの具体的な仕様・実装・テストを確認する場合は、それぞれの正本仕様または対象実装を直接読むとき。

## hash
- cc0a27853fabbc27ab812a405c3c75c809bc95238b50394799b6dd25a5c3f247
