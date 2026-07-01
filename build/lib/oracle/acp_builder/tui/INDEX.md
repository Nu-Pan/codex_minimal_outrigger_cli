# `launch_tui.py`

## Summary
- `cmoc tui` の TUI 起動時に使う AI エージェント呼び出しパラメータの正本実装。ロール、概要、ゴール、各種標準 prompt の有効化フラグ、元プロンプトから完全プロンプトを組み立て、TUI 用ログへ保存し、その保存先を読むよう指示する `AgentCallParameter` を返す。

## Read this when
- `cmoc tui` の起動時に渡す AI エージェント呼び出しパラメータ、モデル種別、推論強度、ファイルアクセスモード、プロンプト保存先、または元プロンプトの取り込み方法を確認・変更したいとき。
- TUI 起動 prompt がどの入力から構成され、どのように完全プロンプト化され、どこへ保存されるかを確認したいとき。
- TUI 起動用の正本 prompt 実装から生成される JSON パラメータとの対応を確認したいとき。

## Do not read this when
- `cmoc tui` 以外のサブコマンドのエージェント呼び出しパラメータを調べたいとき。
- 完全プロンプト全体の構成規則や各標準 prompt フラグの意味を調べたいだけの場合は、prompt 構築側の正本実装を読む。
- パスキーワードやリポジトリルート解決の仕様を調べたいだけの場合は、パスモデル側の正本実装を読む。

## hash
- 34dcc4c5b0222dd5e5dd23ccbd13ee575ea33d5ffb182f921ae0cc74f562fc0a

# `resolve_parameter.json`

## Summary
- AI Agent CLI/TUI がオリジナルプロンプトを実行するために必要な役割、作業概要、ゴール、論理ファイルアクセスモード、読むべき標準群を判定して返すための Structured Output schema を定義する。
- 作業前パラメータ解決の出力契約を固定する入口であり、標準文書を読む必要の有無とその根拠を機械的に揃えたい場合の参照先になる。

## Read this when
- オリジナルプロンプトから実行時パラメータを解決する処理の出力形式を確認・変更する。
- role、summary、goal、file_access_mode の値と根拠を返す契約を確認する。
- oracle and realization basic、oracle standard、realization standard、review oracle standard、apply review standard、index entry standard を読むべきかどうかの判定結果を出力する処理を実装・検証する。
- 論理ファイルアクセスモードとして readonly、pure_oracle_read、repo_write、pure_oracle_write、realization_write のどれを返せるか確認する。

## Do not read this when
- 各標準そのものの内容を確認したい場合は、対応する標準本文を読む。
- 実際のファイル読み書き権限やサンドボックス制御の実装を調べたい場合は、その責務を持つ実装へ進む。
- INDEX.md 用エントリーの書き方やルーティング文書の品質基準だけを確認したい場合は、index entry standard の本文を読む。
- オリジナルプロンプト本文の解析方針ではなく、生成済みの個別パラメータ値だけを確認したい場合は、この schema ではなくその出力結果を読む。

## hash
- ace731f62d898f31a29a3074830d3db6535ba94360c2d015174386292ec9b3f5

# `resolve_parameter.py`

## Summary
- AI Agent CLI/TUI の TUI 実行に先立ち、ユーザー入力プロンプトからエージェント呼び出しパラメータを決定するための正本 prompt を構築する。
- 固定の役割・概要・ゴール、読み取り専用のファイルアクセス規則、各ファイルアクセスモード説明、主要な仕様標準群を組み込んだ complete prompt を生成し、効率重視モデル・中程度 reasoning・読み取り専用モードの呼び出しパラメータとして返す。

## Read this when
- TUI 経由の実行で、元プロンプトから AI Agent CLI/TUI に渡すモデル種別、reasoning effort、ファイルアクセスモード、Structured Output schema の指定をどう決めるか確認したいとき。
- TUI の実行パラメータ解決 prompt に含める固定文脈、placeholder、ファイルアクセス規則、oracle/realization/index 関連標準の有効化状態を確認したいとき。
- ユーザーがエディタ入力した元プロンプトを、パラメータ選定用の complete prompt に埋め込む経路を調べるとき。

## Do not read this when
- TUI 本体の画面制御、エディタ起動、ユーザー入力のコメント除去や strip 処理を調べたいとき。
- 各ファイルアクセスモードの規則本文そのもの、complete prompt の汎用組み立て仕様、または placeholder 解決の実装詳細を調べたいとき。
- AI Agent CLI/TUI の実行パラメータ選定ではなく、通常のサブコマンド実行、作業実行 prompt、またはレビュー prompt の内容を調べたいとき。

## hash
- 8202ec643da88fee167595217c54338e0673284beb20aff300feeccf5af06224
