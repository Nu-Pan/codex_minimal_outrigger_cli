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
- oracle file、realization file、uncategorised fileの基本概念と分類規則を説明するプロンプト部品を構築する関数。oracle doc・oracle src・oracle testとrealization各分類の役割、配置、正本責務、委譲、優先関係をまとめ、path_contextに基づくプレースホルダー展開情報と階層化ヘッダーを返す。個別仕様ではなく、oracleとrealizationの一般関係・分類を確認する入口。

## Read this when
- oracleとrealizationの基本的な役割、正本関係、生成・委譲関係を確認するとき
- oracle doc・oracle src・oracle test、realization implementation・realization test・realization ancillary、uncategorised fileの分類や配置を確認するとき
- oracleとrealizationの基本説明を構築するプロンプト処理を変更・調査するとき

## Do not read this when
- 個別の意味仕様を確認するときは、対応するoracle docを直接読む
- 委譲された正確な実装・定義を確認するときは、対象のoracle srcを直接読む
- PlaceholderMapやSDHeaderの共通仕様・実装だけを確認するときは、対応する共通部品を直接読む
- プロンプト全体の組み立て順序や他のプロンプト部品を確認するときは、該当するprompt builderを直接読む

## hash
- 8476db3067fdfaf3da968c6a510edf9296c20bb95a42d5b66d5e32de9b0b13d2

# `policy`

## Summary
- プロンプト生成に用いる policy 定義群をまとめたディレクトリ。conflict 解消、feedback 報告、ファイルアクセス、INDEX.md routing、oracle／realization の扱いと所見判定など、各 agent call の指示文面を構築する入口を提供する。個別 policy の責務を確認・変更する際は該当モジュールへ進む。

## Read this when
- agent call に共通または特定の規定をプロンプトへ組み込む処理を調査・変更するとき
- ファイルアクセス、INDEX.md routing、oracle／realization、conflict 解消、feedback 報告のいずれかの policy 構築経路を確認するとき
- 複数の policy 定義の役割分担や、該当する個別モジュールへの入口を確認するとき

## Do not read this when
- 個別の oracle file、realization file、INDEX.md、または意味仕様そのものを確認することが目的のとき
- SDHeader・SDPolicy など共通データ構造だけを調査するとき
- プロンプト policy と無関係な CLI 実装や一般的な agent call 処理を調べるとき

## hash
- 29eb50c0417697675226b2e886b9d7f5a3c5f8d8fe5c80f6e0febe6eef1f3d76
