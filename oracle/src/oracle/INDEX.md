# `acp_builder`

## Summary
- AI エージェント呼び出しパラメータと Structured Output schema の正本仕様断片を扱う領域。
- apply fork、oracle review、session join、TUI、indexing、ファイルアクセス規則違反リカバリーなど、各処理で AI に渡す prompt、モデル設定、reasoning effort、ファイルアクセス方針、出力契約を確認する入口になる。
- 共通の呼び出しパラメータ型と、用途別の agent call parameter 構築仕様へ進むためのルーティングを担う。

## Read this when
- 各サブコマンドや処理段階が AI agent call に渡す role、summary、goal、prompt 断片、placeholder、モデル設定、reasoning effort、file access mode を確認または変更したいとき。
- 差分要約、実装レビュー所見、oracle file レビュー、INDEX.md エントリー生成、merge conflict marker 解消、TUI 起動、ファイルアクセス規則違反リカバリーの出力契約や Structured Output schema への接続を調べたいとき。
- AgentCallParameter が保持する論理モデルクラス、reasoning effort、ファイルアクセスモード、プロンプト、schema パスの基本形を確認したいとき。
- AI 呼び出しごとの読み取り・書き込み制約や、対象内容・既知所見・差分・衝突対象などの入力が prompt にどう渡るかを正本仕様断片から確認したいとき。

## Do not read this when
- CLI 引数解析、git 操作、branch 操作、作業レポート保存、結果集約、表示処理など、サブコマンド全体の実行フローを調べたいとき。
- complete prompt builder、markdown rendering、path placeholder 解決、AgentCallParameter の利用側実装など、共通部品の汎用実装詳細だけを確認したいとき。
- oracle file、realization file、index entry、各 standard、review oracle standard などの品質基準本文や定義そのものを読みたいとき。
- バックエンドが受理する具体的なモデル名や reasoning effort 名への変換、agent call のプロセス起動、結果処理、エラー処理を調べたいとき。

## hash
- a46bef60ba9002c0db270954d5fec4e43869ef57dfd555d75fe76672272efb8f

# `other`

## Summary
- cmoc の正本実装断片のうち、設定、パス表記モデル、規範文書モデル、構造化 Markdown レンダリング helper など、複数領域から参照される基礎的な補助モデルを扱う。
- リポジトリ別設定の既定値と永続化境界、ルートプレースホルダ付きパスの解決規則、規範を構造化して保持するデータ構造、階層文書を Markdown へ整形する処理への入口になる。

## Read this when
- cmoc の設定項目、既定値、設定ファイルの永続化先、人間編集される設定の境界を確認したいとき。
- Codex CLI、apply fork、review oracle などに渡るリポジトリ別の挙動設定を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのルート概念、プレースホルダ付きパス、絶対パス、git worktree との関係を確認したいとき。
- 規範文書を背景・要求・判断例などの構造で保持し、構造化ドキュメントへ変換するためのモデルを確認したいとき。
- 階層化された文章、本文、コードブロックを Markdown としてレンダリングする helper の挙動を確認したいとき。

## Do not read this when
- INDEX.md のルーティング規則、oracle file と realization file の管理方針、または実現ファイルに適用される品質基準そのものを確認したいだけのとき。
- 設定の読み書き処理、JSON 変換処理、`cmoc init` の実装箇所を探しているとき。
- CLI サブコマンドの利用者向け入出力、実行フロー、状態ファイル、レビュー所見の生成・検証ロジック自体を確認したいとき。
- Markdown 文書や規範本文の意味そのものを知りたいだけで、文書を構成・整形するモデルやレンダリング helper を確認する必要がないとき。
- 特定の作業ディレクトリ内でどのファイルを読むべきかを知りたいだけで、パス表記モデルやルート解決規則を確認する必要がないとき。

## hash
- 348ed377a452b49241d8bc01765ee8d240d5ba0a2dd1606c2d9bd5dbef29d249

# `prompt_builder`

## Summary
- agent call に渡す完全なプロンプトを構築するための基本型、高水準 builder、横断的な規範 prompt 部品群をまとめる領域。
- 役割・概要・ゴール・ファイルアクセス制限・ルーティング規則・各種 standard・補助プロンプト・placeholder 定義を、どの責務で組み立てるかを確認する入口。
- 完全プロンプトの構成順序を扱う上位処理と、oracle file・realization file・INDEX.md・review・file access などの個別規範部品へ進むための分岐点になる。

## Read this when
- agent call 用の完全なプロンプト生成処理の入口を探しているとき。
- oracle standard、realization standard、review standard、index entry standard、file access rule、routing rule などの prompt 注入に関わる責務境界を切り分けたいとき。
- 静的プロンプト、動的プロンプト、補助プロンプト、placeholder 定義、ファイルアクセス制限をどの順序で統合するかを確認・変更したいとき。
- プロンプト生成で使う placeholder mapping の基本型や、置換先に文字列と Path のどちらを許容するかを確認したいとき。
- 横断的な作業規範の prompt 部品本文を確認・変更するために、目的に合う下位対象を選びたいとき。

## Do not read this when
- 特定の CLI コマンド、状態ファイル、パス解決、テスト方針など、プロダクト個別仕様の正本仕様断片を探しているとき。
- StructDoc、Standard、Requirement など、prompt 部品が利用する共通データ構造そのものを調べたいとき。
- 生成済みプロンプトを実際にどこで agent call へ渡しているかを追いたいとき。呼び出し側の実装を読む方が適切。
- cmoc のパス概念そのもの、または `<cmoc-root>` や `<work-root>` などの意味を調べたいとき。パスモデルの定義を直接読む方が適切。
- 実装ファイルやテストファイルの現在構造を確認して、具体的なコード変更箇所を探したいだけのとき。

## hash
- baa355aa3a8457d1a94c0b8d09123a66849fdba33b203d4b16056a4e7e0df1b0
