# `basic.py`

## Summary
- プロンプト生成で共通利用するプレースホルダ対応表の型 `PlaceholderMap` を定義する標準モジュール。プレースホルダ名から置換先の文字列またはパスを対応付けるための入口であり、具体的なプロンプト構築処理を確認する対象ではない。

## Read this when
- プレースホルダの対応関係を表すデータ構造の型定義や、文字列・`Path` を含む置換値の仕様を確認したいとき。
- プロンプト関連コードで共通の型エイリアスの定義元を特定したいとき。

## Do not read this when
- プロンプトの生成手順、テンプレート展開、置換処理の実装を調べるときは、実際のプロンプト構築モジュールを直接読む。
- プレースホルダ対応表の型定義に関係しないプロンプト仕様やCLI挙動を確認するとき。

## hash
- 526fb2d3d3f5fd312f3f1cc48c630d59e91568f38d6ac0d09bc5241792eb1e18

# `complete_prompt.py`

## Summary
- 選択した規定・追加プロンプト・目的・placeholder 定義を統合し、agent call 用の完全な構造化 prompt を構築する関数を定義する。
- file access、routing、oracle/realization、各種 policy の有効化を個別に反映し、placeholder の競合を拒否する。
- prompt の固定部分を前方、変動しやすい placeholder 定義を末尾に配置する構成も担う。

## Read this when
- agent call に渡す完全 prompt の構築順序や構成を変更・確認するとき
- 複数の policy builder と追加 prompt、目的、placeholder をどのように統合するか調べるとき
- placeholder 定義の重複・異値競合時の扱いを確認するとき

## Do not read this when
- 個別の policy や prompt parts の本文だけを変更・確認する場合
- agent call の path context や placeholder の具体的な生成規則を直接確認したい場合
- prompt 構築結果を利用する呼び出し側の責務を調べる場合

## hash
- c9791cc943c8eb9b7f6a711c477311d280bed62a08bdc4c9794edafa3edc1d35

# `editor_input.py`

## Summary
- ユーザー入力用エディタに注入する初期テキストを構築する関数を定義する。使い方・記入の目安と、完全プロンプトのテンプレートをHTMLコメントブロック内にMarkdownとして埋め込み、後続エージェントへ渡す入力ファイルの初期状態を生成する。

## Read this when
- エディタ経由で後続AIエージェントへ渡すプロンプト入力ファイルの初期文面や、完全プロンプトの埋め込み形式を確認・変更するとき。
- 初期テキストの説明見出し、記入指針、HTMLコメントによる非表示化の構築処理を調べるとき。

## Do not read this when
- プロンプト全体のテンプレート内容や置換規則そのものを確認したい場合は、完全プロンプトのテンプレート定義を直接読む。
- 構造化文書ノードの定義やMarkdownレンダリング仕様を確認したい場合は、struct_docの実装を直接読む。

## hash
- 801c5e31f4bbfc2b036f94ce9ef77536f12136fe02cba369a4f477b5b6150d35

# `parts`

## Summary
- oracle と realization の基本概念を説明するプロンプト部品を収録するディレクトリ。両者の役割、下位分類、配置、分類条件と、uncategorised file の定義・分類規則を扱う。
- oracle／realization の区別や関連する基本説明の構成を確認する際の入口となる。

## Read this when
- oracle file、realization file、uncategorised file の意味や分類条件を確認したいとき
- oracle と realization の役割、編集責任、下位分類、配置先を確認したいとき
- oracle／realization の基本説明をプロンプトへ組み込む処理を調査・変更するとき

## Do not read this when
- 特定の oracle 文書・実装・テストの内容や配置規則を確認したいとき
- プロンプト全体の組み立て方や別の説明部品の責務を確認したいとき
- 実際の oracle／realization ファイルを編集・実装するとき

## hash
- bfc0fd68622b89312d2e1a647dac27581c429a5a06fb523c78de7b35e0d31f15

# `policy`

## Summary
- prompt_builder/policy 配下の各ポリシー定義を、INDEX.md から目的別に案内するための対象です。conflict 解消、feedback 報告、ファイルアクセス、INDEX エントリー生成、oracle／realization の agent call 規定、所見判定、routing policy の構築に関する責務を分担します。
- 個別のポリシー実装や関連する prompt 構築処理の入口として機能し、対象ごとに仕様確認・変更の起点を判断できます。

## Read this when
- session join の conflict 解消方針を確認・変更するとき
- agent call 共通の human feedback reporting、ファイルアクセス制約、INDEX.md エントリー生成方針を確認・変更するとき
- oracle file または realization file 向け agent call の instruction、両者の責務境界、所見判定基準を確認・変更するとき
- INDEX.md routing policy の文面や、作業対象に近い文書への到達方針を確認・変更するとき

## Do not read this when
- session join 全体の実行手順や merge 対象仕様を確認する場合
- conflict 解消用 agent call の prompt part 選択や起動パラメータを確認する場合
- feedback 報告や oracle／realization の個別仕様本文、具体的な実装・テスト内容を確認する場合
- PlaceholderMap、SDHeader、SDPolicy、AgentCallPathContext 自体の定義や、一般的な prompt builder 処理を確認する場合

## hash
- 7ea13cf631ef967ba3fb14d69fa8f75649bcb92c6cb4c677f56bfaa9741d6720
