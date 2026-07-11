# `launch_tui.py`

## Summary
- `cmoc tui` の TUI 起動時に、完全プロンプトを保存して `AgentCallParameter` を組み立てる入口。起動用のモデル選択・推論設定・引数整形と、生成済みプロンプトのログ保存を扱う。

## Read this when
- `cmoc tui` の起動パラメータの組み立て方を変えるとき
- TUI 起動前に保存する完全プロンプトの生成・保存先・文面を確認したいとき
- この起動経路で使うモデル設定や reasoning 設定の根拠を確認したいとき

## Do not read this when
- 完全プロンプトの具体的な構築規則だけを見たいときは、`build_complete_prompt` 側を読む
- `AgentCallParameter` の定義や意味だけを知りたいときは、その定義元を読む
- TUI 起動以外のサブコマンドの起動引数を調べたいとき

## hash
- 2b07d517bed86ccf7503d0a439b5ed3bb033b891637c55bd2ea442c373e04e8b

# `resolve_parameter.json`

## Summary
- AI Agent CLI/TUI に渡すオリジナルプロンプトの実行条件を、役割・概要・ゴール・論理ファイルアクセスモード・参照すべき標準群の要否として構造化するための JSON Schema。
- プロンプト実行前に、どの標準文書を読むべきか、どの権限範囲で作業させるべきかを機械的に判定・検証する設定データの形を定義している。

## Read this when
- オリジナルプロンプトから Agent に与える role、summary、goal、file_access_mode を構造化する処理を確認・変更するとき。
- oracle and realization basic、oracle standard、realization standard、review oracle standard、apply review standard、index entry standard を読む必要があるかどうかの判定結果を扱うとき。
- AI Agent CLI/TUI 向けプロンプト解決結果の JSON 形状、必須項目、各項目の説明、許可されるファイルアクセスモードを確認するとき。

## Do not read this when
- INDEX.md 用エントリー自体の書き方やルーティング文の品質基準を確認したいだけなら、index entry standard を直接読む。
- oracle file と realization file の定義・責務境界を確認したいだけなら、oracle and realization basic を直接読む。
- 実装やテストの品質基準、重複削減、依存追加方針を確認したいだけなら、realization standard を直接読む。

## hash
- 96a62ed7c319eb3a85930b42b02d81163964596f8090725f41c6122d2c76fd71

# `resolve_parameter.py`

## Summary
- `cmoc tui` のエージェント呼び出し用パラメータを組み立てる正本。元プロンプト、ファイルアクセス方針、共通プロンプト断片をまとめて `AgentCallParameter` に落とし込む。

## Read this when
- `cmoc tui` がどのモデル・推論強度・ファイルアクセスで動くかを決める処理を追いたいとき。
- オリジナルプロンプトを入力にして、実行用プロンプト本文と保存先をどう構成しているかを確認したいとき。
- 共通の正本仕様断片をどの固定フラグでプロンプトに埋め込むかを見たいとき。

## Do not read this when
- `cmoc tui` の実行本体や UI 挙動を追いたいだけのとき。
- 個別のプロンプト文面や共通仕様断片の内容そのものを確認したいときは、より下位の生成元や参照先を見るべきで、このファイルは先に読まなくてよい。

## hash
- 6db4e68896a77950cfa27ddc6ea197f79092c79ea474f1f786e5c493763aadb2
