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
- oracle と realization の基本概念をプロンプトへ組み込むための PlaceholderMap と SDHeader を構築する関数。oracle file、realization file、uncategorised file の役割・下位分類・分類条件を説明し、パス文脈から取得した work-root を説明文のプレースホルダーへ渡す。

## Read this when
- oracle file と realization file の責務、正本性、編集主体をプロンプトで説明するとき
- oracle doc・oracle src・oracle test、realization implementation・realization test・realization ancillary の分類を扱うとき
- uncategorised file のパス、git ignore、.git に基づく分類条件をプロンプトへ組み込むとき
- AgentCallPathContext から work-root を取得し、PlaceholderMap または SDHeader を構築する処理を変更・確認するとき

## Do not read this when
- 特定の oracle または realization ファイルの仕様・実装・テスト内容を確認するとき
- oracle と realization の詳細な意味仕様を確認するときは、関数内で参照される oracle 文書を直接読むとき
- プロンプト構築における別の説明パーツの責務だけを変更・確認するとき

## hash
- ce7fa1eaf0c4077b6ab99e81fade8ac588a69dc80620397169fb23b288600026

# `policy`

## Summary
- prompt_builder/policy 配下の各 policy 定義ファイルについて、責務と利用目的を INDEX.md で案内するための対象一覧。session join の conflict 解消、feedback 報告、ファイルアクセス制限、INDEX.md エントリー生成、oracle／realization の扱い、所見判定、routing など、agent call に適用する規定の構築入口を扱う。

## Read this when
- agent call に適用する prompt policy の責務や構築経路を確認したいとき
- conflict 解消、feedback 報告、ファイルアクセス、INDEX.md routing、oracle／realization の扱い、所見判定に関する policy 定義を探すとき
- 対象領域に応じた個別 policy ファイルへの入口を判断するとき

## Do not read this when
- 個別 policy の具体的な規定本文や意味仕様だけを確認したいときは、該当する policy ファイルまたは参照先の仕様を直接読む
- 既存の INDEX.md の内容や routing 構造そのものを確認したいとき
- prompt policy と無関係な oracle file、realization file、実装の具体的内容を調査するとき

## hash
- 4e077aa4c6cb082f8499a11d455fdc9d989e25eb7b926d6cf4bcdc1f560b0d89
