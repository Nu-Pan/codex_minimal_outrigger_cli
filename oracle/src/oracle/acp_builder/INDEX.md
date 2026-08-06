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
- エージェント呼び出しに必要な論理モデルクラス、推論強度、ファイルアクセスモード、および呼び出し固有パラメータを定義する正本仕様の型モジュール。モデル選択やアクセス制御を扱う箇所の入口となる。

## Read this when
- AgentCallParameter の構造、利用可能なモデルクラス・推論強度・ファイルアクセスモードを確認するとき。
- エージェント呼び出しのプロンプト、Structured Output スキーマ、作業ディレクトリ、インデックス事前処理の指定方法を確認するとき。

## Do not read this when
- 実際のバックエンド用モデル名への解決方法を確認したいとき。
- ファイルアクセス規則の詳細や Codex CLI sandbox への適用方法を確認したいとき。
- エージェント呼び出しの生成・実行処理そのものを確認したいとき。

## hash
- 688b81e8c85b0dec3716f65446db036b8c9ca17a9c20987507a52ee63aba7cbc

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
- oracle 関連の agent call パラメータ構築実装を、用途別の下位領域へ案内するディレクトリです。調査用 TUI、レビュー処理、追加された編集関連ファイルの入口として機能します。

## Read this when
- oracle investigation または oracle review の agent call パラメータ構築や関連処理の場所を判断するとき。
- このディレクトリに新しいファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- 特定の下位領域の実装を直接確認できるとき。
- 調査プロンプト本文、一般的な prompt builder の規則、レビュー基準や個別の JSON schema を確認するときは、対応する直接の対象を読む。

## hash
- f9a6ea683fdb1467b3e08bbc813e68caf4347838296cbea3a57fa133663c147e

# `realization`

## Summary
- oracle の変更を realization へ反映する apply fork と、差分要約・ファイル単位レビュー／修正を行う refactor fork の AgentCallParameter 構築実装と出力契約を扱うディレクトリです。各 fork の prompt、作業範囲、モデル・権限設定、検証条件、構造化出力スキーマを確認する入口になります。

## Read this when
- oracle の変更追従用 apply fork の起動パラメータ、prompt、差分参照、worktree 設定、完了条件を変更・調査するとき
- refactor fork の変更要約またはファイルレビュー・修正の出力契約、対象パス、権限、prompt、検証条件を変更・調査するとき

## Do not read this when
- 実際の差分適用ロジックやテストを調べるときは apply の実装・テストを直接読む
- 差分内容、対象 realization file、対応する oracle file の仕様適合性を調べるときは、該当する入力元や対象ファイルを直接読む
- 一般的な prompt 構築、AgentCallParameter、path context の共通定義、または refactor fork 以外の agent call を調べるときは、対応する共通実装や各 fork の入口を直接読む
- 構造化出力のフィールド定義だけを確認するときは、対応する JSON スキーマを直接読む

## hash
- b58111c52a0d7454b89c0305ea7a258f86c5c1b36f7da171e89c5678f57fbfb9

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
