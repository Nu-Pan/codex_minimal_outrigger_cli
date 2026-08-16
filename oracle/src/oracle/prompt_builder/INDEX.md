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
- cmoc agent向けの完全な構造化プロンプトを構築するモジュール。summary・goal、選択された oracle／realization／review／routing などの規則、ファイルアクセス規則、補助プロンプト、placeholder 定義を決定論的に統合し、agent call に渡す StructDoc／StructBlock の列を生成する。
- 各種標準の依存関係を自動的に有効化し、StandardCollection を統合して重複なく出力する。placeholder は call-scoped context と補助定義をマージし、同名異値の衝突を拒否する。

## Read this when
- agent call に渡す完全 prompt の構成要素や注入順序を変更・確認するとき
- oracle／realization／review などの標準間の自動依存関係や、StandardCollection の統合経路を調べるとき
- placeholder 定義の統合、衝突検出、path context からの root 定義初期化を変更・確認するとき
- 新しい静的規則・動的 prompt・補助 placeholder を完全 prompt に組み込む経路を調べるとき

## Do not read this when
- INDEX.md のルーティング文面だけを更新・確認するとき
- 個別の oracle／realization 規則本文や各 builder の内容だけを調べるときは、それぞれの builder・規則定義を直接読む
- 生成済み prompt の具体的な agent 作業内容だけを確認するとき

## hash
- 63598436ba01aaecb0733adfda9fb8c2110e7d6d5c8e4e652cd62af6bcb1bda8

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
