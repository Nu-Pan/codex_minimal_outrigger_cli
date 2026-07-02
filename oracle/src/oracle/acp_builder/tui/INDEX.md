# `launch_tui.py`

## Summary
- `cmoc tui` の起動時に AI エージェントへ渡す呼び出しパラメータを構築する正本実装。ファイルアクセスプロファイル、完全プロンプト、保存先、モデルクラス、推論強度、参照すべきプロンプト指示の組み立て方を定義する。
- TUI 起動で使う元プロンプト、標準類の有効化フラグ、oracle・realization・index のアクセス属性を、最終的な agent call parameter へ接続する入口として扱う。

## Read this when
- `cmoc tui` がどのモデルクラス・推論強度・ファイルアクセスプロファイルで agent call を起動するか確認したいとき。
- TUI 起動時の complete prompt の構築、保存、agent への指示文生成の正本仕様断片を確認したいとき。
- TUI 起動で、ユーザー入力プロンプトや各種 standard フラグが complete prompt にどう渡るかを確認したいとき。

## Do not read this when
- TUI 以外のサブコマンドにおける agent call parameter 構築を確認したいとき。
- complete prompt の内部構成や各 standard フラグの本文内容を確認したいとき。
- ファイルアクセス属性やパスモデルそのものの定義を確認したいとき。

## hash
- 34dcc4c5b0222dd5e5dd23ccbd13ee575ea33d5ffb182f921ae0cc74f562fc0a

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
- `cmoc tui` でユーザー入力プロンプトから AI Agent CLI/TUI の実行パラメータを選ぶための AgentCallParameter を構築する正本実装。
- oracle と realization と index を読み取り可能にしたファイルアクセスプロファイル、実行パラメータ選定担当としての固定プロンプト、元プロンプトの動的埋め込み、Structured Output と根拠行提示を求める goal を組み立てる。
- モデルクラス、推論努力、完成プロンプト、対応する JSON schema path をまとめて返す処理の入口になる。

## Read this when
- `cmoc tui` の実行前に、元プロンプトから選ばれる AgentCallParameter の内容を確認・変更したいとき。
- TUI のパラメータ解決で使う role、summary、goal、読み取り権限、固定プロンプト系フラグ、プレースホルダ定義の正本を確認したいとき。
- AI Agent CLI/TUI 実行パラメータ選定の出力に、Structured Output 準拠や根拠行提示を要求している箇所を確認したいとき。

## Do not read this when
- `cmoc tui` のユーザー入力取得、エディタ起動、コメント除去、strip の処理を調べたいとき。
- AgentCallParameter、ModelClass、ReasoningEffort、PlaceholderMap、complete prompt 構築などの共通部品そのものの定義を調べたいとき。
- TUI 以外のサブコマンド向け実行パラメータ解決 prompt を確認したいとき。

## hash
- 8202ec643da88fee167595217c54338e0673284beb20aff300feeccf5af06224
