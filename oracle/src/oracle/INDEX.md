# `acp_builder`

## Summary
- AI エージェント呼び出しパラメータを定義する oracle src 群への入口。基本パラメータ型、サブコマンド別 prompt、モデル設定、ファイルアクセス方針、Structured Output schema 指定を扱う。
- apply fork、indexing、oracle review、session join、TUI、ファイルアクセス規則違反復旧など、用途別の agent call parameter と出力契約へ進むためのルーティングを担う。

## Read this when
- cmoc が AI エージェントへ渡す prompt、role、goal、ファイルアクセスモード、モデルクラス、reasoning effort、Structured Output schema の正本仕様断片を探すとき。
- 特定サブコマンドや特定処理に対応する agent call parameter の入力、出力契約、placeholder、読み書き制約を確認・変更したいとき。
- 差分要約、レビュー所見、INDEX.md エントリー生成、merge conflict marker 解消、TUI 起動、ファイルアクセス規則違反復旧などの AI 呼び出し条件を用途別にたどりたいとき。

## Do not read this when
- CLI 引数解析、git 操作、branch 操作、実行フロー、保存処理、結果集約、表示処理など、agent call parameter を利用する realization implementation 側の制御を調べたいとき。
- AgentCallParameter 型、complete prompt builder、placeholder 解決、markdown rendering、ファイルアクセス規則本文生成などの共通部品そのものを調べたいとき。
- oracle file、realization file、index entry、各 standard の定義本文や品質基準そのものを確認したいとき。

## hash
- 53cd601ac64ca27f8bf12befffc6740ec1a03d13a273cc7454fe58cbbe587581

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
- agent call に渡す完全なプロンプトを構築する領域で、役割・概要・ゴール・ファイルアクセス制限・ルーティング規則・補助プロンプト・プレースホルダ定義を統合する処理を扱う。
- oracle/realization/review/index entry などの標準プロンプト注入フラグの依存補正、静的プロンプトと動的プロンプトの配置順、プロンプトキャッシュを意識した構成を確認する入口になる。
- プロンプト全体の結合処理と、AI エージェントへ注入される規範・規則のプロンプト断片、およびプレースホルダ置換用 mapping の基本型を下位要素へ分けている。

## Read this when
- agent call 用の完全なプロンプトが、基本ロール・目的・アクセス制限・ルーティング規則・標準プロンプト・補助プロンプトからどう組み立てられるかを確認または変更したいとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard などの注入指定が、他のプロンプト部品の追加へどう波及するかを調べたいとき。
- 静的プロンプト、動的プロンプト、プレースホルダ定義、ファイルアクセスルールの統合位置や並び順を確認したいとき。
- AI エージェントへ注入される oracle/realization 関連の規範文書、レビュー判定、ファイルアクセス規則、ルーティング規則などの部品を探したいとき。
- プロンプト構築処理で使うプレースホルダ名から文字列または Path への mapping の基本的な型境界を確認したいとき。

## Do not read this when
- 個別の CLI コマンド、状態ファイル、パスモデル、出力 schema など、プロンプト構築以外の機能仕様を確認したいとき。
- cmoc のパス概念そのものや、ルート系プレースホルダの意味を調べたいときは、パスモデルの定義を直接読む方が適切。
- 構造化ドキュメント、標準項目、要求項目などの汎用データ構造だけを確認したいときは、それらの型定義元を読む。
- 生成済みプロンプトをどこで agent call へ渡すか、または実際の realization implementation や realization test の現在構造を追いたいときは、呼び出し側や実装側を読む。
- 既存のルーティング文書や生成済みエントリーを確認したいだけのとき。

## hash
- 072fa0ef24800b8f5e0d4136e7935586c5f62c2aad48b653308c2b33202e631a
