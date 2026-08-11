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
- oracle review サブコマンドで新規所見を列挙するための agent call パラメータを構築する実装。レビュー対象 oracle file と関連所見を受け取り、レビュー用プロンプト、モデル・推論設定、oracle 限定アクセス、Structured Output schema、作業ディレクトリ、索引事前処理を含む呼び出し設定を生成する。

## Read this when
- oracle review の新規所見列挙用 agent call のプロンプト、起動パラメータ、モデル設定、ファイルアクセス範囲、Structured Output schema の関連を確認するとき。
- レビュー対象 oracle file や既知の関連所見をプロンプトへ渡す処理を変更するとき。

## Do not read this when
- oracle review 以外の agent call パラメータを調べるとき。
- レビュー結果の判定・保存や、実際の所見内容を扱う処理を直接確認するときは、該当する実装へ進む。

## hash
- 6235807a59d903f852bc88cde09abde185e14f4f21de51e5dc7df99686a7b657

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
- 対象の実装は、oracle review における所見の採否判定を担当するエージェント呼び出し用パラメータを構築する。所見本文と、妥当性を支持・反論する理由をプロンプトへ組み込み、oracle 専用の読み取り範囲、効率重視モデル、最大推論、構造化出力スキーマ、リポジトリを作業ディレクトリとする起動条件をまとめて返す。

## Read this when
- oracle review の所見を人間へ提示すべきか判定する呼び出し仕様を確認・変更するとき
- 所見、支持理由、反論理由を判定用プロンプトへ渡す経路や、判定エージェントの起動パラメータを調べるとき

## Do not read this when
- oracle review の一般的なレビュー規則や、判定結果の JSON スキーマ自体を確認したいとき
- 所見採否判定以外の agent call parameter 構築を調べるときは、該当する別の builder 実装へ直接進む

## hash
- 574454b69b28e5ab442ab49451eea8e489cb39a7ccc03b2eaa48d9ce2e0020fa

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
- oracle review の所見統合用 AI エージェント呼び出しパラメータを構築する実装。所見リストを動的プロンプトへ埋め込み、oracle file の重複・矛盾解消を目的とするレビュー整理処理の入口。

## Read this when
- `cmoc oracle review` の所見統合処理の起動パラメータ、プロンプト構成、対象モデル・推論設定、Structured Output schema の指定を確認するとき。
- oracle review の所見リストを agent call に渡す経路を変更・調査するとき。

## Do not read this when
- oracle review の所見内容そのもの、または所見統合後の編集操作を確認したいとき。
- 一般的な prompt 構築や他の oracle review 処理を確認したいときは、該当する prompt builder または別の review 実装へ直接進む。

## hash
- fecbac120f85587384324bbdada1a287d06daf8e44ee8cf3bf6380685656e5e2

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
- oracle review の所見が妥当である理由を調査するエージェント呼び出し用の prompt と起動パラメータを構築する。
- 所見、既知の擁護理由、既知の反論理由を prompt に渡し、新規かつ重複しない擁護理由の列挙を要求する。
- oracle のみを読む実行条件、効率重視モデル、最大推論、Structured Output schema、リポジトリルートを基準とする作業ディレクトリなどを AgentCallParameter に設定する。

## Read this when
- oracle review の所見擁護用エージェント呼び出しの prompt 内容や起動条件を確認・変更するとき
- 所見・既知理由を動的 prompt に組み込む処理や、呼び出しパラメータの設定を調査するとき

## Do not read this when
- 擁護理由の出力形式そのものを確認するとき
- oracle review の別の所見検証・反論用呼び出し定義を確認するとき
- レビュー対象の仕様断片や所見の内容そのものを調査するとき

## hash
- 55694741fe79a97bc5f04abdec1c0fa5a47b66fa39e18765cdc10fc2cf50ccc2

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
- oracle review で対象所見が妥当ではない理由を調査するためのエージェント呼び出しパラメータを構築する。所見、既知の賛成理由、既知の反証理由をプロンプトへ渡し、重複しない新規の反証理由を列挙する処理への入口となる。

## Read this when
- oracle review の反証理由列挙用エージェント呼び出しのプロンプト内容、モデル設定、ファイルアクセスモード、作業ディレクトリ、Structured Output schema の指定を確認するとき。
- finding や既知の理由を入力としてレビュー検証用の AgentCallParameter を生成する処理を変更・調査するとき。

## Do not read this when
- レビュー所見の妥当性そのものや、反証理由の内容を確認したいときは、生成されたプロンプトの利用先や oracle review のレビュー処理を直接読む。
- 一般的なエージェント呼び出しパラメータの定義を確認したいときは、共通の ACP builder 定義を直接読む。

## hash
- a59cafd47341ea0ef6ccce47a7fa543b7a275e8a0e846a228e787a7e61aa2d5b
