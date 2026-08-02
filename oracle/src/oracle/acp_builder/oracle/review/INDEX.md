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
- `cmoc oracle review` における新規所見列挙用の agent call パラメータを構築する oracle source。レビュー対象 oracle file、関連所見、読み取り専用範囲、完全 prompt、Structured Output schema、実行コンテキストを設定する。

## Read this when
- `cmoc oracle review` の新規所見列挙 prompt や agent call パラメータの生成方法を変更・確認するとき
- レビュー対象ファイルや関連所見を prompt に渡す処理、oracle-only の file access、Structured Output schema の指定を確認するとき

## Do not read this when
- 所見の内容や重複判定のレビュー規則そのものを確認したいとき
- prompt の共通生成仕様だけを確認したいときは、`complete_prompt` などの共通実装を直接読む

## hash
- be22679efc6d383cd746c039b7a3e5d766569ae4e3bb30d1e6fe293052471416

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
- `cmoc oracle review` における所見採否判定用の AI エージェント呼び出しパラメータを構築する実装。所見、支持理由、反対理由を含むプロンプトを生成し、純粋な oracle 読み取り権限と判定結果用 Structured Output schema を指定する。

## Read this when
- `cmoc oracle review` の所見採否判定 prompt、モデル・推論設定、oracle 読み取り権限、または agent call パラメータの構築を変更・調査するとき。

## Do not read this when
- 所見採否判定の Structured Output schema 自体を確認するときは、対応する `.json` schema を直接読む。
- レビュー所見の内容や oracle 仕様の妥当性を確認するときは、この prompt 構築実装ではなく対象の oracle file とレビュー処理を直接読む。

## hash
- 1ed42955b26af142deef76caa9673d14ed9c6a5cc4d057c4010dc83adfa5369b

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
- `cmoc oracle review` における所見リストマージ用の agent call パラメータを構築する。入力所見を prompt に埋め込み、oracle-only の読み取り条件、モデル設定、Structured Output schema などを指定する下位実装への入口。

## Read this when
- `cmoc oracle review` の所見マージ処理、所見整理 prompt、またはその agent call パラメータを変更・調査するとき。

## Do not read this when
- 所見マージ後の編集操作 schema や所見内容の整理ロジックだけを確認したいときは、指定された Structured Output schema や所見処理側を直接読む。
- `cmoc oracle review` と無関係な agent call パラメータや prompt builder を扱うとき。

## hash
- 7179b929717cdb265bfe06c54430d9d8e9c99efef6edfe4b2c0a21fb6b8caf73

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
- `cmoc oracle review` における、レビュー所見が妥当である理由を調査する agent call パラメータを構築する。対象所見と既知の賛成・反対理由をプロンプトへ渡し、重複しない新規理由の列挙を要求する。関連する prompt、パスコンテキスト、アクセスモード、構造化出力設定の組み立てを担う。

## Read this when
- `cmoc oracle review` の所見擁護理由列挙処理を変更・調査するとき
- 所見、既知の理由、Structured Output schema を使った agent call パラメータ生成を確認するとき

## Do not read this when
- 所見が妥当ではない理由の列挙処理だけを確認するとき
- レビュー全体の実行制御や、共通 prompt 構築処理を直接確認するときは、それぞれの担当ファイルを先に読む

## hash
- f6dca65f8a9a5a69abee85b1b0f6fa3587d874fae199cb2541e30bc8fae6e30f

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
- `cmoc oracle review` において、レビュー所見が妥当ではない理由を列挙する agent call パラメータを構築する oracle prompt 実装。対象所見、既知の賛成理由、既知の反対理由をプロンプトへ渡し、重複しない新規理由または空配列を返すよう要求する。

## Read this when
- `cmoc oracle review` の所見反証用 prompt を変更・調査するとき
- レビュー所見の妥当性否定理由を返す Structured Output 呼び出しの構成を確認するとき

## Do not read this when
- `cmoc oracle review` の他の所見判定 prompt を変更するとき
- レビュー実行ロジックや Structured Output schema 本体だけを調査するとき

## hash
- f1e10617ebb16cfad118c34d86e8ee1ff9f985adc26253ad238f96545a1ea728
