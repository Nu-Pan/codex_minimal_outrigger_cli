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
- AI Agent CLI/TUI に渡す元プロンプトから、`cmoc tui` 実行前のエージェント呼び出しパラメータを選ぶための完全プロンプトを組み立てる実装。
- 実行対象の repository/work root、選択可能なファイルアクセスモード、oracle/realization/review/index entry 各標準を含めた読み取り専用の判断依頼を作り、効率重視モデル・中程度推論・読み取り専用アクセス・隣接 JSON schema を指定した呼び出しパラメータとして返す。

## Read this when
- `cmoc tui` がエディタ入力された元プロンプトをどのような実行パラメータ選定タスクへ変換するか確認したいとき。
- TUI 実行時に AI Agent CLI/TUI へ渡すモデル種別、推論努力、ファイルアクセスモード、Structured Output schema の指定元を追うとき。
- TUI のパラメータ解決プロンプトに含める標準文書、ファイルアクセスモード候補、元プロンプト埋め込みの内容を変更するとき。

## Do not read this when
- 実際に各ファイルアクセスモードの規則本文を確認したいだけのときは、ファイルアクセス規則を組み立てる対象を読む。
- 完全プロンプト共通構造や markdown 描画の詳細を確認したいときは、プロンプト部品や構造化文書の共通実装を読む。
- TUI 以外のサブコマンドの実行パラメータ解決や、エディタ入力の取得・コメント除去・strip 処理を調べたいときは、それぞれの呼び出し側または該当サブコマンド実装を読む。

## hash
- 1e011a946898b0ac4409518fa6030b2a2f8ec459733a9eb0d3605c09a9217e8e
