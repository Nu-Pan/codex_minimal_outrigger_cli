# `acp_builder`

## Summary
- AI エージェント呼び出しに渡す論理パラメータと Structured Output schema の正本仕様断片を扱う領域。モデルクラス、reasoning effort、ファイルアクセスモード、prompt、cwd、indexing preflight 有無などの共通定義と、各サブコマンド向け呼び出し設定への入口になる。
- INDEX.md エントリー生成、oracle file レビュー、fork 適用後レビュー、session join の conflict marker 解消、TUI 起動前後のパラメータ選定など、cmoc が AI agent call を組み立てる仕様を確認するためのまとまり。

## Read this when
- cmoc のサブコマンドがどの prompt、Structured Output schema、モデル設定、ファイルアクセス権限、preflight 設定で AI エージェントを呼び出すか確認したいとき。
- agent call parameter の共通データ構造や論理モデル名、論理 reasoning effort、Structured Output schema 指定方法を確認したいとき。
- INDEX.md エントリー生成、oracle file レビュー、fork 適用後の差分要約・所見対応、session join の conflict marker 解消、TUI 用パラメータ選定の正本仕様断片を探すとき。
- prompt と Structured Output schema の対応関係、または個別 agent call の入力契約と出力契約を実装・テストへ反映する前に確認したいとき。

## Do not read this when
- AI エージェント呼び出しではなく、CLI 引数処理、branch 操作、diff 取得、merge 実行、保存処理、表示整形などの実行制御実装を調べたいとき。
- oracle standard、realization standard、apply review standard、index entry standard など、レビューや文書品質の基準そのものを確認したいとき。
- バックエンド API へ送る実際のリクエスト形式、具体的なモデル名解決、agent CLI 実行処理など realization src 側の実装詳細を調べたいとき。
- パスキーワード、work root 解決、prompt builder の共通構成、markdown rendering、placeholder 解決など、agent call parameter 周辺の別概念を直接確認したいとき。

## hash
- 7142a5cb168c925cc744aea3b6f4a520fa798536546f83fa9dc8c3433391887b

# `other`

## Summary
- cmoc の正本実装断片のうち、設定、パスモデル、規範モデル、構造化 Markdown レンダリングなど、特定サブコマンドに閉じない基盤的な型・変換処理をまとめる領域。
- リポジトリごとの設定値、ルートプレースホルダ付きパスの解決、規範文書の構造化、階層文書の Markdown 化といった、他の仕様断片や実装が参照する共通概念を確認する入口になる。

## Read this when
- cmoc 全体で共有される設定値、パス表記、ルート解決、規範データ構造、構造化文書レンダリングの正本実装断片を探すとき。
- Codex CLI に渡すモデル設定やループ・処理件数の既定値など、リポジトリごとの挙動設定を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのパスプレースホルダの意味、探索条件、実パスとの相互変換を確認したいとき。
- 規範文書をプログラム上で保持するための構造、要求ラベル、構造化ドキュメントへの変換を確認したいとき。
- 階層的な文章データを Markdown として出力する helper の見出し生成、本文・コードブロック処理、空行やインデント正規化を確認したいとき。

## Do not read this when
- CLI サブコマンドごとの利用者向け入出力、実行フロー、状態ファイルの仕様を直接確認したいとき。
- oracle file と realization file の管理方針、INDEX.md のルーティング規則、開発時の読み書き制約そのものを確認したいとき。
- doctor、apply fork、review oracle など個別機能の処理手順やワークフローを確認したいとき。
- 生成済み Markdown や個別の規範本文の意味だけを読みたいとき。

## hash
- 66aafe6cd99b4fe22719ea7a51744c2f0c94d4056ef581b0d403119240f4355c

# `prompt_builder`

## Summary
- agent call に渡すプロンプトの構築に関する基本型、完全プロンプトの組み立て処理、標準文書や読み書き規則などのプロンプト部品を扱う領域。
- 役割・概要・ゴール・補助プロンプト・ファイルアクセス制限・ルーティング規則・各種標準の注入指定を統合し、静的部分、動的部分、プレースホルダ定義の配置を決める入口になる。
- oracle file と realization file の責務境界、品質基準、INDEX.md エントリー規範、レビュー規範など、AI に渡す共通規範プロンプトを生成する下位要素への入口でもある。

## Read this when
- agent call 用の完全なプロンプトが、どの部品からどの順序で構築されるかを確認・変更したいとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard などの注入指定が、他のプロンプト部品の追加へどう波及するかを確認したいとき。
- ファイルアクセス制限、ルーティング規則、補助プロンプト、プレースホルダ定義を完全プロンプトへ統合する位置や責務を調べたいとき。
- プロンプトキャッシュヒット率を意識した、静的プロンプト、動的プロンプト、プレースホルダ定義の分離と配置を確認したいとき。
- プロンプト生成で使うプレースホルダ名から文字列またはパスへ置換する mapping の基本型を確認したいとき。
- AI に注入する共通規範として、oracle file、realization file、INDEX.md エントリー、ファイル読み書き、レビュー所見の標準文書を確認・変更したいとき。

## Do not read this when
- 特定の CLI サブコマンド、状態ファイル、入出力形式、パスモデルなど、個別プロダクト仕様を調べたいとき。
- 個別の標準文書本文だけを確認したいときは、この領域全体ではなく、該当するプロンプト部品を直接読む方が適切。
- 構造化ドキュメント、標準文書、要求、プレースホルダ mapping などの汎用データ構造そのものを調べたいだけのとき。
- 生成済みプロンプトが実際にどこで agent call へ渡されるかを追いたいときは、呼び出し側の実装を読む方が適切。
- cmoc のパス概念そのもの、または `<cmoc-root>` や `<work-root>` などの意味を調べたいとき。
- 実装ファイルやテストファイルの現在構造を把握して直接修正したいだけで、プロンプト生成や共通規範の注入に関係しないとき。

## hash
- 6d22edbfda78b6d2616c3e6aa3c260d395390f16d7efa659bc1815aa1b78e4f5
