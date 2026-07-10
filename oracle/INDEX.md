# `doc`

## Summary
- cmoc の oracle doc を置く領域で、アプリケーション仕様、branch/worktree モデル、採用しなかった設計案、開発作法など、自然言語で書かれた正本仕様断片への入口になる。
- 利用者向け挙動やサブコマンド横断仕様を探す場合はアプリケーション仕様へ、git branch・worktree の作業隔離モデルは branch/worktree モデルへ、過去の不採用案は設計判断メモへ、実装・テストの作法は開発規則へ進む。

## Read this when
- cmoc の実装・テスト・レビューで、自然言語の oracle doc から該当する正本仕様断片を探したいとき。
- CLI 挙動、共通処理、外部連携、状態、ログ、実行環境、branch/worktree モデル、開発作法、テスト方針のいずれかに関する仕様を確認したいとき。
- 現行仕様そのものを読むべきか、採用しなかった代替案や設計判断の背景を読むべきかを切り分けたいとき。

## Do not read this when
- oracle file と realization file の一般的な定義、編集責務、品質基準、INDEX.md エントリー作成規則だけを確認したいとき。
- path placeholder、work root、repo root、run root などの語彙定義だけを確認したいとき。
- realization code の現在の実装場所、関数シグネチャ、内部ロジック、テスト期待値だけを直接調べたいとき。

## hash
- cf685940a413585024c118851719249ecda25a3ac597420dfa197a2cb843d12e

# `src`

## Summary
- AI エージェント呼び出しの論理パラメータ、用途別プロンプト、Structured Output 契約を定義する正本仕様断片への入口。indexing、fork 適用、oracle file レビュー、session join の conflict 解消、TUI 起動に伴う呼び出し契約を扱う。
- 完全プロンプトの構成、ファイルアクセス規則と各種 standard の注入、プレースホルダ置換を支えるほか、リポジトリ設定、ルートパス変換、規範の構造化表現、階層文書の Markdown レンダリングに関する正本定義を収める。

## Read this when
- AI エージェント呼び出しについて、論理モデル、reasoning effort、ファイルアクセスモード、prompt、cwd、indexing preflight、Structured Output の正本契約を確認するとき。
- 完全プロンプトにおける静的部分と動的部分の順序、依存する standard の自動追加、プレースホルダの定義・置換、ファイルアクセス規則やルーティング規則の注入方法を確認するとき。
- INDEX.md エントリー生成、fork 適用後の所見列挙・修正・変更要約、oracle file の所見列挙・検証・採否判定・統合、session join の conflict marker 解消、TUI パラメータ解決・起動に使う agent call の入力と出力を確認するとき。
- リポジトリ別設定の構造、各種ルートの探索・相互変換、standard の構造化表現、構造化文書から Markdown へのレンダリング規則を確認するとき。
- これらの正本定義を具体化する realization implementation または realization test を変更する前に、固定すべき人間意図を確認するとき。

## Do not read this when
- CLI の引数解析、サブコマンドの制御フロー、branch・diff・merge・保存・表示など、realization implementation 側の処理だけを調べるとき。
- バックエンド固有の API リクエスト、論理モデルから具体的なモデル名への解決、AI agent CLI のプロセス起動など、正本の呼び出し契約を具体化する実装詳細だけを調べるとき。
- 個別サブコマンドの利用者向け入出力、永続状態、操作手順だけを確認するときは、それらを直接定義または実装する対象へ進む。
- oracle standard、realization standard、review standard、file access rule など、特定の規範本文だけが必要で、呼び出し契約やプロンプト構築との関係を調べないときは、該当する規範定義へ直接進む。
- 生成済みの prompt、Structured Output、Markdown の結果だけを確認し、その構築規則や構造化表現を調べる必要がないとき。

## hash
- 8fc1b2225e134c28c0b8aa6c673aeaff8b1399076acaff95d0c6b596048b78d8
