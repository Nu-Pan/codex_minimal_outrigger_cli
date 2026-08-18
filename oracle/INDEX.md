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
- oracle/src は、cmoc の agent call 構築、prompt 構築、共通設定・パス・構造化文書モデル、feedback 入力処理を担う oracle 実装領域です。
- acp_builder は、モデル・reasoning effort・ファイルアクセスなどの agent call パラメータと、TUI、feedback、oracle review、realization など用途別の起動定義を扱います。
- other は、cmoc 設定、agent call のパスコンテキスト、構造化文書ノードと Markdown 変換など、各 builder が共有する基盤を扱います。
- prompt_builder は、完全 prompt、エディタ入力、oracle・realization の基本説明、ファイルアクセスや routing・review など作業目的別 policy の構築を扱います。
- feedback 関連の実装は、構造化 observation や候補 issue の同一性判断・検証など、人間向け feedback issue の agent call 入力を構築します。

## Read this when
- agent call の共通パラメータ、用途別の起動定義、Structured Output、TUI・feedback・oracle review・realization 関連の builder を調査または変更するとき
- cmoc 設定、agent call cwd に基づくパス解決、構造化文書の生成・Markdown 変換を調査または変更するとき
- 完全 prompt の構成、placeholder、エディタ入力、oracle・realization や review・routing などの policy を調査または変更するとき
- feedback observation や issue candidate の同一性判断・検証に渡す入力契約を調査または変更するとき

## Do not read this when
- 特定の CLI サブコマンドの処理フローや realization の具体的な実装・テストだけを確認したいとき
- 個別の oracle 文書や個別 builder の仕様本文そのものだけを確認したいとき
- 既存の INDEX.md のルーティング内容だけを確認したいとき

## hash
- 9c08f106d636dd94db4bc9270d2fe84aa934a7241ebd636caf1197bd731068d6
