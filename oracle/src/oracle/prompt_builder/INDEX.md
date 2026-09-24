# `basic.py`

## Summary
- プロンプト構築関数間で共有する、プレースホルダ名と文字列またはパスの置換値との対応型を定義する。置換マップの型を確認する入口であり、プロンプトの組み立てや規定文面は各 builder が担う。

## Read this when
- プロンプト構築関数が受け渡す置換マップのキーや値の型を確認・変更するとき。

## Do not read this when
- 完成プロンプトの構成や有効化条件を調べるときは、プロンプト全体を組み立てる実装を読む。
- 特定のポリシーやプロンプト部品の文面を調べるときは、その内容を構築する実装を読む。

## hash
- f8a558f24e4b59e54e49e1729d4c10dfd1b596dc0b1531a5b8e9a8e2f9a6194a

# `complete_prompt.py`

## Summary
- 呼び出し側が選んだ共通規定や追加文面、タスク情報をまとめ、置換定義を統合して agent 向けの完全な prompt を構築する。
- prompt の構成順や各規定を含める条件、同じ名前の置換定義が競合した場合の扱いを確認する入口。個別の規定文を作る builder 群と、具体的な依頼内容を指定する呼び出し側の間に位置する。

## Read this when
- 完全な prompt の共通構成や順序、どの条件で各区画が加わるかを変更・確認するとき。
- 呼び出し側や追加 prompt から集めた置換定義の統合方法、競合時の挙動を変更・確認するとき。

## Do not read this when
- 個別の規定や方針の文面を変更するときは、その文面を構築する対応 builder を読む。
- 特定の agent 呼び出しでどの規定や追加文面を選ぶか、どのタスク情報を渡すかを確認するときは、その呼び出し側を読む。

## hash
- 1b0d6941e94d7a3bb70fff393f0b2f4ee0f151d5556d58b6dbf8196677b8ca81

# `editor_input.py`

## Summary
- エディタ起動前に表示する、人間向けの短い案内文を返す。案内の正確な文面はこの構築定義が担い、依頼本文には含めない。

## Read this when
- エディタ起動前に人間へ表示する案内の文面や、その表示内容を変更・確認するとき。

## Do not read this when
- editor input のライフサイクルや確定手順を調べるときは、その手順を定める仕様から確認する。
- 完全 prompt の構築や handoff のガイド・target の処理を調べるときは、それぞれを担う prompt builder または handoff の仕様から確認する。

## hash
- ed6c215c953dd93134584d847eb261a0d68073e57ead7513cab2ee4cded3e815

# `parts`

## Summary
- `oracle file`、`realization file`、`uncategorised file` の役割と分類を agent 向けプロンプトに示す基本説明文を構築する。分類の意味仕様や実際の列挙処理ではなく、その説明文の表現を担う。

## Read this when
- 生成プロンプトでの各 file 種別の区別や分類説明を変更・確認するとき。
- 完成プロンプトにこの基本分類説明が組み込まれるかを確認するとき。

## Do not read this when
- 分類の意味仕様や列挙アルゴリズムを変更・検証するときは、分類を定める oracle docs または実際の列挙処理を直接確認する。
- file を扱う判断基準や caller 固有の制約など、基本分類説明以外の prompt policy を変更するときは、該当する policy を直接確認する。

## hash
- 15ceae959181089e7d69c5cbc8d976b1c3727958999930a3bc56388caacf0f23

# `policy`

## Summary
- agent call の prompt に個別に挿入する規定文面を組み立てる builder 群です。
- ファイルアクセス、routing、oracle・realization、INDEX エントリー、所見、feedback、handoff、conflict 解消の規定を扱います。意味仕様は各 builder が参照する正本にあり、ここでは prompt 用文面を構築します。

## Read this when
- prompt に含まれる個別規定の文面を調べたり変更したりするとき。
- 特定の規定領域を担当する builder と、その生成内容を確認するとき。

## Do not read this when
- 規定の正本上の意味や変更可否を判断するときは、builder が案内する oracle doc を直接読んでください。
- 規定の有効化条件や prompt 全体の組み立て順を調べるときは、prompt の構築側を直接読んでください。

## hash
- c85472cf46bb89ab21d6ffb46302995d38d40aa5edaa9487ea3c6a2675b0f19d
