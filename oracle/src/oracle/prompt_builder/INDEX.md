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

# `merge_conflict_resolution.py`

## Summary
- run join と session join に共通する競合解消 prompt の構築入口。共通の目的・調査範囲・commit 参照入力を、呼出元のアクセス範囲や追加指示とともに完全 prompt に組み立てる。
- 競合解消の意味上の判断基準や、各 join 固有の起動条件を定める対象ではない。

## Read this when
- run join と session join が共有する競合解消 prompt の目的、Git 参照入力、追加指示の組み込み方、適用する共通規定を確認・変更するとき。

## Do not read this when
- 競合解消の意味上の判断基準や報告要件を確認・変更するときは、正本仕様または共通の競合解消方針の定義を読む。
- 完全 prompt への共通規定や文面の統合方法を変更するときは、汎用 prompt 構築の定義を読む。
- run join または session join の個別のアクセス範囲、起動条件、追加指示を変更するときは、その join 固有の call 構築定義を読む。

## hash
- e1a7317d4ddd169865e0804dcc070a2962827116a4663cb3a51fee42fae7550a

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
- agent call 向けの policy 文面を組み立てる層です。feedback 報告、ファイルアクセス、oracle と realization の扱い、適合性所見、競合解消、INDEX routing と entry、editor handoff の個別規定を扱います。
- 一部の builder は file access mode や path context に応じて文面や参照値を構成します。

## Read this when
- これらの規定の文面や、mode・path context に応じた構築方法を変更・調査するとき。
- 特定の policy が担う制約や、その agent call 向け文面の生成元を確認するとき。

## Do not read this when
- 完全 prompt の構成、policy の選択条件、配置順を調べるときは、prompt 統合側を直接読む。
- エディタ起動前の案内や、競合解消 prompt 全体の構築を調べるときは、それぞれの専用 builder を直接読む。
- policy の正本となる意味仕様を変更・判断するときは、該当する oracle doc を直接読む。

## hash
- 3633df97a332c1d5b7f37a3e994ae78804e1727d6022c2c6b313988982972944
