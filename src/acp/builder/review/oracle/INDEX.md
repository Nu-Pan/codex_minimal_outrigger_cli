# `enumerate_finding.json`

## Summary
- oracle レビューで、新規所見の列挙結果を返すための構造を定義する JSON schema。レビュー対象と関連する正本仕様断片から、既知の関連所見と重複しない所見だけを重大度・見出し・根拠となる正本仕様断片・理由として表す。

## Read this when
- oracle レビュー処理で、新規所見の一覧を機械的に検証できる形で出力する必要があるとき。
- 所見が無い場合の扱いや、所見ごとに保持すべき意味情報の境界を確認したいとき。
- fatal と minor の区分を含む、仕様断片レビュー結果の出力契約を確認したいとき。

## Do not read this when
- 既知の関連所見をどのように収集・比較するかという判定ロジックを調べたいとき。
- oracle file や realization file の基本概念、レビュー基準そのものを確認したいとき。
- INDEX.md エントリー生成やルーティング文書の書き方を調べたいとき。

## hash
- d1bd69c75e8d60791cc304f06e103a7efdcc6566dc16c1254b8a92d6fcb38c5d

# `enumerate_finding.py`

## Summary
- `cmoc review oracle` で、指定された oracle file を起点に新規所見列挙を行う AI エージェント呼び出しパラメータを組み立てる実装。対象 oracle file、既知の関連所見、oracle レビュー用の標準プロンプト断片をまとめ、所見列挙用 schema を指定した呼び出し設定を返す。

## Read this when
- oracle file のレビューで、既知所見と重複しない新規所見を列挙するための prompt 内容や呼び出し設定を確認したいとき。
- `cmoc review oracle` の新規所見列挙処理が、どの入力を受け取り、どのアクセスモード・モデル種別・推論強度・schema を使うか確認したいとき。
- oracle レビュー用の共通標準、既知の関連所見、対象 oracle パスが prompt にどう渡されるかを追いたいとき。

## Do not read this when
- oracle file そのものの正本仕様内容や、レビュー基準の本文を確認したいだけのとき。
- 列挙された所見の出力 schema の詳細だけを確認したいとき。
- review 以外のサブコマンド、または oracle file ではない realization file のレビュー処理を調べたいとき。

## hash
- ed4cfcfe7079b85b8e68b2bc29c1d10e9bbb9b63e89910f6dd2a30ef229cf036

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
- `cmoc review oracle` の所見採否判定用に、AI エージェント呼び出しパラメータを組み立てる実装。判定対象所見、採用側理由、却下側理由を補助プロンプトへ埋め込み、oracle 標準と review oracle 標準に基づく完結プロンプトとして返す。
- 採否判定担当エージェントの役割、目的、参照権限、モデル種別、reasoning effort、出力 schema の指定を 1 箇所で定義する入口。

## Read this when
- `cmoc review oracle` で、個別のレビュー所見を人間へ提示すべきか判定するためのエージェント呼び出し条件を確認・変更したいとき。
- 所見本文、所見が妥当である理由、所見が妥当ではない理由が、採否判定プロンプトへどのように渡るかを確認したいとき。
- review oracle 系プロンプトで、oracle 標準や review oracle 標準を有効にする呼び出し設定を確認したいとき。

## Do not read this when
- 所見の発見、主張生成、反論生成など、採否判定より前段の review oracle 処理を調べたいとき。
- 採否判定結果の JSON schema そのものを確認したいとき。
- 汎用のプロンプト組み立て処理、構造化 markdown レンダリング、パス解決、エージェント呼び出し型の定義を調べたいとき。

## hash
- db0e70e87fafff81bfb61e4ccd0185662810df398bd9b991f8baaf1d1bd32367

# `merge_finding.json`

## Summary
- 入力所見リストを整理する編集操作の応答仕様を定義する。重複・矛盾のある所見を削除、置換、統合する判断結果を返すための構造を扱う。

## Read this when
- 所見リストの重複や矛盾を解消する後処理の出力契約を確認したいとき。
- 削除、単一所見の置換、複数所見の統合という編集操作をどのように表現するかを確認したいとき。
- 編集後の所見として、重大度、見出し、根拠となる oracle file、整理理由を返す場面の仕様を確認したいとき。

## Do not read this when
- 個々の oracle file から所見を検出する基準やレビュー観点を確認したいとき。
- 所見そのものの入力 schema や finding_id の生成規則を確認したいとき。
- 編集操作の JSON を実際に組み立てる実装ロジックやテストを確認したいとき。

## hash
- ef00100875ad3a93bd012fc2fe2f8dceb892a60020b8f202a80594e2426a60c0

# `merge_finding.py`

## Summary
- `cmoc review oracle` で、oracle file に対する既存の所見リストを整理するための AI 呼び出しパラメータを構築する realization implementation。
- 現状の所見リストを補助プロンプトとして渡し、所見同士の内容的な重複や相互矛盾を解消する編集操作を Structured Output として返させるための prompt を組み立てる。
- oracle 標準および review oracle 標準を含む完全プロンプト生成と、読み取り専用の oracle file アクセス設定を結び付ける入口になっている。

## Read this when
- `cmoc review oracle` の所見リスト整理、重複所見の統合、相互矛盾の解消提案に使う AI 呼び出し内容を確認または変更したいとき。
- review oracle 系の prompt が、現状の所見リストをどの役割・目的・ファイルアクセス方針でエージェントへ渡すかを追いたいとき。
- oracle file に対するレビュー結果から、target_ids を持つ編集操作を列挙させる処理の入力文脈やモデル設定を確認したいとき。

## Do not read this when
- 通常の oracle file レビューそのものの検出基準や、個別所見を生成する prompt を探しているとき。
- Structured Output の具体的な JSON schema 定義だけを確認したいとき。
- oracle file や realization file の概念定義、path keyword の意味、または一般的な prompt 共通部品の実装を調べたいとき。

## hash
- 88af6857e331f529f8017682be3fb75d01a7cd10b480906e49beaca208ad5e4c

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
- `cmoc review oracle` でレビュー所見を妥当と擁護できる新規理由を列挙させるための AI 呼び出しパラメータを構築する実装。対象所見、既知の擁護理由、既知の反証理由を補助文脈として渡し、oracle file を根拠にした重複しない擁護理由だけを返す prompt を生成する。

## Read this when
- レビュー所見が妥当である理由を列挙する `cmoc review oracle` 系のプロンプト内容、役割、制約、入力文脈を確認したいとき。
- 所見擁護側の AI 呼び出しで、どの file access mode、model class、reasoning effort、出力 schema が使われるかを確認したいとき。
- 対象所見、既知の妥当理由、既知の非妥当理由が prompt にどう埋め込まれるかを確認したいとき。

## Do not read this when
- レビュー所見が妥当ではない理由を列挙する challenger 側の prompt を確認したいとき。
- oracle file の定義や review oracle 全体の正本仕様そのものを確認したいとき。
- 生成された JSON の後処理、レビュー結果の集約、CLI サブコマンドの引数解析や実行制御を確認したいとき。

## hash
- fd4941548fcf86db04531ac224b4262d0926c233e9470dbd8aa67b8996803222

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
- `cmoc review oracle` で、レビュー所見が妥当ではない理由を列挙する反証担当エージェントの呼び出しパラメータを構築する実装。
- 対象所見、既知の肯定理由、既知の反証理由を補助プロンプトに含め、oracle file を根拠に新規の反証理由だけを返すよう指示する prompt を組み立てる。
- 使用するモデル種別、推論量、ファイルアクセスモード、Structured Output schema の指定をまとめて返す入口になっている。

## Read this when
- `cmoc review oracle` における所見の妥当性否定、反証理由列挙、または challenger 側の prompt 内容を確認・変更したいとき。
- 対象所見、既知の肯定理由、既知の反証理由がエージェントプロンプトへどのように渡されるかを確認したいとき。
- oracle file だけを根拠にし、新規理由のみを列挙し、理由が無い場合は空配列を返す制約の実装箇所を確認したいとき。
- review oracle 用 prompt 構築で使うモデル、推論量、ファイルアクセスモード、出力 schema 指定の組み合わせを確認したいとき。

## Do not read this when
- レビュー所見が妥当である理由を列挙する advocate 側の prompt を確認したいとき。
- `cmoc review oracle` 全体の CLI 引数解析、サブコマンド登録、実行制御を確認したいとき。
- oracle file の定義やパス概念そのものの仕様を確認したいとき。
- Structured Output schema の項目定義や JSON schema 本体を確認したいとき。

## hash
- 0e940691ef68bfa6c135c4db3a5df544eb898e6b5945882fa2e8ee7749789e21
