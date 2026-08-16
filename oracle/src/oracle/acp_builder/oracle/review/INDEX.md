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
- `cmoc oracle review` における新規所見列挙用のエージェント呼び出しパラメータを構築する。レビュー対象 oracle file、関連所見、隔離 review worktree をもとに、完全なプロンプト、読み取り権限、モデル・推論設定、Structured Output schema、索引事前処理をまとめた `AgentCallParameter` を生成する。
- oracle review の新規所見列挙フローで、プロンプト内容と起動パラメータの定義を確認・変更するときの入口。レビュー結果の所見形式そのものや共通プロンプト生成処理を確認する場合は、対応する schema または `build_complete_prompt` 側を直接読む。

## Read this when
- `cmoc oracle review` の新規所見列挙エージェントのプロンプト、モデル設定、ファイルアクセスモード、実行 worktree、Structured Output schema の関連付けを変更・確認するとき
- 既知の関連所見やレビュー対象 oracle file をプロンプトへ渡す起動定義を調査するとき

## Do not read this when
- レビュー所見の出力項目や JSON Schema 自体を確認するだけの場合
- 共通プロンプトの生成規則やパス解決の実装を確認する場合
- oracle review の別処理の起動パラメータを調査する場合

## hash
- 8b8797ef507456499beca0bb578ddabffde6f80fa81f1cc56bc8d407845f8c57

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
- oracle review の所見を人間へ提示すべきか判定するエージェント呼び出しの、プロンプト文面・動的な所見情報・起動パラメータを構築する定義。レビュー所見の採否判定フローを確認・変更するときの入口。

## Read this when
- oracle review の所見採否判定用 agent call の prompt、入力する賛成・反対理由、モデルやアクセスモードなどの起動設定を確認・変更するとき。

## Do not read this when
- 所見採否判定の出力形式だけを確認する場合は、対応する Structured Output schema を直接読む。
- oracle review 全体の判定処理や所見生成の挙動を確認する場合は、実際のレビュー処理を担う対象を直接読む。

## hash
- db883ac644b2bd1ca89bd14991f873e3bcc8bb6f652e0d29886e4683f7d3733c

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
- oracle review における所見リスト統合用の agent call パラメータを構築する定義。隔離済み review worktree を起点に、所見整理の prompt、読み取り範囲、Structured Output schema、モデル設定、起動前インデックス検査をまとめて返す。
- 所見リストの入力を動的 prompt に埋め込み、重複・矛盾の解消を目的とする oracle review 用の prompt 文面を生成する。所見統合の呼び出し仕様や起動パラメータを変更・確認するときの入口となる。

## Read this when
- oracle review で所見リストの統合処理を変更・調査するとき
- 所見マージ用 agent call の prompt、ファイルアクセスモード、モデル・推論設定、実行 worktree、Structured Output schema の関連付けを確認するとき
- finding_id の入力制約や、所見統合 prompt の動的入力方法を確認するとき

## Do not read this when
- oracle review の所見統合ロジックそのものや出力形式の詳細を確認する場合は、直接対応する実装・Structured Output schema を読むとよい
- oracle review 以外の agent call パラメータや一般的な prompt 構築規則だけを調べる場合
- INDEX.md の更新やリポジトリ全体のルーティング方針だけを確認する場合

## hash
- 75aea0ec59f8a29a1a865e7ace357c0d7b2abee38ebda007c3a13f9b9d84d93f

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
- `cmoc oracle review` における、レビュー所見が妥当である理由を列挙するエージェント呼び出しの prompt と起動パラメータを構築する。所見、既知の擁護理由、既知の反論理由を prompt に埋め込み、oracle 専用の読み取り制約、レビュー方針、ルーティング方針、効率重視モデル、最大推論強度、構造化出力 schema を指定した `AgentCallParameter` を返す。

## Read this when
- `cmoc oracle review` の所見妥当性検証で、擁護理由を列挙する agent call の prompt または起動パラメータを変更・調査するとき
- レビュー所見、既知の擁護理由、既知の反論理由を oracle review 用 prompt に渡す処理の入口を確認するとき

## Do not read this when
- 所見が妥当であるか自体のレビューを行うときは、review 対象の仕様・実装を直接読む
- 擁護理由の出力形式や schema の定義だけを確認するときは、対応する構造化出力 schema を直接読む
- oracle review 以外の agent call の prompt 構築を調査するときは、各用途の専用 builder を読む

## hash
- 2b0092ccf54ec6b53b402ade12c4c11c2485b0d90a435da6d98e16a8b3bc0da9

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
- `cmoc oracle review` で、レビュー対象所見が妥当ではない理由を列挙するエージェント呼び出しの prompt と起動パラメータを構築する。対象所見と既知の賛成・反対理由を prompt に渡し、既存理由と重複しない新規の反証理由を Structured Output として生成する処理への入口。

## Read this when
- oracle review の反証担当 prompt の内容や、finding・既知の妥当理由・既知の不妥当理由の受け渡しを変更・調査するとき。
- 反証理由を生成するエージェントのモデル、推論強度、ファイルアクセスモード、隔離 worktree、indexing preflight などの起動条件を確認するとき。

## Do not read this when
- レビュー所見の妥当性そのものを判定する実装や、反証理由の Structured Output schema の定義だけを確認するとき。
- `cmoc oracle review` 以外の prompt 構築や、妥当である理由を列挙する担当の処理を変更・調査するとき。

## hash
- a7bbd95171ebb4d58a03244fda34870dcb334bf9f0b91fccc29e7636ce4e5e35
