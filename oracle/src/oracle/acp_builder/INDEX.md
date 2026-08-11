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
- AI コーディングエージェント呼び出しに必要な論理モデルクラス、推論強度、ファイルアクセスモード、および呼び出し設定を定義する基礎データモデル。バックエンド固有のモデル解決やアクセス規則の具体化ではなく、呼び出しパラメータの共通契約を確認するための入口。

## Read this when
- Agent call のパラメータ構造、モデル選択区分、推論強度、ファイルアクセスモード、または indexing preflight の既定値を確認・変更するとき

## Do not read this when
- バックエンドが受理可能なモデル名への解決やファイルアクセス規則の具体的な文面を確認するとき
- Agent call の生成処理や個別 builder の挙動だけを調べるとき

## hash
- fea717dae8c45705bc5fb1af10be854cbfdbb80b1b58c8d24eb2713a1998da67

# `feedback`

## Summary
- feedback issue の同一性判定と現在状態の検証に関する Structured Output schema、およびそれらの agent call parameter 定義を扱うディレクトリです。既存・新規 issue の判定、候補 issue の verification、各処理の prompt・起動設定・schema 接続を確認する入口になります。

## Read this when
- feedback issue の重複・同一性判定の出力契約や prompt 構築を確認するとき
- issue candidate の unresolved、resolved、not_actionable、inconclusive 判定と必須フィールドを確認するとき
- normalize issue または verify issue の AgentCallParameter、読み取り専用設定、Structured Output 接続を変更・調査するとき

## Do not read this when
- issue の summary、impact、原因、現在性、actionability、human action、verification verdict、relation の生成規則だけを確認したいとき
- feedback state の保存や候補 issue の絞り込み処理を確認したいとき
- 個別 issue の内容や一般的な JSON Schema の仕様だけを確認したいとき

## hash
- 958b81a26d57e92901cc8621a04c1d5ba94950b09875e5febafe6c5fd1017b64

# `indexing`

## Summary
- `cmoc indexing` 用の agent 呼び出し定義をまとめる領域。対象本文からルーティング情報を生成する prompt、読み取り専用実行条件、モデル・推論設定、Structured Output schema への入口を扱う。

## Read this when
- `cmoc indexing` の agent 呼び出しパラメータ、prompt、構造化出力、または indexing preflight 設定を変更・確認するとき
- 目次エントリー生成の入力・出力契約や、呼び出し時のモデル／アクセスモードを確認するとき

## Do not read this when
- 通常の INDEX.md のルーティング内容や生成対象の実際の責務を調べるとき
- agent call の基本型、アクセスモード、モデル設定そのものを確認するときは、参照される共通の acp_builder 定義を直接読む

## hash
- 7ed0f6846e096720d2f7d2a69285d337daa2f24eac213c21c379e5e343106d61

# `oracle`

## Summary
- oracle 関連の agent call 起動処理を用途別に分けた領域です。oracle 編集フロー、調査フロー、レビュー処理の prompt・起動条件・パラメータ構築を確認する入口として機能します。

## Read this when
- `cmoc oracle edit` の TUI 起動、agent call パラメータ、完全 prompt の生成、作業環境・権限・ログ保存を確認するとき。
- `cmoc oracle investigation` の調査用 prompt、Codex CLI TUI 起動条件、ファイルアクセスモード、モデル・推論設定を確認するとき。
- oracle review の所見列挙・判定・擁護や反証・統合、Structured Output schema、prompt、モデル設定、アクセス範囲、起動条件を確認するとき。
- 配下に具体的なファイルが追加され、その内容や用途を確認するとき。

## Do not read this when
- oracle file の編集内容や仕様そのものを確認するとき。
- prompt の共通構築規則や agent call パラメータの型定義だけを確認するとき。
- oracle investigation の調査対象や oracle review の所見内容・根拠仕様を確認するとき。
- 通常の Codex CLI 起動処理や、oracle 以外の cmoc コマンドの起動パラメータだけを確認するとき。
- 個別の出力形式だけを確認する場合。

## hash
- ff9b5a6bb78972a6f54edbfcf2ff9f2a5a8397313d275cbeca7f97d3b8d5c6a3

# `realization`

## Summary
- `realization` 配下で、`apply` と `refactor` に関する agent call の構築定義および出力契約へ進むための入口です。`apply` は oracle file の差分適用に必要な prompt と実行条件を扱い、`refactor` は変更差分の要約およびファイル単位のレビュー・修正に必要な定義を扱います。

## Read this when
- `cmoc realization apply fork` の prompt、作業範囲、実行設定、事前インデックス処理を確認・変更するとき。
- refactor fork の変更差分要約、ファイル単位レビュー・修正、検証要求、出力契約を確認・変更するとき。
- `apply` または `refactor` の構造化出力契約を確認するとき。

## Do not read this when
- 他の realization コマンドの prompt や起動パラメータを確認するとき。
- 差分の適用・生成処理や、レビュー対象となる個別ファイルの内容を直接確認するとき。
- 一般的な prompt 構築規則や `AgentCallParameter` の共通仕様を確認するとき。

## hash
- a9ffad9cbef33e2d1044ac20db53eabfa542d5f97dc16d9edd0b56982fb572b7

# `session`

## Summary
- 対象ディレクトリは、`session join` 中に検出された競合ファイルを解消するエージェント呼び出し設定を扱い、競合パス、専用プロンプト、モデル・推論設定、書き込み権限、作業ディレクトリ、indexing preflight 制御をまとめる実装への入口となる。

## Read this when
- `session join` の merge conflict 解消エージェントについて、呼び出し条件、プロンプト、モデル・推論設定、権限、作業ディレクトリ、または indexing preflight 制御を変更・確認するとき。

## Do not read this when
- 通常の `session join` 処理や競合検出ロジックだけを確認するときは、まずそれらの処理実装を直接読む。
- 共通のプロンプト構築仕様や agent call パラメータ型を確認するときは、対応する共通実装を直接読む。

## hash
- f9b6ab8066c54f3623b16a0a9087939e50ee0527811916416a3134d17d9e9f25

# `tui`

## Summary
- `cmoc tui` の起動パラメータを構築する実装を扱う。リポジトリルートを作業ディレクトリとして確定し、オリジナルプロンプトを埋め込んだ完全プロンプトを生成・保存して、モデル・推論・アクセス設定と起動条件をまとめる入口。

## Read this when
- `cmoc tui` の起動パラメータ、作業ディレクトリ、モデル設定、推論設定を確認または変更するとき。
- TUI に渡す完全プロンプトの生成・保存方法や、オリジナルプロンプトの組み込み方を確認するとき。

## Do not read this when
- TUI 以外のサブコマンドの起動パラメータを扱うとき。
- 完全プロンプトの共通構造そのものを確認または変更するとき。

## hash
- 1901fa26779495632843837964128ea0a674e04b843cebca68728d0d752ff32b
