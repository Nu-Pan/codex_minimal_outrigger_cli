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
- agent 向け完全プロンプトを構築する中心的な組み立て処理。依頼概要・完了条件・プレースホルダ定義を含むプロンプトを生成し、選択された oracle／realization／レビュー／ルーティング等の規則を依存関係に従って注入する。各規則の有効化条件や複数 Standard の統合、共通 feedback reporting の常時注入を確認したい場合の入口であり、個別規則の本文や各 builder の詳細を直接調べる前に読む対象。

## Read this when
- agent call に渡す完全プロンプトの構成、規則の注入順序、Standard の依存関係、プレースホルダ統合、または共通 feedback reporting の適用範囲を変更・調査するとき。
- 複数の prompt builder の結果を統合して StructDoc 列へ変換する経路を確認するとき。

## Do not read this when
- 特定の規則の文面や個別 builder の内容だけを確認したいときは、対応する parts 配下の対象を直接読む。
- StructDoc や StandardCollection のデータ構造自体、FileAccessMode、AgentCallPathContext の仕様を確認したいときは、それぞれの定義元を直接読む。

## hash
- 63598436ba01aaecb0733adfda9fb8c2110e7d6d5c8e4e652cd62af6bcb1bda8

# `editor_input.py`

## Summary
- 後続の AI エージェントへ渡す、エディタ経由ユーザー入力ファイルの初期表示文面を構築する関数を定義する。利用方法・記入方針・完全プロンプトのテンプレートを構造化文書として組み立て、HTML コメントブロックで囲んだ初期テキストとして返す。

## Read this when
- エディタ経由で受け取るプロンプト入力ファイルの初期内容や、その表示文面の構成を変更・確認するとき。
- 完全プロンプトへのユーザー入力の埋め込み位置、HTML コメントによる説明文の扱い、記入案内の内容を確認するとき。

## Do not read this when
- エディタ経由ではないプロンプト生成や、完全プロンプトの全体構造そのものを確認するとき。
- 構造化文書の一般的なレンダリング仕様を確認するときは、文書構造・レンダリングを定義する対象を直接読む。

## hash
- 5c9e9e87d54de02310774e7c73bcf2310d820930162eac85d23e8862263c3fbe

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
