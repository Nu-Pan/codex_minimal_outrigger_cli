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
- 各種ポリシー、補助文面、作業目的、パス用 placeholder を統合し、agent call に渡す完全な構造化 prompt の構築入口。
- 有効化されたポリシーだけを所定の順序で追加し、placeholder 定義の衝突を拒否して一貫した prompt を生成する。

## Read this when
- agent 向け prompt 全体の構成順序や、基礎規定・個別規定・目的・placeholder の組み立て方を変更または確認するとき。
- 新しい prompt policy や補助 prompt を完全 prompt に組み込む位置と有効化条件を判断するとき。
- 同名 placeholder の統合や異値衝突時の扱いを確認するとき。

## Do not read this when
- 個別ポリシーの本文や、そのポリシー固有の規則だけを変更・確認する場合は、対応する policy 実装を直接読む。
- placeholder のパス文脈や構造化文書型の仕様だけを確認する場合は、対応する path model または struct document の実装を直接読む。

## hash
- 8384e966043491a8d273f45b1696d0d50df4fcebbcc8f9eacf73bcf82a9d2697

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
- agent call 向けの各種 prompt policy builder をまとめる入口。ファイルアクセス、oracle／realization、routing、INDEX.md エントリー、feedback 報告、conflict 解消などの規定文面を個別の責務ごとに構築する。

## Read this when
- agent call の prompt policy 生成経路や、対象となる規定文面の構築責務を調べるとき。
- 特定の policy builder が担う要求・禁止・許可事項や、関連する placeholder・header の組み立てを確認するとき。

## Do not read this when
- policy の根拠となる意味仕様や oracle／realization の正本規定を確認するときは、該当する oracle file を直接読む。
- 生成された prompt の実行処理や、CLI の実際のファイルアクセス・conflict 解消処理を確認するときは、対応する実装を直接読む。

## hash
- 636ae6f6435091b52dc231d6eb815385240799bf94933d2706ab8a46f57abd42
