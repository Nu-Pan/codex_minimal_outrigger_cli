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
- `oracle/src` は、cmoc の agent call を構成する実装のルートです。共通の AgentCallParameter、モデル・推論・ファイルアクセスの論理設定、call-scoped path context を土台に、処理別の起動パラメータと完全 prompt を組み立てます。
- 配下には、indexing・feedback・oracle・realization・session・tui の agent call builder、prompt の共通組み立てと policy 部品、パス・設定・構造化文書の補助実装があります。各処理の具体的な prompt や Structured Output schema を調べる際の入口になります。

## Read this when
- agent call の共通パラメータ契約、論理モデルクラス、Reasoning effort、ファイルアクセスモード、cwd、indexing preflight の設定責務を調査・変更するとき。
- 複数の cmoc 処理にまたがって、agent call builder と完全 prompt・policy 部品の分担を確認するとき。
- 処理別 builder、prompt builder、Structured Output schema、パスモデルや設定モデルへ進むための実装上の入口を確認するとき。

## Do not read this when
- agent call の実行、Codex CLI への変換、sandbox の具体的な解決、または終了結果の処理を調べるときは、対応する realization 実装や呼び出し側を直接読む。
- 特定処理の prompt 文面や Structured Output schema の詳細だけを確認したいときは、該当する `acp_builder` の下位実装や schema を直接読む。
- oracle・realization の正本仕様、開発規則、または test 実行手順を確認したいときは、対応する oracle 文書や repository local の手順を直接読む。

## hash
- 1f8b9a32d27dc0fa26f0d9009cbcfa3458df7928fb707c82233c05e99a585746
