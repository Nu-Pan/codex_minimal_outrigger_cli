# `basic.py`

## Summary
- プレースホルダ名と、文字列またはパスによる置換値の対応を表す型定義。

## Read this when
- プレースホルダ置換値を保持するマップの型や、値としてパスを許容する定義を確認したいとき。

## Do not read this when
- プレースホルダの置換処理そのものや、プロンプト生成全体の規則を確認したいとき。

## hash
- f8a558f24e4b59e54e49e1729d4c10dfd1b596dc0b1531a5b8e9a8e2f9a6194a

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
- oracle file と realization file の役割・正本関係・下位概念を説明するプロンプト部品への入口
- oracle／realization／uncategorised file をパス、git ignore、.git metadata から分類する基本条件を扱うプロンプト部品への入口

## Read this when
- agent call のプロンプトに oracle file と realization file の基本知識を組み込む処理を変更・調査するとき
- oracle／realization／uncategorised file の分類条件を説明するプロンプト構築部品を確認するとき

## Do not read this when
- oracle と realization の責務やファイル列挙を正本仕様として確認するとき
- 実際のファイル分類ロジックや個別の oracle／realization ファイルを確認するとき

## hash
- 15ceae959181089e7d69c5cbc8d976b1c3727958999930a3bc56388caacf0f23

# `policy`

## Summary
- agent call 向けプロンプトに組み込む各種 policy 文面の構築定義をまとめた入口。ファイルアクセス、oracle・realization、routing、INDEX.md エントリー、conflict 解消、feedback 報告、editor input handoff など、個別の規定生成責務へ進むための階層。

## Read this when
- agent call の policy 文面を構築・変更・検証するとき。
- 対象が file access、oracle、realization、routing、INDEX.md エントリー、conflict 解消、feedback 報告、editor input handoff のいずれかに関する場合に、該当する policy 定義への入口を確認するとき。

## Do not read this when
- 個別 policy の意味仕様や正本規定そのものを確認する場合は、対応する仕様文書を直接読むとき。
- prompt builder の policy 以外の実装、実際に生成されたプロンプト、または realization・oracle の具体的な内容を確認する場合。

## hash
- 0554e67574c13677943bfba1d668f7564e4ca894d44ca124c69a88a20843d114
