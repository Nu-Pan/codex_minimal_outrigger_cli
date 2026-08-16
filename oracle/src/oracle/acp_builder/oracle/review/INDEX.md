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
- `cmoc oracle review` の新規所見列挙用に、レビュー対象 oracle file と関連既知所見をもとに prompt および AgentCallParameter を構築する定義です。
- oracle file の読取範囲、既知所見との重複排除、新規所見がない場合の空配列、隔離 review worktree を起点とした起動条件を扱います。

## Read this when
- oracle review の新規所見列挙処理における prompt 文面やエージェント起動パラメータを確認・変更するとき
- レビュー対象 oracle file と関連所見からレビュー呼び出しを構築する経路を調査するとき

## Do not read this when
- 所見の Structured Output schema 自体だけを確認するとき
- oracle review の実行制御、所見の保存、またはレビュー結果の後処理を調査するとき

## hash
- 4a3f6dc5f8aa496280c174119b4e558107ad4079dd123222f3d508c6420c962d

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
- oracle review の所見を採用するか判定する agent call の prompt と起動パラメータを構築する定義。所見本文、妥当性を支持する理由、反対理由を prompt に埋め込み、隔離 review worktree と oracle review 用ポリシーを適用した AgentCallParameter を生成する。

## Read this when
- oracle review で所見の採否判定を行う agent call の prompt 構成や起動パラメータを変更・確認するとき
- 所見、advocate/challenger の理由、Structured Output schema、review worktree の扱いの接続を確認するとき

## Do not read this when
- oracle review の所見内容そのものや判定ロジックを確認したいとき
- 一般的な agent call パラメータや共通 prompt 生成規則を確認したいときは、対応する共通 builder を直接読む

## hash
- c8518bf14447046432c548a359e2d3325ab6f7ec71353d92a5f46eeb38af4ce3

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
- 日本語の技術文書として、対象ファイルの責務と、oracle review の所見統合に関する作業で読むべき入口を簡潔に示します。

## Read this when
- oracle review の所見リストを整理・統合するための prompt 文面や agent call パラメータの構築を確認するとき
- 所見マージ処理が参照する oracle ツリーの読み取り範囲、動的 prompt、Structured Output、起動条件の関係を確認するとき

## Do not read this when
- oracle review の所見統合以外の処理を調べるとき
- 対象ファイルが構築する prompt や agent call パラメータを変更・検証する必要がないとき

## hash
- a14a2c52e67adf5a8cf5f4d417b00c6282ad08d752df287ed5c7aee220e243ef

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
- oracle review で、対象所見が妥当である理由を調査するエージェント呼び出しの prompt と起動パラメータを構築する定義。所見、既知の擁護理由、既知の反論理由を prompt に埋め込み、既存理由と重複しない新規理由の列挙を依頼するレビュー処理の入口。

## Read this when
- oracle review の所見について、妥当性を擁護する理由の調査呼び出しを追加・変更・確認するとき。

## Do not read this when
- 妥当ではない理由の列挙、一般的な仕様レビュー、または prompt 構築以外の oracle review 処理を扱うときは、対応する別の定義を直接読む。

## hash
- b68909f956021705b95e820ac2c75fbcad7dbad2e046619a8b5647019c1269f3

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
- oracle review の所見反証エージェント呼び出しを構築する定義。対象所見、既知の賛成理由・反対理由をプロンプトへ埋め込み、既存理由と重複しない新たな反証理由の列挙を依頼する。oracle review の反証調査や、その起動パラメータ・実行ポリシーを変更するときの入口となる。

## Read this when
- oracle review で所見が妥当ではない理由を調査するエージェント呼び出しのプロンプトや起動設定を確認・変更するとき
- 対象所見と既知の理由を渡す反証担当の入力構成、モデル・推論設定、構造化出力指定を確認するとき

## Do not read this when
- oracle review の賛成理由の列挙や、反証理由以外のレビュー処理を確認するとき
- エージェント呼び出しの共通仕様や構造化出力スキーマ自体を確認する場合は、それぞれの共通定義・スキーマを直接読むとき

## hash
- 2541cf67004953e1b03602ae6e09b4afa7e0040a0d1467cfd5ad14719c8e949e
