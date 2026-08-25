# `app_spec`

## Summary
- cmoc のアプリケーション仕様を構成する正本文書群。共通の実行・出力・エラー・隔離・状態管理から、Codex 呼び出し、feedback、補完、通知、各サブコマンドの仕様までを扱い、個別の挙動仕様へ進むための入口となる。
- サブコマンド仕様、workflow、prompt、feedback、run/session lifecycle など、cmoc の利用契約や状態遷移を確認する際に参照する。共通仕様と個別仕様の境界を判断し、必要な下位文書へルーティングするためのディレクトリ。

## Read this when
- cmoc のアプリケーション仕様全体から、実行契約・状態管理・出力・エラー・隔離・feedback・通知・補完などの関連する正本文書を選ぶとき
- 特定のサブコマンド、session/run lifecycle、Codex CLI 呼び出し、feedback report、prompt 入力、Windows toast 通知の仕様入口を確認するとき
- 共通仕様と個別サブコマンド仕様のどちらを読むべきか判断するとき

## Do not read this when
- 特定の機能の詳細仕様を確認する場合は、このディレクトリの案内ではなく対応する個別の正本文書を直接読むとき
- 具体的な実装責務、テスト手順、oracle・realization の分類、既存 INDEX.md の内容だけを調べるとき

## hash
- e52e7b0f1537334c3a2d7ab368be7d6cf10d1f0045492ea00409bd3eeb38b2c4

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
- `oracle/doc/dev_rule` は、cmoc の Python 開発における実装規約・CLI 配置方針・開発環境・テスト要件・テスト実行手順をまとめた正本文書群への入口です。コードの書き方、実装の責務配置、環境操作、テストの意味要件、品質検査の実行方法を、目的に応じて下位文書へ振り分けます。

## Read this when
- Python 実装の命名、型ヒント、import、docstring、コメント、ログなどのコーディング規約を確認するとき
- cmoc CLI のエントリーポイント、サブコマンド、共通処理の配置や責務分担を判断するとき
- Python 環境の構築、依存関係追加、pip 操作の規則を確認するとき
- テストの意味上の要件、隔離、実経路統合テスト、Fake Codex CLI の適用条件を確認するとき
- 既存環境で focused/full test、Ruff、mypy などの品質検査を選択・実行・判定するとき

## Do not read this when
- cmoc の CLI 挙動や出力内容そのものの正本仕様を確認するときは app_spec 配下を直接読む
- 特定機能の仕様や設計上の責務を確認するときは、該当する正本仕様や design_rule.md を直接読む
- テストの意味要件を確認するときは test_rule.md を、テストの実行手順だけを確認するときは test_execution.md を直接読む
- Python 環境の新規構築、依存関係追加、pip 操作を行うときは development_environment.md を直接読む

## hash
- 0b52a720361759ae57f0cb498da300a523b3ab67c0ec3586c57522da36ba1d3b
