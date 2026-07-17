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
- agent call 用の完全なプロンプト組み立てを担当する。静的な規約類、可変な役割・概要・完了条件、ファイルアクセス制約、プレースホルダ定義を 1 つの prompt 列にまとめる。
- 各種 standard をフラグで注入する入口であり、依存する標準の組み合わせ調整、注入順序、プレースホルダの合成方法を確認したいときに読む。

## Read this when
- 完全な agent 用プロンプトをどう構成しているか知りたいとき。
- oracle / realization の基本情報や各 standard を、どの順序と依存関係でプロンプトに入れるか確認したいとき。
- 静的プロンプトと動的プロンプトの分離方針、またはプレースホルダ定義のまとめ方を変えたいとき。

## Do not read this when
- 個別 standard の本文そのものを確認したいときは、それぞれの build 関数の本文を読む。
- ファイルアクセス制御やルーティング規則の細部だけを確認したいときは、対応する個別の定義を直接読む。
- 呼び出し側のコマンド処理や agent の業務ロジックを追いたいときは、このファイルではなく利用側の実装を読む。

## hash
- 3cbe2d3402e0d238008c12300e617ba0291532aa0e7fa1f47aa8af8e2c72168c

# `parts`

## Summary
- oracle と realization、レビュー基準、ファイルアクセス規則、ルーティング規範などの prompt builder 部品を集約するディレクトリ。各 Python ファイルが特定の正本仕様・標準文面・構造化プロンプト生成責務を担い、該当するプロンプト規範や生成処理を変更・調査する際の入口となる。

## Read this when
- oracle と realization の基本定義や責務境界を確認・変更するとき
- oracle standard または realization standard の規範文面を確認・変更するとき
- oracle review や apply review の所見判定基準を確認・変更するとき
- FileAccessMode ごとのアクセス規則プロンプトを調査・変更するとき
- INDEX.md エントリーの規範や routing rule の生成処理を確認するとき
- これらの標準・規則を構造化プロンプトへ変換する部品を変更するとき

## Do not read this when
- 個別の oracle file や realization file の具体的な仕様・実装を調査するとき
- CLI の実行処理、実際のファイル操作、レビュー実行処理そのものを調査するとき
- StructDoc、Requirement など共通データ構造の定義を確認するとき
- 対象本文に対する INDEX.md エントリーの具体的な要約だけを作成するとき

## hash
- 7179177f7600e2e0e9792aefa7e7b5426a207392915d4408dddb07421468f488
