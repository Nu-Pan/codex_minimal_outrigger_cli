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
- oracle review で新規所見を列挙する agent call の prompt と起動パラメータを構築する。レビュー対象 oracle file、関連所見、隔離済み worktree のパス文脈を prompt に組み込み、oracle 専用の読み取り制約・所見ポリシー・ルーティング方針を適用する。
- レビュー用 agent のモデル種別、推論強度、Structured Output schema、作業ディレクトリ、インデックス事前処理など、所見列挙呼び出しに必要な実行設定を一括して返す関数が、oracle review 実装からの入口となる。

## Read this when
- oracle review の新規所見列挙処理を変更・調査するとき
- レビュー用 prompt の構成、関連所見の注入、oracle file の参照範囲を確認するとき
- 所見列挙 agent call のモデル、アクセスモード、出力 schema、実行ディレクトリなどの起動設定を確認するとき

## Do not read this when
- oracle review の既存所見の更新・適用処理だけを調べるとき
- レビュー対象となる個別 oracle file の仕様本文を直接確認したいとき
- Structured Output schema の定義だけを確認したいときは、対応する schema ファイルを直接読む方が適切な場合

## hash
- 5fd4454361dae3841005b3d5cc58315762f8123db0da13333a5f0ded6b0b07bd

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
- oracle review で検出した所見について、所見本文と妥当性を支持・反証する理由を埋め込んだ判定用プロンプトを構築し、判定エージェントの起動パラメータを返す実装。レビュー所見を人間へ提示すべきか判断する処理への入口であり、oracle review の所見採否判定の実装を確認するときに読む。

## Read this when
- oracle review の所見採否判定プロンプトを変更・レビューするとき
- 所見、支持理由、反証理由のプロンプトへの埋め込み方や判定エージェントの起動設定を確認するとき
- 所見採否判定用のモデル、推論強度、ファイルアクセス権限、Structured Output 設定を確認するとき

## Do not read this when
- oracle review の所見自体を生成する処理を確認するとき
- 判定結果の Structured Output schema の定義だけを確認するときは、対応する JSON schema を直接読むとき
- oracle review 全体の実行制御や、判定後の結果処理だけを確認するとき

## hash
- bdbf83764fdd3d561824980798ff219c12f21c170db1bcb1ee24075c55257f09

# `merge_finding.json`

## Summary
- 入力されたレビュー所見の重複や矛盾を整理するための編集操作を定義する JSON Schema。所見の削除・単一所見の置換・複数所見の統合を扱い、各操作で所見の重大度、見出し、根拠となる oracle file、整理理由を表現する。

## Read this when
- レビュー結果の所見リストを重複なく統合・整理する処理の入出力契約を確認するとき。
- 所見の削除、置換、統合に必要な構造や、統合後の所見情報を確認するとき。

## Do not read this when
- 個々のレビュー所見の内容や、所見の根拠となる仕様を確認したいとき。
- レビュー対象の実装や仕様そのものを調査したいとき。

## hash
- 2bc386bc0505b1b36badaa509c55df0cdad5af1e6ebb64dcc8bcb528fee4c1d2

# `merge_finding.py`

## Summary
- oracle review の所見統合処理に対する AI エージェント呼び出し用の prompt と AgentCallParameter を構築する。現状の所見リストを動的 prompt に埋め込み、oracle 配下のみを読む隔離 worktree 向けに、所見の重複・矛盾を整理する編集操作を Structured Output として返す処理への入口。

## Read this when
- `cmoc oracle review` で所見リストの統合パラメータや prompt の構築内容を確認・変更するとき
- 所見統合エージェントのモデル、推論強度、ファイルアクセス範囲、Structured Output schema、起動前インデックス処理の設定を確認するとき

## Do not read this when
- 所見統合後の編集操作 schema 自体を確認したいときは、同じディレクトリの schema ファイルを直接読む
- oracle review の所見収集・個別レビュー・実際の編集実行の責務を確認したいときは、それぞれの処理対象を直接読む

## hash
- 50affefac294b0b4c70f5938d12f48d109d12074394b042eac9c3d6eb320f73e

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
- oracle review で、指定された所見が妥当である理由を調査するためのエージェント呼び出しパラメータとプロンプトを構築する。対象所見、既知の妥当理由、既知の反証理由をプロンプトへ渡し、既存理由と重複しない新規理由のみを Structured Output で返させる処理の入口。レビュー用の起動モデル、推論強度、読み取り範囲、隔離 worktree、構造化出力スキーマを設定する。

## Read this when
- `cmoc oracle review` の所見擁護処理におけるプロンプト文面やエージェント起動パラメータを確認・変更するとき
- 所見、既知の賛成理由・反対理由の渡し方、重複排除や空配列の要求を確認するとき
- oracle review 用 agent call の読み取り範囲、worktree、モデル設定、構造化出力設定の入口を確認するとき

## Do not read this when
- 所見の妥当性そのものや仕様適合性の判定理由を確認したい場合は、生成された agent call の対象となる仕様・レビュー資料を直接読む
- 擁護理由の出力形式だけを確認したい場合は、直接対応する Structured Output schema を読む
- oracle review の別の役割や別サブコマンドのプロンプト構築を確認したい場合は、それぞれの専用 builder を読む

## hash
- b1f6c5800f2969086aad85780df8520037a50640485b4650564a256100248f6d

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
- oracle review の所見反証担当エージェント向けプロンプトと AgentCallParameter を構築する定義。所見、既知の妥当理由、既知の反証理由をプロンプトへ渡し、重複しない新規反証理由の出力を要求する。レビュー用 worktree のパスコンテキスト、読み取り権限、モデル設定、Structured Output schema、索引付け前処理も指定する。

## Read this when
- oracle review で所見が妥当ではない理由を列挙するエージェント呼び出しのプロンプトを変更するとき
- finding、known_advocate_reasons、known_challenger_reasons のプロンプトへの渡し方や、重複排除・空配列の要求を確認するとき
- 反証担当呼び出しの AgentCallParameter、モデル・推論設定、oracle 読み取り権限、Structured Output schema、worktree 設定を変更または確認するとき

## Do not read this when
- oracle review の所見判定そのものや、反証理由の内容を生成する実装を直接確認するとき
- 所見・既知理由の入力内容、または Structured Output schema の具体的な形式だけを確認するとき
- oracle review 全体のサブコマンド構成や、別のレビュー役割のプロンプト定義を直接確認するとき

## hash
- 97800e90fe663267b13c21289fa6d93a66cc9a8e18179a91550271fbb208f9d2
