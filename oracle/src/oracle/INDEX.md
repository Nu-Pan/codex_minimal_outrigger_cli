# `acp_builder`

## Summary
- AI エージェント呼び出しパラメータを組み立てる oracle src 群への入口。共通の基本パラメータに加え、apply、indexing、review、session、tui など各機能で使う prompt と Structured Output schema の正本仕様断片を扱う。
- 個別サブコマンド用の agent call parameter と出力契約を探す前に、どの下位領域へ進むべきかを判断するためのルーティング対象。

## Read this when
- cmoc が AI エージェント呼び出しへ渡す parameter、prompt、Structured Output schema の正本仕様断片を探すとき。
- agent call parameter の共通構造と、特定機能向け builder のどちらを読むべきか切り分けたいとき。
- apply fork 後処理、INDEX.md エントリー生成、oracle review、session join の conflict 解消、tui 起動前後のいずれかで使う agent 呼び出し仕様を確認したいとき。

## Do not read this when
- AI エージェント呼び出しではなく、CLI 実行制御、branch 操作、diff 取得、レポート保存、対象ファイル探索、表示整形などの実装を調べたいとき。
- oracle standard、realization standard、index entry standard、file access mode、path placeholder など、agent call parameter 以外の概念定義そのものを確認したいとき。
- realization code 側の prompt builder 実装、外部コマンド起動、バックエンド固有モデル名への変換、テスト構成を確認したいとき。

## hash
- a643bbf574a5c9dc77b567a0427f2dc430f33e2ad30712163217fd2db685d284

# `other`

## Summary
- cmoc の横断的な正本仕様断片を置く領域。リポジトリ単位設定、ルートパスプレースホルダとパス解決、規範文書モデル、構造化 Markdown レンダリング helper への入口になる。

## Read this when
- cmoc の設定値、パス表記モデル、規範文書の構造化、または仕様文生成用 Markdown helper の正本仕様断片を探すとき。
- サブコマンド固有仕様ではなく、複数領域から参照される基礎概念や補助モデルを確認したいとき。

## Do not read this when
- 特定サブコマンドの利用者向け入出力、実行手順、状態ファイル仕様だけを確認したいとき。
- oracle file と realization file の管理方針、INDEX.md のルーティング規則、または個別の規範本文そのものを確認したいとき。

## hash
- f00594a311874ec9cce50630cb6035d65acb894265ac8fb87f197c2268899207

# `prompt_builder`

## Summary
- agent call に渡すプロンプトの構築に関する基本型、完全プロンプトの組み立て処理、標準文書や読み書き規則などのプロンプト部品を扱う領域。
- 役割・概要・ゴール・補助プロンプト・ファイルアクセス制限・ルーティング規則・各種標準の注入指定を統合し、静的部分、動的部分、プレースホルダ定義の配置を決める入口になる。
- oracle file と realization file の責務境界、品質基準、INDEX.md エントリー規範、レビュー規範など、AI に渡す共通規範プロンプトを生成する下位要素への入口でもある。

## Read this when
- agent call 用の完全なプロンプトが、どの部品からどの順序で構築されるかを確認・変更したいとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard などの注入指定が、他のプロンプト部品の追加へどう波及するかを確認したいとき。
- ファイルアクセス制限、ルーティング規則、補助プロンプト、プレースホルダ定義を完全プロンプトへ統合する位置や責務を調べたいとき。
- プロンプトキャッシュヒット率を意識した、静的プロンプト、動的プロンプト、プレースホルダ定義の分離と配置を確認したいとき。
- プロンプト生成で使うプレースホルダ名から文字列またはパスへ置換する mapping の基本型を確認したいとき。
- AI に注入する共通規範として、oracle file、realization file、INDEX.md エントリー、ファイル読み書き、レビュー所見の標準文書を確認・変更したいとき。

## Do not read this when
- 特定の CLI サブコマンド、状態ファイル、入出力形式、パスモデルなど、個別プロダクト仕様を調べたいとき。
- 個別の標準文書本文だけを確認したいときは、この領域全体ではなく、該当するプロンプト部品を直接読む方が適切。
- 構造化ドキュメント、標準文書、要求、プレースホルダ mapping などの汎用データ構造そのものを調べたいだけのとき。
- 生成済みプロンプトが実際にどこで agent call へ渡されるかを追いたいときは、呼び出し側の実装を読む方が適切。
- cmoc のパス概念そのもの、または `<cmoc-root>` や `<work-root>` などの意味を調べたいとき。
- 実装ファイルやテストファイルの現在構造を把握して直接修正したいだけで、プロンプト生成や共通規範の注入に関係しないとき。

## hash
- 6d22edbfda78b6d2616c3e6aa3c260d395390f16d7efa659bc1815aa1b78e4f5
