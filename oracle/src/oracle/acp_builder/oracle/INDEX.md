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
- oracle review の所見列挙・妥当性検証・採否判定・統合に使う Structured Output schema と agent call パラメータ定義を集約するディレクトリ。各ファイルは、所見の出力形式または対応するレビュー担当の prompt・モデル設定・読み取り制約・Structured Output schema の関連付けを定義する。oracle review の特定処理の入出力契約や起動条件を確認・変更するときの入口であり、レビュー全体の処理ロジックや共通 prompt 生成を調べる場合は配下の対応実装または別の共通処理へ進む。

## Read this when
- oracle review で新規所見を列挙するとき
- レビュー所見の妥当性を支持・反証する理由の出力形式や agent call 設定を確認・変更するとき
- レビュー所見の採否判定や、重複・矛盾を含む所見リストの統合処理を確認・変更するとき

## Do not read this when
- oracle review の対象仕様・実装や個々の所見内容を調査するとき
- oracle review 全体の判定・統合ロジックを確認するとき
- 共通 prompt 生成規則やパス解決など、各処理に固有でない agent call 構築処理を調査するとき

## hash
- fdf23c1f03c875ca5aab02d0b7eaf78a63c54cac82bdfe0915a11189e4bc9d03
