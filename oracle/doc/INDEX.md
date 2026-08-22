# `app_spec`

## Summary
- cmoc の主要サブコマンドと session・run lifecycle に関する正本仕様を集約するディレクトリ。doctor、indexing、feedback、oracle・realization 操作、session、run、TUI などの実行契約、状態遷移、report 要件を確認するための入口であり、各仕様ファイルへ進む起点となる。

## Read this when
- cmoc のサブコマンド仕様を横断して探すとき
- 対象サブコマンドの実行条件、処理手順、終了経路、primary report、state 遷移の正本を確認するとき
- realization の fork・run lifecycle、session の fork・join・abandon、または oracle 操作の仕様入口を選ぶとき

## Do not read this when
- 特定サブコマンドの詳細仕様が既に分かっており、該当する仕様ファイルを直接読めるとき
- 内部実装の配置、テスト実行手順、または個別 oracle・realization file の内容だけを確認するとき
- 既存 report の具体例や生成物だけを調査するとき

## hash
- 52780ffe419f1be924586512fbca3cd1d29f0619db8a13a3d4f0c3c62793285c

# `branch_model.md`

## Summary
- cmoc の branch・commit・worktree に関する用語と関係を定義する正本仕様。session と run の分岐、各 branch の役割、分岐・merge commit、run 用 linked worktree の位置づけを確認する入口。

## Read this when
- cmoc の session fork、run の隔離、branch／commit／worktree の命名や責務を変更・調査するとき
- run report、差分検査、apply、session join などで基準 commit や merge 先を確認するとき
- workload の種類を branch 名や commit の別名で表す設計を検討するとき

## Do not read this when
- 特定の CLI サブコマンドの実装詳細だけを調査しており、branch model の用語やライフサイクルを確認する必要がないとき
- oracle の一般原則や開発環境・テスト手順を確認したいときは、対応する oracle 文書を直接読む

## hash
- 60e0fa11a169c939bcecc5b8527c50f43bb563b7365db6f9e3e9d29e0baaba7d

# `considered_alternative`

## Summary
- cmoc の設計・リファクタで採用しなかった作業方式や仕様案を記録する検討資料群。事前計画、並列所見管理、事後アクセス違反検査、`.gitignore` 連携、AI-generated memory などの不採用理由を確認するための入口であり、採用済みの現行仕様や具体的な実装手順の正本ではない。

## Read this when
- cmoc realization の作業フローや調査単位について、採用しなかった代替案とその理由を比較するとき
- AI による作業計画・memory の自動継承や、アクセス制御の事後検査、`.gitignore` 連携案の採否背景を調査するとき
- 現行設計が特定の代替方式を採用しなかった根拠を確認したいとき

## Do not read this when
- 現行のアクセス制御、refactor state、oracle、realization の仕様を確認・変更するとき
- 具体的な realization file の実装方法、CLI の挙動、テスト手順を調べるとき
- 採用済み workflow の操作方法や現在の実行結果だけを確認したいとき

## hash
- 2306639b6cb9d46169d1e0614cafd6a1ff50856b67ccfe5f40849ae09d0cd405

# `dev_rule`

## Summary
- Python 開発規約、cmoc の CLI 設計・実装配置、開発環境、テスト要件、テスト実行と品質検査の手順を扱う開発ルール文書群。Python 実装や CLI 配置、環境構築、テスト設計・実行に応じて各正本文書へ進む入口。

## Read this when
- Python コードの書き方、命名、型ヒント、import、コメント、docstring、ログ、最小限の実装方針を確認するときは coding_rule.md
- CLI のエントリーポイント、サブコマンド、共有処理の配置や責務分担を確認するときは design_rule.md
- Python 仮想環境の作成、依存関係追加、pip 操作、実行環境の前提を確認するときは development_environment.md
- realization test の意味要件、隔離、実経路統合テスト、Fake Codex CLI の適用条件を確認するときは test_rule.md
- 既存環境での test・Ruff・mypy などの選択、実行、完了判定、結果報告を行うときは test_execution.md

## Do not read this when
- CLI の挙動や出力内容そのものの正本仕様を確認したいときは app_spec 配下を直接読む
- テストの意味要件を確認したいときは test_execution.md ではなく test_rule.md を直接読む
- 環境構築、依存関係追加、pip 操作を行いたいときは test_execution.md ではなく development_environment.md を直接読む
- 実装の設計責務や CLI 配置を確認したいときは test_rule.md ではなく design_rule.md など実装側の正本を直接読む

## hash
- e56b2fe9c76c29fabba93b9c167539407454585fd9045d783db221f7bf21f2e8
