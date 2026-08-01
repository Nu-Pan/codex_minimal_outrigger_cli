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
- `cmoc oracle review` で新規所見を列挙する agent call パラメータを構築する oracle prompt 実装。レビュー対象 oracle file、関連所見、oracle ツリーの参照範囲、Structured Output schema、モデル・アクセスモード・作業ディレクトリを組み立てて返す。

## Read this when
- `cmoc oracle review` の新規所見列挙 prompt の内容、agent call 設定、関連所見の受け渡し、または Structured Output schema の指定を変更・確認するとき。
- oracle review 用 agent call のパスコンテキスト、oracle-only 読み取り制約、モデル設定、indexing preflight の構成を確認するとき。

## Do not read this when
- レビュー所見の判定基準そのものを確認したいときは、oracle review の標準仕様を直接読む。
- 新規所見の Structured Output schema の詳細だけを確認する場合は、対応する schema ファイルを直接読む。
- 一般的な prompt 生成処理や共通の agent call 型定義を確認する場合は、このファイルではなく参照先の共通実装を読む。

## hash
- 148e9d0f73ea582f8b50bb5714b38b80b18c6fd0b00c1cb97dc2bab5b7e4cba0

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
- `cmoc oracle review` における所見採否判定用の AI エージェント呼び出しパラメータを構築する。所見、賛成理由、反対理由をプロンプトへ組み込み、oracle-only 読み取り、モデル設定、構造化出力スキーマ、作業ディレクトリなどを指定する。

## Read this when
- `cmoc oracle review` の所見採否判定プロンプトやエージェント呼び出し設定を変更・調査するとき。
- 所見・賛成理由・反対理由を受け取る判定パラメータ構築処理を確認するとき。

## Do not read this when
- `cmoc oracle review` の判定結果スキーマ自体を確認したいときは、対応する JSON スキーマを直接読む。
- 一般的なプロンプト生成処理やパス解決処理の仕様を確認したいときは、それぞれの共通モジュールを直接読む。

## hash
- d2415c2c6ab61638fb0830b3ad7b591c3b42289d23e1637ccb744cfa4af791e1

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
- `cmoc oracle review` で、oracle file のレビュー所見リストを整理する agent call パラメータを構築する。
- 入力所見をプロンプトへ渡し、所見の重複・矛盾を解消する編集操作の Structured Output を要求する。
- oracle の読み取り専用アクセス、main worktree の cwd、効率重視モデル、最大推論、対応する schema を設定する。

## Read this when
- `cmoc oracle review` の所見マージ処理や、その agent call 用 prompt の生成を変更・調査するとき。
- 所見リストを Structured Output として整理する仕様や、oracle 専用の agent call 設定を確認するとき。
- 同じディレクトリにある所見マージ用 Structured Output schema と実装の対応を確認するとき。

## Do not read this when
- oracle review 以外のサブコマンドの prompt 構築を調べるとき。
- 所見の内容そのものやレビュー判定ロジックを調べるとき。
- 一般的な agent call の型、モデル、アクセスモードの定義を確認するだけのときは、共通定義側を直接読む。

## hash
- d071297966a428b9e28ac26c62c66f255112366b3a98018dd4e7c9f22fc54442

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
- `cmoc oracle review` でレビュー所見が妥当である理由を列挙するための AI エージェント呼び出しパラメータを構築する。所見・既知の賛成理由・反対理由をプロンプトへ渡し、oracle file を根拠とする新規理由のみを Structured Output で返す処理への入口。

## Read this when
- `cmoc oracle review` の所見擁護プロンプト生成や、妥当性理由の Structured Output 呼び出し条件を変更・調査するとき。
- モデル、推論強度、oracle-only のファイルアクセス、パスコンテキスト、補助プロンプト、出力スキーマの設定を確認するとき。

## Do not read this when
- レビュー所見そのものの判定ロジックや、擁護理由を生成した後の処理を調べるとき。
- 他の `cmoc oracle review` 用プロンプトの役割・出力形式だけを確認したいときは、対象の prompt builder や Structured Output schema を直接読む。

## hash
- bf44ab877fbf942ff1af35f5aba4a7ccd7397d7b762bb3d4bb4aee5dd7033114

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
- `cmoc oracle review` における、所見が妥当ではない理由を列挙する agent call パラメータを構築する prompt 正本。対象所見・既知の賛成理由・反証理由を入力として完全な prompt を生成し、oracle file の参照、Structured Output、実行モデル、作業ディレクトリなどの呼び出し条件を定義する。

## Read this when
- `cmoc oracle review` の所見反証 prompt を変更・レビューするとき
- 所見、既知の理由、oracle file 根拠を agent call に渡す構成を確認するとき
- この prompt に対応する Structured Output schema や prompt builder との接続を調査するとき

## Do not read this when
- `cmoc oracle review` の所見が妥当である理由を列挙する prompt を調査するとき
- レビュー所見の判定ロジックや oracle file 自体の内容を調査するとき
- agent call の共通パラメータ定義だけを確認したいときは、共通 builder・型定義を直接読む

## hash
- af44d538d1f4bdfe58adecb64c0d83a967947620185b3bf348a75c9ab702f28e
