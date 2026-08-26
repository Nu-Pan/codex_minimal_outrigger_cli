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
- oracle と realization の基本概念・役割・分類条件を説明するプロンプト断片を構築する関数。oracle file、realization file、uncategorised file、および各下位分類の説明を組み立てる際の入口となる。

## Read this when
- oracle と realization の役割や分類方法を説明するプロンプトを変更・確認するとき
- oracle doc・oracle src・oracle test、realization implementation・realization test・realization ancillary の定義を確認するとき
- oracle file、realization file、uncategorised file の分類条件を扱うとき

## Do not read this when
- oracle と realization の正本仕様そのものを確認するときは、参照先として示された oracle 文書を直接読む場合
- 個別の prompt builder 部品や PlaceholderMap・SDHeader の実装を確認するときは、それぞれの対象を直接読む場合
- INDEX.md や AGENTS.md など分類対象外ファイルの扱いだけを確認するとき

## hash
- c1f2a677da54e277eb63b538bc1e82a59c4094ff7a0167a4d05216dabf9ae3ad

# `policy`

## Summary
- agent call 向けの各種 prompt policy 構築定義をまとめるディレクトリ。conflict 解消、feedback 報告、ファイルアクセス、INDEX routing、oracle／realization の指示、findings 判定などを扱い、それぞれの policy 実装へ進む入口となる。

## Read this when
- prompt builder の policy 構築処理を調査・変更するとき
- agent call に適用されるアクセス制限、routing、oracle／realization、レビュー所見、feedback 報告、conflict 解消の規定を確認するとき
- 特定の policy 定義の責務や構成を追跡するとき

## Do not read this when
- 個別の oracle file、realization file、意味仕様、既存 INDEX.md の内容を直接確認することが目的のとき
- prompt policy と無関係な CLI 実装や通常のプロンプト生成処理だけを調査するとき
- 特定の下位 policy の内容だけを確認したい場合は、該当する下位ファイルを直接読むとき

## hash
- 66526cacd25ec587b54b019c8335520d9ccb56a736d0d94730793b7b165fe8c4
