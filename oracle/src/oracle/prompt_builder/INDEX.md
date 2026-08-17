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
- agent 向け完全プロンプトを、基礎規定・選択規定・目的・追加文面・placeholder 定義から構築する中核関数を扱う。各種 policy builder の組み込み、placeholder の競合検出、プロンプト内参照用の構造化を確認する入口であり、agent prompt の構成や policy の選択条件を変更・調査するときに読む。

## Read this when
- agent call に渡す完全 prompt の構成順序や、fundamental policy・objective・placeholder の配置を変更するとき
- 各種 oracle、realization、routing、file access、index entry policy を prompt へ組み込む条件を調査するとき
- placeholder 定義の統合や同名定義の競合処理を変更・検証するとき

## Do not read this when
- 個別 policy の本文や文面だけを変更・調査する場合は、該当する policy module を直接読む
- prompt builder の基本型や placeholder 型の定義だけを確認する場合は、該当する basic module を直接読む
- agent prompt の利用側や個別 agent の作業内容だけを調査し、完全 prompt の構築ロジックに関係しない場合

## hash
- 2c6cd7c9867cae5feb897fd57055b7cbe8b0e95c3191e687f46d35a747286e07

# `editor_input.py`

## Summary
- エディタ経由で後続の AI エージェントへ渡すユーザー入力ファイルの初期テキストを構築する定義。使い方・記入方針・完全プロンプトのテンプレートを HTML コメント内にまとめる入口であり、プロンプト入力用ファイルの初期内容やコメント除去前の構造化レンダリングを確認したい場合に読む。

## Read this when
- エディタ経由のプロンプト入力ファイルにどの初期案内やテンプレートを注入するかを変更・確認するとき
- 完全プロンプト中のユーザー入力差し込み位置を、初期テキスト生成側から調査するとき

## Do not read this when
- 後続エージェントへ渡す完全プロンプト全体の構築規則を調べるとき
- StructDoc、StructBlock、Markdown レンダリング自体の仕様を調べるとき
- エディタ経由ではないユーザー入力経路や、保存記録としてのプロンプト管理を調べるとき

## hash
- ef8b185c6711e48c549cd12fc63e19d1412a834885495065bc4b0eabef94017f

# `parts`

## Summary
- oracle と realization の分類境界、Git ignore や常時対象外 root を含む分類規則、および両者の役割を説明する基本文を構築する。
- oracle file と realization file の下位概念として、oracle doc/src/test、realization code/implementation/test/ancillary の定義と配置を整理する。
- call-scoped context から work-root を取得し、説明文のプレースホルダーへ渡す生成経路を扱う。

## Read this when
- oracle と realization の分類規則や責務を確認するとき。
- oracle doc/src/test と realization implementation/test/ancillary の区分を確認するとき。
- oracle と realization に関する基本説明文の生成経路を変更・調査するとき。

## Do not read this when
- oracle と realization の分類や基本概念を扱わず、別の prompt_builder part を直接確認すべきとき。
- 具体的な分類アルゴリズムやテスト実装を確認する場合に、対応する実装・テスト対象へ直接進めるとき。

## hash
- 20dd888fb1bacc5753ab0ab8ab2bdcda36f9edd817b4f69762216a9ef88654b9

# `policy`

## Summary
- agent call のプロンプト構築に用いる各種 policy 定義を扱うディレクトリ。oracle／realization の正本関係、レビュー・conflict 解消、file access、feedback reporting、routing、INDEX エントリー生成など、特定の開発判断や文書ルーティングに必要な共通方針への入口を提供する。

## Read this when
- agent call の共通 policy、oracle／realization の扱い、レビュー基準、conflict 解消、アクセス制約、feedback 報告、routing、INDEX エントリー生成のいずれかを確認・変更するとき
- 対象の作業内容に応じて、該当する policy 定義へ進む入口を特定するとき

## Do not read this when
- 具体的な oracle file や realization file の仕様・実装挙動を直接確認することが目的のとき
- policy を利用するだけで、その構築規則自体を確認・変更する必要がないとき
- 通常の CLI 実装、テスト、文書作成など、ここにある共通 prompt policy を扱わないとき

## hash
- 29c54977e8f1fef13959efd0d8a5e1498baeb07efcac1c00740db5ca18a69146
