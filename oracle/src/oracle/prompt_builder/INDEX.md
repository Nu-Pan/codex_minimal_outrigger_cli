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
- oracle と realization の各種規範およびパス文脈を組み合わせ、agent call に渡す完全なプロンプトを決定論的に構築する。静的・動的プロンプト、placeholder 定義、規範間の依存関係を扱う。

## Read this when
- agent call 用プロンプトの全体構成、注入する規範、placeholder、ファイルアクセス・ルーティング規則を変更または確認するとき
- 静的プロンプトと動的プロンプトの分離、規範の自動有効化、placeholder の競合処理を調査するとき

## Do not read this when
- 個別の oracle／realization 規範本文だけを確認したいとき
- 特定のプロンプト部品の文面や内容を変更・確認する場合で、その部品の実装を直接読めるとき

## hash
- 809587f3af485137443c65358d9600db1f5b8f02770dab4b6267aa0829497260

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
- oracle と realization、適合性レビュー、ファイルアクセス、INDEX.md ルーティングなどの規範を prompt builder 用の構造化文書へ変換する実装群を収録するディレクトリ。各ファイルは特定のレビュー規範・アクセス制約・仕様分類・ルーティング規則の生成責務を持つ。

## Read this when
- oracle file と realization file の適合性、レビュー所見、conflict 解消規範を調査・変更するとき
- AI エージェント向けのファイルアクセス規則や oracle・realization の定義を変更するとき
- INDEX.md のエントリー規範やルーティング規則の生成処理を調査・変更するとき
- prompt builder に注入する標準文書の構造、Requirement・Standard の扱い、oracle 参照ルールを確認するとき

## Do not read this when
- 特定の oracle 文書や realization 実装そのものの仕様・挙動を調査するとき
- Codex CLI の実行権限や sandbox 設定そのものを確認するとき
- prompt builder 以外のサブコマンド処理や、一般的なコード品質・ベストプラクティスだけをレビューするとき

## hash
- 64f41aa2cca1fda8f8258429b314afc03bcd26666154c0ef725c4dac6ca92905
