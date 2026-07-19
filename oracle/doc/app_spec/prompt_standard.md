
# prompt standard

## 概要

- cmoc が agent に渡すプロンプトが従うべき規範を述べる
- これは cmoc に固有の規範である（任意のプロダクトに適用可能な規範ではない）ため oracle doc として述べる

## agent call に渡すプロンプトは、oracle src 定義の関数を使用する

- agent call に渡すプロンプトは `{{cmoc-root}}/oracle/src/oracle/acp_builder/**/*.py` で定義されている `build_*_parameter` 関数で動的に構築する
- 原則として、この動的構築されたプロンプトをそのまま agent call 側に渡すこととし、realization file 側でプロンプトを加工するのは禁止
- 例外として、oracle src 側にバグがあって realization file 側でフォローする必要がある場合は、必要最低限の範囲内での加工を許容する

## 記法

### ベース記法

- プロンプトのベース記法は Markdown とし、採用する Markdown 方言は GitHub Flavored Markdown（GFM）とする
- 以下で定めるプレースホルダとプロンプト上の参照関係は、GFM に加える cmoc 固有の記法とする

### プレースホルダ

- プレースホルダは、`{{repo-root}}` のように名前を二重波括弧で囲って表記する

### プロンプト上の参照関係

- 参照される対象は、次の XML タグ風の記法で囲う

    ```xml
    <cmoc_block id="target-1">
    ...
    </cmoc_block>
    ```

- 対象への参照は、次の XML タグ風の記法で表す

    ```xml
    <cmoc_ref target="target-1"/>
    ```

- `cmoc_block`、`id`、`cmoc_ref`、`target` は固定の名前とし、`target-1` は参照先を対応付ける可変値とする
- 動的なプロンプト構築では、`cmoc_block` を参照対象の `StructDoc` を子に持つ構造として表し、`cmoc_ref` は参照元のプロンプト文字列内に直接記述する
- Markdown へのレンダリング時に、各 `cmoc_ref` の参照対象が構築結果内に一つだけ存在することを検査し、参照対象の欠落、`cmoc_block` の `id` 重複、または不正な `cmoc_ref` 記法を検出した場合はプロンプト構築を失敗させる

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
