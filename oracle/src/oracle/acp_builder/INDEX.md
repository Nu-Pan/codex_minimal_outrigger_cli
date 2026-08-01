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
- AIコーディングエージェント呼び出しに渡すパラメータの論理モデルを定義する。モデルクラス、推論強度、ファイルアクセスモード、プロンプト、Structured Output スキーマ、作業ディレクトリ、インデックス事前処理の実行可否を扱う。各列挙値の意味と、バックエンド固有値への解決を実装側に委ねる境界も示す。

## Read this when
- Agent Call Parameter の構造や既定値を確認・変更するとき
- モデル選択、推論強度、ファイルアクセス権限、Structured Output、agent call の作業ディレクトリを扱うとき
- indexing preflight の実行条件を確認するとき

## Do not read this when
- Codex CLI の具体的なファイルアクセス規則を確認したいときは、指定された正本仕様を直接読む
- バックエンドが受理可能なモデル名や Reasoning Effort 名への解決方法を確認したいときは realization src を読む
- agent call の prompt 構築処理や builder の実装詳細だけを確認したいとき

## hash
- f9b3e077a13bda4bd4bd865643b4da0fcd9f5291fb6e597c04629c9eb3037c46

# `indexing`

## Summary
- 対象ディレクトリは、INDEX.md エントリー生成用の出力スキーマと、その生成 agent call を構築する正本実装を扱う。JSON Schema はエントリーの必須配列構造を定義し、Python 実装は対象本文・生成規則・パス文脈・Structured Output 設定・実行パラメータを組み合わせる。

## Read this when
- INDEX.md エントリー生成の JSON 出力形式、必須項目、検証方法を確認するとき。
- cmoc indexing が構築する INDEX.md エントリー生成 prompt や agent call の設定を変更・調査するとき。

## Do not read this when
- 対象ファイルやディレクトリの実際のルーティング内容を判断するとき。
- INDEX.md 生成処理全体の共通実行フローや prompt 組み立て規則を調査するとき。

## hash
- f4b3700b4ac69f46991ba15a9f8387648f1b5ac005e21e82d83214093f2a1652

# `oracle`

## Summary
- oracle の edit、investigation、review 用 ACP builder をまとめるディレクトリです。TUI 起動用の prompt・起動パラメータと、oracle file の所見レビューに用いる prompt builder・Structured Output schema を下位領域への入口として提供します。

## Read this when
- `cmoc oracle edit` または `cmoc oracle investigation` の TUI 起動 prompt、ログ保存、作業ディレクトリ、モデル、推論強度、ファイルアクセスモードを確認・変更するとき。
- `cmoc oracle review` の新規所見列挙、所見の採否判定、擁護理由・反証理由の列挙、所見リストの統合を確認・変更するとき。
- oracle review の Structured Output schema または各レビュー処理の agent call パラメータを確認・変更するとき。

## Do not read this when
- oracle file の仕様内容や編集対象そのものを確認・変更するとき。
- 一般的な prompt 構築、パス解決、構造化文書レンダリング、agent call の共通実装を確認するとき。
- 対象配下の具体的な実装ファイルまたは schema を直接確認できるとき。

## hash
- f8549241d4fb54d417327338497a2e57d53cf6e2453147179b95d0d40ff36b7c

# `realization`

## Summary
- `cmoc realization apply fork` 用の AgentCallParameter 生成に関する正本コードを扱う。prompt、権限、oracle 差分、実行用 worktree、commit 範囲、モデル設定の確認・変更に進む入口。
- refactor fork の変更要約および単一ファイルレビュー・修正用 AgentCallParameter 生成の正本コードを扱う。Structured Output schema、対象 path、prompt、権限、検証条件、git 操作制約の確認・変更に進む入口。

## Read this when
- `cmoc realization apply fork` の AgentCallParameter、prompt、実行環境、oracle 差分、commit 範囲、モデル設定を調査・変更するとき。
- refactor fork の変更要約または単一ファイルレビュー・修正の schema、prompt、対象 path、権限、検証条件、git 操作制約を調査・変更するとき。

## Do not read this when
- 通常の realization 実装・テスト、oracle 変更に追従する realization 実装を調査するとき。
- `cmoc realization apply fork` 以外の agent call 起動処理を調査するとき。
- レビュー対象ファイルの実装内容や個別の oracle・realization file の仕様だけを調査するとき。
- 一般的な prompt 構築、path 解決、構造化文書レンダリングの実装だけを調査するとき。

## hash
- d045e443305f770674659ad4c196e7a2db0d2893c5fa7fc39b4020670cb369a9

# `session`

## Summary
- `cmoc session join` における merge conflict marker 解消用 AI エージェント呼び出しパラメータの正本ソースを収録するディレクトリ。競合対象パスの解決、プロンプト、最高品質・リポジトリ書き込み設定を扱う。

## Read this when
- `cmoc session join` の merge conflict 解消 prompt、競合対象ファイルのパス解決、または agent call 設定を変更・確認するとき。

## Do not read this when
- 通常の prompt 生成を扱うとき。
- `session join` の conflict 解消以外の agent call を扱うとき。

## hash
- 42b7025ceb8aaf4f1ed8061851f8793a0396ffdbb7909339d12f80b4176ef9cc

# `tui`

## Summary
- `cmoc tui` の起動・実行パラメータ解決に関わる oracle src と、標準文書の参照要否を判定する入力 schema を含むディレクトリ。TUI 起動条件、完全 prompt、AgentCallParameter、実行環境設定、Structured Output schema の関連箇所への入口となる。

## Read this when
- `cmoc tui` の AgentCallParameter、起動条件、完全 prompt、モデル・推論設定、ファイルアクセスモード、agent call の cwd、prompt 保存処理を確認・変更するとき。
- AI Agent CLI/TUI 実行時の標準文書参照要否を判定する処理や入力 schema を確認するとき。
- TUI 用の構造化出力 schema の指定箇所や、ユーザー入力から後続 agent 呼び出しまでの prompt 構築経路を追跡するとき。

## Do not read this when
- TUI の画面表示、対話制御、エディタ入力処理そのものを確認するとき。
- 通常の CLI サブコマンド実装や、prompt 本文の共通生成ロジックだけを調査するとき。
- oracle standard、realization standard、レビュー標準の本文や、TUI 実行後の agent 呼び出し実装を直接確認するとき。

## hash
- 383e81fb868c8c17d59795551289e7f1a7d21d6220e651e3863af536f6a08f5d
