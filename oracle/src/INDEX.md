# `oracle`

## Summary
- AI Agent 呼び出しに必要な正本ソースを、共通パラメータ、用途別の呼び出し設定、prompt 構築、Structured Output 契約、基礎モデルに分けて収録する領域です。
- Agent call のモデル・推論・ファイルアクセス・cwd・prompt・Structured Output schema を表す定義と、feedback、indexing、TUI の用途別起動設定が下位要素への入口になります。
- prompt 構築部品は、oracle・realization 規範、ファイルアクセス、ルーティング、feedback 報告などを組み合わせて完全な prompt やエディタ入力初期文を生成します。
- 基礎モデル群は、設定、call-scoped なパス解決、Standard、構造化 Markdown の表現とレンダリングを扱います。

## Read this when
- AI Agent 呼び出しの共通パラメータ、モデルクラス、Reasoning effort、ファイルアクセスモード、cwd、Structured Output schema を調査・変更するとき。
- feedback、indexing、TUI など特定用途の agent call 設定や入力契約の入口を探すとき。
- 完全な prompt の組み立て、共通 prompt 規則の注入、プレースホルダ、prompt editor の初期テキストを調査・変更するとき。
- CmocConfig、agent call の root path 解決、Standard、Requirement、構造化 Markdown の基盤を確認するとき。

## Do not read this when
- 通常の realization 実装・テスト、CLI や TUI の実行フロー自体を調査するとき。
- 正本仕様の本文、Codex CLI の sandbox・permission profile の一般規則、個別用途の prompt や schema の詳細だけを確認したいとき。
- 特定の prompt builder 部品、用途別 schema、個別モデルの定義を直接調査する場合は、該当する下位要素へ進むとき。

## hash
- ecce9fc9a50f80162e21f497e901e4099f9ad92555c305920293d082a71654e2
