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
- oracle review における「新規所見列挙」エージェント呼び出しの定義。レビュー対象 oracle file と関連所見を入力として、関連 oracle file の読解範囲、読み取り専用モード、プロンプト、モデル・推論設定、Structured Output schema、実行コンテキストを組み立てる。
- `build_oracle_review_enumerate_finding_parameter` が、レビュー目的・重複排除条件・既知の関連所見・oracle のパス情報を完全な prompt に統合し、`AgentCallParameter` として返す実装上の入口。

## Read this when
- `cmoc oracle review` の新規所見列挙フローを変更・調査するとき
- oracle review agent call の prompt、読み取り対象、モデル設定、実行ディレクトリ、Structured Output schema の起動パラメータを確認するとき
- レビュー対象ファイル以外の関連 oracle file を読む条件や、既知の所見との重複排除を確認するとき

## Do not read this when
- レビュー所見の出力項目や JSON schema 自体だけを確認したいときは、対応する `.json` schema を直接読む
- oracle review の既存所見更新・修正や、別の review サブコマンドの起動定義を調べるときは、それぞれの担当ファイルを直接読む
- 一般的な agent call パラメータ構築や共通 prompt の仕様だけを調べるときは、参照される共通 builder・型定義を直接読む

## hash
- b458fa2bad8d724bdc46dc4a420d04e8e188b127c74d4e3332d1a3739f8cb472

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
- oracle review の所見採否判定エージェント呼び出しを構築する関数。所見本文と賛成・反対理由をプロンプトへ組み込み、純粋な oracle 読み取り権限、効率重視モデル、最大推論、構造化出力スキーマ、起動前インデックス処理などの実行パラメータを設定する。

## Read this when
- `cmoc oracle review` の所見採否判定プロンプトやエージェント起動パラメータを変更・確認するとき
- 所見、賛成理由、反対理由が判定エージェントへどのように渡されるかを確認するとき

## Do not read this when
- 所見採否判定の出力形式そのものを確認する場合は、同じディレクトリの構造化出力スキーマを直接読むとき
- 一般的なプロンプト組み立て規則や共通のパス・アクセス制御を確認する場合は、それぞれの共通ビルダーやポリシー定義を直接読むとき

## hash
- a4560c43ba1ba148c24543369a07fc5f8d32622180cbd494eca4e4f85803f7b1

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
- oracle review の所見リスト統合を担当するエージェント呼び出しパラメータを構築する定義。所見の重複・矛盾を解消する編集操作を列挙させる prompt、入力所見、読み取り専用の oracle アクセス、モデル・推論設定、Structured Output schema、実行時の索引付け事前処理をまとめて構成する。

## Read this when
- oracle review の所見リストを統合する agent call の prompt または起動パラメータの構築経路を確認するとき
- 所見の重複・矛盾を解消する編集操作と、入力された finding_id の制約を確認するとき

## Do not read this when
- oracle review の所見統合以外の agent call パラメータを確認するとき
- Structured Output schema の定義そのものや、レビュー所見の生成・判定処理を直接確認するとき

## hash
- dffb0fe017ecfb4ffaeb4b2e4ca38d6030e2e287988b3781adeb24998d1df848

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
- oracle review で、対象所見が妥当である理由を追加調査するための AI エージェント呼び出しパラメータを構築する。所見、既知の妥当理由、既知の反対理由をプロンプトに埋め込み、既存理由と重複しない新規理由のみを Structured Output で返す処理の入口となる。

## Read this when
- oracle review の所見について、妥当性を支持する追加理由を列挙する prompt や起動パラメータの構築を確認・変更するとき
- finding、既知の妥当理由、既知の反対理由を入力とするレビューエージェント呼び出しの構成を確認するとき

## Do not read this when
- 所見が妥当でない理由の列挙や、レビュー結果そのものの検証を扱うとき
- 共通 prompt の生成規則、構造化文書のレンダリング、または出力 schema の定義を直接確認するときは、それぞれの担当対象を先に読むべき場合

## hash
- 01f1096937cd0753389d1b787992732dc938690da912bbbfecf3253b0d2e94d5

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
- `cmoc oracle review` で、所見が妥当ではない理由を列挙するエージェント呼び出しパラメータを構築する。
- 対象所見と既知の賛成・反証理由をプロンプトへ渡し、既存理由と重複しない新規の反証理由だけを返すよう指定する。
- 使用モデル、推論強度、oracle 専用読み取り権限、Structured Output schema、実行前インデックス処理などの起動条件を設定する。

## Read this when
- oracle review の所見反証担当エージェントの prompt や起動パラメータを確認・変更するとき。
- 対象所見、既知の妥当理由、既知の反証理由が反証調査用 prompt にどう組み込まれるか確認するとき。
- 反証理由の重複排除や、反証理由がない場合の空配列応答を要求する呼び出し条件を確認するとき。

## Do not read this when
- 所見の妥当性を判定するレビュー実装そのものを確認したいとき。
- Structured Output schema の具体的な出力項目・型・形式だけを確認したいときは、対応する schema ファイルを直接読む。
- 共通 prompt の組み立て規則や構造化文書の Markdown レンダリング実装だけを確認したいときは、各共通ビルダーを直接読む。

## hash
- 74cd266f58e1e8283ff93dc921c41de11cc916849046ced37623a86ec9285249
