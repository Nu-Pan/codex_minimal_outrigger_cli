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
- oracle と realization の基本概念を説明するプロンプト断片を構築する。
- oracle file、realization file、uncategorised file の役割、下位概念、パス・git ignore・.git に基づく分類方法を扱う。
- パス用プレースホルダーを展開可能な構造化文書ヘッダーとして組み立てる処理への入口である。

## Read this when
- oracle file と realization file の責務や生成関係を確認・変更するとき
- oracle doc、oracle src、oracle test、realization implementation、realization test、realization ancillary の分類を確認するとき
- uncategorised file のパス、git ignore、.git による分類条件を確認するとき
- この説明を PlaceholderMap と SDHeader を用いて構築する処理を追跡するとき

## Do not read this when
- oracle と realization の意味仕様そのものを確認するとき
- プロンプト全体の組み立てや PlaceholderMap、SDHeader の一般仕様だけを確認するとき
- 実装・テストの具体的な配置や挙動を調査するとき

## hash
- 83945362a1d47872fc2949b0af2fcdc1c3b5ddcc317626d697ee3d9c0ce2f929

# `policy`

## Summary
- prompt builder が agent call 向けの各種 policy を構築する実装群を収めるディレクトリ。conflict 解消、feedback 報告、ファイルアクセス、INDEX.md routing、oracle／realization の instruction、所見判定など、個別の prompt policy の生成入口を扱う。各ファイルの責務や生成規定を確認・変更するときの入口として利用する。

## Read this when
- agent call に注入する prompt policy の構築処理を調査・変更するとき
- conflict 解消、feedback 報告、ファイルアクセス、INDEX.md routing、oracle／realization、所見判定のいずれかの policy 生成責務を確認するとき
- 個別 policy の責務に応じて、このディレクトリ内の該当ファイルへ進む必要があるとき

## Do not read this when
- policy の根拠となる意味仕様や oracle file の本文を確認したいとき
- 生成済み prompt の実行処理や、PlaceholderMap・SDHeader・SDPolicy など共通型の実装詳細だけを調べるとき
- realization／oracle file の実装・挙動そのものや、INDEX.md の既存エントリーを確認するとき

## hash
- d7def112d2bcbc71be43a534b3e276b3d207c694264313decc919f5c79374013
