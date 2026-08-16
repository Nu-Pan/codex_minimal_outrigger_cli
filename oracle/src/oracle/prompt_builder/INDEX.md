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
- cmoc の agent 向け完全プロンプトを構築する中核モジュール。概要・完了条件・各種ポリシー・ファイルアクセス規則・ルーティング規則・プレースホルダ定義を、選択された構成に応じて決定論的に統合する。
- ポリシー間の依存関係を自動的に有効化し、重複するポリシーやプレースホルダ定義を統合しながら、agent call に渡す構造化文書列を生成する。
- agent prompt の構成、ポリシー注入、プレースホルダ統合、または特定の作業種別に必要な規定の有効化条件を変更・調査するときの入口。個別ポリシーの具体的内容は同階層の各 policy builder を直接確認する。

## Read this when
- agent 向け完全プロンプトの生成順序や構造を確認するとき
- 各種ポリシーの依存関係、自動有効化、重複統合の挙動を変更・調査するとき
- プレースホルダ定義の統合や動的・静的プロンプトの組み立てを変更するとき

## Do not read this when
- 個別ポリシーの本文や規則だけを確認したいときは、対応する policy モジュールを直接読む
- プロンプト生成とは無関係な CLI 実装や oracle・realization の個別仕様を調査するとき

## hash
- 13790db92ca3b83f1368a45ae45af37eaf652006aa16bce87800ab5af5cfec97

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
- agent instruction policy builder 群をまとめるディレクトリ。oracle・realization file の権威関係、レビュー所見、conflict 解消、editor handoff、feedback reporting、file access、INDEX.md routing など、用途別のポリシー構成を扱う。共通ポリシー定義と基本型を土台に、各作業向けの適用ポリシー群へ進む入口となる。

## Read this when
- agent call に埋め込む instruction policy の構成や、用途別に選択されるポリシー群を確認するとき
- oracle・realization file の作成、変更、レビュー、conflict 解消、editor handoff に適用される規定の組み合わせを確認するとき
- feedback reporting、file access、INDEX.md routing など共通 instruction の生成方針を確認するとき
- Policy の定義、衝突検査、決定的な合成、StructDoc への変換を含む共通基盤の責務を確認するとき

## Do not read this when
- 特定のポリシーの具体的な判定文だけを確認したいときは、個別ポリシー定義へ直接進む
- Policy や PolicyGroup の基本データ構造・合成規則だけを確認したいときは、基本型の定義へ直接進む
- 個別の oracle／realization file の内容、実行時 CLI 処理、またはポリシーを利用する realization 実装を調査するとき

## hash
- 0243d6b0c121f46496019eaacecae3818ad9e026967233c0ddc539497648db73
