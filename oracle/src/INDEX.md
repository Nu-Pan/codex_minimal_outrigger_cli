# `oracle`

## Summary
- oracle の設定・パスモデル・規範構造・Markdown 構造化文書、AI Agent 呼び出しパラメータ、エージェントプロンプト構成を扱う実装群の入口。共通定義から indexing・tui の AgentCall 構築、prompt の部品・規則まで下位領域へ案内する。

## Read this when
- cmoc 設定値、ルートパス解決、Standard/Requirement、StructDoc の構造や Markdown レンダリングを調べるとき。
- AgentCallParameter、モデル・推論負荷・アクセスモード、indexing・tui の呼び出しパラメータ構築を調べるとき。
- エージェントプロンプトの組み立て、プレースホルダ、oracle・realization 標準、ファイルアクセス・ルーティング規則を調べるとき。

## Do not read this when
- サブコマンドの実行処理、ファイル探索、モデル呼び出しの実行経路を確認したいとき。
- 個別の prompt 部品、個別のモデル・StructDoc 定義、パス解決、アクセス規則、Structured Output schema の詳細だけを確認したいときは、対応する下位領域を直接読む。
- 個別の規範本文や、Markdown レンダリングを経由しない別機能の仕様を確認するとき。

## hash
- ecfb211b74a3b36ef7c4165b16fa31a886076a96700d47903c9031ee97526fa1
