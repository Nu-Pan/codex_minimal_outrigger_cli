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
- `cmoc oracle` 各サブコマンドの agent call 構築に関する oracle source をまとめたディレクトリ。TUI 起動、完全 prompt、アクセス制約、実行パラメータ、Structured Output schema、管理ログ保存の定義を扱う。

## Read this when
- `cmoc oracle edit`、`investigation`、`review` の TUI 起動処理や agent call パラメータを変更・調査するとき
- oracle file 編集・調査・レビュー用 prompt、アクセス権限、構造化出力契約を確認するとき
- レビュー所見の構造化出力、採否判定、重複・矛盾整理の agent call 条件を確認するとき

## Do not read this when
- oracle file の編集・調査・レビュー処理そのものを変更・調査するとき
- 共通の prompt 構築や実行制御だけを変更・調査するとき
- `cmoc oracle` 以外の agent call や TUI を調査するとき

## hash
- 88671e68ed8b6dd1edab55bcdcc53f34699136b4a2c15647d79376d630b7fa89

# `realization`

## Summary
- realization apply fork と refactor fork の agent call 起動処理に関する正本 schema・prompt 構築・実行条件を扱うディレクトリ。各 fork の変更要約、レビュー・修正処理、AgentCallParameter、Structured Output 契約を確認する入口。

## Read this when
- realization apply fork の agent call 起動処理、oracle 差分・commit 範囲・linked worktree の prompt 組み込み、AgentCallParameter 設定を変更・調査するとき。
- refactor fork の変更要約、単一ファイルのレビュー・修正、prompt 構築、実行条件、Structured Output schema を確認・変更するとき。

## Do not read this when
- refactor fork の実際のレビュー対象ファイルや変更差分の実装内容を調査するとき。
- 共通 prompt 生成仕様だけを確認するとき。
- 実際の realization implementation や test の追従内容を調査するとき。
- 要約・レビュー結果の詳細な出力形式だけを確認するとき。

## hash
- f7659db7413c66338eaabc75319db16f7a14d6fc37c17fdf34cae33b401d7135

# `session`

## Summary
- `cmoc session join` の merge conflict marker 解消用 AI エージェント呼び出しパラメータを構築する実装への入口。競合ファイルの実パス解決、解消用 prompt、書き込み権限、最高品質のモデル・推論設定を扱い、下位の conflict resolution 実装へ進むためのディレクトリ。

## Read this when
- `cmoc session join` の conflict marker 解消フローを変更・調査するとき
- 競合対象ファイルの解決、解消用 prompt、エージェント呼び出しのモデル・推論・実行ディレクトリ設定を変更するとき

## Do not read this when
- `session join` 以外のサブコマンドを変更・調査するとき
- merge conflict 解消処理や共通 prompt 構築処理そのものを直接変更・調査するとき

## hash
- 4c706eb84cb41f9d2aab9c4192c75ab4fa1fe36ca58af7b6d7e1bb30e5f9eb6b

# `tui`

## Summary
- `cmoc tui` の TUI 起動用 AgentCallParameter を構築するソース。オリジナルプロンプトから動的プロンプトを生成・保存し、モデル、推論強度、ファイルアクセス、作業ディレクトリ、インデックス事前処理、構造化出力などの起動設定をまとめる。TUI 起動条件や agent call パラメータを調べる入口。

## Read this when
- `cmoc tui` の TUI 起動処理を変更・調査するとき
- TUI 用のプロンプト生成・保存や起動パラメータを確認するとき

## Do not read this when
- TUI 以外のサブコマンドの起動パラメータを調べるとき
- 完全なプロンプトの共通生成仕様を確認するとき
- TUI の実行本体や画面操作の挙動だけを調べるとき

## hash
- 3790fe52c359504b97c539a1d998a5863c2e4db98a9eee1b38f19487aeabe679
