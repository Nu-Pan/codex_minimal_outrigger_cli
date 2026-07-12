# `launch_tui.py`

## Summary
- `cmoc tui` の起動時に、編集後の元プロンプトを共通プロンプトへ組み込み、完全プロンプトを保存したうえで `AgentCallParameter` を組み立てる入口。モデル選択、推論強度、ファイルアクセス方針、保存先の扱いを確認したいときに読む。
- TUI 実行本体やエディタ起動の流れではなく、TUI 起動用の呼び出しパラメータを決める責務に絞られている。

## Read this when
- `cmoc tui` の起動パラメータの決め方、保存される完全プロンプト、または起動時に固定されるモデル・推論強度・ファイルアクセス方針を変えたいとき。
- 元プロンプトをどう共通プロンプトに束ねて、どのファイルへ保存してからエージェント呼び出しに渡すかを確認したいとき。
- `cmoc tui` の実行フローのうち、TUI 起動用の `AgentCallParameter` を生成する部分だけを追いたいとき。

## Do not read this when
- `cmoc tui` の実行本体、エディタ選択、対話 UI の制御を追いたいだけのとき。
- 実行パラメータ解決や別の prompt 構築経路を見たいときは、そちらの定義側を読む。
- `AgentCallParameter` 型そのものや共通のモデル定義だけを確認したいとき。

## hash
- 607eeb5916ee1fcc251d67879a123cc05eda2bbceda36eaba5a385090c8bc45c

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
- `cmoc tui` の実行パラメータを決めるための正本。TUI から AI 呼び出しに渡すモデル選択・推論強度・ファイル参照方針・生成プロンプト組み立てを確認したいときに読む。

## Read this when
- `cmoc tui` の起動時に、どの AI 呼び出しパラメータを選ぶかを変更・確認したいとき。
- TUI 用プロンプトに、作業対象・ファイル参照方針・出力要求をどう埋め込むかを確認したいとき。
- 実行パラメータの決定根拠や、固定で強制している方針を追いたいとき。

## Do not read this when
- TUI の画面操作や入力取得そのものを追いたいときは、より上位のサブコマンド実装を読む。
- プロンプト本文の細部ではなく、個別の文言や構成要素の定義を確認したいときは、プロンプト生成部品側を読む。
- ファイルアクセス制御の一般ルールだけを確認したいときは、個別のパラメータ解決ではなくアクセスルール定義側を読む。

## hash
- ba88d436e907996d730353a98297fbd3e870f1ed20710cbf986e081d3619c71f
