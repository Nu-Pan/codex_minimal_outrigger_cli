# `launch_tui.py`

## Summary
- `cmoc tui` の TUI 起動時に、動的な役割・概要・完了条件・アクセスモード・各種標準フラグ・ユーザープロンプトから完全なプロンプトを構築し、ログへ保存する処理を担う。生成したプロンプトのパスと固定のモデル・推論設定を含む AI エージェント呼び出しパラメータを返す。

## Read this when
- `cmoc tui` の起動パラメータ生成、完全なプロンプトの保存先、または TUI 呼び出し時のモデル・推論設定を変更・調査するとき。
- 動的プロンプトの構成要素や、エディタ入力されたオリジナルプロンプトの受け渡しを確認するとき。

## Do not read this when
- 完全なプロンプトの共通生成規則そのものを調査するときは、プロンプト構築側の実装を直接読む。
- TUI の画面表示や対話処理、JSON パラメータ定義だけを調査するときは、それぞれの担当実装を直接読む。

## hash
- 7c0db24a7b74ab1c08a6efa7046738f3df2fdf60ae813eeb9183471d3d031242

# `resolve_parameter.json`

## Summary
- AI Agent CLI/TUI 実行用プロンプトの構造化スキーマを定義する oracle src。役割・作業概要・ゴール・ファイルアクセス権限、および各種標準の適用要否を表現する。

## Read this when
- oracle/acp_builder/tui のパラメータ解決やプロンプト生成の仕様を確認するとき
- この構造化スキーマの項目、必須項目、アクセスモード enum、標準適用フラグを変更・検証するとき

## Do not read this when
- INDEX.md のルーティング方針だけを確認したいとき
- 実際の TUI パラメータ解決処理やプロンプト生成実装を確認したいときは、対応する realization source を直接読む

## hash
- 12d009e1cfa34942aedce8ffb405c9e9d69e9865325945e69e189f13857506c7

# `resolve_parameter.py`

## Summary
- `cmoc tui` の実行パラメータ解決用 AgentCallParameter と、そのための固定プロンプトを構築する。元プロンプト、ファイルアクセス規則、oracle/realization・レビュー・INDEX 規則を組み合わせ、読み取り専用で実行するパラメータ選択タスクの prompt とモデル設定を生成する。

## Read this when
- `cmoc tui` の実行パラメータ解決 prompt や AgentCallParameter の生成方法を確認するとき
- 元プロンプトから AI Agent CLI/TUI のモデル、推論強度、ファイルアクセスモード、生成 prompt を決定する処理を変更・調査するとき

## Do not read this when
- `cmoc tui` の通常の UI 実装や、パラメータ解決後の AI Agent CLI/TUI 実行処理を確認するときは、対応する実装ファイルを直接読む
- prompt の共通構築規則やファイルアクセス規則そのものを確認するときは、各 prompt builder の定義元を直接読む

## hash
- 4b21b1ed6d72e90c4e269a9117dadb8e88366ca5da2ba12ce834d39aceacac78
