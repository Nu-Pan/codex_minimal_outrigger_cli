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
- oracle review の新規所見を列挙するためのプロンプトと、AI エージェント呼び出しパラメータを構築する実装。レビュー対象 oracle file と関連所見を入力に、oracle-only 読み取り、関連 oracle file の参照、隔離 worktree を起点とするパス解決、標準レビュー条件を組み立てる。oracle review の該当サブコマンドから呼び出し定義を確認する入口。

## Read this when
- oracle review で新規所見を列挙する agent call のプロンプト内容、読み取り範囲、モデル・推論設定、実行コンテキストを確認または変更するとき
- レビュー対象ファイルに関連する既知の所見を重複除外用の入力として渡す呼び出し経路を調査するとき
- oracle review の所見列挙処理で、パス解決、oracle/realization の基本条件、ルーティング前処理の設定を確認するとき

## Do not read this when
- oracle review の別の処理や、所見の保存・表示・更新の責務だけを調査するとき
- 新規所見列挙で使用する Structured Output schema の定義だけを確認するとき
- プロンプト構築ではなく、レビュー対象 oracle file の仕様本文そのものを確認するとき

## hash
- 2ea0be5e85835790b410ab666b8f9e908c04afc2c03f3c64b1b8a7bd8cc0bc37

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
- oracle review における所見の採否判定を担当するエージェント呼び出しパラメータを構築する。所見本文と、妥当性を支持・反論する理由を判定用プロンプトへ組み込み、レビュー用の実行条件・モデル設定・Structured Output schema・隔離 worktree をまとめた起動パラメータを返す。

## Read this when
- oracle review の所見を人間へ提示すべきか判定する処理を変更・調査するとき
- 所見、支持理由、反論理由を判定用 agent call の prompt に渡す方法を確認するとき
- この判定処理のモデル、推論強度、ファイルアクセスモード、出力 schema、起動前 indexing の設定を確認するとき

## Do not read this when
- oracle review の所見採否判定ではなく、別種類の agent call の prompt や起動パラメータを扱うとき
- 判定結果の schema 定義そのものを確認する必要があり、直接 schema ファイルを読む方が適切なとき
- レビュー所見の生成・仕様適合性レビューなど、判定後の別処理だけを調査するとき

## hash
- ae7fbb7ec673f5162f11cd3e9f5604b296743a3948cd9137bebfe66c66b36df6

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
- oracle review の所見リストを統合する agent call の prompt と起動パラメータを構築する定義。レビュー用 worktree のパス文脈、所見リストの動的埋め込み、モデル・推論設定、Structured Output schema、索引付け前処理などをまとめて扱う。

## Read this when
- `cmoc oracle review` で所見リストの重複や矛盾を整理する agent call の prompt または起動パラメータを変更・確認するとき。
- oracle review の merge finding 処理で、所見入力の埋め込みや oracle 専用のファイルアクセス・ルーティング設定を確認するとき。

## Do not read this when
- oracle review の所見統合以外の agent call を扱うとき。
- 所見統合の出力形式や編集操作の契約だけを確認する場合は、対応する Structured Output schema を直接読むとき。

## hash
- 3de0c1575f765ecb5251ded36ae4452157ed2040e459a5f0d8d09540eed103b6

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
- oracle review の擁護理由列挙用 agent call の prompt と起動パラメータを構築する。対象所見、既知の妥当理由、既知の反証理由を prompt に渡し、重複しない新規の妥当理由だけを Structured Output として返させる。
- oracle review の所見について妥当性を支持する根拠を調査する処理の入口であり、prompt 生成、oracle-only のファイルアクセス、隔離 review worktree、実行モデルと推論設定を扱う。

## Read this when
- oracle review の所見について、妥当である理由を列挙する agent call の prompt または起動設定を変更・確認するとき。
- finding と既知の advocate/challenger reasons の受け渡し、または review worktree を起点とする oracle review agent call の構築を調査するとき。

## Do not read this when
- 所見が妥当でない理由を列挙する処理や、擁護・反証を統合する別の review 処理を調査するとき。
- oracle review 以外の agent call 構築や、Structured Output schema の内容だけを確認したいとき。

## hash
- bb66a4a875f3f5484d2831e5d942cdf88e157bc5d8345b8d3052e6cc54adf38f

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
- oracle review で、対象所見が妥当ではない理由を調査し、既知の妥当性理由および既知の反証理由と重複しない新規理由を列挙するエージェント呼び出し定義。
- 隔離済み review worktree を起点に、読み取り専用の oracle review 用 prompt、実行モデル、推論強度、Structured Output schema、索引付け前処理を構築する。
- 対象所見と既知の理由を prompt に埋め込み、反証理由が無い場合は空配列を返す処理への入口となる。

## Read this when
- oracle review の所見に対する反証理由の追加調査や重複排除の挙動を確認するとき
- 反証理由列挙用エージェントの prompt 内容、起動パラメータ、worktree 起点、読み取り権限を変更またはレビューするとき
- この呼び出しが使用する Structured Output schema や oracle review の標準 prompt 構成との関係を確認するとき

## Do not read this when
- 所見が妥当である理由を列挙する処理を確認したいとき
- oracle review の対象所見そのものや仕様断片の内容を直接レビューしたいとき
- 反証理由列挙を伴わない一般的なエージェント呼び出しパラメータや別サブコマンドの実装を確認するとき

## hash
- a08720a68bd538897852fc821346b6cc2adcb0da07621f25f2667855cf9fb0a9
