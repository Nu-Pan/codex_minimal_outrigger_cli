# `oracle`

## Summary
- ACP builder 配下には参照可能な正本ソースがなく、ACP 呼び出し設定に関する正本ソースの有無と配置を確認するための入口。基礎パラメータ、indexing、oracle、realization、session、tui の領域を含む。
- cmoc の oracle 実装に用いる設定・パスモデル・規範データ構造・構造化 Markdown 文書化を定義するファイル群。設定、ルート探索、規範文書の構造化、Markdown 変換を確認する入口。
- プレースホルダと実パス・文字列の対応、完全なエージェント呼び出しプロンプトの構築、プロンプトへ注入する標準ルール部品を定義するファイル群。

## Read this when
- ACP builder 配下に参照可能な正本ソースがあるか、または ACP 呼び出し条件に関係する正本ソースの配置先を探索するとき。
- cmoc の設定値、既定値、Codex CLI・provider 設定、oracle review の上限を確認・変更するとき。
- cmoc・repo・run・work のルート探索、パスプレースホルダ変換、git worktree 対応を確認するとき。
- 規範文書のデータ構造や Requirement・Standard の構造化、StructDoc の Markdown レンダリングを確認するとき。
- プレースホルダ展開の型、完全なプロンプトの構造、標準ルールの依存関係や動的プロンプトの組み立てを調査・変更するとき。
- oracle・realization、INDEX.md、ファイルアクセス規則、レビュー基準など、プロンプトへ注入する標準ルールの内容を調査・変更するとき。

## Do not read this when
- 具体的な ACP 実装仕様、処理内容、呼び出しパラメータの詳細を確認したい場合は、該当する配下ファイルを直接読む。
- CLI の設定読み書き、doctor による生成・同期、または設定利用側の個別機能を確認したい場合。
- モデル分類や推論 effort の Enum 定義だけを確認したい場合。
- 個別の標準文書の内容、oracle file の配置・命名規則、CLI の実行経路、プロンプト生成全体、Markdown 以外の文書レンダリングを確認したい場合。
- プロンプト本文の生成手順や置換ロジック、特定の注入パーツや個別標準ルール、個別の oracle file・realization file、CLI コマンド、実際のファイル操作だけを調べたい場合。

## hash
- 2e6ddef2c8b80836226612a6f347d3488acca8902c9a67daa799e044b797d519
