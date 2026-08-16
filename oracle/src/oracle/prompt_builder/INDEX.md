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
- agent 向けの完全なプロンプトを組み立てる中心実装。summary・goal、各種 policy、補助 prompt、placeholder 定義を選択順に統合し、構造化された prompt 要素として返す。
- 同名 placeholder の定義を統合する際は、文字列表現が異なる値の衝突を検出して拒否する。
- oracle・realization、ファイルアクセス、routing、index entry、feedback reporting などの作業規則を、指定されたフラグと call context に応じて prompt へ注入する入口である。

## Read this when
- agent call に渡す完全 prompt の構成、注入される policy の順序、summary・goal・補助 prompt の配置を変更または確認するとき。
- 複数の prompt builder が提供する placeholder 定義の統合や、定義衝突時の挙動を変更または調査するとき。
- 新しい policy または補助 prompt を完全 prompt へ組み込む設計を確認するとき。

## Do not read this when
- 個別 policy の本文や規則だけを確認する場合は、対応する policy builder を直接読む。
- prompt の構造化文書型、ファイルアクセスモード、agent call path context の定義だけを確認する場合は、それぞれの定義元を直接読む。
- INDEX.md のルーティング文書そのものを作成・確認する場合は、この prompt 組み立て実装ではなく対象文書と index-entry 規則を読む。

## hash
- f3e56c078cd0628f9739fe69dd93ec31e11f3caf288ddbe6f442c722dd7aab0f

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
