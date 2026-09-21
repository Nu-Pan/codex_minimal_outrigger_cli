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
- 人間が直接記入する editor work file の初期文面を構築する関数を扱う。入力先を示す短い HTML コメントと、後続 AI エージェントへの指示に含めるべき成果・範囲・制約の案内を定義している。

## Read this when
- editor work file の初期表示文面や、人間向けの入力案内を確認・変更したいとき。
- prompt editor input の構築定義から、初期文面の正確な生成箇所を確認するとき。

## Do not read this when
- editor input handoff の target lifecycle、MCP interface、handoff ガイド、上書き処理を確認したいとき。
- editor input の保存・編集・確定手順全体を確認したいときは、prompt editor input の仕様や editor input handoff の実装を直接読む。

## hash
- 03cafd44b4796d454e5d88c18a1e838f441ea7bba43e5968fbffc5ecba1ff92b

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
- prompt_builder が agent call 向けの共通方針文面を構築する oracle source 群。
- feedback 報告、oracle/realization の扱い、ファイルアクセス、文書 routing、editor handoff、conflict 解消、INDEX.md エントリー生成の規定を個別の builder として定義する。

## Read this when
- agent call に注入する共通方針の責務や適用範囲を確認するとき。
- prompt_builder の方針文面を追加・変更するとき。
- 特定の作業種別に対応する policy builder の所在を判断するとき。

## Do not read this when
- 個別 policy の詳細な文面や実装を確認する段階では、対象ディレクトリ全体ではなく該当する Python ファイルを直接読むべきとき。
- prompt_builder の方針以外の実装、テスト、または oracle doc の意味仕様を確認したいとき。

## hash
- 4df12d7b3142fc58756e971376a5e53ff89c517f8303b87d73134ea7938827d9
