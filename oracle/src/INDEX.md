# `oracle`

## Summary
- AI エージェント呼び出しの論理パラメータとプロンプト構築、およびそれらを支える設定・パス・規範表現・Markdown レンダリングの正本仕様断片を扱う領域。
- 個別の agent call 契約や共通プロンプト規範から、リポジトリ設定、ルートパス変換、構造化文書モデルまで、実装・テストへ反映する前に参照するソース形式の仕様群への入口となる。

## Read this when
- AI エージェント呼び出しについて、モデル設定、reasoning effort、ファイルアクセス権限、prompt、cwd、indexing preflight、Structured Output schema の正本仕様断片を確認するとき。
- 完全プロンプトの構成順序、静的部分と動的部分の配置、プレースホルダ置換、ファイルアクセス規則や各種標準文書の注入方法を確認するとき。
- INDEX.md エントリー生成、oracle file レビュー、fork 適用後レビュー、session join の conflict marker 解消、TUI 起動に用いる agent call の入力・出力契約を確認するとき。
- リポジトリ別設定、ルートパスの探索と変換、規範の構造化表現、階層文書の Markdown レンダリングに関する正本仕様断片を探すとき。
- これらの概念を利用する realization implementation または realization test を変更する前に、人間意図との境界を確認するとき。

## Do not read this when
- CLI 引数処理、branch・diff・merge・保存・表示など、個別サブコマンドの実行制御だけを調べるとき。
- バックエンド API の実リクエスト形式、具体的なモデル名への解決、agent CLI の起動処理など、realization implementation 固有の詳細だけを調べるとき。
- 個別サブコマンドの利用者向け入出力、実行フロー、永続状態だけを確認するときは、その仕様を直接扱う領域へ進む。
- oracle standard、realization standard、review standard などの具体的な規範本文だけを確認するときは、対象の標準文書へ直接進む。
- 生成済みプロンプトや Markdown の内容・配置だけを確認し、その構築規則や構造化表現を調べる必要がないとき。

## hash
- 473fd3377ae88f67818028f908bf5242f993bfa19b535220c8a9417c7b61bc74
