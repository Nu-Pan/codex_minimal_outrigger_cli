# `oracle`

## Summary
- cmoc の oracle 側実装をまとめるディレクトリで、パス・設定・文書構造などの基盤モデル、agent 向け完全 prompt と各種 policy の構築、agent call 用パラメータ、indexing・oracle/realization 操作・feedback 処理・TUI 起動を扱う。
- `other` は設定・パス解決・文書参照・構造化文書などの共有モデル、`prompt_builder` は agent に渡す prompt と制約文面、`acp_builder` は各処理の agent call パラメータと実行単位、`editor_input_handoff` と `feedback` は入力引き渡しおよび問題報告用の補助処理への入口である。

## Read this when
- oracle 側の共有データモデル、パス placeholder、設定、文書参照、または構造化 Markdown の責務を確認するときは `other` 配下から読む。
- agent に渡す prompt の組み立て、ファイルアクセスや oracle/realization、routing、index entry などの policy を確認するときは `prompt_builder` 配下から読む。
- 特定の cmoc 操作がどの agent call を構築し、どの schema・cwd・アクセスモードを指定するかを確認するときは `acp_builder` 配下の該当操作から読む。
- indexing の INDEX.md エントリー生成の起点を確認するときは `acp_builder/indexing`、問題報告の入力形式や処理を確認するときは `feedback`、エディタ経由の入力処理を確認するときは `editor_input_handoff` から読む。

## Do not read this when
- 単一の処理の具体的な実装だけを確認したい場合は、このディレクトリ全体ではなく、該当する `acp_builder`・`prompt_builder`・`other` の下位ファイルを直接読む。
- 正本仕様や利用者向けの動作説明を確認したい場合は、oracle 実装ディレクトリではなく対応する `oracle/doc` を読む。
- 実際に動作する realization 実装やテストの挙動を確認したい場合は、oracle/src 配下ではなく `src` または `test` の該当箇所を読む。

## hash
- 9b9ebf7f9e409b92aac9eb76699beaa45b07da345063e258fce40abbb3a26d52
