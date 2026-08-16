# `edit`

## Summary
- `cmoc oracle edit` の起動定義を扱うディレクトリで、空の `fork` サブディレクトリと、oracle file 編集向けの本命・仕様削減 agent call の起動パラメータを構築する定義を含みます。oracle edit の起動条件、prompt 構成、アクセス範囲、モデル設定、作業ディレクトリ、索引事前処理を確認する入口です。

## Read this when
- `cmoc oracle edit` の agent call 起動パラメータを変更・レビューするとき
- oracle file 編集用 prompt の構成や、仕様削減時の参照境界を確認するとき
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき

## Do not read this when
- realization 実装の責務や配置を確認する場合
- oracle file の内容や仕様自体を確認・変更する場合
- 通常の agent call 起動処理や `codex exec` 共通設定だけを確認する場合
- 配下の具体的なファイルを直接確認できる場合

## hash
- cce89dd47310bfeac39c8acda72ae098907e8036d70b37d4b4486cc5d0f6fe4b

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータを構築する実装。ユーザーの調査指示を完全プロンプトへ組み込み、oracle-only の読み取り制約、パスコンテキスト、モデル・推論設定、構造化出力設定、起動前処理を含む `AgentCallParameter` を定義する、oracle 調査起動フローの入口。

## Read this when
- `cmoc oracle investigation` の TUI 起動時に、完全プロンプトへのユーザー指示の組み込み方を確認・変更するとき
- oracle 調査用 agent call のモデル、権限、作業ディレクトリ、構造化出力、起動前処理などの固定パラメータを確認・変更するとき
- oracle 調査プロンプトの構築元や、調査・ルーティング・エディタ引き渡しポリシーの適用箇所を追うとき

## Do not read this when
- oracle file の調査内容そのものや正本仕様を確認したいときは、対象の oracle file を直接読む
- 一般的な agent call パラメータの型・列挙値の定義を確認したいときは、`oracle.acp_builder.basic` の定義を読む
- 完全プロンプトの共通生成規則だけを確認したいときは、`oracle.prompt_builder.complete_prompt` の実装を直接読む

## hash
- 6e0088b946d13c9e9e795047a4736a1d9371f641410df22e31e1c72510c55104

# `review`

## Summary
- oracle review の所見処理に関する Structured Output schema と agent call builder をまとめた領域です。新規所見の列挙、所見の妥当性を支持・反証する理由の列挙、所見の採否判定、重複や矛盾の整理を扱います。
- 所見の入出力契約だけでなく、レビュー対象 oracle file の読取範囲、既知情報の重複排除、隔離 review worktree、prompt、実行ポリシー、Structured Output schema を接続する agent call 構築の入口です。

## Read this when
- cmoc oracle review の所見列挙、妥当性検証、採否判定、または所見リスト統合の挙動を確認・変更するとき
- oracle review 用 agent call の prompt、Structured Output schema、oracle file の読取条件、または起動パラメータの接続を調査するとき

## Do not read this when
- oracle review の実行制御、所見の永続化、またはレビュー結果の後処理だけを調査するとき
- 所見の根拠となる個別の oracle file や、共通の agent call・prompt builder の仕様だけを確認するとき

## hash
- 64b1f4b6aabb33eb333325074ed958870157a64c9fb26794ef4d7601da941d0c
