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
- agent call に渡す完全なプロンプトを構築する正本実装。役割・依頼概要・完了条件、静的／動的プロンプト、placeholder 定義を組み合わせ、各種 oracle／realization／レビュー／ルーティング規則を依存関係に従って注入する。

## Read this when
- agent call の完全プロンプト生成処理を変更・レビューするとき
- 静的プロンプトと動的プロンプトの構成、placeholder 統合、各種プロンプト規則の注入順序を確認するとき
- oracle／realization や INDEX エントリー生成に関わるプロンプト注入条件を調査するとき

## Do not read this when
- 個別のプロンプトパーツ本文だけを変更・確認するときは、対応する parts 配下の実装を直接読む
- プロンプト生成とは無関係な CLI、パスモデル、構造化文書の実装を調査するとき

## hash
- 9074a0c9fb71f1a3a24fe08e84f5e996faa837f038e4f656aaf0295737f9a3e3

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
- oracle と realization の規範、および両者を適用したレビュー基準を prompt builder の構造化文書として生成する部品群。oracle／realization の定義、レビュー所見、INDEX.md ルーティング、ファイルアクセス規則など、エージェント向けプロンプトの基礎規則への入口となる。

## Read this when
- oracle・realization の定義や責務境界、各種標準規範を prompt に組み込む処理を確認・変更するとき
- oracle file と realization file の不整合や致命的問題をレビュー所見として扱う基準を確認するとき
- INDEX.md のエントリー生成・ルーティング規則、またはエージェント向けファイルアクセス規則を確認するとき
- これらの規範文書を構造化して生成する prompt builder 部品を調査するとき

## Do not read this when
- 個別の oracle 文書や realization 実装・テストの内容を調査するとき
- 特定のサブコマンドやプロダクト機能の実装責務を調査するとき
- StructDoc や Standard など共通の構造化文書機構そのものを変更・確認するとき
- Codex CLI の実行環境やテスト手順の正本仕様を確認するときは、対応する oracle 文書を直接読む

## hash
- a0b2facad381820e0979d3d636b984c9619b42e718975c4c195e979a0f3a93ef
