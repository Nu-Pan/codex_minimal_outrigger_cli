# `oracle`

## Summary
- cmoc が AI エージェントへ渡す完全なプロンプト、作業規定、目的、プレースホルダーを組み立てる正本実装。
- ACP 呼び出しのパラメータ、ファイルアクセスモード、各サブコマンド向けのプロンプト生成を定義する。
- editor input handoff の本文・ガイド生成、文書参照や構造化 Markdown、パス・設定モデルなどの共通データ構造を提供する。
- indexing、oracle 編集・調査、realization の適用・リファクタリング、feedback 処理、session join の conflict 解消といった個別エージェント呼び出しの構築入口を含む。

## Read this when
- エージェント呼び出しの prompt、アクセス制約、Structured Output、cwd、indexing preflight の組み立てを変更・確認するとき。
- cmoc の各サブコマンドがどの agent call builder を使い、どのポリシーや入力を注入するかを追跡するとき。
- editor input handoff、feedback、conflict 解消、INDEX エントリー生成などの実行用パラメータや本文生成の責務を確認するとき。
- 共通のパスモデル、文書参照、構造化ドキュメント表現、設定モデルの仕様を参照するとき。

## Do not read this when
- INDEX.md のルーティング規則そのものだけを確認したいときは、対象ディレクトリではなく indexing の正本仕様を直接読む。
- 特定のサブコマンドの実行処理や CLI/TUI の制御フローだけを調べる場合は、対応する realization 実装を直接読む。
- oracle の意味仕様や利用者向け要件を確認する場合は、この実装群ではなく oracle/doc の正本仕様を読む。
- テストの期待値や回帰条件だけを確認する場合は、対応する oracle/test または realization test を直接読む。

## hash
- ce9371b2c72c30277876c76e3264d62760bc37803434a13347f6077c6bcfde2e
