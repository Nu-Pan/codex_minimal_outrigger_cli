
# prompt standard

## 概要

- cmoc が agent に渡すプロンプトが従うべき規範を述べる
- これは cmoc に固有の規範である（任意のプロダクトに適用可能な規範ではない）ため oracle doc として述べる

## agent call に渡すプロンプトは、oracle src 定義の関数を使用する

- agent call に渡すプロンプトは `{{cmoc-root}}/oracle/src/oracle/acp_builder/**/*.py` で定義されている `build_*_parameter` 関数で動的に構築する
- 原則として、この動的構築された　プロンプトをそのまま agent call 側に渡す事し、realization file 側でプロンプトを加工するのは禁止
- 例外として、oracle src 側にバグがあって realization file 側でフォローする必要がある場合は、必要最低限の範囲内での加工を許容する

## 言語

### 原則

- Codex CLI で取り扱う自然言語的な部分は、原則として日本語とする
- e.g.
    - 入力プロンプト
    - 作業レポート
    - レビューレポート
    - INDEX.md の Summary / Read this when / Do not read this when
    - エラーの説明・次に取るべきアクション
    - Codex CLI によるレビュー結果・調査結果の文章部分
    - ...

### 例外

- 個別の仕様に言語指定がある場合はそちらに従う
- 個別の仕様として識別子が規定されている場合はそちらに従う
    - e.g. Structured Output の schema として定義されているキー名
- 元々が英語のワードは、英語のままで良い
    - e.g. コード識別子、ファイルパス、コマンドライン、JSON schema のキー、ログ原文、引用文、…
- LLM 内の思考言語 (e.g. reasoning 時の言語) のように、人間が直接読む想定ではない部分は自由にして良い
