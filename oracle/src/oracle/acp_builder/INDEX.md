# `apply`

## Summary
- このディレクトリには、参照可能な正本ソース本文がない。正本ソースの有無を確認するための入口である。

## Read this when
- このディレクトリの内容や、参照可能な正本ソースの有無を確認するとき。

## Do not read this when
- 実装仕様や処理内容を確認したいとき。

## hash
- 0af302f7be7ef5db5b5b3790733cdc5b9d23e3de43be05b57a4287af7ea9be0d

# `basic.py`

## Summary
- AI コーディングエージェント呼び出し用の論理パラメータとデフォルト値を定義する。モデルクラス、推論負荷、ファイルアクセスモード、プロンプト、Structured Output schema、indexing preflight、作業ディレクトリを扱う。関連する agent call 設定の入口。

## Read this when
- Agent call のパラメータ構造、モデル選択区分、推論負荷、ファイルアクセスモード、preflight 実行方針、cwd の既定値を確認するとき
- Agent Call Parameter の生成・受け渡し処理を変更または調査するとき

## Do not read this when
- バックエンドが受理する具体的なモデル名への解決方法を確認したいとき
- 各ファイルアクセスモードの詳細規則や Codex CLI sandbox の仕様を確認したいとき
- パス解決そのものの仕様を確認したいとき

## hash
- 5bfd68846014d69f50ee19162dd738616d5814856daa60487cce0322b5da12e9

# `indexing`

## Summary
- `cmoc indexing` の目次エントリー生成に関する正本実装と、その呼び出しパラメータ用 JSON Schema を扱うディレクトリ。対象本文を埋め込んだ読み取り専用プロンプトの構築、構造化出力によるルーティングエントリー生成、モデル・推論・設定の指定を確認する入口。

## Read this when
- `cmoc indexing` のエントリー生成プロンプト、対象本文の埋め込み、構造化出力設定を変更・調査するとき
- 目次エントリー生成に使う呼び出しパラメータや JSON Schema を確認するとき

## Do not read this when
- 目次エントリーの一般的なルーティング基準や記述形式だけを確認したいとき
- 実際の indexing 実行処理、対象ファイルの探索、モデル呼び出しの実行経路を調べるとき

## hash
- a52af7824ce6dae69368045f30fc19b36ce54e0ddf050a1d601d51933aec63b5

# `oracle`

## Summary
- `cmoc oracle edit`、`investigation`、`review` 各処理の AgentCall 構築に関する実装をまとめたディレクトリ。TUI 起動設定、oracle 調査用プロンプトとログ保存、レビュー所見処理および各種 Structured Output schema を下位ファイルへの入口として扱う。

## Read this when
- `cmoc oracle` の TUI 起動条件、oracle 調査用プロンプト、editor_input ログ保存、またはレビュー所見の生成・判定・統合を変更・調査するとき。
- oracle 専用のファイルアクセス制約、モデル・推論設定、Structured Output の入出力契約を確認するとき。
- このディレクトリに含まれる個別処理の実装や用途を確認するとき。

## Do not read this when
- oracle file の編集・調査そのものの実行処理や、oracle review の一般的な判定基準を確認するとき。
- prompt 共通生成規則、パス解決、通常の ACP builder、または JSON schema の詳細実装だけを確認するときは、対応する共通実装・仕様文書・schema ファイルを直接読む。

## hash
- a9d071bc749ef34ecbb92855a6e7c88c76af2353cd083d2f637cc983f78f2883

# `realization`

## Summary
- Oracle 側の差分を realization file 全体へ反映する `codex exec` 用 AgentCallParameter の構築処理を扱う。raw git diff、commit 範囲、実行設定、linked worktree を prompt に組み込む。
- 変更要約とファイル単位レビュー・修正を行う agent call の oracle source と Structured Output schema を扱う。

## Read this when
- `cmoc realization apply fork` の実行 prompt、realization 追従処理、対象 agent call の実行設定を変更・調査するとき。
- refactor fork の change_summary または file_review_and_fix の出力形式、prompt、入力差分、対象パス、アクセスモード、モデル設定、検証要件、schema 指定を確認するとき。

## Do not read this when
- 通常の realization 実装・テストの挙動を変更または調査するとき。
- prompt の一般的な組み立て規則や、refactor 差分そのもの・レビュー対象の realization 実装を調査するとき。

## hash
- dd96a0937830b0d39dca023f54862aaf6883aa6baf7212231b44e6428fa68827

# `session`

## Summary
- `cmoc session join` の merge conflict marker 解消用 AgentCallParameter を構築する正本ソース。競合対象パスを実パスへ解決して prompt に列挙し、conflict 解消時の役割・目標・追加アクセス規則・モデルおよび推論設定を定義する。

## Read this when
- `cmoc session join` の conflict marker 解消 prompt の内容、対象ファイル指定、AgentCallParameter のモデル・推論・アクセス設定を変更または確認するとき。

## Do not read this when
- 通常の `session join` 実装や conflict 解消処理そのものを調べるときは、該当するサブコマンド実装・テストを直接読む。
- prompt 全体の共通構築規則を調べるときは、prompt builder や共通 prompt 定義を直接読む。

## hash
- 3c6b42e6170984ac75d89b0faddac0bb84751e6f83dc374948e382fecd729dfa

# `tui`

## Summary
- `cmoc tui` の起動・実行パラメータ解決に関する正本実装群。完全プロンプトの生成・保存、標準文書参照要否の判定、モデルや推論強度などの Agent CLI/TUI 設定を扱う。

## Read this when
- `cmoc tui` の起動処理、完全プロンプト、ログ保存先、AgentCallParameter を変更・調査するとき。
- AI Agent CLI/TUI に適用する標準文書の判定や、読み取り専用の実行設定を確認するとき。

## Do not read this when
- TUI 以外のサブコマンドの起動処理やプロンプト構築を調査するとき。
- 共通プロンプト構築規則、標準文書本文、実際の後続 AI Agent CLI/TUI 実装だけを確認したいとき。

## hash
- 7746b9c3f3debfda158128b34c5b8bf25fcc5c934e27473ef7a8f234e5ad3975
