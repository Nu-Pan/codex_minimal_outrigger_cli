# `enumerate_finding.json`

## Summary
- 対象 JSON は、レビューで見つかった新規所見を構造化して返すための出力スキーマです。所見ごとに重大度、短い見出し、主な根拠となる oracle file、理由を保持します。

## Read this when
- oracle file のレビュー結果を新規所見として列挙するとき。
- 所見の重大度や根拠ファイル、既知の所見との差分を確認するとき。

## Do not read this when
- レビュー所見を扱わない通常の ACP builder 実装を読むとき。
- INDEX.md のルーティング情報だけを確認するとき。

## hash
- bf1beeb7e863efdb9f38a22902dbccae13ddd76b070e8492eeb4dd1e929aa085

# `enumerate_finding.py`

## Summary
- `cmoc oracle review`で新規所見を列挙するAIエージェント呼び出しパラメータを構築する。レビュー対象oracle file、関連所見、読み取り権限、モデル設定、生成prompt、Structured Output schemaをまとめて返す処理の入口。

## Read this when
- `cmoc oracle review`の新規所見列挙処理、レビューpromptの構築、関連所見との重複排除条件、AIエージェント呼び出し設定を変更・確認するとき。

## Do not read this when
- レビュー結果のschema定義だけを確認したいとき。
- oracle review以外のprompt構築や、実際のoracle file内容のレビュー規則を確認したいとき。

## hash
- 0a42b17a25fa31ba7ffb756a394cfc4104a8374e92a59f7df884e987db116293

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
- `cmoc oracle review` の所見採否判定用エージェント呼び出しパラメータを構築する。所見、賛成理由、反対理由を正本レビュー基準付きプロンプトへ組み込み、判定結果の Structured Output schema と実行条件を指定する。

## Read this when
- `cmoc oracle review` の所見採否判定プロンプトや、そのエージェント呼び出しパラメータを変更・確認するとき。
- 所見・賛成理由・反対理由を入力とする判定処理の呼び出し条件を確認するとき。

## Do not read this when
- 所見採否判定以外のプロンプト生成や、一般的なレビュー基準そのものを確認するとき。
- 実際の判定結果の schema 定義や、別サブコマンドの実装を直接確認すべきとき。

## hash
- 913b95041e7fa55c632c0f595b3511052af3f93a5c42df8d055bffdeec33a0b6

# `merge_finding.json`

## Summary
- 対象 JSON Schema は、入力所見リストの重複・矛盾を整理する編集操作を表す。各操作は delete・replace・merge のいずれかで、対象 finding_id と、削除時の null または編集後所見を指定する。

## Read this when
- 所見の重複や矛盾を解消するための編集操作形式を確認するとき。
- finding の重大度、タイトル、根拠 oracle file、整理理由の構造を確認するとき。

## Do not read this when
- 個別の所見内容やレビュー判定の基準だけを確認したいとき。
- この JSON Schema を実装・検証するコードを直接確認したいとき。

## hash
- 0966bfdbee83e16727ad5010f02f8010e46f6ea9121624f7093757678ed500eb

# `merge_finding.py`

## Summary
- `cmoc oracle review` における所見リストマージ用の AI エージェント呼び出しパラメータを構築する。入力所見を埋め込んだレビュー整理プロンプトを生成し、oracle の読み取り専用設定・モデル設定・Structured Output schema を指定して返す。

## Read this when
- `cmoc oracle review` の所見リストの重複排除・矛盾解消・編集操作列挙に関する prompt 構築を変更または確認するとき。

## Do not read this when
- 所見マージ処理そのものや Structured Output schema の定義だけを変更するとき。
- `cmoc oracle review` の別用途の prompt、一般的な agent 呼び出し設定、oracle file のレビュー規則を直接確認するとき。

## hash
- b71a9c4ef83fb165cdeea6aba98c4636c980b12e9359fd5d7bcb8f5ee48c76cf

# `validate_finding_advocate.json`

## Summary
- 対象 JSON は review 用 oracle src で、validate_finding_advocate の入力・出力契約を定義する。

## Read this when
- review finding の advocate 検証処理の入出力契約を確認するとき。

## Do not read this when
- review finding の advocate 検証処理以外を扱うとき。

## hash
- 229fedb31871f51de412eb7dd3a7026bc34829344851b2bc81dc8231b250e296

# `validate_finding_advocate.py`

## Summary
- `cmoc oracle review` における、レビュー所見が妥当である理由を列挙する AI エージェント呼び出しパラメータの正本実装。所見、既知の擁護理由・反論理由をプロンプトへ組み込み、oracle file を根拠とする新規理由のみを返すよう指定する。関連する JSON スキーマと対になる実装入口。

## Read this when
- `cmoc oracle review` の所見擁護理由列挙処理を変更・検証するとき
- 擁護担当エージェントの役割、入力情報、oracle 限定のファイルアクセス、重複理由の除外条件を確認するとき
- この処理が生成するエージェント呼び出しパラメータやプロンプト構築を追跡するとき

## Do not read this when
- 所見が妥当でない理由の列挙処理を調べるとき
- レビューサブコマンド全体の実行フローや、プロンプト以外のレビュー処理を調べるとき
- 既存のエージェント呼び出しパラメータを実行・送信する処理だけを確認するとき

## hash
- efd0a7bf36eba36df8d17c5b5c30028cf9c546952e43f80ecffb0ceee6bc5026

# `validate_finding_challenger.json`

## Summary
- 対象所見が妥当ではない新規理由を返すための JSON Schema を定義している。理由がない場合は空配列を許容する。
- `reasons` は必須かつ追加プロパティを認めないため、出力形式が明確に制約されている。

## Read this when
- 対象所見に対する反証理由の出力形式を確認するとき
- レビュー用 Structured Output の schema を確認するとき

## Do not read this when
- 妥当性の判定基準そのものを確認したいとき
- レビュー処理のプロンプト生成実装を確認したいとき

## hash
- dfeec2f83fac0acf4622e1f9286a65c266d11d3943bcbf685448b58b9ce245bc

# `validate_finding_challenger.py`

## Summary
- `cmoc oracle review` で所見の否定理由を列挙するための agent call パラメータを構築する。所見、既知の賛成理由、既知の反対理由を prompt に埋め込み、oracle file のみを根拠に新規の反証理由を返す呼び出し設定を定義している。

## Read this when
- `cmoc oracle review` の所見妥当性検証における、否定理由列挙 prompt や agent call 設定を変更・確認するとき。
- 所見・既知理由の prompt 埋め込み、oracle-only のファイルアクセス、モデル設定、出力 schema の関連を調査するとき。

## Do not read this when
- `cmoc oracle review` の別のレビュー処理や、所見の妥当性を支持する理由を扱う実装を直接調査するとき。
- 一般的な prompt 構築処理やパス解決処理だけを確認する場合は、それぞれの共通実装を直接読むこと。

## hash
- f61b1918c3446a55f3aa139ced9c760c289ad943eec90ad8e546bc5f72476637
