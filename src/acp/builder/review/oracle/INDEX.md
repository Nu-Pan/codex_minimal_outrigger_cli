# `enumerate_finding.json`

## Summary
- oracle レビューで、レビュー対象と関連する正本仕様断片から未登録の所見を列挙するための構造化出力を定義する。
- 所見がない場合も含め、既知の関連所見と重複しない新規所見だけを返す境界を示す。
- 各所見について、重大度、短い見出し、根拠となる正本仕様断片、所見として扱う理由を残すための出力契約を担う。

## Read this when
- oracle レビュー結果として、新規所見をどの粒度で返すべきか確認したいとき。
- 既知の関連所見と重複しない問題だけを報告する出力契約を確認したいとき。
- 正本仕様断片に対する所見の根拠や理由を、レビュー出力へどう含めるか確認したいとき。
- 所見の重大度を、致命的な矛盾・欠落と軽微な曖昧さ・改善余地に分ける基準を確認したいとき。

## Do not read this when
- oracle レビューで実際にどの正本仕様断片を調査するかを探しているだけのとき。
- 所見検出のアルゴリズム、探索順序、既知所見との照合方法などの実装を確認したいとき。
- oracle file や realization file の基本定義、編集責任、配置ルールを確認したいとき。
- INDEX.md エントリーそのものの記述方針やルーティング文書の一般基準を確認したいとき。

## hash
- d1bd69c75e8d60791cc304f06e103a7efdcc6566dc16c1254b8a92d6fcb38c5d

# `enumerate_finding.py`

## Summary
- `cmoc review oracle` で oracle file をレビューし、新規所見を列挙するための AI エージェント呼び出しパラメータを構築する実装。
- レビュー起点となる oracle file と既知の関連所見を受け取り、oracle ツリーの読み取り、重複しない新規所見の列挙、所見なしの場合の空配列返却を求める complete prompt を組み立てる。
- 呼び出しモデル、推論量、ファイルアクセスモード、prompt、対応する構造化出力 schema への参照をまとめたパラメータを返す。

## Read this when
- `cmoc review oracle` のうち、oracle file から新規のレビュー所見を列挙するエージェント呼び出し内容を確認・変更したいとき。
- 既知の関連所見を prompt にどう渡し、新規所見との重複回避をどう指示しているかを確認したいとき。
- oracle file レビュー用 prompt に適用されるファイルアクセスモード、標準 prompt 部品、構造化出力 schema 参照の組み立てを追いたいとき。

## Do not read this when
- レビュー所見の列挙ではなく、所見の保存、表示、集約、実行フロー全体を確認したいとき。
- oracle file 以外の実装レビューや、通常の realization file レビューの prompt 構築を確認したいとき。
- 構造化出力 schema そのものの項目定義や検証規則を確認したいとき。

## hash
- 2e119a092ea4489b8c9c813ed7acc4cdf1208d064d708afaf75192945fd22ef2

# `judge_finding.json`

## Summary
- レビューで得られた対象所見を、人間に要確認項目として提示するかどうかを判定するための出力契約を定める。
- 判定結果だけでなく、所見が妥当と見なせる点と妥当でない点を踏まえた具体的理由を返すことを求める。

## Read this when
- レビュー所見を採用して人間へ提示するか、却下して提示しないかを機械的に受け渡す出力を実装・検証する場合。
- レビュー所見の採否判定を行うプロンプト、ビルダー、レスポンス検証、テストを確認する場合。
- 採否の理由に、妥当性と不妥当性の両面を踏まえた説明が必要かを確認する場合。

## Do not read this when
- レビュー所見そのものの生成条件、検出ルール、重大度分類、表示形式を確認したい場合。
- 人間へ提示された後のレビュー UI、保存形式、集計処理、通知処理を確認したい場合。
- 汎用的な JSON Schema の構文や、他のレビュー用出力契約を調べたい場合。

## hash
- 260ad5636b98dcbb46dc9ebf3181533f5c550384320219dd6c44661e7ec4e53e

# `judge_finding.py`

## Summary
- `cmoc review oracle` の所見採否判定用に、所見本文と賛成・反対理由を入力として AI エージェント呼び出しパラメータを組み立てる実装。
- 判定担当ロール、提示可否の判定目的、純粋 oracle 読み取りモード、レビュー oracle 基準付きの complete prompt、効率向けモデル設定、対応する Structured Output schema への参照をまとめて設定する。

## Read this when
- レビュー oracle が検出した個別所見を人間へ提示するかどうかを判定するプロンプト構築処理を確認・変更したいとき。
- 所見本文、所見が妥当である理由、所見が妥当ではない理由をどのように採否判定エージェントへ渡すかを確認したいとき。
- `cmoc review oracle` の所見採否判定で使う file access mode、モデルクラス、reasoning effort、Structured Output schema の紐付けを確認したいとき。

## Do not read this when
- 所見候補を生成する処理、所見への賛成理由・反対理由を作る処理、またはレビュー対象の oracle file 自体の解析処理を探しているとき。
- 所見採否判定の JSON schema の項目や型を確認したいだけのとき。
- complete prompt の共通構築ロジックや markdown rendering の汎用仕様を確認したいとき。

## hash
- f8769d64f769ab87396c4bd48b4b7bbcbdfaffdb32e6cfcff0c6de828850b943

# `merge_finding.json`

## Summary
- 入力された所見リストについて、重複や矛盾を解消する編集方針を返すための構造を定めるスキーマ。
- 十分に整理済みの所見群は変更なしとして扱い、必要な場合だけ削除・置換・統合によって新しい所見内容へまとめる境界を示す。

## Read this when
- 複数の oracle review 所見を後段で整理し、重複・矛盾・過剰な細分化を解消する出力を生成または検証する。
- 所見を削除する場合と、単一所見を置き換える場合と、複数所見を統合する場合の扱いを揃える必要がある。
- 編集後に残す所見へ重大度、短い見出し、根拠となる oracle file、整理理由を持たせる処理を確認する。

## Do not read this when
- 個別の oracle file から新しい所見そのものを発見する基準を確認したい。
- 整理済み所見の表示順、CLI 表示、保存先、レポート文面など、編集操作の構造以外を扱う。
- oracle file と realization file の基本概念やレビュー対象の選び方を確認したい。

## hash
- ef00100875ad3a93bd012fc2fe2f8dceb892a60020b8f202a80594e2426a60c0

# `merge_finding.py`

## Summary
- `cmoc review oracle` で、oracle file レビューの既存所見リストを整理・マージするための AI 呼び出しパラメータを構築する実装。
- 入力された所見リストを補助プロンプトとして渡し、所見同士の内容的な重複や相互矛盾を解消する編集操作を Structured Output として返させる prompt を組み立てる。
- 対象領域を oracle file に限定した読み取りモード、oracle 標準、review oracle 標準を適用し、所見マージ専用のモデル種別・推論量・出力 schema を指定する。

## Read this when
- `cmoc review oracle` の所見リスト整理・重複排除・矛盾解消用 prompt の作り方を確認したいとき。
- レビュー結果の finding_id を持つ所見群から、追加・更新・削除などの編集操作を AI に列挙させる呼び出し条件を確認したいとき。
- oracle file レビュー向けの AgentCallParameter で、読み取り権限、モデルクラス、推論量、出力 schema の対応を確認したいとき。
- review oracle 標準や oracle 標準を有効にした complete prompt の組み立て方を、所見マージ用途の具体例として確認したいとき。

## Do not read this when
- oracle file の個別仕様本文や、レビュー対象そのものの内容を確認したいだけのとき。
- 所見を新規検出する prompt、レビュー実行全体の制御、または CLI サブコマンドの入口処理を探しているとき。
- Structured Output schema の項目定義や編集操作の JSON 形式そのものを確認したいとき。
- 一般的な AgentCallParameter の構造、path 解決、markdown レンダリングなどの共通 helper の詳細を調べたいとき。

## hash
- e66e8b43df7e91c85929a443e6698c3d778f4ce9aefdce9bd84f893adc659271

# `validate_finding_advocate.json`

## Summary
- レビュー対象の所見について、正本仕様断片に基づき妥当性を支持できる新規根拠だけを返すための構造を定める。
- 既知の根拠と重複しない理由があるかを判定し、推測ではなく oracle file の記述に基づく根拠へ限定する出力契約として位置づけられる。

## Read this when
- レビュー所見が正本仕様断片に照らして妥当かどうかを、追加の根拠として列挙する出力を扱うとき。
- 既に提示済みの根拠と重複しない、新規の妥当性理由だけを返す必要がある処理を確認するとき。
- oracle file の記述を根拠にしたレビュー検証結果の構造を実装・テスト・調整するとき。

## Do not read this when
- 所見が不当である理由、反証、修正提案、設計改善案を返す構造を探しているとき。
- レビュー対象そのものの検出ロジックや、oracle file の読み取り・探索手順を確認したいとき。
- 正本仕様断片に基づかない一般的なレビュー品質評価や、LLM 出力文面の改善を扱うとき。

## hash
- f265bb48178831b146ee5d071395ff0dd9dfb6bb509f2d062fa54e3243f4cb4e

# `validate_finding_advocate.py`

## Summary
- `cmoc review oracle` で、レビュー所見が妥当である理由を追加調査するための AI 呼び出しパラメータを構築する実装。対象所見、既知の擁護理由、既知の反対理由を prompt に含め、oracle file を根拠にした新規の擁護理由だけを返すよう指示する。
- 所見検証系 prompt のうち、所見を支持する側の理由列挙に特化した入口であり、Structured Output schema、モデル設定、推論強度、oracle 読み取り専用のアクセス条件をまとめて決める。

## Read this when
- `cmoc review oracle` の所見検証で、対象所見が妥当である理由を列挙する agent 呼び出し内容を確認・変更したいとき。
- 既知の擁護理由や既知の反対理由を踏まえて、重複しない新規の擁護理由だけを返す prompt 構築を確認したいとき。
- 所見の根拠調査を oracle file に限定する制約、または review oracle 標準を有効にする prompt 生成経路を確認したいとき。
- この系統の呼び出しで使用するモデル種別、推論強度、ファイルアクセスモード、Structured Output schema の対応付けを確認したいとき。

## Do not read this when
- 所見が妥当ではない理由、反証、却下理由を列挙する prompt 構築を探しているとき。
- oracle file そのものの正本仕様内容や、レビュー所見の実際の妥当性を直接確認したいとき。
- 汎用的な prompt 結合処理、Markdown レンダリング、構造化ドキュメントの実装詳細を調べたいとき。
- CLI サブコマンドの引数解析、実行制御、出力表示など、agent 呼び出しパラメータ構築より外側の処理を調べたいとき。

## hash
- ddc5c0144f1ad335748a4d297b1dc05658fb418b99a97454d6ddced04fc15041

# `validate_finding_challenger.json`

## Summary
- 対象所見が妥当ではないと判断できる新規理由だけを返すための Structured Output schema。
- 理由は推測ではなく oracle file の記述に基づく具体的根拠に限定し、既知理由と重複するものがなければ空のリストで表す。

## Read this when
- レビュー所見に対して、oracle file を根拠に反証・異議申し立てとなる理由を構造化して返す処理を確認する。
- 既知の反証理由と重複しない、新しい不当性の根拠だけを出力すべき場面の出力契約を確認する。
- oracle file の記述に基づく理由と、推測や実装都合に基づく理由を区別する必要がある。

## Do not read this when
- レビュー所見そのものを生成するための出力契約を確認したい。
- 所見が妥当である理由、修正案、実装方針、テスト方針を扱いたい。
- oracle file ではなく realization file、一般的なベストプラクティス、推測に基づく判断理由を扱いたい。
- 個々の oracle file の内容や、所見の妥当性判断に使う正本仕様断片そのものを読みたい。

## hash
- a90232c11fe6071e9aaf6200efe525e546aef4775f06fb11cc71018c28f1d214

# `validate_finding_challenger.py`

## Summary
- `cmoc review oracle` で、レビュー所見を否定する新規理由を列挙するための AI 呼び出しパラメータを組み立てる実装。対象所見、既知の肯定理由、既知の否定理由を補助プロンプトに含め、oracle を根拠に反証担当へ調査させるプロンプトと出力 schema パスを設定する。

## Read this when
- `cmoc review oracle` の所見検証フローで、所見が妥当ではない理由を探す側のプロンプト内容、役割、ゴール、参照権限を確認したいとき。
- 既知の肯定理由や否定理由を踏まえて、重複しない新規の否定理由だけを返させる呼び出し条件を変更したいとき。
- レビュー所見の反証用エージェントに渡すモデル種別、推論強度、ファイルアクセスモード、Structured Output schema の対応関係を確認したいとき。

## Do not read this when
- 所見が妥当である理由を列挙する側のプロンプトを確認したいとき。
- `cmoc review oracle` 全体のコマンド実行、入出力処理、結果集約、または CLI 表示の挙動を確認したいとき。
- oracle file の定義やレビュー基準そのものを確認したいとき。

## hash
- de331e5be31635dba0c8e8cde674f4bbdc384d3df1ccb04bc9aa7c5da4ecaac8
