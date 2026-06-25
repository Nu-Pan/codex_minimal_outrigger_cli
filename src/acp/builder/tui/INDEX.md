# `resolve_parameter.json`

## Summary
- AI Agent CLI/TUI が受け取った作業依頼を、実行時に必要な論理ファイルアクセス権限と、参照すべき標準群の有無へ分類するための判定結果を定義する。
- 権限設定の理由付けと、oracle・realization・review・INDEX.md エントリー作成に関する各標準を読む必要があるかどうかの理由付けを、同じ形で返すための入口になる。

## Read this when
- 作業依頼から、読み取り専用・oracle 読み取り・realization 編集・oracle 編集・リポジトリ編集のどれを選ぶべきかを判定する出力を扱うとき。
- AI Agent CLI/TUI の parameter resolve 処理で、各種標準文書を読む必要があるかどうかを構造化して返す仕様を確認するとき。
- 依頼内容に対する権限選択や標準参照要否の理由を、実装やテストで検証するために期待形を確認するとき。

## Do not read this when
- 実際の oracle file や realization file の責務、編集可否、品質基準そのものを確認したいだけのとき。
- INDEX.md エントリー本文の書き方やルーティング文書としての判断基準だけを確認したいとき。
- TUI 表示、対話フロー、コマンドライン引数、ファイルシステム操作など、判定結果の外側にある挙動を調べるとき。

## hash
- c2f005d3f1e5fe15233afabe47653322e47dd41db9a8180e474a2221e7b8bbe0

# `resolve_parameter.py`

## Summary
- AI Agent CLI/TUI へ渡す実行パラメータを、ユーザー入力の元プロンプトから選定させるための呼び出しパラメータを構築する。
- 読み取り専用のファイルアクセスモード、効率重視モデル、中程度の推論 effort、対応する JSON schema 出力先を固定し、完全 prompt には元プロンプト、ファイルアクセスモード一覧、oracle・realization・review・INDEX エントリー関連の標準断片を含める。

## Read this when
- `cmoc tui` で入力された元プロンプトを実行前に解析し、AI Agent CLI/TUI のモデル、推論 effort、ファイルアクセスモード、prompt、schema をどう決めるか確認したいとき。
- 実行パラメータ解決用 prompt に含める role、summary、goal、補助文書、標準仕様断片の組み合わせを変更または調査したいとき。
- 元プロンプトの該当行や work tree 内ファイル行を根拠として示す、パラメータ選択タスクの要求内容を確認したいとき。

## Do not read this when
- TUI の画面表示、入力編集、イベント処理、対話 UI の挙動を調べたいだけのとき。
- AI Agent CLI/TUI の実行そのもの、プロセス起動、結果表示、または選定済みパラメータの利用箇所を調べたいとき。
- 個別のファイルアクセスルール本文、完全 prompt の組み立て共通処理、パス解決、または `AgentCallParameter` などの基礎データ構造そのものを調べたいとき。

## hash
- 11ebb7eea367d7b96ce877c6d17fbb1812301af8b345645272ee8073e4d8a256
