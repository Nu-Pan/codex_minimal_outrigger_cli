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
- エディタ起動前に stderr へ表示する、人間向け入力案内の文面を構築する関数を定義する。
- 完全な prompt や editor input handoff のライフサイクルではなく、直接入力時の短い console 案内だけを担当する。

## Read this when
- エディタ起動前に表示する入力案内の文面を確認・変更するとき。
- 人間が editor work file に記入すべき内容の案内を調べるとき。

## Do not read this when
- 完全 prompt の構築、prompt skeleton、または agent call 固有の prompt 文面を調べるとき。
- editor work file の生成・検証・保存・削除や handoff target のライフサイクルを調べるときは、対応する lifecycle または handoff の仕様・実装を直接読む。

## hash
- 3de6b88dbdaa9fe6a5c264e7320b747738cac05b66a607ff2dc2ec77f46f6c2f

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
- agent call に埋め込む各種 policy 文面の構築定義をまとめた領域。oracle／realization の扱い、ファイルアクセス制限、INDEX.md routing、feedback 報告、editor handoff、conflict 解消、適合性所見など、作業種別ごとの規定生成が必要な場合の入口となる。
- 各ファイルは個別の policy 構築関数を提供し、`SDHeader` と `SDPolicy` による要求・禁止・許容事項、および必要な path placeholder を定義する。ファイルアクセス policy だけはアクセスモードにより内容を分岐し、共通規定がないモードでは `None` を返す。
- この領域を変更・確認する際は、生成される agent 向け instruction の規定文面や、policy の適用対象を調べる場合に進む。正本仕様そのものや prompt 全体の組み立てを確認する場合は、参照先の oracle 文書または上位の prompt_builder 定義を直接読む。

## Read this when
- agent call に含める規定の種類、適用条件、要求・禁止事項を確認したいとき。
- oracle／realization の責務、INDEX.md の routing、ファイルアクセス mode、feedback 報告、editor handoff、conflict 解消の policy 文面を変更・レビューするとき。
- policy 文面に必要な root path placeholder の渡し方や、mode に応じた生成結果の分岐を確認したいとき。

## Do not read this when
- 正本仕様の意味や要件そのものを確認したいときは、各ファイルの NOTE に示された oracle 文書を直接読む。
- 生成された prompt の全体構成や policy の呼び出し順を確認したいときは、上位の prompt_builder 実装を直接読む。
- 対象となる一つの policy の文面だけを調べる場合は、このディレクトリ全体ではなく該当する policy 定義ファイルへ直接進む。

## hash
- c85472cf46bb89ab21d6ffb46302995d38d40aa5edaa9487ea3c6a2675b0f19d
