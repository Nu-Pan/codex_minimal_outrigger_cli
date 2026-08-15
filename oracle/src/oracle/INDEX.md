# `acp_builder`

## Summary
- AI コーディングエージェント呼び出し用の prompt、Structured Output、モデル、推論強度、ファイルアクセス、作業ディレクトリなどを組み立てる定義を集約する。共通の AgentCallParameter と論理列挙に加え、feedback、indexing、oracle、realization、session、TUI、quota probe の呼び出し定義へ進む入口となる。

## Read this when
- agent call の共通パラメータモデルや論理的なモデル種別、推論強度、ファイルアクセスモードを確認・変更するとき
- 特定の cmoc サブコマンドに対応する prompt、Structured Output、起動条件、実行権限の定義を探すとき
- feedback issue、INDEX.md エントリー生成、oracle 操作、realization、session join、TUI、quota availability probe の agent call 構築実装を調査するとき

## Do not read this when
- 実際の agent call 実行処理や Codex CLI sandbox の正本仕様を確認するとき
- 個別のサブコマンドの業務ロジック、issue 状態、oracle file、realization file の具体的内容を確認するとき
- 共通 prompt builder やパス解決、Structured Output の一般的な実装だけを確認するとき

## hash
- b93052f9b89abf53dbc983debe2ab2434c5bab7f878e01f05cca6471d1c4c702

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- cmoc の oracle 実装における、設定・パスモデル・標準定義・構造化文書生成を扱うモジュール群への入口。設定値や agent call のパス解決、instruction 標準の合成、StructDoc による Markdown レンダリングを調査・変更するときに、該当する下位モジュールへ進むためのルーティング対象。

## Read this when
- cmoc のリポジトリ固有設定、root placeholder と agent call のパスコンテキスト、agent 向け標準、または構造化 Markdown 文書生成の実装入口を探すとき。
- 複数の oracle 共通モデルや文書生成ヘルパーの責務を確認し、該当する下位モジュールを選ぶとき。

## Do not read this when
- 特定の CLI 機能や realization の挙動だけを調査する場合は、その機能の実装・仕様を直接読む。
- 永続化された設定ファイルの同期や doctor の実装、列挙型の定義、標準値の個別利用箇所だけを確認する場合は、それぞれの直接の定義元・利用元へ進む。
- INDEX.md のルーティング情報だけを確認する場合。

## hash
- 018c0fde9b3993302e7a717cde4029175e2f662e0e9d3d77a80f4014c6d39f35

# `prompt_builder`

## Summary
- cmoc の agent call 向け完全プロンプトを構成する実装群。placeholder 型、完全 prompt の合成、エディタ入力の初期文面、用途別 instruction 部品を扱い、prompt builder の構成や注入規則を調査・変更する際の入口となる。

## Read this when
- agent call に渡す prompt の構成、Standard・静的規則・動的内容の組み合わせを調査・変更するとき。
- placeholder の型定義、完全 prompt の合成、エディタ入力テンプレート、用途別 prompt 部品の責務を確認するとき。
- oracle・realization、file access、routing、feedback などの共通 instruction がどの部品から構成されるかを調査するとき。

## Do not read this when
- 個別の oracle file や realization file の本文を確認したいとき。
- 特定の Standard 本文だけを確認したいとき。
- 生成された prompt の利用側や CLI の実際のファイル操作を調査するとき。

## hash
- e823001d82aea6a5b4a381afff55a8d6e70dbcd621809111379384002884f214
