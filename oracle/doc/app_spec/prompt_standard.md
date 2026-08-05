
# prompt standard

## 概要

- cmoc が agent に渡すプロンプトが従うべき規範を述べる
- これは cmoc に固有の規範である（任意のプロダクトに適用可能な規範ではない）ため oracle doc として述べる

## cmoc 固有契約と installed skill の責務境界

- cmoc の agent call が解釈に必要とする次の契約は、cmoc が所有する oracle src から動的プロンプトへ注入する
    - cmoc 固有の概念
    - file access
    - `INDEX.md` routing
    - 出力契約
    - agent call 固有契約
    - cmoc の状態遷移または完了判定が解釈する判断基準
- installed skill は任意の追加規範として利用してよい
- installed skill の有無によって、cmoc の各サブコマンドが agent に要求する意味または判定基準を変えてはいけない
- cmoc 固有契約と installed skill が競合する場合は、cmoc 固有契約を優先する
- 言語、framework、tool、および対象 repository 固有の開発手順を cmoc が網羅することは目的としない
- 対象 repository 固有の手順は、repository が追跡する任意の文書、設定、script、または skill から取得してよい
- 対象 repository 固有の手順の配置先を `{{work-root}}/.agents/skills` に限定してはいけない

## 規範を決定論的に注入する

- agent call ごとに必要な規範は、対応する `build_*_parameter` 関数が `build_complete_prompt` の固定引数として選択する
- 規範の選択に installed skill、設定による任意切替、または追加の agent call を使用してはいけない
- `cmoc tui` は、適用条件を明記した cmoc の基本規範を固定で注入する
- `cmoc tui` のオリジナルプロンプトに応じて規範を選択する agent call を行ってはいけない
- indexing agent call は、`build_index_entry_standard` が定める index entry standard の責務を維持する

## Structured Output schema の責務

- Structured Output schema は、field、型、必須性、列挙値、および入れ子構造からなる出力構造を定義する
- cmoc が解釈する判定基準は、対応する prompt part の単一の正本に置く
- 同じ判定基準を複数の schema、個別 prompt、および prompt part に重複させてはいけない
- schema の field description は、field の意味と構造を説明する範囲に留める

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
- root path placeholder の意味と値は、`{{cmoc-root}}/oracle/src/oracle/other/path_model.py` の `AgentCallPathContext` を正本とする
- 個別の prompt part は、自身の文面で参照する root path placeholder の定義を、同じ `AgentCallPathContext` から取得して `PlaceholderMap` として返す
- 個別の prompt part は、`{{work-root}}` または `{{repo-root}}` の値を独自に解決してはならない
- 個別の prompt part が path に応じて文面を変える場合は、`build_complete_prompt` と同じ call-scoped path context を明示的に受け取る
- `build_complete_prompt` は、call-scoped path context の root 定義と各 prompt part の `PlaceholderMap` を統合し、最終 prompt では placeholder ごとに 1 個の定義を出力する
- 複数の prompt part が同じ placeholder 名と同じ値を要求する場合は、1 個の定義へ統合する
- 同じ placeholder 名へ異なる値を登録しようとした場合は、後勝ちで上書きせず prompt 構築を失敗させる

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
