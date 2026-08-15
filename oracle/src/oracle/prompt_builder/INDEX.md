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
- cmoc agent 向けの完全な構造化プロンプトを組み立てる中核ユーティリティ。担当・完了条件・選択された Standard・静的規則・動的プロンプト・placeholder 定義を、依存関係に応じて合成して返す。
- Standard の依存関係を決定的に有効化し、重複する Standard を統合して一度だけ出力するほか、placeholder の競合を検出する。プロンプト生成条件、Standard の注入、ファイルアクセスや routing などの静的規則、agent 固有の動的内容の接続を変更・調査するときの入口となる。
- 個別の Standard 本文や各 builder の詳細を読む対象ではなく、完全 prompt 全体の構成、Standard 間の依存、静的・動的 prompt の配置、placeholder 統合の挙動を確認する場合に読む。

## Read this when
- agent call に渡す完全 prompt の構成や、summary・goal・Standard・静的規則・動的 prompt の注入順を変更または確認するとき。
- 特定の Standard を有効化した際に必要な上位概念や依存 Standard が自動的に含まれる仕組みを調査するとき。
- 複数の Standard の統合、重複排除、placeholder 定義の競合検出に関する挙動を調査するとき。
- prompt builder の各種 builder をどの条件で呼び出し、生成結果をどの構造に配置するかを確認するとき。

## Do not read this when
- 個別 Standard の本文、oracle/realization 規則、file access 規則、routing 規則の内容だけを確認したい場合は、それぞれの builder または正本規則を直接読む。
- agent call の具体的な担当や完了条件だけを確認したい場合は、この共通構築器ではなく呼び出し側の動的 prompt 定義を読む。
- prompt の出力 schema や機械的な placeholder 名・型だけを確認したい場合。

## hash
- 5800dbe1fb3a4faf97ae37a1b531fb143c3fb11d27170355f14c1cc69118c0e7

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
- 対象ディレクトリは、cmoc の agent call 向けプロンプトを構成する部品群を収め、oracle・realization の扱い、標準選択、ファイルアクセス制約、routing、feedback などの個別規範を用途別に組み立てる入口である。各部品の具体的な構成や責務を確認するときに、まずこのディレクトリから該当する部品へ進む。

## Read this when
- prompt builder の部品構成や、用途別にどの instruction・standard collection を組み合わせるかを調査・変更するとき
- oracle・realization、INDEX.md routing、file access、feedback reporting など、agent call の共通 instruction を構築する経路を確認するとき

## Do not read this when
- 個別の oracle file・realization file の本文や実装を調査するとき
- 特定の標準本文そのものだけを確認したいときは、対応する standard definition へ直接進む
- 生成された prompt の利用側や、CLI の実際のファイル操作を調査するときは、該当する利用側・操作実装へ直接進む

## hash
- 9506d16ac6b4bb4f91f00e047cfd94cce7909fe40abb0c6461f63977e7631ddd
