# `builder`

## Summary
- AI エージェント呼び出し用のパラメータ構築を扱う領域。各処理で渡す role、summary、goal、補助プロンプト、参照する標準文書、ファイルアクセスモード、モデル種別、推論量、Structured Output schema の接続を組み立てる入口である。
- フォーク適用、目次エントリー生成、oracle review、session の conflict 解消、TUI 実行パラメータ解決など、上位コマンドが実際の処理を AI に委ねる直前の呼び出し条件を、用途別の下位領域へ分けて収める。
- 実際の差分解析、レビュー所見の保存、merge 実行、CLI/TUI の起動制御、共通 prompt 部品そのものを担う領域ではなく、それらを使って個別の agent 呼び出し契約を作る builder 群である。

## Read this when
- AI エージェントに渡す complete prompt の内容、補助プロンプトへの入力データ埋め込み、参照標準、ファイルアクセス権限、モデル種別、推論量、出力 schema の対応を確認または変更したいとき。
- 上位コマンドのどのフェーズが、読み取り専用の調査、oracle file のレビュー、realization file の修正、conflict marker 解消、実行パラメータ選定のどの agent 呼び出しへつながるかを追いたいとき。
- raw diff、対象パス、所見リスト、元プロンプト、conflict 対象ファイル一覧などの入力が、AI への作業指示や Structured Output の契約としてどう渡されるかを確認したいとき。
- 下位領域のうち、フォーク適用用、目次生成用、oracle review 用、session conflict 解消用、TUI パラメータ解決用のどれを読むべきか判断したいとき。

## Do not read this when
- コマンド全体の実行フロー、サブコマンド入口、状態管理、ファイル走査、保存、通知、CLI/TUI 入出力の外側の制御を調べたいとき。
- git 操作、ブランチ操作、merge 実行、conflict 検出、差分取得、作業ツリーへの反映など、実際のリポジトリ操作を調べたいとき。
- AI 呼び出し後の結果検証、所見の統合実行、修正結果の確認、テスト実行など、builder が返したパラメータを使った後段処理を調べたいとき。
- complete prompt の共通構築、構造化 Markdown 描画、パス解決、ファイルアクセスモード定義、AgentCallParameter 型などの汎用部品そのものを確認したいとき。
- Structured Output schema の項目名・型・JSON 形式だけを機械的に確認したいときは、該当する schema 本文へ直接進めばよい。

## hash
- 04335ab886dd86f56ee356ae141d2429baf25c7dacb7cf5975382521c0b241b0

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
