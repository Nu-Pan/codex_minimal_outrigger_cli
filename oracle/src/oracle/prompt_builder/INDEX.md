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
- oracle と realization の役割・下位分類・分類条件、および uncategorised file の扱いを、call-scoped な work-root に基づく説明文として構築する prompt builder part の入口。配下には、この基本概念を生成する定義がある。

## Read this when
- oracle file、realization file、uncategorised file の役割や分類規則を動的プロンプトへ反映する処理を変更・調査するとき
- oracle と realization の配置先や、oracle を正本として realization を生成する関係の説明文を確認するとき

## Do not read this when
- 個別の oracle doc・oracle src・oracle test の内容や仕様を確認するとき
- realization の実装・テストの具体的な挙動を確認するとき
- 共通の prompt builder 定義や、oracle/realization の基本概念を扱わない別のプロンプト部品を調査するとき

## hash
- 9ebb611920d5f29b9ec0c8971c1e527f782c40448b314a32da771340d4c2824f

# `policy`

## Summary
- agent call の instruction 文面や routing、file access、oracle／realization、feedback、INDEX エントリーなど、cmoc の prompt builder policy を構成する方針定義をまとめた領域です。個別ポリシーの責務と適用条件を確認するための入口になります。

## Read this when
- prompt builder が生成する共通 policy の追加・変更・レビューを行うとき
- oracle／realization の扱い、conflict resolution、handoff、feedback reporting、file access、routing、INDEX エントリー生成の規定を確認するとき
- 複数の agent call に共有される instruction 方針の構成や責務分担を調査するとき

## Do not read this when
- 個別の oracle file や realization file の具体的な仕様・実装挙動を確認するとき
- prompt builder のデータ型、placeholder 処理、通常の文面生成ロジックを直接調べれば足りるとき
- cmoc の通常の実装・テスト・文書作成で、agent 向け policy の構築規則を扱わないとき

## hash
- 60e632b2e618782282bf0e11e9c475ebd4c069ab7b6328128d8b14f8be15047c
