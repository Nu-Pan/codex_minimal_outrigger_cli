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
- エージェント呼び出し用の完全なプロンプトを、固定・動的パーツ、プレースホルダ、各種標準ルールの有効化設定から構築するモジュール。プロンプト生成仕様や注入パーツの構成を確認する入口。

## Read this when
- プロンプト全体の構造、標準ルールの依存関係、動的プロンプトやプレースホルダの組み立てを変更・調査するとき。

## Do not read this when
- 特定の注入パーツの本文や個別標準ルールだけを変更・調査する場合は、対応する parts モジュールを直接読む。プロンプト生成と無関係な oracle 構造体やファイルアクセス規則の調査にも不要。

## hash
- 2217343e656f775f0701b674731aa9fa2adf94085beaf1e59dee573301f29b56

# `parts`

## Summary
- oracle と realization、INDEX.md、ファイルアクセス規則、レビュー基準などの prompt builder 部品をまとめるディレクトリ。各 Python ファイルは特定の正本仕様・規範・ルーティング情報を StructDoc やプロンプトとして構築する。

## Read this when
- oracle・realization の基本定義や記述規範を変更・確認するとき
- INDEX.md のルーティング規則やエントリー生成基準を変更・確認するとき
- oracle review・apply review の所見判定基準を変更・確認するとき
- ファイルアクセスモード別のプロンプト生成や deny ルールを調査するとき
- prompt builder のこれらの部品の生成内容や構成を変更するとき

## Do not read this when
- 個別の oracle file や realization file の具体的な仕様・実装を調査するとき
- CLI の個別コマンドや実際のファイル操作を調査するとき
- prompt builder の別領域や、生成処理・ファイル探索処理の実装詳細だけを調べたいとき

## hash
- a6fd78125ff56314ce8480de0ccbf177b52abd355ea33f6be0c15c04915f2f11
