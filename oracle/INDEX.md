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
- AI エージェント呼び出し仕様、共通基盤型、プロンプト構築仕様を扱う oracle src 配下の領域。agent call parameter、Structured Output schema、モデル・reasoning effort・ファイルアクセス設定、パスモデル、設定、規範モデル、構造化 Markdown、共通規範プロンプトへの入口になる。
- INDEX.md エントリー生成、oracle file レビュー、fork 適用後レビュー、session join の conflict marker 解消、TUI 起動前後のパラメータ選定、prompt と schema の対応、共通標準文書の注入方法を確認するための下位領域へ進む起点になる。

## Read this when
- cmoc が AI agent call をどの prompt、Structured Output schema、モデル設定、ファイルアクセス権限、preflight 設定で組み立てるか確認したいとき。
- agent call parameter の共通データ構造、論理モデル名、論理 reasoning effort、Structured Output schema 指定方法を確認したいとき。
- cmoc 全体で共有される設定値、パス表記、ルート解決、規範データ構造、構造化文書レンダリングの正本実装断片を探すとき。
- agent call 用の完全なプロンプトが、標準文書、読み書き規則、補助プロンプト、プレースホルダ定義などの部品からどう構築されるか確認・変更したいとき。
- oracle file、realization file、INDEX.md エントリー、レビュー所見、ファイル読み書きなど、AI に注入する共通規範プロンプトを確認・変更したいとき。

## Do not read this when
- CLI 引数処理、branch 操作、diff 取得、merge 実行、保存処理、表示整形など、AI エージェント呼び出し以外の実行制御実装を調べたいとき。
- CLI サブコマンドごとの利用者向け入出力、実行フロー、状態ファイルの仕様を直接確認したいとき。
- oracle standard、realization standard、apply review standard、index entry standard など、規範本文の意味だけを確認したいとき。
- バックエンド API へ送る実際のリクエスト形式、具体的なモデル名解決、agent CLI 実行処理など realization src 側の実装詳細を調べたいとき。
- 生成済み Markdown、個別の標準文書本文、パス概念そのもの、または実装ファイルやテストファイルの現在構造だけを調べたいとき。

## hash
- d420ca3d1e03c5097c86f6dbdcec6d5316e6f34bbe1cb7f185feb4fcc88944d4
