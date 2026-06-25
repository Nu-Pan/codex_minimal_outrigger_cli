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
- `cmoc tui` でユーザー入力プロンプトを実行する前に、AI Agent CLI/TUI へ渡す実行パラメータ選定用の呼び出しパラメータを組み立てる実装。
- 元プロンプト、候補となるファイルアクセスモード、oracle/realization/index entry の各標準を含む完全プロンプトを生成し、効率重視モデル・中程度 reasoning・readonly 実行・対応する Structured Output schema を指定した `AgentCallParameter` として返す。

## Read this when
- `cmoc tui` の実行前に、モデル種別、reasoning effort、ファイルアクセスモード、または出力 schema をどう選ばせるかを確認・変更したいとき。
- TUI から渡された元プロンプトを、実行パラメータ選定担当向けの完全プロンプトへどう埋め込むかを確認したいとき。
- 実行パラメータ解決で提示するファイルアクセスモード候補、または oracle/realization/review/index entry 標準の同梱有無を調整したいとき。

## Do not read this when
- 実際に選定された実行パラメータの JSON schema 定義だけを確認したいときは、対応する schema 側を読む。
- 各ファイルアクセスモードの具体的な規則本文を確認したいときは、ファイルアクセス規則を生成する部品側を読む。
- `cmoc tui` のユーザー入力取得、コメント除去、strip、またはサブコマンド起動フローを確認したいときは、呼び出し元の TUI 実装を読む。

## hash
- c93263bfac439dc8c5aa10669cff96e007bad153d8dfc8ecbd9e3a8e18e1cb6f
