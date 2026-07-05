# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語で書かれた文書群への入口。アプリケーション仕様、branch/worktree モデル、不採用設計案、開発規則など、実装差を避けたい外部挙動・共通境界・開発作法を扱う下位領域を選ぶための上位ルーティング情報を担う。
- 個別領域は、利用者に見える CLI 挙動や状態管理、git branch/worktree の概念、過去に退けた代替案、realization code/test の作成基準などの責務ごとに分かれている。

## Read this when
- cmoc の自然言語仕様から、アプリケーション仕様、branch/worktree モデル、不採用設計判断、開発規則のどこを読むべきか判断したいとき。
- 新しい実装やテストの前に、対象機能の正本仕様が外部挙動、git 隔離モデル、設計判断の背景、開発作法のどの領域で述べられているかを切り分けたいとき。
- 複数の仕様領域にまたがる変更で、CLI 挙動、run 隔離、状態管理、branch/worktree、テスト方針、実装規則、不採用案の背景をどこから確認するか決めたいとき。

## Do not read this when
- oracle file と realization file の一般的な定義、編集責務、品質基準、INDEX.md エントリー生成規則だけを確認したいとき。
- <cmoc-root>、<repo-root>、<work-root>、<run-root> などのパス語彙そのものの定義だけを確認したいとき。
- 実装ファイルの具体的な関数、内部 helper、モジュール分割、テスト期待値を直接調べたいとき。
- 対象の仕様領域や個別文書が既に特定できており、その下位対象を直接読めば足りるとき。

## hash
- 7809770dd262d38994027bb3d09da132b9e16acaf95d6e6c99afe9f1d21b76eb

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
