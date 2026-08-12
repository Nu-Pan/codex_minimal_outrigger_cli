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
- oracle review の新規所見列挙用エージェント呼び出しパラメータを構築する。レビュー対象 oracle file、関連する既知の所見、隔離済み worktree、oracle file の読み取り制約、レビュー用プロンプト、Structured Output schema、および起動設定を組み合わせる。
- レビュー対象ファイルを直接読む入口ではなく、oracle review の新規所見列挙処理に必要なプロンプトと AgentCallParameter の構築定義へ進むための対象である。

## Read this when
- oracle review で新規所見を列挙する agent call のプロンプト内容や起動パラメータを変更・確認するとき。
- レビュー対象 oracle file と既知の関連所見を、レビュー用 agent call にどう渡すか確認するとき。
- oracle file 専用の読み取り制約、パス解決、レビュー用 Structured Output schema、実行 worktree の指定を確認するとき。

## Do not read this when
- oracle review の既存所見の保存・更新や、所見の内容判定そのものを確認するとき。
- 新規所見列挙以外の oracle review サブコマンドのプロンプト構築を確認するとき。
- レビュー用 agent call の実行結果だけを確認するとき。

## hash
- f16438f54db251bab9471eed40b02debce0eef5ed81e99a8b614c2555f33a440

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
- oracle review の所見について、妥当性を支持する理由と反対理由を提示して採否を判定するエージェント呼び出し用のプロンプトおよび起動パラメータを構築する。`cmoc oracle review` の判定処理における、所見判定エージェント呼び出し設定への入口となる。

## Read this when
- `cmoc oracle review` の所見採否判定のプロンプトやエージェント起動設定を確認・変更するとき
- 所見、支持理由、反対理由を判定エージェントへ渡す処理や、判定用のモデル・アクセス権限・Structured Output 設定を調査するとき

## Do not read this when
- oracle review の別のレビュー工程や、所見判定以外のエージェント呼び出しを確認するとき
- 判定結果のスキーマ定義だけを確認するときは、対応するスキーマを直接読む

## hash
- 613d6fafc34f483a7f7a43464296566c426b603bd0220cde65754f60d8a3ad89

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
- oracle review の所見リストを整理する agent call の prompt と起動パラメータを構築する関数。所見の重複・矛盾を解消するための入力、パスコンテキスト、読み取り権限、構造化出力スキーマ、モデル設定をまとめ、実行用の AgentCallParameter を返す。

## Read this when
- oracle review で既存の所見リストを統合・整理する agent call の入力条件や起動設定を確認・変更するとき。
- 所見リストを動的 prompt に埋め込み、構造化出力による編集操作を要求する処理の入口を確認するとき。

## Do not read this when
- oracle review の所見統合結果を表す Structured Output schema 自体を確認したいときは、対応する schema 定義を直接読む。
- prompt 全体の共通構築規則や一般的な agent call パラメータの仕様を確認したいときは、共通の prompt builder または ACP 定義を直接読む。

## hash
- 05d00dc5b9e05040214802ca55f24769d523a08021f602f2f6cb3abdb01d90f1

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
- oracle review で、所見が妥当である理由を追加調査するためのエージェント呼び出しパラメータを構築する。所見と既知の賛成・反対理由をプロンプトへ渡し、重複しない新規理由の列挙を求めるレビュー用入口である。

## Read this when
- oracle review の所見について、妥当性を支持する理由を検証・追加列挙する処理を変更するとき
- 所見、既知の賛成理由、既知の反対理由をレビューエージェントへ渡すプロンプトや、読み取り専用のレビュー実行条件を確認するとき
- この処理が使用するモデル、推論強度、Structured Output、隔離 worktree での起動条件を変更するとき

## Do not read this when
- 所見が妥当でない理由を列挙する処理を確認するときは、反対理由側の直接の実装を読む
- oracle review 以外のサブコマンドのプロンプトや起動パラメータだけを変更・調査するとき
- レビュー所見の出力スキーマそのものを変更するときは、この呼び出し構築処理ではなく対応するスキーマ定義を直接読む

## hash
- 5f59bd266c9a6a07a4a982e9639c30d81c88633228afd22cec02dd3107793cd3

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
- oracle review で、対象所見が妥当ではない理由を列挙するエージェント呼び出しの prompt と起動パラメータを構築する。
- 所見、既知の肯定理由、既知の反証理由を prompt に渡し、既存理由と重複しない新規の反証理由だけを返すレビュー処理への入口となる。

## Read this when
- oracle review の反証理由列挙処理を変更・調査するとき。
- レビュー所見、既知の理由、Structured Output、または隔離済み review worktree を用いたエージェント呼び出しパラメータの関係を確認するとき。

## Do not read this when
- 所見が妥当である理由の列挙処理だけを確認するとき。
- レビュー結果のスキーマ定義だけを確認するときは、対応するスキーマ定義を直接読む。
- 共通の prompt 構築処理やパスモデルの仕様だけを確認するときは、それぞれの共通実装を直接読む。

## hash
- 32e2736874299c71ba576076e5327172085768e7e02ff12c9a6948817363bc9e
