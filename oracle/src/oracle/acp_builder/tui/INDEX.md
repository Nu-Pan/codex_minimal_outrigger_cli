# `launch_tui.py`

## Summary
- `cmoc tui` 起動時に使用する AgentCallParameter を構築する oracle src。ユーザー入力を完全な作業 prompt として保存し、最高品質のモデル設定・リポジトリ書き込み権限・構造化出力 schema・実行対象 cwd・事前 indexing を含む TUI 起動条件を定める。

## Read this when
- `cmoc tui` の AgentCallParameter、起動 prompt、モデル・推論設定、ファイルアクセスモード、agent call の cwd、または prompt 保存処理を変更・確認するとき。
- oracle/realization standard の適用可否や、TUI 用の構造化出力 schema の指定箇所を確認するとき。

## Do not read this when
- TUI 起動パラメータではなく、通常の CLI サブコマンド実装や prompt 本文の共通生成ロジックだけを調査するとき。
- TUI の画面表示・対話制御・エディタ入力処理そのものを変更・確認するときは、該当する直接の実装へ進む。

## hash
- 280da05e84f9a11b620d03624d553378a44e0532caa12f2e44cef9ec9655f372

# `resolve_parameter.json`

## Summary
- このファイルは、AI Agent CLI/TUI 実行時に oracle standard、realization standard、oracle review standard、apply review standard を読む必要があるかを判定する JSON Schema を定義する。各判定には真偽値と理由を求める。

## Read this when
- AI Agent CLI/TUI の標準文書参照要否を判定する処理や、その入力スキーマを確認するとき。

## Do not read this when
- oracle standard や realization standard の本文そのものを確認するとき。
- 実装・テストの配置やレビュー適用手順を確認するときは、対応する標準文書または実装・テストを直接読む。

## hash
- 22a4c43bcee0978a70007dbaf2a6487403ce7b2829df218cad8d608141bc0b0e

# `resolve_parameter.py`

## Summary
- `cmoc tui` の実行パラメータ解決用 AgentCallParameter と、後続エージェント呼び出し向けの完全プロンプトを構築する oracle src。ユーザー入力プロンプトを動的プロンプトへ埋め込み、標準適用方針・読み取り専用アクセス・モデル等の実行条件を定義する。

## Read this when
- `cmoc tui` の実行パラメータ解決処理を変更・レビューするとき
- 後続 AI Agent CLI/TUI 呼び出しの prompt、path context、model、access mode、structured output 設定を確認するとき
- ユーザー入力プロンプトを含む完全 prompt の構築経路を追跡するとき

## Do not read this when
- `cmoc tui` の実際の対話処理や UI 制御だけを調べるとき
- 実行パラメータ解決後の Agent CLI/TUI 呼び出し実装を直接確認すべきとき
- Structured Output schema の詳細だけを確認するときは、対応する schema ファイルへ直接進む

## hash
- cd5c4c1693503436f0cbd5f4a6d4a47f2e2f5156a868b93ad091885caefc5bce
