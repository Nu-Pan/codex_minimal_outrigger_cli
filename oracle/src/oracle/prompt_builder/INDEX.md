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
- 選択したポリシー、補助プロンプト、目的、プレースホルダー定義を統合し、agent call 用の完全な構造化プロンプトを構築するエントリーポイント。
- プロンプトの基礎規定・規定ブロック・動的な目的情報を組み立てる流れや、placeholder 定義の衝突検査を確認したいときの入口。
- 個別ポリシーの内容や各種 builder の実装を調べる場合は、このファイルではなく対応する policy または parts 配下の対象へ進む。

## Read this when
- agent 向け完全プロンプトの構築順序、含めるポリシーの選択、補助プロンプトの統合を変更・確認するとき。
- placeholder 定義の統合規則や同名定義の衝突時の挙動を確認するとき。
- プロンプト全体の構造化された出力を生成する入口を特定するとき。

## Do not read this when
- 個別のファイルアクセス、routing、oracle、realization、review などのポリシー本文だけを確認したいとき。
- 特定の policy builder や oracle/realization 部品の詳細実装を直接調べる場合。
- Structured Output の項目形式だけを確認したい場合。

## hash
- c4da43851f828229d2dc12dd0eec0d03d7964d4e206e06f46fc0106286fe0f0b

# `editor_input.py`

## Summary
- 対象ファイルは、エディタ経由で後続 AI エージェントへ渡すユーザー入力ファイルの初期表示文面を構築する関数を定義する。使い方・記入上の目安・完全プロンプトのテンプレートを HTML コメント内にまとめ、入力本文が所定のプレースホルダーへ注入される前提を扱う。

## Read this when
- エディタ経由のプロンプト入力ファイルに表示する初期文面の構成や、ユーザーへの記入案内、テンプレート埋め込みの挙動を確認・変更するとき。
- 初期テキストに含める構造化見出し・タグブロックの組み立てと、HTML コメントとしてのレンダリング範囲を確認するとき。

## Do not read this when
- エディタ入力の初期文面ではなく、完全プロンプト全体の生成規則や別経路のプロンプト入力処理を確認するときは、それぞれの担当実装・仕様を直接読む。
- 構造化ドキュメント要素の定義や Markdown レンダリング仕様そのものを確認したい場合は、インポート元の構造化ドキュメント実装を読む。

## hash
- 801c5e31f4bbfc2b036f94ce9ef77536f12136fe02cba369a4f477b5b6150d35

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
- prompt_builder の各 policy 実装を対象とするルーティング入口。agent call の file access、oracle/realization の扱い、feedback、conflict 解消、handoff、レビュー、INDEX.md 生成など、個別の指示文面を構築する責務ごとに下位ファイルへ進む。

## Read this when
- prompt_builder policy の責務や構築規則を確認・変更するとき
- 対象の責務に対応する個別 policy 実装の入口を特定するとき

## Do not read this when
- 個別 policy の具体的な挙動だけを確認する場合は、該当する下位ファイルを直接読む
- oracle・realization file の具体的な仕様や実装内容を確認する場合は、それらの対象を直接読む
- INDEX.md の一般的な routing 規則だけを確認する場合は、routing.py を読む

## hash
- 8b57b05ed4216dcb5fba622cbed153958b5610ab06c11bb3e7620032584bd1d7
