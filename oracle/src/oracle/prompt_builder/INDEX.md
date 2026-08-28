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
- oracle と realization の基本概念・責務・下位分類・ファイル分類条件をプロンプトに組み込む関数。対象ディレクトリにある基本概念の入口。

## Read this when
- oracle file と realization file の役割や編集主体、正本仕様との関係を確認するとき。
- oracle doc・src・test、realization implementation・test・ancillary の区分を確認するとき。
- ファイルが oracle、realization、uncategorised のどれに分類されるか、パス・git ignore・.git による条件を確認するとき。

## Do not read this when
- 個別の oracle 文書、実装、テスト、補助ファイルの内容や詳細仕様を確認したいときは、対応する対象を直接読む。
- プロンプト部品の共通構築方法や、INDEX.md の生成・探索規則だけを確認したいとき。

## hash
- 11fdebe915f6bc100905ce43e60b6e379d88ab51f3caa587627a16810c95f172

# `policy`

## Summary
- agent call 向けの prompt builder policy 群をまとめたディレクトリ。conflict 解消、feedback 報告、ファイルアクセス、INDEX.md routing、oracle／realization、所見判定など、各作業領域の規定文面を構築する入口を提供する。

## Read this when
- prompt builder における共通または作業種別別の policy 構築責務を調べるとき
- agent call のファイルアクセス、routing、oracle／realization、conflict 解消、所見判定、feedback 報告に関する指示生成を確認・変更するとき
- 対象 policy の責務に応じた具体的な prompt 構築ファイルを特定するとき

## Do not read this when
- 個別 policy の意味仕様そのものを確認するときは、各 policy が参照する oracle の仕様を直接読む
- 生成済みプロンプトの実行規則や Codex CLI のサンドボックス設定を確認するとき
- realization や oracle の具体的な実装・仕様本文を確認するときは、該当する realization file、oracle file、または設計規則へ直接進む

## hash
- ceaf60626c4641336dd5d600594c0ae367b36f5622f0a1ab08204ec8be75b910
