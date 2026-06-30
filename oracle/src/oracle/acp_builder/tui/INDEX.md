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
- AI Agent CLI/TUI がオリジナルプロンプトを実行する前に、役割・作業概要・ゴール・論理ファイルアクセスモード・各種標準文書を読む要否を、根拠付きで解決するための入力パラメータ schema を定義する。
- 権限設定は readonly / pure_oracle_read / realization_write / oracle_write / repo_write から選ばせ、oracle と realization の基本、oracle standard、realization standard、review oracle standard、apply review standard、index entry standard の参照要否を boolean と理由の組で表す。

## Read this when
- オリジナルプロンプトから、AI Agent CLI/TUI に渡す実行前パラメータを構造化して決める処理を実装・検証する。
- 作業の役割、概要、ゴール、必要最小限のファイルアクセス権限を、理由付きで出力する schema を確認する。
- oracle / realization 関連の標準文書を読むべきかどうかを、各標準ごとに boolean と根拠で表す出力仕様を確認する。
- TUI のパラメータ解決結果について、追加プロパティ禁止、必須項目、列挙値、各フィールドの意味を確認する。

## Do not read this when
- 個別の標準本文そのものの要求内容を確認したいとき。対象の標準セクション本文を直接読む。
- INDEX.md エントリーの文章作成規則を確認したいとき。index entry standard の本文を直接読む。
- 実際の oracle file や realization file の定義・分類を確認したいとき。oracle and realization basic の本文を直接読む。
- AI Agent が実行する具体的な実装・テスト・レビュー手順を知りたいだけで、解決済みパラメータの JSON 形状を確認しないとき。

## hash
- ff75f059106ad9edc2b3ecda599f770b0173e67d21c17a3d4423ba9b46b0145d

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
