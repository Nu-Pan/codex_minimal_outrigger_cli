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
- oracle review で新規所見を列挙する agent call の prompt と起動パラメータを構築する。レビュー対象 oracle file、関連所見、隔離 worktree のパス文脈を受け取り、oracle review 用の完全な prompt と Structured Output schema、モデル・推論・ファイルアクセス設定をまとめた AgentCallParameter を返す。
- レビュー対象ファイルの指定、既知の関連所見の重複除外、oracle review 用 agent call の起動条件や prompt 構成を確認・変更するときの入口である。

## Read this when
- oracle review の新規所見列挙処理の prompt 文面を確認または変更するとき
- 関連所見を prompt に埋め込み、oracle file のパス文脈や review 用ポリシーを設定する処理を確認するとき
- 新規所見列挙用 agent call のモデル、推論強度、Structured Output schema、実行 worktree 設定を確認するとき

## Do not read this when
- oracle review の既存所見の更新・保存処理だけを確認するとき
- 新規所見の出力項目や JSON schema の定義自体を確認するときは、直接対応する schema ファイルを読むとき
- 一般的な prompt 完成処理や agent call 共通型の仕様だけを確認するときは、それぞれの共通実装を直接読むとき

## hash
- b487371154d9db12bcb98c9c4adcbea345ef3a8d10cdb302468c0fa7ab8a9b8f

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
- oracle review の所見採否判定を行う AI エージェント呼び出し用の prompt と起動パラメータを構築する関数。所見、その妥当性を支持・反論する理由を prompt に埋め込み、レビュー判定用の Structured Output schema、効率重視モデル、最大推論、oracle 専用読み取り権限、隔離 worktree、事前索引付けを設定した AgentCallParameter を返す。

## Read this when
- oracle review サブコマンドで、個別のレビュー所見を人間へ提示すべきか判定する prompt や agent call パラメータの構築を確認・変更するとき。
- 所見本文と、妥当性を支持・反論する理由を動的 prompt に渡すレビュー判定呼び出しの入口を調べるとき。

## Do not read this when
- レビュー所見の採否判定ロジックや Structured Output の判定結果形式そのものを確認したいときは、直接その実装または同ファイルの schema を読む。
- 一般的な prompt 完成処理、構造化文書の Markdown 化、パスコンテキスト、agent call 基本型の仕様を確認する場合は、それぞれの担当モジュールを直接読む。

## hash
- 103f299a89f661f80d80f89297b608161f3b00231eb23f89e6782c2f38910d91

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
- oracle review の所見リストを統合するための AI エージェント呼び出しパラメータを構築する。入力された findings を動的プロンプトへ埋め込み、oracle file 専用の読み取り権限、レビュー方針、ルーティング方針、Structured Output schema などを設定する。
- 隔離済み review worktree のパスコンテキストを基に、所見の重複・矛盾を解消する編集操作の列挙を要求する prompt を生成し、効率重視・最大推論 effort の AgentCallParameter として返す。

## Read this when
- oracle review の所見リスト統合に用いる prompt 文面、動的 findings の渡し方、または agent call 起動パラメータを確認・変更するとき
- oracle/acp_builder 配下で oracle review 用の AgentCallParameter 構築処理の責務や設定を確認するとき

## Do not read this when
- 所見統合の Structured Output の項目や検証規則そのものを確認したいときは、対応する JSON schema を直接読む
- oracle review 全体の実行制御や所見の生成処理を確認したいときは、該当する review サブコマンドや個別の agent call 定義を直接読む

## hash
- a9d162afe88477a50026c91dcda3915256540f6dce3646637564a0bc7a92e459

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
- oracle review で、指定された所見が妥当である理由を調査するための AI エージェント呼び出しパラメータを構築する。所見、既知の擁護理由、既知の反論理由をプロンプトへ埋め込み、既存理由と重複しない新規理由のみを Structured Output で返すよう指定する。
- レビュー用の隔離 worktree を起点にパスコンテキストを構成し、oracle・レビュー・ルーティングの各ポリシーを有効化した完全なプロンプトを生成する。返却する AgentCallParameter には効率モデル、最大推論、oracle 読み取り専用アクセス、対応する JSON schema、事前インデックス実行を設定する。

## Read this when
- oracle review の所見について、妥当性を擁護する理由列挙用 agent call のプロンプトや起動パラメータを変更・確認するとき
- finding と既知の擁護理由・反論理由をレビュー用プロンプトへ渡す構築経路を確認するとき
- oracle review 用 AgentCallParameter のモデル、推論強度、ファイルアクセス、schema、worktree 起点の設定を確認するとき

## Do not read this when
- 所見の妥当性を否定する理由の列挙を扱うとき
- oracle review の他の判定・検証処理や、実際のレビュー所見の内容を直接確認するとき
- 共通のプロンプト生成処理や Structured Output schema の定義そのものを確認することが目的のときは、それぞれの実装・schema ファイルへ直接進む

## hash
- d8e8223896f98f28c91a884f4c205f64afc4350da6d2a69c68f8a2c2b77ecf07

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
- oracle review で、所見が妥当ではない理由を列挙するエージェント呼び出しの prompt と起動パラメータを構築する。所見、既知の賛成理由、既知の反証理由を prompt に埋め込み、既存理由と重複しない新規の反証理由のみを返すよう指定する。
- oracle および realization を読み取る隔離 review worktree 向けのアクセス方針・レビュー方針・ルーティング方針を含む AgentCallParameter を生成する実装への入口である。

## Read this when
- `cmoc oracle review` の所見反証処理で、反証理由列挙用エージェントの prompt 内容や起動パラメータを確認・変更するとき。
- 所見、既知の妥当理由、既知の反証理由の受け渡し方法、または反証理由の重複排除方針を確認するとき。

## Do not read this when
- oracle review の所見判定全体の仕様やレビュー適合性を確認する場合は、まず該当する正本仕様・レビュー実装を読む。
- Structured Output の出力形式だけを確認する場合は、対応する schema を直接読む。
- 反証理由ではなく、別の oracle review エージェント呼び出しの prompt 構築を調べる場合は、その処理に対応する実装へ進む。

## hash
- bc07bf4e25570a7c76e83e881fb52ae8a32d47ff74ab5d1250fd0a47debfd896
