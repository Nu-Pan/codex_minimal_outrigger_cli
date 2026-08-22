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
- `cmoc oracle investigation` 向けに、ユーザー指示を埋め込んだ完全プロンプトと Codex CLI TUI 起動パラメータを構築する実装。調査対象、達成条件、oracle file の根拠提示、未定義事項の扱い、読み取り専用のファイルアクセス範囲を定義する。
- TUI 起動時のモデル、最大推論強度、oracle 専用読み取りモード、リポジトリルートの作業ディレクトリ、indexing preflight を固定する。oracle investigation の prompt 構成と起動条件を確認するための入口。

## Read this when
- `cmoc oracle investigation` の完全プロンプトの構成や、ユーザー指示の埋め込み方法を確認するとき
- oracle investigation の読み取り専用調査範囲、調査結果の達成条件、oracle file の根拠提示や未定義事項の扱いを確認するとき
- oracle investigation の TUI 起動に使うモデル、推論強度、作業ディレクトリ、ファイルアクセスモード、indexing preflight を変更または確認するとき

## Do not read this when
- oracle file 自体の正本仕様や調査内容を確認するときは、対象の oracle file を直接読む
- 一般的な TUI 起動処理や `AgentCallParameter` の共通仕様を確認するときは、共通実装を直接読む
- `cmoc oracle investigation` 以外のコマンドの prompt や TUI 起動パラメータを確認するときは、該当する実装を直接読む

## hash
- b4def0a02e5b634b8e7a614c92927ecee3b72253b09c42ade1bcb502ee9094f4

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
