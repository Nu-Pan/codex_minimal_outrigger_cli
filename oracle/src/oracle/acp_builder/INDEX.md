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
- エージェント呼び出しに渡すモデル種別、推論強度、ファイルアクセス権、プロンプト、Structured Output schema、作業ディレクトリなどのパラメータ型と既定値を定義する基礎モジュール。ACP 呼び出し条件やファイルアクセスモードの意味を確認する際の入口。

## Read this when
- エージェント呼び出しパラメータの構造、モデルクラス、推論強度、ファイルアクセスモード、既定の作業ディレクトリを変更・確認するとき。
- ACP builder が受け取るパラメータや Structured Output schema の指定方法を調査するとき。

## Do not read this when
- 具体的なバックエンドモデル名への解決や実際のエージェント呼び出し処理を調べるとき。
- 各ファイルアクセスモードの詳細な実行規則や Codex CLI の制約を確認するときは、対応する正本仕様を直接読む。

## hash
- f91c2bdf4465ac41f25992aa68d2b5dd683ae48609a6bb4abae4fdc63a1dbe73

# `indexing`

## Summary
- indexing 用の agent 呼び出しパラメータを構築するファイルと、INDEX.md エントリーの JSON Schema を定義するファイルを含む。`cmoc indexing` の呼び出し条件、入力の渡し方、出力形式を確認するための入口。

## Read this when
- `cmoc indexing` の目次情報生成用 agent 呼び出しの構築方法を確認するとき。
- indexing 用エントリーの入力・出力形式や検証条件を確認するとき。

## Do not read this when
- indexing の実行本体や生成された目次情報そのものを確認するとき。
- prompt の共通組み立てや、他サブコマンド向けの呼び出し設定だけを確認したいとき。

## hash
- 05d354f9306a4d79e5cdde86862b45fca33f2443725b3db2a3a55045ad235bb7

# `oracle`

## Summary
- `cmoc oracle edit` の TUI 起動関連を扱うディレクトリ。現時点では空の `fork` と、TUI 起動パラメータを構築する `launch_tui.py` を含む。
- `cmoc oracle investigation` の TUI 起動用パラメータを構築する実装。ユーザー調査指示を含む完全プロンプトの生成・保存と、モデル・アクセス権限などの固定起動設定を扱う。
- `cmoc oracle review` の所見レビュー用 agent call 定義と Structured Output schema をまとめるディレクトリ。所見列挙、採否判定、理由検証、重複・矛盾整理の入口となる。

## Read this when
- `cmoc oracle edit` の TUI 起動方法、編集 prompt、モデル・権限・作業ディレクトリなどの起動設定を確認または変更するとき。
- `cmoc oracle investigation` の TUI 起動処理、完全プロンプトの構築・保存、モデルやアクセス権限の固定値を確認または変更するとき。
- `cmoc oracle review` の所見処理、agent call の prompt・読み取り権限・モデル設定、Structured Output schema、入力出力形式や重複排除条件を確認または変更するとき。

## Do not read this when
- oracle file の編集処理そのもの、prompt 共通生成規則、パス解決、構造化文書のレンダリングを確認または変更するとき。
- 調査用プロンプトの本文構成や共通プロンプト生成規則だけを確認したいとき。
- 通常の ACP builder 実装、oracle review 以外の prompt 構築、または個別に確認できるレビュー schema・実装だけを調べるとき。

## hash
- f6e74f11290a047cc12858dce98edb4f93c2c87eecc564ab03e1d39058ceb23c

# `realization`

## Summary
- Oracle 側の差分を realization file 全体へ反映する `codex exec` 用 AgentCallParameter を構築する処理を扱う。raw git diff、commit 範囲、実行設定、linked worktree を prompt に組み込む `apply` 領域への入口。
- realization refactor fork の変更要約およびファイル単位レビュー・修正用の prompt 構築処理と Structured Output schema を扱う。差分要約、レビュー対象の調査・修正・検証へ進む `refactor` 領域への入口。

## Read this when
- `cmoc realization apply fork` の実行 prompt、モデルや推論強度、ファイルアクセス、作業ディレクトリ、indexing preflight を変更・調査するとき。
- realization refactor fork の変更要約 agent call、またはファイル単位レビュー・修正 agent call の入力、設定、対象パス、検証要件を確認するとき。

## Do not read this when
- 通常の realization 実装・テストを変更または調査するとき。
- prompt の一般的な組み立て規則だけを確認したいとき。
- refactor fork の差分内容、候補ファイルの処理順、レビュー対象ファイルの実装詳細を確認したいとき。
- 変更要約またはレビュー・修正の Structured Output schema の詳細だけを確認したいとき。対応する JSON schema を直接読む。

## hash
- 842a1a8ab6566485c410c86e186af84ac17370ed791c40275008f6a3e23ab998

# `session`

## Summary
- `cmoc session join` の merge conflict 解消に向けて、AI 呼び出しへ渡す入力条件・指示内容・実行設定を組み立てる入口。競合ファイルの正規化と、conflict 解消に必要な範囲の制御が中心。

## Read this when
- `cmoc session join` で merge conflict marker を解消する呼び出し条件や、AI に渡す指示内容・実行設定を確認したいとき。
- 競合ファイルの扱いを変えたいとき、または conflict 解消時に許される編集範囲や品質設定の根拠を確認したいとき。

## Do not read this when
- session join の通常の接続や同期処理を探しているときは、join 本体の実装や周辺の session モジュールを先に読む。
- merge conflict 解消の実行結果そのものや後段の適用処理を知りたいときは、このパラメータ生成ではなく、呼び出し先の実行経路を読む。

## hash
- bf40a25ab5021c33ab48527dccecbcbea01a82485dd3232f13b96888e803c66f

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
- a86f9ff19eac21b319181b860b34bd22e570ac9a8657ea960a23507e32f83db6
