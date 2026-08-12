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
- oracle review の新規所見列挙用エージェント呼び出しパラメータを構築する。レビュー対象 oracle file と関連所見を受け取り、隔離済み worktree のパス文脈でレビュー prompt を生成し、oracle file の読み取り専用範囲・標準レビュー指示・Structured Output schema・実行設定を含む AgentCallParameter を返す。

## Read this when
- oracle review の新規所見を列挙するサブコマンドの prompt やエージェント起動パラメータを変更・確認するとき。
- レビュー対象ファイル、関連所見、oracle のパス解決、読み取り専用アクセス、モデル・推論設定、または index preflight の構成を確認するとき。

## Do not read this when
- oracle review の所見内容そのもの、レビュー基準の詳細、または Structured Output schema の定義だけを確認するとき。
- 新規所見列挙以外の oracle review 操作や、一般的な agent call パラメータ構築を直接確認するとき。

## hash
- a63caa587a139b36c565b9524cb6a68cb206a64d7b8aa17966df900d28e33947

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
- oracle review で検出された所見について、提示可否を判定するためのエージェント呼び出しパラメータを構築する。所見本文、妥当性を支持する理由、反対理由を prompt に組み込み、判定用モデル・推論強度・読み取り範囲・Structured Output schema などの起動条件を定義する。

## Read this when
- oracle review の所見を人間へ提示すべきか判定する prompt または agent call パラメータの構築を変更・確認するとき。
- 所見、支持理由、反対理由を入力として判定用の隔離 worktree と oracle-only の読み取り条件を組み立てる処理を調査するとき。

## Do not read this when
- oracle review の所見そのものの検出・生成ロジックを調査するとき。
- 判定結果の Structured Output schema の内容だけを確認するときは、対応する schema 定義を直接読む。
- 一般的な agent call パラメータや別の review 処理の実装を確認するときは、それぞれの定義を直接読む。

## hash
- c0c6286837ced7bc09fda5c0466ae32a9537a35175713b49f4252aa465ba6129

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
- `oracle review` における所見リスト統合用のエージェント呼び出しパラメータを構築する定義。所見内容を埋め込んだプロンプト、oracle 読み取り専用のアクセス制約、Structured Output schema、モデル・推論設定、起動時の索引処理をまとめて指定する。

## Read this when
- `oracle review` の所見統合処理のプロンプトやエージェント起動パラメータを変更・確認するとき
- 所見リストを入力として、重複・矛盾を整理する Structured Output 呼び出しの構成を確認するとき
- oracle review 用の worktree、ファイルアクセスモード、モデル設定、事前索引処理の指定を確認するとき

## Do not read this when
- 所見統合の出力形式そのものを確認したいだけで、呼び出し構築側を調べる必要がないときは、対応する Structured Output schema を直接読む
- oracle review の一般的なレビュー規則や oracle file の内容を確認する場合は、この呼び出し構築定義ではなく、該当する oracle 文書を直接読む
- 所見リストの生成・収集やレビュー実行本体を調べる場合は、それぞれの処理を定義する対象へ直接進む

## hash
- f81e54cf49a51a2ff298959075d6680b8228f4a326cb319e11c6fd59215fd4f3

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
- oracle review で、指定された所見を妥当と判断できる新たな理由を調査するためのエージェント呼び出しパラメータを構築する。所見と既知の賛成・反対理由をプロンプトへ渡し、重複しない追加理由の列挙を求めるレビュー用の入口である。

## Read this when
- oracle review の所見について、妥当性を擁護する理由の調査や、そのためのエージェント呼び出し設定を確認・変更するとき。

## Do not read this when
- 所見が妥当でない理由の調査だけを行うとき。
- レビュー以外のエージェント呼び出しや、一般的なプロンプト構築の実装を確認するとき。

## hash
- 328f57d2c863c27d97b844d4100606ca31b6a6089c06eb4b3645618542fff9c2

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
- oracle review で、指定された所見が妥当ではない理由を調査する agent call の prompt と起動パラメータを構築する。対象所見と既知の賛成・反対理由を prompt に埋め込み、oracle の読み取り専用レビューとして実行できる呼び出し設定を返す。
- レビュー用 prompt の役割・目的・完了条件を組み立て、所見に対する既存理由と重複しない新規の反証理由だけを Structured Output で返すよう指定する。

## Read this when
- oracle review の所見に対する反証理由列挙用 agent call の prompt 構築を変更・確認するとき
- 所見、既知の妥当理由、既知の反証理由をレビュー prompt に渡す処理や、レビュー agent の読み取り権限・モデル・推論設定・実行コンテキストを変更するとき
- この呼び出しが使用する Structured Output schema の対応関係を確認するとき

## Do not read this when
- oracle review の別の判定段階や、反証理由の内容そのものを実装・変更するとき
- 一般的な prompt 構築や agent call パラメータの仕様を確認したいだけで、この反証担当の呼び出し経路が対象でないとき
- 出力形式の詳細だけを確認するときは、対応する Structured Output schema を直接読む方が適切な場合

## hash
- c6d272a57459434467de46e92cd17d42ab04e48d07cb51c22f037d29e42927b1
