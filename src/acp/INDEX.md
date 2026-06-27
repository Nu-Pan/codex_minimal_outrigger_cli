# `builder`

## Summary
- AI エージェント呼び出し用パラメータを組み立てる builder 群への入口。フォーク適用、目次エントリー生成、oracle レビュー、session 処理、TUI パラメータ解決など、各機能が下流エージェントへ渡す役割・目的・補助文脈・権限・モデル設定・Structured Output schema の接続を扱う。
- 実際の業務処理、差分解析、レビュー判定そのもの、ファイル更新、CLI 制御フローを直接担う領域ではなく、AI に依頼する作業内容と返却契約を機能別に構成するための入口である。

## Read this when
- 各コマンドや処理フェーズから AI エージェントへ渡す complete prompt、role、summary、goal、補助プロンプト、モデル選択、推論量、ファイルアクセス権限を確認または変更したいとき。
- フォーク適用、INDEX.md 用エントリー生成、oracle file レビュー、session 関連の conflict 解消、TUI 入力からの実行パラメータ解決のどの呼び出し設定へ進むべきかを判断したいとき。
- AI 呼び出しの入力文脈と Structured Output schema の対応、または schema による返却形の制約を、機能別の builder 実装から確認したいとき。
- raw diff、対象本文、oracle file、既存所見、対象ファイル一覧、利用者入力などが、どのような補助文脈として prompt に埋め込まれ、どの権限でエージェントに渡されるかを追いたいとき。

## Do not read this when
- フォーク適用、目次更新、レビュー、session、TUI などのコマンド全体の制御フロー、保存、表示、状態管理、CLI 入出力を調べたいとき。
- git 操作、差分解析、所見の統合・重複排除、修正結果の検証、merge 実行や conflict 検出など、AI 呼び出しパラメータ構築の外側にある実処理を探しているとき。
- complete prompt の共通構築、Markdown レンダリング、パスモデル、ACP の基礎型など、複数領域で共有される汎用部品だけを確認したいとき。
- 個別の Structured Output 項目の意味や詳細だけを確認したいときは、該当する schema 本文へ直接進めばよい。

## hash
- db3debc81c0ddff3d09773cf623d66c945face4a1e7eafc5954e8b9fea4f9953

# `prompt_parts`

## Summary
- ACP の agent call 向けプロンプトを構成する個別部品を収める領域。ファイルアクセス規則、ルーティング規則、oracle・realization の基本概念、各種標準、レビュー基準、INDEX.md エントリー基準などを StructDoc として組み立てる実装がまとまっている。
- 完全なプロンプトを作る処理から参照される標準プロンプト断片の実体を確認する入口であり、各部品は特定の規則や品質基準を AI に提示するための文書断片生成を担う。

## Read this when
- ACP で agent に渡すプロンプト本文へ含める規則・標準・基礎説明の生成箇所を探したいとき。
- ファイルアクセス規則、INDEX.md を使ったルーティング規則、oracle file と realization file の概念説明など、プロンプト部品ごとの責務を切り分けて確認したいとき。
- oracle standard、realization standard、oracle review standard、apply review standard、index entry standard など、AI の判断基準として注入される規範文書の内容や組み立てを変更したいとき。
- 完全な agent call 用プロンプトが、どの標準プロンプト断片と前提情報を連鎖的に含めるかを追いたいとき。

## Do not read this when
- ACP の通信処理、CLI サブコマンド、状態管理、ファイル入出力など、プロンプト本文の生成以外の制御フローを調べたいとき。
- StructDoc、Standard、Requirement などの文書表現やデータ構造そのものの実装を確認したいとき。
- 実際のファイルシステムアクセス制御やサンドボックスの強制処理を探しているとき。
- 特定の oracle file や realization file の本文内容、または個別機能の仕様そのものを確認したいとき。

## hash
- e45db61782d2b00f497dbd5c18f39c0751c879d4eaac52d71f9f0580f4ec9d3b
