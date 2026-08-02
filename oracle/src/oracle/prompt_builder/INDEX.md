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
- agent call に渡す完全なプロンプトを、役割・依頼概要・完了条件、静的／動的プロンプト、各種規則、プレースホルダ定義から構築する。
- oracle・realization、realization から oracle 参照、INDEX エントリー、ファイルアクセス、ルーティングの各規則を条件付きで注入し、placeholder の競合を検出する。

## Read this when
- agent call 用プロンプトの構成や注入順序を変更するとき
- 静的／動的プロンプト、補助プロンプト、placeholder 定義の統合処理を確認するとき
- oracle・realization 関連規則や INDEX エントリー規則の有効化条件を変更するとき

## Do not read this when
- 個別のプロンプト部品の本文や規則の内容だけを変更するときは、対応する parts 配下の実装を直接読む
- プロンプト生成と無関係な CLI、パスモデル、構造化文書の処理を変更するとき

## hash
- 9ee989a6beb974e3cecde4497393189632a7ddc50ec34869be9805681c5b1aac

# `editor_input.py`

## Summary
- ユーザー入力用エディタに表示する初期テキストを構築する正本実装。AI Agent CLI/TUI向けプロンプトの記述形式・品質基準・指定事項を案内するHTMLコメントの固定接頭辞を定義し、サブコマンド固有の自動注入指示を結合して返す。

## Read this when
- プロンプト入力エディタの初期表示内容、案内文、HTMLコメントによる注入指示の構造を変更・確認するとき。
- 自動注入されるサブコマンド固有指示を初期テキストへ組み込む処理を変更・確認するとき。

## Do not read this when
- 特定サブコマンドのプロンプト内容や、エディタ以外のプロンプト生成処理を調査するとき。

## hash
- 5622a37bf21a60f5ae6bc90f00c4a5d9350402e529f28f004aa46d3b26aa1c76

# `parts`

## Summary
- prompt builder が生成する各種規則・定義文書の部品を収めるディレクトリ。ファイルアクセス制約、oracle/realization の基本定義、INDEX.md ルーティング、oracle file 参照規則など、個別のプロンプト構成要素への入口となる。

## Read this when
- prompt builder の規則文書を追加・変更・確認するとき
- ファイルアクセス、oracle/realization、INDEX.md ルーティング、realization code の oracle 参照のいずれかに関する生成規則を調べるとき

## Do not read this when
- 個別の oracle 文書や realization 実装の内容を調べるとき
- prompt builder 全体の構成や、このディレクトリに含まれない別の生成部品だけを調べるとき

## hash
- a337f6fe855ab67cb0994ec92a4da67f8e23c517fc9b5afddee0c5fa8927c59b
