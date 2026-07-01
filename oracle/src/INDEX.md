# `oracle`

## Summary
- AI Agent 呼び出し条件と Structured Output schema、完全プロンプト構築、設定・パス表記・規範文書モデルなど、cmoc の正本実装断片のうち複数機能の基礎になる領域をまとめる。
- 用途別の AgentCallParameter、プロンプトへ注入される標準文書、ルートプレースホルダ付きパスや設定の正本仕様断片を探すための入口になる。

## Read this when
- cmoc の機能が AI Agent へ渡す prompt、model class、reasoning effort、file access mode、role、summary、goal、Structured Output schema を正本仕様断片として確認または変更したいとき。
- agent call 用の完全なプロンプトの構成順序、静的パーツと動的パーツの分離、標準文書の注入条件、placeholder mapping の扱いを確認したいとき。
- oracle/realization の基本概念、各種 standard、review や routing の規範、file access rule など、エージェント用プロンプトに組み込まれる規範文書への入口を探すとき。
- cmoc の設定項目、既定値、設定ファイルの永続化境界、リポジトリ別挙動設定の正本仕様断片を確認したいとき。
- <cmoc-root>、<repo-root>、<run-root>、<work-root> などのルート概念、placeholder 付きパス、絶対パス、git worktree との関係を確認したいとき。
- 規範文書を構造化して保持するモデルや、階層化された文章・本文・コードブロックを Markdown として整形する helper の挙動を確認したいとき。

## Do not read this when
- agent call のプロセス起動、実行制御、結果処理、エラー処理など、正本仕様断片ではなく realization implementation 側の処理を調べたいとき。
- CLI 引数、git 操作、branch 操作、状態管理、ファイル探索、INDEX.md 更新など、agent call parameter やプロンプト構築以外のサブコマンド実行フローを確認したいとき。
- StructDoc、Standard、Requirement などの共通データ構造ではなく、規範本文の意味だけを確認したいとき。
- 生成済みプロンプトが実際にどこで agent call へ渡されるか、または設定の読み書き処理や JSON 変換処理の実装を追いたいとき。
- 特定の作業ディレクトリ内で読むべきファイルを知りたいだけで、パス表記モデル、ルート解決規則、agent call 条件、プロンプト部品を確認する必要がないとき。

## hash
- 7826fd8e9a35fe7ce4aadad73fb60bb7e4d4e6e0b639b678858a9931b7a6d5e6
