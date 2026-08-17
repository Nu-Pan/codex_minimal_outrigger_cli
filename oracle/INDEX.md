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
- cmoc の oracle 実装領域。Agent Call Parameter、モデル・推論・ファイルアクセス設定、パスモデル、設定、構造化 Markdown、完全 prompt の構築を定義する。
- indexing、feedback、session join、oracle review、realization など、用途別 agent call の prompt と Structured Output の起動パラメータを扱う。
- 下位の `oracle`、`acp_builder`、`prompt_builder` 配下へ進むための実装上の入口であり、個別機能の調査では対応する下位領域を直接読む。

## Read this when
- oracle の実装責務と、agent call・prompt・設定・パス・構造化文書の共通基盤を横断して確認するとき
- 用途別 agent call の構築定義や Structured Output 呼び出しの配置を探すとき

## Do not read this when
- 実際の CLI 実行制御や realization の実装本体だけを調査するとき
- 特定の prompt builder、agent call builder、設定モデル、またはスキーマが判明しており、対応する下位対象を直接読めば足りるとき

## hash
- 5d290583e82d92e8a81210dfa76bfedd41916b014e8d102fb307ddd6b803a3b2
