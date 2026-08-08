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
- oracle 向け各サブコマンドの起動関連実装を扱う領域で、`edit`・`investigation`・`review` の個別フローへ進むための入口です。
- oracle 編集、調査、レビューに関する TUI 起動設定、agent call パラメータ、プロンプト保存・構成、Structured Output 契約を対象とします。

## Read this when
- `cmoc oracle edit` の TUI 起動設定や完全 prompt の保存・動的構成を確認または変更するとき。
- `cmoc oracle investigation` の調査プロンプト、起動条件、モデル・アクセスモード、ログ保存を確認または変更するとき。
- `cmoc oracle review` の所見生成・判定・整理・擁護・反証フローや、対応する agent call パラメータと Structured Output 契約を確認または変更するとき。

## Do not read this when
- oracle file の編集内容や realization 側の実装だけを確認する場合。
- prompt の共通構築ロジックや一般的な agent call 基盤だけを確認する場合。
- レビュー所見の内容・妥当性基準そのものを確認する場合。
- 上記以外の `cmoc oracle` サブコマンドを扱う場合。

## hash
- 688845a88fc138077403bb2d1ceb4f464ec7bbcba1e73e01ea73ec8018bd9f42

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
- `cmoc tui` の TUI 起動用 `AgentCallParameter` を構築する実装。オリジナルプロンプトから完全プロンプトを生成して保存し、リポジトリ書き込み権限、作業ディレクトリ、モデル、推論強度、インデックス事前処理などの起動条件を固定する。下位の起動処理を確認するための入口。

## Read this when
- `cmoc tui` の起動パラメータ、完全プロンプトの保存、エディタ入力の埋め込み、TUI 呼び出し時のモデル・推論強度・作業ディレクトリ・アクセスモードを確認または変更するとき。

## Do not read this when
- TUI 以外のサブコマンドや起動方式のパラメータを調べるとき。
- 完全プロンプトの共通構造やレンダリング仕様だけを調べるときは、プロンプト生成側の実装を直接読む。

## hash
- 9b2c3cf92ffd59d90024b24e9c1320332c4d1f24636b15d102c777df6ac56149
