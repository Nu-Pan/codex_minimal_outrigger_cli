# `app_spec`

## Summary
- cmoc のアプリケーション仕様を集約するディレクトリ。CLI 実行、Codex 呼び出し、ログ・エラー処理、feedback、session/run、補完、通知、INDEX.md 更新など、主要機能の正本仕様への入口を提供する。各文書は個別機能の責務、挙動、状態管理、入出力、実装・テスト時の確認条件を定義する。

## Read this when
- cmoc のアプリケーション仕様を横断的に探すとき
- CLI サブコマンド、Codex 実行、feedback、session/run、ログ、エラー処理、補完、通知、INDEX.md 更新の仕様を確認するとき
- 個別機能の正本仕様や、実装・レビュー時に参照すべき仕様の入口を判断するとき

## Do not read this when
- 特定機能の詳細仕様を確認したい場合は、該当する個別仕様書へ直接進むとき
- 具体的な実装配置、テスト実行手順、または realization file の責務だけを確認するとき
- 既存の INDEX.md エントリー内容そのものを確認・更新するとき

## hash
- 5db7a00276fb18d3d8711efc357536f0562a9bd52c5f16f7b49d8a7c856ce74a

# `branch_model.md`

## Summary
- cmoc における branch・commit・worktree のモデルを定義する正本文書。session と run の分岐、命名、分岐元・統合先 commit、run 用 linked worktree の役割と境界を整理し、branch 名ではなく run state と report で workload を表す方針を示す。
- session branch はユーザーが oracle の変更確認やサブコマンド実行に使い、run branch と run worktree は各 run を隔離して差分を commit として積み上げるための実行経路である。

## Read this when
- cmoc の session fork、run 隔離、run join、差分検査、report がどの branch・commit・worktree を基準に動くか確認するとき
- cmoc 管理 branch と通常の local branch・remote-tracking branch・既定 branch の責務や関係を確認するとき
- branch・commit・worktree に workload 別の別名を付けてよいか、または共通概念を使うべきか判断するとき

## Do not read this when
- 特定の CLI サブコマンドの詳細な実装手順や report の個別フォーマットだけを確認したいとき
- oracle の変更内容そのものや、branch model 以外の開発環境・テスト規約を確認したいとき

## hash
- e1e018f45407868dbe8998337a79a15e90cdf11c82febf6207a1758408e0767d

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
