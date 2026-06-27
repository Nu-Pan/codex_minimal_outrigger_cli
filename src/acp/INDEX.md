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
- ACP の agent call 向けプロンプトを構成する prompt part 群を収める領域。ファイルアクセス規則、ルーティング規則、oracle と realization の基本概念、各種レビュー規範、INDEX.md エントリー規範、完全プロンプト合成など、AI に渡す構造化された標準文書の生成処理を扱う。
- 各 prompt part は、規範本文や判断基準を Standard・Requirement・StructDoc などの構造化文書として組み立て、個別の作業種別に応じて agent prompt へ注入される前提情報の入口になる。

## Read this when
- ACP の agent call に渡すプロンプト本文が、どの標準規範や基本情報から構成されるかを確認したいとき。
- ファイルアクセス規則、INDEX.md を使ったルーティング規則、oracle file と realization file の関係、oracle 記述規範、realization 品質規範、レビュー所見基準、INDEX.md エントリー作成基準など、AI 向け標準プロンプト断片の生成箇所を探すとき。
- 新しい標準プロンプト断片を追加したり、既存の規範文書の内容・順序・依存関係・注入条件を変更したいとき。
- レビュー、apply review、index entry 生成などの作業で、agent にどの判断基準を渡しているかを実装側から確認したいとき。

## Do not read this when
- ACP の通信処理、CLI サブコマンド、永続状態、ファイル入出力、外部コマンド実行など、プロンプト断片生成以外の実装挙動を調べたいとき。
- StructDoc、Standard、Requirement などのデータ構造そのものや、構造化文書の汎用変換・レンダリング処理を調べたいとき。
- 特定の oracle file や realization file の本文内容、または個別機能の正本仕様を確認したいだけのとき。
- 実際のレビュー結果、差分内容、INDEX.md エントリー文面など、生成された成果物そのものを確認したいとき。

## hash
- 7de84f6753d646d11135ae048728a39ad7700881686b272bc6f21514c30eff14
