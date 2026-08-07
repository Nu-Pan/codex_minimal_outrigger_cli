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
- AI コーディングエージェント呼び出し用の論理パラメータを定義する oracle src。モデルクラス、推論強度、ファイルアクセスモードの列挙と、プロンプト・cwd・Structured Output 設定・indexing preflight 指定をまとめる不変データ構造を扱う。

## Read this when
- Agent call のパラメータ項目、モデル選択区分、推論強度、ファイルアクセスモード、indexing preflight の既定動作を確認するとき。
- Agent call parameter を生成・検証する実装の正本定義を確認するとき。

## Do not read this when
- 具体的な agent call builder の生成ロジックや prompt 構築規則を確認したいとき。
- Codex CLI sandbox や permission profile の詳細なアクセス規則を確認したいとき。

## hash
- 1c637587b1fc7c500c21c3ac412fbb9d47bb80714478ba0421882b003f8a53d8

# `feedback`

## Summary
- feedback observation を既存 issue への統合または新規 issue 作成へ正規化するための Structured Output schema と prompt builder 実装を扱う。観測結果、既存 issue 候補、原因・影響・対応候補・存在可能性の評価を入力から整理し、feedback 正規化処理の出力契約と AgentCallParameter 構築の入口を提供する。

## Read this when
- feedback observation から issue の統合または新規作成を判断する出力契約を確認するとき。
- 正規化 prompt の参照範囲、読み取り専用制約、モデル設定、推論強度、Structured Output schema の対応を確認するとき。

## Do not read this when
- feedback issue の保存・取得や human disposition の決定だけを調べるとき。
- raw Codex call log、feedback observation の保存形式、または別の prompt builder の実装を直接調べるとき。

## hash
- 7aa0e70e501d38db3db0a1f193884c2dd6184ef9f9185b0c83b0da4278d24337

# `indexing`

## Summary
- `cmoc indexing` における INDEX.md エントリー生成用の agent call パラメータを構築する実装を収める。対象内容を含む prompt、読み取り専用アクセス、モデル・推論設定、Structured Output schema の参照、実行コンテキストを定義する。
- indexing 用の prompt 構築と agent call 設定を確認する際の入口であり、出力形式の詳細は同階層の schema 定義から確認できる。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 prompt を変更・調査するとき。
- indexing 用 agent call のモデル、推論強度、ファイルアクセス権限、実行コンテキスト、Structured Output schema の指定元を確認するとき。

## Do not read this when
- 実際の INDEX.md 生成処理や indexing サブコマンド全体の実行フローを調査するときは、呼び出し側や実行フローの対象を直接読む。
- Structured Output の JSON Schema 自体の定義だけを確認するときは、schema 定義を直接読む。
- 一般的な prompt 構築処理や indexing 以外の agent call 種別を調査するときは、共通 prompt 実装や該当する agent call の対象を直接読む。

## hash
- 1dd8a883f7a42a61b5eaa5537221aa9a875de4ea75f11bfb6003d148a04f9317

# `oracle`

## Summary
- oracle の編集・調査・レビューに関する agent call パラメータ構築を担う領域です。編集・調査では固定プロンプト、oracle 専用アクセス制御、モデル設定、作業ディレクトリ、完全プロンプトの管理ログ保存を扱い、レビューでは所見の列挙・採否判定・重複整理・擁護理由・反証理由の Structured Output 契約と起動パラメータを扱います。各サブディレクトリが個別フローの実装と出力スキーマへの入口です。

## Read this when
- oracle file の編集または調査 TUI の起動条件、完全プロンプト、アクセスモード、モデル・推論設定、ログ保存を確認・変更するとき。
- oracle review の所見列挙、採否判定、所見リストの統合、擁護理由または反証理由の生成処理や Structured Output 契約を確認・変更するとき。

## Do not read this when
- 共通の完全プロンプト構築処理、AgentCallParameter の型定義、パスコンテキストやファイルアクセスモードの一般仕様を確認するとき。
- oracle file の編集・調査・レビューにおける正本仕様や判定基準そのものを確認するとき。
- この領域以外の realization 側 CLI・TUI 実装や、対象外の oracle サブコマンドを調査するとき。

## hash
- 0313b08739217e98c3c00180fa69ba2d52449a8b52183526e009c0ff2e37986e

# `realization`

## Summary
- `cmoc realization apply fork` の追従処理に向けた起動パラメータと codex exec 用プロンプトを構築する実装入口です。oracle file の差分、対象コミット範囲、linked worktree、実行モデル・推論設定・ファイルアクセス権限の対応を扱い、apply fork の prompt 構築を調べる際の入口になります。
- refactor fork の変更差分要約、およびファイル単位の実装レビュー・修正・検証に向けた AgentCallParameter と prompt を構築します。Structured Output の契約、変更 path、モデル・権限・作業ディレクトリ設定を扱い、refactor fork の prompt や出力契約を確認・変更する際の入口になります。

## Read this when
- `cmoc realization apply fork` の追従用 AgentCallParameter や codex exec prompt の構築方法を確認するとき
- apply fork で oracle file の差分、対象コミット範囲、linked worktree、実行条件がどのように prompt へ組み込まれるか調べるとき
- refactor fork の変更差分要約、ファイルレビュー、修正、検証の prompt または AgentCallParameter を確認・変更するとき
- refactor fork の Structured Output の項目や対応条件、モデル・権限・作業ディレクトリ設定を確認するとき

## Do not read this when
- `cmoc realization apply fork` 以外の prompt 構築を調べるときは、各用途に対応する prompt builder を直接確認してください
- 実際にレビューされる個別の oracle file や realization file の内容を調査するときは、対象ファイルを直接確認してください
- 通常の realization 実装・テストの挙動を確認するときは、対応する realization implementation または realization test を直接確認してください
- refactor fork を呼び出す上位の運用を調査するときは、上位の prompt builder を直接確認してください

## hash
- 0362bbd63b78a44f0eee34b5486855e6967264eff4548b0f49bc3d9a71957335

# `session`

## Summary
- `cmoc session join` の Git merge conflict marker 解消用 agent call パラメータを構築する実装を含む。競合対象ファイルの実パス解決、専用 prompt の生成、リポジトリ書き込み権限、最高品質のモデル・推論設定、事前 indexing 無効化をまとめて指定する下位実装への入口。

## Read this when
- `cmoc session join` の conflict marker 解消用 agent call 設定や prompt を変更・確認するとき。
- 競合対象パスの解決、モデル・推論設定、ファイルアクセス権限、agent call の作業ディレクトリ、実行前 indexing 設定を調査するとき。

## Do not read this when
- 通常の merge conflict 解消処理や Git 操作そのものを調査するとき。
- `session join` と無関係な prompt builder や agent call パラメータを調査するとき。

## hash
- 4052f74c94d2c7069dec6d6443a4de00cec4703a801960b6880c8b8fdedd9aec

# `tui`

## Summary
- `cmoc tui` の起動パラメータ構築を担う実装を収録する。完全な作業プロンプトの生成・保存と、モデル、推論、作業ディレクトリ、リポジトリ書き込み権限などの固定起動条件を確認する入口である。

## Read this when
- `cmoc tui` の起動条件、プロンプト保存先、AI Agent CLI/TUI への指示の渡し方を変更・確認するとき。

## Do not read this when
- TUI 以外のサブコマンドの起動パラメータを扱うとき。
- 完全なプロンプトの生成規則、パス解決、構造化ドキュメントの仕様だけを確認するとき。

## hash
- b37860f69cbc472d960270b0ef95baf7b266f61e4672aad3328d9302e1196061
