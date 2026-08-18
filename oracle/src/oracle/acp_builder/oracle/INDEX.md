# `edit`

## Summary
- `cmoc oracle edit` の起動処理を構成するディレクトリ。本命の oracle 編集 call と仕様削減 call の起動パラメータ・prompt 構成を担う `launch_exec.py` と、現時点では内容のない `fork` が入口となる。

## Read this when
- `cmoc oracle edit` の codex exec 起動パラメータ、prompt 構成、または本命 call／仕様削減 call の責務やアクセス制約を確認・変更するとき
- このディレクトリに追加されたファイルの内容や用途を確認するとき

## Do not read this when
- oracle file 自体の仕様内容や編集方針を確認するとき
- 一般的な agent call の基底型、パス解決、prompt builder、構造化文書レンダリングの実装を確認するとき
- realization 側の CLI 動作やテストの実装を確認するとき
- `fork` 配下の具体的なファイルを直接確認できるとき

## hash
- ef16e1ea0461f03261a52b1ea1295c90d55e7ac56547ebb0f1c846435b8f00e5

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータ構築を担う実装への入口。ユーザー指示を完全プロンプトへ組み込み、oracle 調査向けの読み取り専用設定、パスコンテキスト、モデル・推論設定、インデックス事前処理を備えた `AgentCallParameter` を構築する。

## Read this when
- `cmoc oracle investigation` の TUI 起動設定を変更・調査するとき
- oracle 調査用プロンプトへのユーザー指示の組み込み方、起動時のアクセスモード、モデル、作業ディレクトリを確認するとき

## Do not read this when
- 完全プロンプトの共通構造だけを調べる場合
- エージェント呼び出しパラメータの型や列挙値の一般仕様だけを調べる場合
- oracle 調査の正本仕様や対象ファイルの内容を調べる場合

## hash
- e8bd6dd7a801e70d1153970beaae392ac5c90e4c5d827c5cc270ac99122ebb75

# `review`

## Summary
- oracle review の所見列挙・擁護・反証・判定・統合に関する agent call 定義と Structured Output schema を扱うディレクトリ。各ファイルは、所見レビューの呼び出し構築、出力形式、または所見整理の入出力契約を確認・変更するための入口となる。

## Read this when
- oracle review の所見列挙、妥当性検証、採否判定、重複・矛盾整理の agent call や Structured Output を確認・変更するとき。
- 所見本文と既知の理由を review prompt に埋め込む処理、oracle-only の読み取り条件、モデル・推論設定、schema 指定を調べるとき。

## Do not read this when
- oracle review の所見内容や、その根拠となる oracle file・review policy 自体を確認するとき。
- Structured Output の項目や JSON 形式だけを確認するときは、対象の同名 schema を直接読む。
- agent call の共通生成規則や、実際の所見編集・判定ロジックを確認するときは、それぞれの共通定義または処理実装へ直接進む。

## hash
- 9166aa0b005e8b7d11d948191de420d742c2aaca3fb09eb55987532599cb79b6
