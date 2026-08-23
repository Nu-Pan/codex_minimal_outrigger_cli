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
- oracle review で新規所見を列挙する agent call の prompt と起動パラメータを構築する定義。レビュー対象 oracle file、関連する既知所見、隔離 worktree を入力として、共通 policy を含む prompt と Structured Output schema、モデル・推論強度・ファイルアクセスモード・index preflight などの実行条件をまとめた AgentCallParameter を返す。

## Read this when
- oracle review サブコマンドの新規所見列挙フローを変更・調査するとき
- レビュー用 prompt の構成、既知所見の重複防止、oracle の読み取り範囲を確認するとき
- enumerate finding agent call のモデル、推論設定、起動ディレクトリ、preflight 設定を確認するとき

## Do not read this when
- oracle review の所見内容そのものや所見 policy の詳細を確認したいときは、該当する oracle policy・finding 定義を直接読む
- レビュー対象 oracle file の仕様本文を確認したいときは、その対象ファイルを直接読む
- 新規所見列挙以外の oracle review 段階の prompt 構築を調査するとき

## hash
- b455925111fa983867e3d3bacbf61cb4e0b1b1fccebf64fe40499028e6a499f8

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
- oracle review における所見採否判定用の prompt と AgentCallParameter を構築する定義。
- 所見、妥当性を支持する理由、妥当ではない理由を動的入力として完全 prompt を生成し、判定結果の Structured Output schema と、隔離 worktree・モデル・推論強度・preflight などの起動条件をまとめる。

## Read this when
- oracle review で所見を人間へ提示すべきか判定する処理の prompt 構成を確認または変更するとき。
- 所見採否判定 agent call のモデル、推論強度、ファイルアクセスモード、worktree、preflight、Structured Output schema の起動設定を確認するとき。

## Do not read this when
- oracle review の所見採否判定以外の処理を確認するとき。
- 判定結果の出力項目や形式だけを確認するときは、対応する Structured Output schema を直接読むとき。

## hash
- 02c37b929d3c79115e77129fe9460d8e8e90307950ecbd311aa53123a65aa679

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
- oracle review の所見リスト統合に使う agent call の prompt と起動パラメータを構築する実装。所見の重複・矛盾を整理するための固定／動的 prompt、oracle 専用の読み取り範囲、Structured Output schema、モデル・推論設定、preflight 実行条件を定義している。
- 所見マージ処理の呼び出し条件、所見リストの注入方法、finding ID の事後条件、または agent call パラメータを変更・調査するときの入口となる。

## Read this when
- `cmoc oracle review` の所見統合 call の prompt 内容や起動設定を変更・確認するとき
- 所見マージ時のファイルアクセス範囲、finding ID 検証、モデル設定、indexing preflight の挙動を追うとき
- この関数に対応する Structured Output schema との組み合わせを確認するとき

## Do not read this when
- 所見の列挙や単一所見のレビュー処理を調べる場合は、それぞれの専用実装を直接読むとき
- prompt の共通生成規則だけを確認する場合は、`build_complete_prompt` など共通 prompt builder を直接読むとき
- 出力項目の形式だけを確認する場合は、対応する Structured Output schema を直接読むとき

## hash
- 088365d4b7d96bfbf4a76fb808f7e360ff8de74854b66324692a73dc00e75a94

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
- oracle review で所見が妥当である理由を列挙するための prompt と AgentCallParameter を構築する。
- 所見、既知の擁護理由、既知の反証理由を dynamic prompt に組み込み、既存理由と重複しない新規理由の返却を要求する。
- oracle-only のファイルアクセス、oracle findings policy、routing policy、効率モデルの最大推論、indexing preflight など、当該 agent call の実行設定を定義する。
- prompt 本文は共通の complete prompt builder で生成し、Structured Output schema と prompt を含む起動パラメータを返す。

## Read this when
- 妥当性を擁護するレビュー所見の調査 prompt や agent call の起動設定を確認・変更するとき。
- 所見と既知理由を入力として、重複を避けた新規の擁護理由を生成する経路を追跡するとき。
- 対象サブコマンドの oracle 読み取り制約、モデル・推論設定、routing 前の indexing preflight を確認するとき。

## Do not read this when
- 妥当ではない理由を列挙する処理や、別の oracle review サブコマンドの prompt 構築だけを調べるときは、それぞれの専用対象を直接読む。
- Structured Output の出力項目・型・形式だけを確認したいときは、対応する schema を直接読む。

## hash
- e6236811461b4ae0497cf220710fc63ac4619b635bc18166432471262883f720

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
- oracle review で、対象所見が妥当ではない理由を列挙するエージェント呼び出し用の prompt と起動パラメータを構築する。対象所見、既知の賛成理由、既知の反証理由を動的入力として prompt に埋め込み、oracle 専用の読み取り範囲、所見ポリシー、ルーティングポリシーを適用する。
- 効率モデルの最大推論を指定し、構造化出力スキーマ、隔離された review worktree、indexing preflight を含む AgentCallParameter を返す。

## Read this when
- oracle review の所見について、妥当ではない理由を列挙する agent call の prompt や起動パラメータを変更・確認するとき
- 対象所見や既知理由の動的入力、oracle 専用ファイルアクセス、構造化出力、preflight の設定を確認するとき

## Do not read this when
- oracle review の別の判定段階や、妥当である理由を列挙する処理を直接確認するとき
- 一般的な prompt 構築処理や、構造化出力スキーマの定義そのものを確認するとき

## hash
- fc96b333d21685ccb3e133a5a72cf74cb5f3d6e255d4bd6818338d8ef8017765
