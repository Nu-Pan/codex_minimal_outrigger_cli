# `launch_tui.py`

## Summary
- `cmoc tui` の TUI 起動時に AI エージェント呼び出しパラメータを組み立てる正本実装。ユーザー入力プロンプトを complete prompt に統合し、TUI 用ログへ保存したうえで、その保存先を読む指示を含む `AgentCallParameter` を返す。

## Read this when
- `cmoc tui` の TUI 起動で渡される role、summary、goal、file access mode、各 standard フラグ、元プロンプトがどのように complete prompt と呼び出しパラメータへ反映されるか確認したいとき。
- TUI 起動時の complete prompt 保存先、ログファイル名、保存された prompt を AI Agent CLI/TUI に読ませる指示文の正本を確認したいとき。
- TUI 起動用パラメータの model class、reasoning effort、file access mode、JSON 対応ファイル、実行可否フラグの正本値を確認したいとき。

## Do not read this when
- `cmoc tui` 以外のサブコマンドの AI エージェント呼び出しパラメータを確認したいとき。
- complete prompt 全体の構成規則や各 standard フラグの意味そのものを確認したいときは、prompt builder 側の正本を読む。
- パスキーワードや repository root 解決の定義を確認したいときは、path model 側の正本を読む。

## hash
- 425b1e8a3cb5778476b6f5ac9bf9c710b35901e2e0f909fb22e7edd47fa89e5b

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
- `cmoc tui` でエディタ入力された元プロンプトから、AI Agent CLI/TUI の実行パラメータ選定用 AgentCallParameter を構築する oracle src。
- 完全プロンプトの role、summary、goal、ファイルアクセスモード候補、placeholder、各種標準プロンプトフラグを組み立て、読み取り専用・効率モデル・中程度 reasoning の呼び出し条件と Structured Output schema path を返す。

## Read this when
- `cmoc tui` の実行前に、元プロンプトからどの agent call パラメータ選定 prompt が作られるか確認したいとき。
- TUI 用の実行パラメータ解決で使うモデルクラス、reasoning effort、ファイルアクセスモード、schema path の正本仕様断片を確認したいとき。
- `build_complete_prompt` に渡す固定プロンプト要素や標準プロンプトフラグの扱いを確認したいとき。

## Do not read this when
- TUI 以外のサブコマンドの実行パラメータ解決を確認したいとき。
- ファイルアクセスルール自体の本文や FileAccessMode ごとの詳細を確認したいとき。
- prompt builder の共通構造、StructDoc の表現、path placeholder 解決の詳細実装を確認したいとき。

## hash
- 9d458ce69f80106270b20b16fc6cd4820f082c03c665730c6fadd4292a70aafe
