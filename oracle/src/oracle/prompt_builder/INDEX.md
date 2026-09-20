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
- 選択した規定、追加プロンプト、呼び出し固有の目的、プレースホルダー定義を順序付けて統合し、agent 呼び出しへ渡す完全な構造化 prompt を構築する。
- 各 prompt 部分のプレースホルダー定義を衝突検出付きで統合し、同名異値の定義を拒否することで、呼び出し内のパス文脈の一貫性を保つ。

## Read this when
- agent 呼び出しへ渡す prompt の構成順序や、各種 policy フラグがどの規定を有効化するかを確認するとき。
- 追加 prompt・目的情報・path context 由来のプレースホルダーが最終 prompt にどう組み込まれるか、または定義衝突時の挙動を確認するとき。

## Do not read this when
- 個別の policy や prompt 部分の本文を変更・確認する場合は、この統合処理ではなく対応する builder を直接読む。
- agent 呼び出しの path context 自体やプレースホルダーの元データを確認する場合は、path context の定義元を直接読む。

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
- agent call に埋め込む各種ポリシー文面の構築定義をまとめたディレクトリ。
- ファイルアクセス、oracle／realization の責務、feedback 報告、routing、INDEX.md エントリー、editor handoff、conflict 解消など、個別の作業条件に応じた規定文面を生成する。
- ポリシーの適用条件や構築内容を変更・確認するときの入口であり、実際の仕様本文や個別機能の実装を調べる入口ではない。

## Read this when
- agent call に渡される共通または作業種別固有のポリシーを追加・変更・確認するとき。
- ファイルアクセスモード、oracle／realization の扱い、INDEX.md 生成、routing、feedback 報告などの指示文面がどこで構築されるか調べるとき。
- 複数のポリシー構築関数にまたがる prompt_builder の挙動を確認するとき。

## Do not read this when
- 正本仕様そのものの意味や要求を確認したいときは、各ファイルの NOTE が示す oracle/doc の仕様を直接読む。
- ポリシーを実際に組み合わせて agent call を生成する流れを調べたいときは、prompt_builder の呼び出し側を直接読む。
- 個別の実装・テストの挙動や不具合を調べるだけなら、このポリシー定義群ではなく該当する realization code または realization test を読む。

## hash
- 4660bf87f78374397dc3926501123161537f907a6bffbb66ffce6634101b7309
