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
- AI Agent CLI/TUI がオリジナルプロンプトを実行する際に解決する実行パラメータの構造を定義する JSON schema。
- 役割、作業概要、任意のゴール、論理ファイルアクセスモード、各標準文書を読む必要性を、それぞれ値と根拠の組で返す形式を扱う。
- プロンプト内容から実行条件を判定し、過不足のない権限と参照すべき標準を構造化する処理の入口になる。

## Read this when
- オリジナルプロンプトから AI Agent に与える役割、概要、ゴールを構造化する出力形式を確認したいとき。
- 論理ファイルアクセスモードの選択肢や、その選択理由をどの形で返すべきか確認したいとき。
- oracle/realization の基本、oracle standard、realization standard、review/apply review/index entry standard を読む必要性の判定結果をどの形で表すか確認したいとき。
- resolve parameter 系の出力検証、schema 適合性、必須項目、追加プロパティ禁止の扱いを変更するとき。

## Do not read this when
- 個々の標準文書の要求内容そのものを確認したいとき。
- CLI/TUI の実行フローや UI 表示の実装を調べたいだけのとき。
- INDEX.md エントリー本文の書き方やルーティング方針を確認したいとき。
- oracle file や realization file の定義・分類を自然言語仕様として読みたいとき。

## hash
- ace731f62d898f31a29a3074830d3db6535ba94360c2d015174386292ec9b3f5

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
