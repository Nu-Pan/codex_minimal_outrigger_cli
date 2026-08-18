# `doc`

## Summary
- cmoc の正本文書を領域別にまとめた入口。CLI・workflow の挙動仕様は app_spec、Python 開発・設計・テスト・環境は dev_rule、branch／session／run の関係は branch_model、採用しなかった設計案の背景は considered_alternative へ進む。

## Read this when
- cmoc の仕様、設計、開発環境、テスト、branch／session／run、または採用しなかった代替案を調査し、対応する正本文書群の入口を判断するとき
- 実装やテストの変更に先立ち、アプリケーション仕様と開発ルールのどちらを確認すべきか整理するとき

## Do not read this when
- 対象の個別仕様書や開発ルール文書が既に特定できており、そこへ直接進む方が適切なとき
- 実装ファイルや既存テストの具体的内容だけを調査し、正本文書群の横断的な案内が不要なとき

## hash
- 940b333372e1bb8d5db506d6d72de3447e9dc82f3175b2e4a537fdf82d814306

# `src`

## Summary
- `oracle/src` は、cmoc の agent call に必要な oracle 実装をまとめたソースディレクトリです。agent call の基本パラメータ・パスモデル・設定・構造化文書処理、prompt の共通部品と目的別 policy、feedback・indexing・oracle review・realization 操作などの起動処理と Structured Output schema を扱います。
- `oracle/src/oracle` が主要な実装入口で、`acp_builder` は用途別 agent call の prompt・起動パラメータ・schema、`prompt_builder` は共通 prompt と policy、`other` は設定・パス解決・構造化文書ヘルパーを担当します。

## Read this when
- agent call の起動パラメータ、モデル分類、Reasoning effort、ファイルアクセスモード、作業ディレクトリ、indexing preflight を確認するとき
- agent call 用 prompt の共通構成、oracle・realization・feedback・routing・conflict resolution・review の policy を確認するとき
- oracle review、feedback 処理、index entry 生成、realization の apply/refactor、session join など用途別の agent call 定義を確認するとき
- cmoc 設定、root placeholder を含むパス解決、Git worktree のパスモデル、構造化文書の Markdown 化を確認するとき
- agent call の Structured Output schema または schema と prompt の対応を調査するとき

## Do not read this when
- 特定の agent call の具体的な挙動だけを確認する場合は、`oracle/src/oracle/acp_builder` 配下の対応する実装と schema を直接読むとき
- prompt の個別 policy や構成部品だけを確認する場合は、`oracle/src/oracle/prompt_builder` 配下を直接読むとき
- 設定・パス解決・構造化文書処理の個別仕様だけを確認する場合は、`oracle/src/oracle/other` 配下を直接読むとき
- oracle の正本仕様、realization の実装本体、または test の外部挙動を確認する場合は、この実装ディレクトリではなく対応する oracle・realization・test を読むとき

## hash
- 609ef03a109932a15b677a08c097294b3126c3a6b268886b5d44340adb4ef966
