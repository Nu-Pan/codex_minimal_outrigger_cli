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
- 選択した規定、補助文面、担当目的、パス由来の定義を統合し、agent 向けの完全な構造化 prompt を構築する入口。
- 基礎規定を先頭にまとめ、個別ポリシー、追加文面、objective、placeholder 定義を所定の順序で配置する。
- placeholder 名の重複は同値のみ統合し、異なる値の定義は拒否して prompt 内のパスコンテキスト分裂を防ぐ。

## Read this when
- agent call 用 prompt の全体構成、規定フラグの反映、補助 prompt の挿入位置を確認するとき。
- placeholder 定義の統合や、同名異値を拒否する契約を確認するとき。
- oracle・realization・routing・INDEX エントリーなどの各ポリシーを完全 prompt に含める経路を追うとき。

## Do not read this when
- 特定の個別ポリシー本文の内容や生成規則だけを確認したいときは、該当する policy builder を直接読む。
- placeholder の具体的なパス値や path context の生成方法だけを調べるときは、パスコンテキストまたは placeholder 定義の担当対象を直接読む。
- agent call の実行、CLI の責務、oracle・realization ファイル自体の規則を確認したいときは、この prompt 構築定義ではなく対応する正本仕様を読む。

## hash
- 13960a4cb2822dc1d407c258248b09c4c8e90377d035cea4f5ad95ae6894c549

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
- merge conflict 解消結果に適用する policy を構築し、両方の oracle file の意図・挙動の保持と、両立不能時の未解消事項としての報告を定める。
- active な prompt editor input へ完成済み content を handoff する際の要求事項、結果報告、失敗時の扱い、直接書き換え禁止を定める。
- 全 agent call 共通の human feedback 報告 policy を構築し、未解決問題の報告手段と、報告してはいけない事項を定める。
- FileAccessMode と path context に応じて、repo-root・work-root・oracle file・realization file などの読み書き制限を構築する。
- INDEX.md エントリー生成時の routing 情報に必要な責務・読む条件・境界と、詳細説明や推測の禁止事項を定める。
- oracle doc と oracle src の正本責務、委譲、優先関係、仕様断片の扱い、oracle file の要求・禁止・許可事項を構築する。
- oracle file の具体的記述に基づく所見の成立条件と、fatal・minor の分類基準、重複報告の禁止を定める。
- realization file 向け policy を構築し、oracle file を正本仕様断片として扱う条件、実装者裁量、最小限の実装、検証要求を定める。
- oracle file と realization file の記述・挙動の適合性を評価する所見 policy を構築し、修正対象とすべき明確な不整合・致命的問題を定める。
- INDEX.md による routing のため、path context から root placeholder を取得し、対象本文へ進む判断規定と INDEX.md の位置づけを構築する。

## Read this when
- session join の conflict 解消結果に求められる oracle file の意図保持や未解消事項の扱いを確認するとき。
- prompt editor input への明示的な handoff 方法、結果区分、失敗時の正式回答を確認するとき。
- agent call 共通の human feedback 報告方法や、報告対象外の問題を確認するとき。
- FileAccessMode ごとのエージェント向けアクセス制限や、repo-root と work-root の関係を確認するとき。
- INDEX.md エントリー生成時に routing 情報へ記載する責務・条件・境界を確認するとき。
- oracle doc と oracle src の責務分担、委譲先、優先関係、oracle file の作成・レビュー規定を確認するとき。
- oracle file の問題を所見として扱う基準や fatal・minor の分類を確認するとき。
- realization file の実装方針、oracle file との関係、検証要求、不要実装の整理方針を確認するとき。
- oracle file と realization file の適合性に関する所見の根拠と修正対象の基準を確認するとき。
- INDEX.md を起点とした本文の探索規定や、本文と INDEX.md が食い違う場合の扱いを確認するとき。

## Do not read this when
- session join の意味仕様や oracle file 規定の優先順位そのものを確認するとき。
- handoff の意味仕様そのもの、または通常のファイル編集方法を確認するとき。
- human feedback 報告の意味仕様そのものや、個別 agent call の別 policy を確認するとき。
- アクセス制限の正本仕様、Codex CLI の sandbox enforcement、個別 oracle・realization file の内容を確認するとき。
- 既存の INDEX.md エントリーや、routing policy の根拠となる意味仕様を直接確認するとき。
- oracle doc・oracle src の意味仕様そのもの、realization file の配置・実装責務、または test execution を確認するとき。
- 個別 oracle review の意味仕様や、所見の定義そのものを確認するとき。
- realization file の意味仕様や判断基準、または policy 構築後の agent call 実行を確認するとき。
- oracle file 自体の仕様不足や定義上の問題を検討するとき。
- INDEX.md の具体的な意味仕様、または PlaceholderMap・SDHeader・SDPolicy の一般実装を確認するとき。

## hash
- b0c4e4ba71e7ae3432443a1985feb58065d5fd9498b0470631f1b917160ac3dd
