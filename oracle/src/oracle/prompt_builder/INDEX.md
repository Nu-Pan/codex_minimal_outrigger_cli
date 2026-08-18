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
- agent 向け完全プロンプトを、基礎規定・各種ポリシー・目的・placeholder 定義から組み立てる関数と補助処理を定義する。prompt の構成順序、選択可能な policy block、placeholder の競合検出と統合、追加 prompt の注入を扱う。プロンプト生成仕様や各 policy の組み込み条件を確認・変更するときの入口であり、個別 policy の本文や構造化文書の実装詳細を直接扱う作業では下位の policy モジュールを読む。

## Read this when
- agent call に渡す完全 prompt の構成、挿入順序、選択可能な policy、目的・placeholder の扱いを確認または変更するとき
- placeholder 定義の競合検出や path context 由来の定義統合の挙動を調査するとき
- prompt builder の呼び出し側が指定する policy フラグや追加 prompt の反映経路を確認するとき

## Do not read this when
- 特定の policy block の文面や規則そのものを確認・変更する場合は、対応する oracle/policy モジュールを直接読む
- SDHeader・SDTagBlock の構造化文書仕様を確認する場合は、struct_doc の定義を直接読む
- agent call の path context や placeholder の根本定義を確認する場合は、AgentCallPathContext の実装を直接読む

## hash
- 61696021ff8a986f22b453be9bdcf6022ace9136c32d331a9caf0ea231977921

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
