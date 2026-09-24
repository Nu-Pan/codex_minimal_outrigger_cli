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
- run join・feedback の自動 join・session join で共有する、競合解消 agent 向け prompt を組み立てます。共通の目的と作業範囲、両 commit の参照入力、Git から変更と競合状態を取得する指示、適用する共通 policy をまとめます。
- 呼び出し元固有の追加指示も共通 prompt に組み込みます。各 join の起動設定や競合解消方針の具体的な文面ではなく、それらを組み合わせる入口です。

## Read this when
- join 間で共通する競合解消 prompt の目的、入力、調査指示、policy の構成を変更・確認するとき。
- agent に渡す commit 情報や、進行中の競合状態を Git から取得させる指示を変更・確認するとき。
- 呼び出し元固有の追加指示を共通 prompt に取り込む方法を確認するとき。

## Do not read this when
- 競合解消の判断基準、編集上の制約、完了報告の具体的な文面を変更するときは、競合解消 policy の定義を読む。
- 個別 join の起動パラメータ、アクセス範囲、追加指示を変更するときは、その join の call 構築を読む。
- join の状態管理・復旧などの契約や、完全 prompt の汎用的な構成処理を変更するときは、それぞれの仕様または共通構築処理を読む。

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
- agent call の完全 prompt に組み込む共有規定文面を構築する。ファイルアクセス、oracle・realization file の扱い、適合性所見、INDEX routing と entry 生成、feedback 報告、editor handoff、競合解消を扱う。
- 各規定の文面と placeholder を作る層であり、どの規定を有効にするかや完全 prompt 内の配置は上位の組み立て側が担う。

## Read this when
- agent に渡す共有規定の文面や、その規定用 placeholder の生成を変更するとき。
- ファイルアクセス、oracle・realization の扱い、適合性所見、INDEX routing・entry 生成、feedback 報告、editor handoff、競合解消のどの規定を確認すべきか判断するとき。

## Do not read this when
- 規定の意味や優先関係を変更・判断するときは、人間が所有する正本仕様を起点にする。
- 完全 prompt で規定を有効化する条件、追加順序、全体の構成や placeholder 統合を変更するときは、prompt 組み立て側を起点にする。
- sandbox の設定やファイルアクセス制限の実際の強制動作を変更するとき。この対象が定義するのは agent に渡す規定文面。

## hash
- 3633df97a332c1d5b7f37a3e994ae78804e1727d6022c2c6b313988982972944
