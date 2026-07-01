# `enumerate_finding.json`

## Summary
- oracle file レビュー結果の Structured Output schema を定義する JSON Schema。レビュー対象 oracle file と関連 oracle file から、既知所見と重複しない新規所見だけを `findings` 配列として返す形式を固定する。

## Read this when
- oracle file レビューの出力形式、必須項目、許容される重大度を確認したいとき。
- 新規所見が無い場合の表現や、所見ごとに必要な根拠情報を確認したいとき。

## Do not read this when
- INDEX.md 用エントリーの生成形式を確認したいだけのとき。
- レビュー所見そのものの判断基準や、特定 oracle file の内容を確認したいとき。

## hash
- d1bd69c75e8d60791cc304f06e103a7efdcc6566dc16c1254b8a92d6fcb38c5d

# `enumerate_finding.py`

## Summary
- `cmoc review oracle` で oracle file をレビューし、新規所見を列挙するための agent call parameter を組み立てる prompt 正本。レビュー対象 oracle file、既知の関連所見、oracle 読み取り専用権限、Structured Output schema を含む完全 prompt の生成条件を扱う。

## Read this when
- `cmoc review oracle` の新規所見列挙で AI エージェントへ渡す role、summary、goal、補助 prompt、placeholder、file access mode、model class、reasoning effort を確認または変更したいとき。
- 既知の関連所見を prompt に含め、新規所見だけを返すレビュー呼び出しの入力構成を確認したいとき。
- oracle review 用 prompt builder がどの oracle standard 群を有効化しているか確認したいとき。

## Do not read this when
- oracle review の所見を保存・表示・集約する処理を調べたいだけのとき。
- `cmoc review oracle` 以外の review サブコマンドや、oracle review 以外の agent call parameter を調べたいとき。
- 実際の oracle file の仕様内容やレビュー基準本文を読みたいとき。

## hash
- c0ba0303bddf30b463e595a94cc6e4b8d1ad8da4611c37d3bb73747ee246fe32

# `judge_finding.json`

## Summary
- レビュー所見を人間へ提示するかどうかを判定するための JSON schema。判定値と、その具体的な採否理由を必須項目として定義する。

## Read this when
- レビュー所見の採否判定を返す出力形式を確認したいとき。
- 人間への要確認項目として提示する判定結果の構造を実装・検証したいとき。
- 判定理由にどの程度の説明責務があるかを確認したいとき。

## Do not read this when
- レビュー対象そのものの検出条件や所見生成ロジックを確認したいとき。
- oracle file と realization file の一般的な責務境界を確認したいとき。
- INDEX.md エントリーの生成規則やルーティング方針を確認したいとき。

## hash
- 260ad5636b98dcbb46dc9ebf3181533f5c550384320219dd6c44661e7ec4e53e

# `judge_finding.py`

## Summary
- `cmoc review oracle` で検出された単一のレビュー所見について、採用側理由と棄却側理由を入力に取り、人間へ提示すべきかを判定する AI agent call parameter を組み立てる oracle src。
- 完全 prompt 生成、純粋 oracle 読み取りモード、効率モデル、中程度 reasoning、対応する Structured Output schema の指定をまとめて扱う。

## Read this when
- `cmoc review oracle` の所見採否判定で、どの role・summary・goal・file access mode・補助 prompt が agent に渡るかを確認したいとき。
- 判定対象所見、所見が妥当である理由、所見が妥当ではない理由が prompt にどう埋め込まれるかを確認したいとき。
- レビュー所見の採否判定用 agent call parameter のモデル種別、reasoning effort、出力 schema 対応を確認または変更したいとき。

## Do not read this when
- `cmoc review oracle` の所見を生成する側、採用側理由や棄却側理由を作る側の prompt を確認したいとき。
- oracle review 全体の基準や、所見採否そのものの判断規則本文を読みたいとき。
- agent call parameter の共通データ構造、path placeholder 解決、完全 prompt 構築処理の実装詳細を調べたいとき。

## hash
- 40c7fd2c40eec83d0287b4c617caa9e274e52845e9cd11d8739bd49e792226ce

# `merge_finding.json`

## Summary
- 入力された所見リストの重複や矛盾を解消するための編集操作リストを表す JSON Schema。削除、単一置換、複数統合の操作と、編集後所見に必要な重大度・見出し・根拠 oracle file・理由を規定する。

## Read this when
- 所見リストを整理する処理の出力形式を確認したいとき。
- 所見の削除、置換、統合を JSON で表す必要があるとき。
- 編集後の所見に含める重大度、見出し、根拠 oracle file、整理理由の制約を確認したいとき。

## Do not read this when
- 個別の oracle file の内容や所見の正しさを確認したいとき。
- 所見の重複や矛盾を判定する実装ロジックを調べたいとき。
- ルーティング文書や INDEX.md エントリーの作成規則を確認したいとき。

## hash
- ef00100875ad3a93bd012fc2fe2f8dceb892a60020b8f202a80594e2426a60c0

# `merge_finding.py`

## Summary
- `cmoc review oracle` で得られた oracle file レビュー所見リストを整理するための agent call parameter を構築する。入力所見を prompt に埋め込み、重複・矛盾を解消する編集操作列挙を Structured Output として求める呼び出し設定を定義する。

## Read this when
- oracle file レビュー所見のマージ・整理用 prompt の目的、入力、期待出力を確認したいとき。
- `cmoc review oracle` の所見リスト統合処理で、AI エージェントに渡す role、goal、file access mode、placeholder、標準文脈の組み立てを確認したいとき。
- レビュー所見の重複・相互矛盾を解消するための agent call parameter 生成箇所を変更したいとき。

## Do not read this when
- oracle file 本体のレビュー基準そのものを確認したいだけのとき。
- 所見リストを生成するレビュー実行側の処理や、マージ結果の適用処理を調べたいとき。
- 汎用的な prompt 構築処理、agent call parameter の共通データ構造、または path placeholder 解決の詳細を確認したいとき。

## hash
- 121f1c8d5a7d7310ce88be0c545eb6c131ea0f58f23aa5db12331d2576bda0d9

# `validate_finding_advocate.json`

## Summary
- 対象所見が妥当といえる根拠を、oracle file の記述に基づいて返すための出力契約を定める。
- 既知理由と重複しない新規理由だけを扱い、該当する根拠がない場合は理由なしとして表現する。

## Read this when
- oracle file を根拠に、対象所見を支持できる新規理由を返す処理の出力条件を確認したいとき。
- 対象所見の妥当性を説明する理由が、推測ではなく oracle file の記述に基づく必要があるとき。
- 既知理由との重複を除外し、追加で返すべき理由がない場合の扱いを確認したいとき。

## Do not read this when
- 対象所見そのものを検出する基準やレビュー手順を確認したいとき。
- oracle file 以外の根拠を含めた一般的な説明や改善提案の出力仕様を確認したいとき。
- Structured Output の機械的な項目名や型だけを確認したいとき。

## hash
- f265bb48178831b146ee5d071395ff0dd9dfb6bb509f2d062fa54e3243f4cb4e

# `validate_finding_advocate.py`

## Summary
- `cmoc review oracle` で検出されたレビュー所見について、その所見が妥当である理由を追加調査する AI エージェント呼び出しパラメータを構築する。
- 対象所見、既知の擁護理由、既知の反証理由を補助入力として prompt に埋め込み、oracle file のみを根拠に新規の擁護理由を Structured Output で返すよう指示する。

## Read this when
- `cmoc review oracle` の所見検証で、所見を擁護する側の agent call parameter の構築内容を確認したいとき。
- 既知理由との重複を避けて新規の妥当理由だけを列挙させる prompt 条件を確認したいとき。
- oracle file だけを根拠にし、不確実な推測を理由から除外するレビュー所見検証の入力制約を確認したいとき。

## Do not read this when
- レビュー所見が妥当ではない理由を調査する challenger 側の prompt を確認したいとき。
- `cmoc review oracle` 以外のサブコマンド用 agent call parameter を確認したいとき。
- Structured Output schema 自体の定義や、その JSON ファイルの内容を確認したいとき。

## hash
- 51d5566db5aec3c28a53aadf595bd5c5c24b0fec1d5c6a2cd3186fea3a2646bf

# `validate_finding_challenger.json`

## Summary
- レビュー対象の所見に対して、妥当ではないと言える新規理由を返すための Structured Output schema。理由は oracle file の記述に基づく具体的根拠に限定し、既知理由と重複するものがない場合は空配列で表す。

## Read this when
- レビュー所見への異議申し立て結果を、どのような構造で返すべきか確認したいとき。
- 対象所見が妥当ではない理由を、oracle file に基づく根拠として出力する制約を確認したいとき。
- 既知理由と重複しない新規理由がない場合の返し方を確認したいとき。

## Do not read this when
- レビュー所見そのものの検証手順や判定ロジックを知りたいとき。
- oracle file の内容や、所見が妥当かどうかの判断材料を探しているとき。
- Structured Output schema ではなく、人間向けのレビュー文面や説明文を確認したいとき。

## hash
- a90232c11fe6071e9aaf6200efe525e546aef4775f06fb11cc71018c28f1d214

# `validate_finding_challenger.py`

## Summary
- `cmoc review oracle` で検出されたレビュー所見について、妥当ではない理由を追加調査する agent call parameter を構築する。
- 対象所見、既知の肯定理由、既知の否定理由を prompt に埋め込み、oracle file だけを根拠に新規の否定理由を列挙させるための呼び出し設定を定義する。

## Read this when
- `cmoc review oracle` の所見検証フローで、対象所見への反証・否定理由を列挙する agent 呼び出しの prompt 内容や実行条件を確認したいとき。
- 既知理由との重複排除、oracle file に基づく根拠要求、新規理由が無い場合の扱いを確認したいとき。
- レビュー所見の challenger 側 agent call parameter の model class、reasoning effort、file access mode、出力 schema 参照先を確認したいとき。

## Do not read this when
- レビュー所見が妥当である理由を列挙する advocate 側の prompt を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、oracle review 以外の agent call parameter を調べたいとき。
- prompt 構築共通処理、構造化 markdown rendering、path placeholder 解決そのものの実装を確認したいとき。

## hash
- 16c35263efbf43d122010deeb0ebd707263b51dbe28cad39611624cf3a462b96
