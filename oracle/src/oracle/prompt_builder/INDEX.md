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
- agent call に渡す完全な構造化 prompt を、基礎規定・任意ポリシー・目的・追加文面・placeholder 定義から組み立てる入口。
- ファイルアクセス、routing、oracle/realization、feedback、INDEX エントリーなどの各ポリシーを独立したフラグで選択し、placeholder の競合を拒否しながら統合する。

## Read this when
- agent 向け prompt の構成順序、任意ポリシーの注入条件、caller 指定の目的や追加 prompt の組み込み方を確認するとき。
- path context 由来の placeholder 定義と追加定義の統合、および同名異値の拒否動作を調べるとき。

## Do not read this when
- 個別ポリシーの具体的な文面や生成ロジックだけを確認したいときは、対応する policy モジュールを直接読む。
- prompt に含まれる oracle、realization、routing、file access などの個別規定の内容自体を確認したいとき。

## hash
- 1b0d6941e94d7a3bb70fff393f0b2f4ee0f151d5556d58b6dbf8196677b8ca81

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
- agent call 向けの各種 prompt policy を構築する実装群への入口。ファイルアクセス、oracle／realization、routing、conflict 解消、feedback 報告、editor handoff、INDEX.md エントリー生成、適合性所見に関する個別 policy の構築責務を扱う。

## Read this when
- agent call の prompt policy 生成処理を調査・変更するとき
- 複数の共通 policy のうち、どの policy builder が担当するかを判断するとき
- INDEX.md routing 用 instruction や oracle／realization 関連 instruction の構築経路を確認するとき

## Do not read this when
- policy の意味仕様そのもの、oracle doc の規定、realization の設計・実装を確認したいとき
- 個別 policy の詳細だけを調べる場合は、該当する policy builder を直接読む
- 生成済み prompt の実行処理や、SDHeader・SDPolicy など共通データ型の実装だけを確認したいとき

## hash
- 25cd9d33fbc3b8ebdca0919263ba3f84e07dd17adb061a70f3baa8d01c6a0e63
