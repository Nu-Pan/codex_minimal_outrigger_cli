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
- 6e95602a3cfe36294b1814a9c2d1b7fd6b8f5d30a80fc807df88bd9c457099d3

# `resolve_parameter.json`

## Summary
- AI Agent CLI/TUI がオリジナルプロンプトを実行するための解決済みパラメータ構造を定義する JSON Schema。役割・作業概要・ゴール、oracle file・realization file・INDEX.md へのアクセス権、各標準断片を読む必要性を、値と根拠の組で表す。
- プロンプト実行前に、対象作業で必要なファイルアクセス範囲や読むべき標準セクションを機械的に受け渡すための構造を確認する入口になる。

## Read this when
- AI Agent CLI/TUI に渡す解決済み実行パラメータの JSON 形状を確認したいとき。
- role、summary、goal、ファイルアクセス権、各標準セクションの要否をどの項目として持つかを確認したいとき。
- oracle file、realization file、INDEX.md に対する deny/read/write の判定結果と、その理由を出力に含める処理を扱うとき。
- oracle and realization basic、oracle standard、realization standard、review oracle standard、apply review standard、index entry standard の読解要否を構造化する処理を扱うとき。

## Do not read this when
- 個別の標準本文そのものの要求内容を確認したいとき。対象の標準セクション本文を直接読む。
- INDEX.md エントリーの文章作成規則を確認したいとき。index entry standard の本文を直接読む。
- 実際の oracle file や realization file の定義・分類を確認したいとき。oracle and realization basic の本文を直接読む。
- AI Agent が実行する具体的な実装・テスト・レビュー手順を知りたいだけで、解決済みパラメータの JSON 形状を確認しないとき。

## hash
- 2b60813c7d9fceaaa0147eb512473e0bf8863a05e9667632ea5dee459ad0a42c

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
- 66edd4b7dace80756392913d05bf41f7b4d65a40ffcdfdea792d9c578b459c71
