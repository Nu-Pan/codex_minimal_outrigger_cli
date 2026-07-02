# `acp_builder`

## Summary
- AI Agent 呼び出しに渡す AgentCallParameter と Structured Output schema の正本仕様断片を集める領域。共通の基本パラメータに加え、apply fork、indexing、review oracle、session join、tui、ファイルアクセス違反リカバリーなど用途別の呼び出し条件と出力契約への入口になる。
- prompt、model class、reasoning effort、file access mode、placeholder、schema パスなど、cmoc の各機能が agent call をどの条件で構成するかを確認するための下位対象を収める。

## Read this when
- cmoc の機能ごとに、AI Agent へ渡す AgentCallParameter、prompt、Structured Output schema の正本仕様断片を探したいとき。
- agent call の model class、reasoning effort、file access mode、role、summary、goal、placeholder、標準文書の組み込み方を、用途別に確認または変更したいとき。
- apply fork のレビュー・報告、indexing の INDEX.md エントリー生成、review oracle、session join の conflict 解消、tui、ファイルアクセス違反リカバリーのいずれかに関する agent call parameter の入口を選びたいとき。

## Do not read this when
- agent call のプロセス起動、実行制御、結果処理、エラー処理など realization implementation 側の処理を調べたいとき。
- CLI 引数、git 操作、branch 操作、状態管理、ファイル探索、INDEX.md 更新など、agent call parameter 構築以外のサブコマンド実行フローを確認したいとき。
- oracle standard、review oracle standard、index entry standard、パスモデル、ファイルアクセス規則本文など、各 prompt に組み込まれる標準文書や共通概念そのものを読みたいとき。

## hash
- df23de11068ec1104d57c7f95d7094f711ea9a966df4235071e179fe709efed5

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
- agent call 用の完全なプロンプトを構築する型・高水準 builder・規範文書パーツ群をまとめる領域。
- oracle/realization の基本概念、各種 standard、レビューやルーティングの規範、ファイルアクセス規則などを StructDoc として組み立て、静的パーツ・動的パーツ・プレースホルダ定義を統合する入口になる。
- 完全プロンプトの構成順序や標準注入フラグ間の依存関係を確認し、必要に応じて個別の規範パーツへ進むためのまとまり。

## Read this when
- agent call に渡す完全なプロンプトの生成順序、静的プロンプトと動的プロンプトの分離、プレースホルダ定義の統合タイミングを確認・変更したいとき。
- oracle standard、realization standard、review standard、index entry standard、file access rule、routing rule など、エージェント用プロンプトへ注入される規範文書の内容や選択入口を探すとき。
- 標準プロンプト注入フラグが他の標準や基本概念の注入へどう波及するかを確認したいとき。
- プロンプト生成で使うプレースホルダ mapping の基本型、または置換先 value として文字列や Path を扱う境界を確認したいとき。
- プロンプトキャッシュヒット率を意識したパーツ配置や、完全プロンプト構築の高水準な責務境界を確認したいとき。

## Do not read this when
- 個別の CLI コマンド、状態ファイル、パスモデル、入出力 schema など、プロンプト構築以外の機能実装や仕様を確認したいとき。
- StructDoc、Standard、Requirement など、規範文書を表す共通データ構造そのものを確認したいとき。
- 生成済みプロンプトが実際にどこで agent call へ渡されるかを追いたいとき。呼び出し側の実装を読む方が適切。
- cmoc のパス概念そのもの、またはプレースホルダを実際に展開・置換する処理の流れを知りたいとき。
- INDEX.md エントリー生成対象の本文がすでに特定されており、この領域内のプロンプト部品や builder を選ぶ必要がないとき。

## hash
- 0c3611734bb5cd14ca676af4f15ba27e04305a67207ad6dce1b3b5caba211df5
