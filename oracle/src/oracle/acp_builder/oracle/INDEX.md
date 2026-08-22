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
- oracle review の所見列挙・妥当性検証・採否判定・統合に関する Structured Output schema と、各 agent call の prompt／起動パラメータ定義を収録するディレクトリ。個別処理の出力契約を確認する場合は対応する JSON schema、呼び出し内容やレビュー役割の実装を確認する場合は対応する Python builder が入口となる。

## Read this when
- oracle review の所見を生成、擁護、反証、判定、統合する処理の入出力契約を確認するとき
- レビュー用 agent call の prompt、モデル設定、読み取り範囲、Structured Output 設定を確認するとき
- 所見の重複整理や採否判定に関する処理を変更・調査するとき

## Do not read this when
- レビュー対象となる oracle file や個々の所見内容そのものを確認したいとき
- oracle review 全体の実行制御や、判定後の編集・適用処理を確認したいとき
- 特定の出力形式だけを確認する場合に、対応する JSON schema または特定の agent call builder を直接読む方が適切なとき

## hash
- 8c73568afcfa3af1a765510800f8c7dd3c760071c420576894c5f37bdfe01321
