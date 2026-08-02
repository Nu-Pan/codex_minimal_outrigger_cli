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
- `cmoc oracle` 配下の各機能に対応する実装領域へのルーティング情報を提供します。`edit` は空の追加予定領域、`investigation` は調査 TUI の起動パラメータ構築、`review` はレビュー各段階の Structured Output と agent call パラメータ構築を扱います。

## Read this when
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。
- `cmoc oracle investigation` の TUI 起動パラメータ、完全プロンプト生成、作業パス確定、起動ログ保存を変更・調査するとき。
- `cmoc oracle review` の所見生成・判定・擁護・反証・統合、または関連する prompt、アクセス権、モデル設定、Structured Output 接続を確認するとき。

## Do not read this when
- `edit` 配下の具体的なファイルを直接確認できるとき。
- oracle investigation の調査プロンプト本文や一般的な prompt 組み立て規則だけを確認したいとき。
- TUI 起動以外の agent call パラメータ構築を変更するとき。
- レビュー基準や個別所見の内容を確認するとき。
- 共通の agent call パラメータ、prompt 構築、パス解決の仕様だけを確認するとき。
- 所見統合結果の適用処理など、agent call パラメータ構築以外の実装を調査するとき。

## hash
- 7c6a5e5598abeb010097ad3b5cb9afe643d3be7da6aede15304eef29220caff7

# `realization`

## Summary
- `cmoc realization apply fork` の起動パラメータを構築し、oracle 差分・commit 範囲・linked worktree を prompt に組み込んで realization file の追従を委譲する実装。差分追従の AgentCallParameter、モデル・worktree 設定、完了条件を確認する入口。
- `refactor fork` の変更要約およびファイル単位レビュー・修正に用いる AgentCallParameter と Structured Output schema の定義。変更要約、根拠、所見、oracle 要求、対応、検証結果、prompt 構成や実行条件を確認する入口。

## Read this when
- oracle file の変更を realization file へ追従させる起動パラメータ、prompt、差分参照、モデル設定、worktree 設定を確認・変更するとき。
- refactor fork の変更要約出力、レビュー・修正結果の形式、根拠ファイル、oracle・realization 参照規則、prompt 構成や Structured Output schema を確認・変更するとき。

## Do not read this when
- realization apply fork の差分適用ロジックやテストだけを調べるとき。
- 一般的な prompt 構築、AgentCallParameter、path context の共通定義を調べるとき。
- レビュー対象ファイルの具体的な実装、個別の差分や所見、通常の実装・テスト仕様を調べるとき。

## hash
- f56229be53dc5064f5cccdbd3ef31848c8bbf52321d759f9bd80295846949760

# `session`

## Summary
- `cmoc session join` のマージ競合解消用 AI エージェント呼び出しパラメータを構築する。対象パス、プロンプト、モデル・推論設定、書き込み権限、作業ディレクトリ、preflight 設定を扱う。

## Read this when
- `cmoc session join` の競合解消フローや agent call パラメータを変更・調査するとき
- 競合対象パス、プロンプト、モデル・推論設定、preflight 設定を確認するとき

## Do not read this when
- マージ競合の実際の解消ロジックや git 操作を調査するとき
- `session join` と無関係な agent call パラメータやプロンプト生成を調査するとき

## hash
- 9edbb85d9e4980b4dc7e83b2451f75687b86f1226f54c5c9d585cd0a300120fe

# `tui`

## Summary
- `cmoc tui` の TUI 起動用パラメータを構築する正本実装。完全なプロンプト、モデル・推論設定、リポジトリ書き込み権限、作業ディレクトリ、索引付け前処理などを含む `AgentCallParameter` を返す。TUI の起動条件・プロンプト保存先・エージェント呼び出し設定を確認する入口。

## Read this when
- `cmoc tui` の起動動作を変更・調査するとき
- TUI 用のプロンプト保存先、パスコンテキスト、モデル・推論設定、ファイルアクセスモードを確認するとき
- TUI 起動パラメータの入力と返却内容の関係を確認するとき

## Do not read this when
- TUI 以外のサブコマンドのエージェント呼び出し設定を調べるとき
- 完全なプロンプトの構成や共通レンダリング処理自体を調べるとき
- エージェント呼び出しパラメータの型定義や列挙値の意味だけを確認するとき

## hash
- a6acf4afeb76df2a1fede86e399c363d611a15371b18ef1edc76a7397439eb83
