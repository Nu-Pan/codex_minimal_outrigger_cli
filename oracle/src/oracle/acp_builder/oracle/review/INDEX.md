# `enumerate_finding.json`

## Summary
- 対象スキーマと関連する oracle review 仕様を確認しました。明白な論理矛盾や実装不能な制約は見つかりませんでした。

## Read this when
- oracle review の所見列挙出力を扱うとき。

## Do not read this when
- 所見列挙以外の oracle review 処理を確認するとき。

## hash
- 3c851fade3f048b47c7dec3c065395d99fbadaea6bda723c7ae63ba3b9020225

# `enumerate_finding.py`

## Summary
- `cmoc oracle review` における新規所見列挙用のエージェント呼び出しパラメータを構築する正本。レビュー対象 oracle file、関連所見、oracle ツリーのパス、プロンプト、モデル・アクセス設定、Structured Output schema を組み立てる。

## Read this when
- `cmoc oracle review` の新規所見列挙処理を変更・調査するとき
- レビュー用 prompt の役割、対象範囲、既知所見との重複排除条件、実行パラメータを確認するとき
- oracle review 用 Structured Output schema や prompt builder との接続を追うとき

## Do not read this when
- 所見の内容や oracle file の仕様レビュー基準だけを確認したいときは、レビュー対象の oracle file やレビュー基準の正本を直接読む
- 新規所見列挙以外の `cmoc oracle review` 処理を調査するときは、該当する実装・prompt 定義を直接読む
- 一般的な agent call パラメータやパス解決の共通仕様だけを確認したいときは、参照先の共通モジュールを直接読む

## hash
- d36c0d49839198aeee9af491179040c8b9899879cda2c1d7530414e1aef60013

# `judge_finding.json`

## Summary
- 対象は `verdict` と `reason` を必須とする判定結果用 JSON Schema です。

## Read this when
- 対象の判定結果形式を確認するとき。

## Do not read this when
- 判定対象の所見そのものを確認するとき。

## hash
- a024022fc7378f92b7df63be281522661d57e9b773f1d51db649dbcb5b673512

# `judge_finding.py`

## Summary
- `cmoc oracle review` における所見採否判定用の AI エージェント呼び出しパラメータを構築する。所見、妥当性を支持する理由、反対理由をプロンプトへ組み込み、oracle 読み取り専用の実行条件、モデル・推論設定、構造化出力 schema、作業ディレクトリを指定する。

## Read this when
- `cmoc oracle review` の所見採否判定プロンプトの生成内容や agent call パラメータを確認・変更するとき
- 所見・賛成理由・反対理由のプロンプトへの渡し方を確認するとき
- oracle review 用の実行権限、モデル設定、構造化出力 schema の指定を確認するとき

## Do not read this when
- 所見採否判定の出力 schema 自体を確認したいときは、対応する JSON schema を直接読む
- レビュー所見の判定ロジックや oracle review サブコマンド全体の処理を確認したいときは、それぞれの実装・仕様ファイルを直接読む
- 一般的な prompt 構築や agent call の共通仕様だけを確認したいときは、共通 builder・型定義を直接読む

## hash
- 880f80ca17cd50ea96674b8e02121af0666fda838048fa191bce18ec20d4a311

# `merge_finding.json`

## Summary
- 所見リストの重複・矛盾を整理する編集操作を定義する JSON Schema。delete、replace、merge の操作形式と所見フィールドを検証する。

## Read this when
- 所見統合処理の入力・出力契約や、編集操作の JSON 構造を確認するとき。

## Do not read this when
- 個別の所見内容や、実際の統合ロジックの実装を確認したいとき。

## hash
- dbeea7c7b9bbc2c9552e7b69100001b19434ca89d296c5ea9615247b74b1546a

# `merge_finding.py`

## Summary
- `cmoc oracle review` で oracle file のレビュー所見リストをマージするための AI エージェント呼び出しパラメータを構築する。所見データをプロンプトへ埋め込み、oracle-only のアクセス制約と編集操作列挙用スキーマを設定する実装。

## Read this when
- `cmoc oracle review` の所見マージ処理を変更・調査するとき
- 所見リストを入力にした prompt 構築、agent call のモデル・権限・実行ディレクトリ設定を確認するとき
- 所見マージ用 Structured Output schema の参照元を確認するとき

## Do not read this when
- レビュー所見の内容や重複・矛盾の判定基準そのものを確認したいときは、所見マージ prompt の正本ではなくレビュー標準を読む
- `cmoc oracle review` のマージ結果を実際に適用する処理を調査するときは、agent call parameter の構築処理ではなく実行・編集側の実装を読む
- 一般的な prompt 構築や共通の agent call 設定を調査するときは、専用の共通 builder 実装を直接読む

## hash
- 6a03fe9ccb4cc5a19525e8cefbf5ff55df017aaf78939366c4474cf009c0f3ab

# `validate_finding_advocate.json`

## Summary
- 対象 JSON は、レビュー所見の妥当性を支持する新規理由を `reasons` 配列で返すための Structured Output schema を定義する。追加プロパティは禁止され、`reasons` は必須である。

## Read this when
- レビュー所見の妥当性を支持する理由を構造化出力として生成・検証するとき。

## Do not read this when
- レビュー所見の内容や妥当性判定ロジックを確認するとき。出力形式ではなく、関連するプロンプトまたは検証処理を直接読む。

## hash
- e375c55fcdef28f2b23f82065da03126e8885307b7b63ab505cb428574c5c73f

# `validate_finding_advocate.py`

## Summary
- `cmoc oracle review`でレビュー所見が妥当である理由を調査するAIエージェント呼び出しパラメータを構築する。対象所見、既知の擁護理由・反論理由をプロンプトへ渡し、重複しない新規理由のStructured Output生成を指定する。

## Read this when
- `cmoc oracle review`の所見擁護処理、またはそのプロンプト・エージェント呼び出し設定を変更・調査するとき。
- 所見、既知の理由、Oracle読み取り専用アクセス、構造化出力スキーマの受け渡しを確認するとき。

## Do not read this when
- 所見が妥当ではない理由の列挙処理を確認する場合。
- レビュー機能の一般的な実装や、対象ファイルが呼び出す共通プロンプト構築処理だけを確認する場合は、対応する直接の実装・仕様へ進む。

## hash
- 0b8e03af59bebba76cf4040569d32542b3c13554989c09530d3d3c096fced082

# `validate_finding_challenger.json`

## Summary
- 対象所見が妥当ではない新規理由は確認できません。

## Read this when
- 対象所見に対する妥当性検証結果の理由を扱う出力形式を確認するとき。

## Do not read this when
- 対象所見の内容そのものや、既知理由の定義を確認するとき。

## hash
- d784259c47bd99b2599523de5d28145bb4bfffd252b7f4d2042a1ed553270c85

# `validate_finding_challenger.py`

## Summary
- `cmoc oracle review` における、レビュー所見が妥当ではない理由を列挙する agent call パラメータ生成の正本。対象所見と既知の賛成・反対理由をプロンプトへ組み込み、oracle-only 読み取り、モデル設定、構造化出力 schema、作業ディレクトリを指定する。

## Read this when
- `cmoc oracle review` の所見反証・否定理由列挙の prompt 構築を変更または確認するとき
- finding、既知の妥当理由、既知の不妥当理由の入力方法や、重複しない新規理由を求める prompt を確認するとき
- この agent call のモデル、アクセスモード、構造化出力、パス解決などの実行パラメータを確認するとき

## Do not read this when
- レビュー所見そのものの判定ロジックや oracle review の別段階を変更・確認するときは、対応する別の prompt builder またはサブコマンド実装を直接読む
- 構造化出力の項目定義だけを確認するときは、対応する JSON schema を直接読む
- 共通 prompt の組み立て規則や agent call 型定義だけを確認するときは、参照先の共通 builder・型定義を直接読む

## hash
- dbbcb59fb9d8baa2656e6e8623a2e154df3fb41e10433d9f03a4597653636451
