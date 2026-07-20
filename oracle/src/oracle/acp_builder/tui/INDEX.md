# `launch_tui.py`

## Summary
- `cmoc tui` 起動時に、ユーザー入力を埋め込んだ完全なプロンプトを生成・保存し、Codex CLI/TUI 用の固定実行パラメータを返す正本実装。プロンプト構築、ログファイルの保存先、モデル・推論強度・アクセスモードなどの起動設定を扱う。

## Read this when
- `cmoc tui` の起動処理、起動用 AgentCallParameter、完全プロンプトの生成または保存先を変更・調査するとき。
- TUI 起動時のモデル、推論強度、ファイルアクセスモード、レビュー標準の適用条件を確認するとき。

## Do not read this when
- TUI 以外のサブコマンドのプロンプト構築や起動パラメータを調査するときは、該当する起動実装を直接読む。
- プロンプト本文の共通構築規則だけを確認したい場合は、共通プロンプト構築モジュールを読む。

## hash
- 583f8c45266c929434d4e91bf0c53219d9dfad92b3d795d591584e722eab4246

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
- `cmoc tui` の実行パラメータ解決用プロンプトを正本として構築する oracle src。後続 AI Agent CLI/TUI に適用する標準の選択を依頼する完全プロンプトを生成し、効率重視・最大推論の呼び出しパラメータとして返す。

## Read this when
- `cmoc tui` の実行パラメータ解決プロンプト、適用する標準、読み取り専用の agent call パラメータを変更・確認するとき。
- `build_tui_resolve_parameter_parameter` の入力プロンプト埋め込み、placeholder、出力 schema パス、モデル・推論設定を確認するとき。

## Do not read this when
- `cmoc tui` の通常の対話実行や、実際の後続 AI Agent CLI/TUI の実装を確認したいとき。
- 共通プロンプト生成処理の詳細だけを確認したいときは、プロンプトビルダー側の対象を直接読む。

## hash
- 7d442f0a37e22042352348e3bbd4eebe1afb38cfea28f5137362d8d698952d33
