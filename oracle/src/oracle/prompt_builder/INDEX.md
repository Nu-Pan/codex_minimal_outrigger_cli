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
- 選択されたポリシー、呼び出し固有の目的、追加文面、placeholder 定義を所定の順序で統合し、agent call 用の完全な構造化 prompt を構築する中心実装。
- placeholder の重複定義を検査し、同名異値を拒否することで、呼び出し内のパス文脈や入力定義の不整合を防ぐ。

## Read this when
- agent call に渡す完全 prompt の構成順序、ポリシーの有効化、目的情報や動的入力の注入、placeholder 定義の統合を変更・確認するとき。
- 複数の prompt builder 部品をどの順序で組み合わせ、どの条件で含めるかを調べるとき。

## Do not read this when
- 特定のポリシー本文や prompt 断片の内容だけを確認・変更する場合は、対応する policy または parts の実装を直接読む。
- 完全 prompt の呼び出し元がどの場面でこの builder を呼ぶかを調べる場合は、acp_builder 側の呼び出し実装を直接読む。

## hash
- a6adab4c25e7bebecb0dfc393aaa0d172684b09d4bd954c53bfe624891526ce3

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
- prompt_builder が agent call 向けに埋め込む各種 policy の構築定義をまとめるディレクトリ。
- INDEX.md routing、file access、oracle／realization、feedback observation、conflict resolution、editor input handoff など、作業種別ごとの instruction 文面と placeholder の構築入口を提供する。
- 個別 policy の責務・規定文面・関連 path context の扱いを確認するための下位ファイル群への入口。

## Read this when
- agent call の prompt に組み込まれる policy の種類、文面、適用条件、または構築処理を確認・変更するとき。
- 複数の prompt policy のうち、oracle／realization、routing、file access、feedback reporting など特定領域の構築定義を探すとき。
- policy builder が返す構造化文面や placeholder の組み立て方を調査するとき。

## Do not read this when
- policy の意味仕様そのものを確認したいとき。各実装の docstring が参照する oracle/doc 配下の正本仕様を直接読むべきである。
- prompt builder の共通構築処理、構造化文書型、FileAccessMode、path context などの定義だけを確認したいときは、それぞれの定義元を直接読むべきである。
- 個別の agent call の実行処理や、生成された prompt の実際の呼び出し結果を確認したいとき。

## hash
- eebd402ded5725ce86c97aac6f9677832f521a8f6e0ce55f8ffd449358efcd3b
