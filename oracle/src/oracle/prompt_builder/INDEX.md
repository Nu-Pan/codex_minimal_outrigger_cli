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
- agent向け完全プロンプトを構築する中心的な入口。基礎規定、選択式の各種ポリシー、caller追加文面、作業目的、placeholder定義を所定の順序で統合し、構造化されたプロンプトとして返す。
- プロンプトの構成順、重要情報への参照、placeholder定義の競合検査、各ポリシーの組み込み条件を変更・確認するときに読むべき対象であり、個別ポリシーの本文だけを読む場合は直接その下位モジュールへ進む。

## Read this when
- agent callへ渡す完全プロンプトの構成や順序を変更・確認するとき
- 複数のポリシー、追加プロンプト、目的、placeholder定義がどのように統合されるかを調査するとき
- 同名placeholderの異値上書きを拒否する統合処理を変更・確認するとき

## Do not read this when
- 特定のポリシーの文面や単一のprompt builderの詳細だけを確認する場合は、対応するpolicyまたはparts配下のモジュールを直接読む
- 構造化文書の基本型やpath contextのplaceholder定義自体を確認する場合は、対応するoracleモジュールを直接読む

## hash
- 529d1f6962680681dcd3aa5ae8ad0da75320b318a755b768ce8f4d4b9c4e5d45

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
- oracle file・realization file・uncategorised file の役割、下位概念、分類条件を StructDoc として構築する prompt builder part。call-scoped context から work-root を取得し、oracle と realization の正本仕様・具体化の関係や配置境界を説明する基本知識への入口となる。

## Read this when
- oracle file、realization file、uncategorised file の定義や分類条件を確認するとき
- oracle file と realization file の責任範囲、正本仕様と具体化の関係、配置先を確認するとき
- これらの基本知識を含む prompt builder part の文面構築処理を変更・調査するとき

## Do not read this when
- oracle または realization の個別ファイルの内容や実装詳細だけを確認するとき
- 分類条件ではなく、別の prompt builder part の文面や生成ロジックを確認するとき
- 生成済み StructDoc の具体的な出力だけを確認すれば足りるとき

## hash
- 754af53ac0f6a1fb99a71d8fe635f362fc1aeaa6b2c109eae4a4ea57fdf6b334

# `policy`

## Summary
- oracle と realization の扱い、agent 向け file access、feedback、routing、conflict 解消、editor handoff、INDEX.md エントリー生成など、prompt builder が共通 policy 文面を構築する領域。各 policy の責務を確認・変更する際の入口として機能する。

## Read this when
- oracle・realization 関連の agent instruction policy を確認または変更するとき
- agent call に共通する file access、feedback reporting、routing、handoff、conflict resolution の規定を確認または変更するとき
- INDEX.md 用エントリー生成規定や oracle review の判定基準を確認または変更するとき

## Do not read this when
- 個別の oracle file、realization file、または具体的な実装の内容だけを確認するとき
- prompt builder の policy 以外の CLI 実装や仕様内容を直接確認するとき
- Structured Output の出力項目や形式だけを確認するとき

## hash
- 0015aef87fa5823d6dc7481727138d715097f8ff3d96b8b3827dd1101da6e745
