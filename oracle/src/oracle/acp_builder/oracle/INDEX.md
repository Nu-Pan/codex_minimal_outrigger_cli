# `edit`

## Summary
- `cmoc oracle edit` の TUI 起動関連を扱うディレクトリです。現時点では空の `fork` と、TUI 起動パラメータを構築する `launch_tui.py` を含みます。

## Read this when
- `cmoc oracle edit` の TUI 起動方法、編集 prompt、モデル・権限・作業ディレクトリなどの起動設定を確認または変更するとき。
- このディレクトリに追加されたファイルの内容や用途を確認するとき。

## Do not read this when
- oracle file の編集処理そのものを確認または変更するとき。
- prompt 共通生成規則、パス解決、構造化文書のレンダリングを確認または変更するとき。
- `launch_tui.py` など対象ファイルを直接確認できるとき。

## hash
- c2d7be308c0da03ba02dc172c32c84646643a7b7356b27d85318fccd6beb2462

# `investigation`

## Summary
- `cmoc oracle investigation` 用の TUI 起動パラメータを構築し、oracle file 調査向けの完全プロンプトと editor_input ログ保存を扱う実装。固定モデル、推論設定、oracle 読み取り権限、インデックス事前処理を指定した起動情報を返す。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件を変更・確認するとき
- 調査プロンプトの構成や editor_input ログ保存を変更・確認するとき

## Do not read this when
- oracle 調査プロンプトの共通生成規則を変更するときは、まず共通 prompt builder を読む
- TUI 起動後の agent 実行処理や oracle file の内容を調査するときは、対応する実行処理または oracle file を直接読む

## hash
- 7f380ea9b83f602cfad5fcf5e4fdcc220fc6968b7ee974a4b056845a14440eef

# `review`

## Summary
- `cmoc oracle review`の所見検出・擁護・反証・採否判定・重複整理に使うAgentCallパラメータ実装と、各処理のStructured Output用JSON Schemaをまとめたディレクトリ。レビュー所見のプロンプト、oracle-onlyの読み取り制約、モデル設定、入出力契約を確認するための入口。

## Read this when
- `cmoc oracle review`の所見列挙、擁護理由・反証理由の生成、採否判定、所見リストのマージ処理を変更または調査するとき。
- レビュー用AgentCallのプロンプト埋め込み、oracle fileアクセス制約、モデル・推論設定、Structured Output schemaの対応を確認するとき。
- 所見の重大度、見出し、根拠oracle file、理由、編集操作などの出力形式を確認するとき。

## Do not read this when
- 通常のACP builder実装や、oracle review以外のAgentCall構築を調査するとき。
- oracle reviewの一般的な判定基準・レビュー規則を確認したいときは、対応するoracle review仕様文書を直接読む。
- JSON Schema自体の詳細な実装・検証方法だけを確認したいときは、対象schemaを直接読む。

## hash
- 55d4e6eb1fcb230017789d0368fa03dc22f9bc8fe61bccd55385d32e926f2007
