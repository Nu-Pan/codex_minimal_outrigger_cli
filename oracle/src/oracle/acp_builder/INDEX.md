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
- oracle 関連の agent call 構築定義を扱うディレクトリです。対話型の oracle 編集・調査と、oracle file のレビューに関する prompt、ファイルアクセスモード、実行設定、Structured Output schema の確認入口になります。
- 編集・調査の TUI 起動処理を確認する場合は edit または investigation へ、所見の列挙・妥当性検証・採否判定・統合を確認する場合は review へ進みます。review では、処理本体と対応する出力 schema を目的に応じて確認します。

## Read this when
- oracle 用 agent call の責務分担、prompt 構築、読み取り・書き込み権限、実行設定の入口を判断するとき。
- oracle 編集や調査の TUI 起動処理を確認するとき。
- oracle review の所見生成から検証、採否判定、重複・矛盾の整理までの処理群を確認するとき。

## Do not read this when
- oracle file 自体の編集内容、調査対象、レビュー基準を確認するときは、対象の oracle file やレビュー処理を直接読みます。
- 個別の起動処理だけを確認するときは edit または investigation を直接読みます。
- 個別の Structured Output の形式だけを確認するときは review 配下の対応する schema を直接読みます。

## hash
- dfad978d10e074acb1d73329f183c66b21aefcbff2c643ea0b34b91a21a71447

# `quota_probe.py`

## Summary
- Codex CLI の quota 回復確認用 agent call を構築する定義。quota probe 用の完全 prompt と起動パラメータを組み立てる入口として機能する。

## Read this when
- Codex CLI の利用可能性や quota 回復確認用 agent call の構築を変更・調査するとき。
- quota probe の prompt、モデル・推論設定、読み取り専用設定、実行コンテキストの決定を確認するとき。

## Do not read this when
- quota probe 以外の agent call 構築を変更・調査するとき。
- 一般的な prompt 生成規則や他の ACP パラメータ定義を直接確認する場合。

## hash
- 1e350f6b6a20e73903ee41b54ac531753f8e67704ccf9d2250cbd15cd1ebd448

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
