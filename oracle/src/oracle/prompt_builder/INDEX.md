# `basic.py`

## Summary
- プレースホルダ名を実パスや文字列へ対応付ける型定義を置く。プロンプト組み立てで、置換対象の名前と置換先を共通の表現で扱いたいときに読む。

## Read this when
- プレースホルダ展開に使う型の意味を確認したいとき。
- 文字列と `Path` を混在させる置換対象の表現を統一したいとき。

## Do not read this when
- プロンプト本文の生成手順や置換ロジックの詳細を知りたいときは、実装側を読む。
- プレースホルダを使わない処理や、別の設定値の表現を確認したいだけのとき。

## hash
- 526fb2d3d3f5fd312f3f1cc48c630d59e91568f38d6ac0d09bc5241792eb1e18

# `complete_prompt.py`

## Summary
- agent 向けの完全なプロンプトを構築する中核モジュール。固定ポリシー、補助プロンプト、動的な目的、placeholder 定義を統合し、指定された順序で返す。
- placeholder の重複定義は同値のみ許容し、異値の衝突を検出する。各種 oracle／realization／review／routing ポリシーの注入可否もここで制御する。

## Read this when
- agent call に渡す完全プロンプトの構成順序、注入するポリシー、placeholder 定義の統合や衝突処理を調べるとき。
- 新しい prompt builder の構成要素を完全プロンプトへ追加する変更を検討するとき。

## Do not read this when
- 個別のポリシーや oracle／realization builder の内容自体を確認したいときは、対応する下位モジュールを直接読む。
- agent 向けプロンプトの組み立てではなく、構造化文書の基本型や placeholder の定義だけを調べるときは、対応する基礎モジュールを直接読む。

## hash
- 42610509acde7f1a0e69d6e6eb85d4bb840350e0a9757fd7f9b63654076531cf

# `editor_input.py`

## Summary
- エディタ経由で後続 AI エージェントへ渡すユーザー入力ファイルの初期表示文面を構築する関数を定義する。使い方・記入の目安・完全プロンプトのテンプレートを構造化文書として組み立て、入力時に除去される HTML コメントブロックとして返す。

## Read this when
- エディタ経由プロンプト入力の初期テキスト形式や、ユーザー向け記入案内、完全プロンプト雛形の埋め込み位置を確認したいとき。

## Do not read this when
- 後続エージェントへ渡す完全プロンプトの構成やテンプレート自体を確認したいときは、完全プロンプトの定義を直接読む。
- 構造化文書ノードのレンダリング仕様を確認したいときは、`oracle.other.struct_doc` の定義を直接読む。

## hash
- 196f57f157e1d3a90dc8c76ccdf9afa221d88963cfc555d45b5cb59337b48f40

# `parts`

## Summary
- prompt builder の構成部品を集約するディレクトリ。agent call 向けの共通説明・制約・判断規範を、構造化文書やプレースホルダー付きのプロンプト断片として生成する。oracle と realization の責務、分類、アクセス規則、レビュー、handoff など、複数のプロンプト生成経路から参照される部品の入口である。
- oracle と realization の基本概念や uncategorised file の分類を確認する場合は、配下の基本説明部品から読み始める。共通 Standard の定義や用途別の規範を調べる場合は、該当する個別部品へ直接進む。

## Read this when
- prompt builder が生成する共通説明・制約・判断規範の構成部品を追加、変更、調査するとき
- oracle と realization の責務境界、ファイル分類、アクセス規則をプロンプトへ組み込む経路を確認するとき
- oracle review、apply review、conflict resolution、editor handoff などの用途別規範がどの部品から構成されるかを確認するとき
- call-scoped な path context や placeholder を構造化プロンプトへ渡す処理を確認するとき

## Do not read this when
- oracle または realization の正本仕様、実装、テスト本文そのものを確認したいとき
- 生成済みプロンプトの結果だけを確認すればよく、prompt builder の構成元を調べる必要がないとき
- 特定の用途別規範の内容だけを確認したいときは、このディレクトリ全体ではなく該当する個別部品へ直接進むとき

## hash
- 324eecfb9061893f39786e1704466b30fed5ab8a34d05eef147328b1b45ea0c7

# `policy`

## Summary
- prompt builder の policy 実装群を扱うディレクトリ。agent call に適用するアクセス制限、oracle／realization の扱い、feedback 報告、conflict 解消、handoff、routing、INDEX.md エントリー生成など、作業目的ごとの instruction 文面を構築する入口となる。
- 個別の policy ファイルは、対応する作業規定や prompt 生成ロジックを確認・変更するときに参照する。oracle／realization の具体的な仕様や CLI 本体の実装を確認するための直接の入口ではない。

## Read this when
- agent call 用の共通または作業目的別 policy の構築規則を調査・変更するとき
- FileAccessMode ごとの読み書き制限、oracle／realization の扱い、feedback 報告、handoff、conflict 解消の instruction を確認するとき
- INDEX.md ルーティングや oracle／realization 適合性レビューに関する prompt policy を確認するとき

## Do not read this when
- oracle file や realization file の具体的な仕様・実装内容を確認するとき
- CLI 本体、共通型、パス解決など、policy 文面の構築以外の実装責務を調査するとき
- 対象となる個別 policy の利用箇所や生成済みプロンプト全体だけを確認したいとき

## hash
- f170449acd770270f646df173362be90f228106ce042ae784d7a4d65dea83897
