# `launch_tui.py`

## Summary
- `cmoc tui` の TUI 起動用 AgentCallParameter を構築する oracle src。完全なプロンプトを生成・保存し、最高性能モデル・最大推論設定・リポジトリ書き込み権限などの固定起動パラメータを返す。TUI 起動条件、プロンプト生成、モデル設定、作業ディレクトリ、構造化出力スキーマの確認における入口。

## Read this when
- `cmoc tui` の TUI 起動処理や AgentCallParameter の設定を変更・調査するとき
- TUI 用の完全プロンプト保存先、パスコンテキスト、動的プロンプトの構成を確認するとき
- TUI 起動時のモデル、推論強度、ファイルアクセスモード、インデックス事前処理の設定を確認するとき

## Do not read this when
- TUI 以外のサブコマンドのプロンプト生成や AgentCallParameter を調査するとき
- `cmoc tui` の呼び出し元やエディタ入力処理だけを確認するとき
- TUI 起動で使用する構造化出力スキーマの詳細だけを確認するとき

## hash
- 6dce0148f0c47eb025a9dc391bdf7fbdf4bcf0bc730dcc026d6289e9eb6ebff2

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
- `cmoc tui` の実行パラメータ解決用プロンプトと、後続の AI Agent CLI/TUI 呼び出しに渡す `AgentCallParameter` を構築する正本実装。モデル、推論強度、読み取り専用アクセス、作業ディレクトリ、構造化出力スキーマなどの実行条件を定義し、関連する prompt builder や path context の入口となる。

## Read this when
- `cmoc tui` の実行パラメータ解決処理を変更・レビューするとき
- 後続エージェント向けプロンプトの role、summary、goal、標準規則の適用条件を確認するとき
- TUI 用 AgentCallParameter のモデル、アクセスモード、cwd、構造化出力設定を確認するとき

## Do not read this when
- `cmoc tui` のユーザー入力受付や画面表示など、実行パラメータ解決以外の TUI 挙動を調べるとき
- 構造化出力スキーマの項目定義だけを確認したいときは、対応する JSON スキーマを直接読む
- 共通の完全プロンプト生成仕様やパス解決仕様だけを確認したいときは、それぞれの共通モジュールを直接読む

## hash
- d0178af4f620a213141d82c8c31e1590cfbf08b15105b1d5bf3254ee5a6bc236
