# `app_spec`

## Summary
- cmoc のアプリケーション仕様を定義する正本文書群。CLI 自動補完、Codex CLI 呼び出し、ログ、doctor preprocess、prompt、session/run lifecycle、サブコマンドなど、主要な利用者向け挙動と運用規約を扱う。個別仕様を探す際の入口となる。

## Read this when
- cmoc のアプリケーション挙動に関する正本仕様を探すとき
- CLI、agent call、ログ、prompt、session/run、サブコマンドの仕様を確認するとき
- 対象となる個別仕様文書がまだ特定できていないとき

## Do not read this when
- 対象となる個別仕様文書が明確なときは、その文書を直接読む
- 開発環境、設計ルール、テスト実行手順を確認するとき
- 実装構造やテストの詳細だけを確認するとき

## hash
- 13ceb178106f5d8fbdbe54ffed5da49ecff6b4a1e3819bcff85b70add5a4847e

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
- cmoc realization refactor で採用しなかった作業方式・検査方式・状態管理方式の検討記録をまとめたディレクトリ。事前計画、並列所見管理、事後差分検査、gitignore 連携、AI-generated memory などの不採用理由を確認する入口であり、採用済みの現行仕様や実装の直接の参照先ではない。

## Read this when
- cmoc realization refactor の作業フローや調査・修正単位の設計理由を確認するとき
- 事前計画方式、並列所見調査、ダーティフラグ方式、事後検査方式の採否理由を調べるとき
- AI-generated memory や継続的な自動注入を採用しない根拠を確認するとき
- .gitignore と permission profile の連携案など、採用しなかった設計案の背景を追うとき

## Do not read this when
- 現在の realization refactor state、investigation_required、file access rule、差分検査、agent 呼び出し経路の現行仕様を確認・変更するとき
- 具体的な realization file の修正方法や実装責務を調べるとき
- 単に対象ファイルの実装内容・テスト内容・CLI 挙動を確認したいとき
- INDEX、oracle、ログ、実行成果物の具体的な形式や生成手順を調べるとき

## hash
- e8ae09d4765b54ddbb1f85d76ac964f673594e7c13e23286b94d284255689829

# `dev_rule`

## Summary
- cmoc の開発ルールをまとめた正本仕様群。Python コーディング規則、CLI の実装配置、開発環境、realization test の方針を扱い、実装・テスト・環境構築時の判断入口となる。

## Read this when
- Python 実装の命名、責務分割、型ヒント、import、docstring、コメント、公開範囲を確認するとき。
- CLI のエントリーポイント、サブコマンド、共有処理の配置境界を判断するとき。
- Python 環境の構築、依存関係の追加、pip の実行方法を確認するとき。
- realization test の設計・実装・レビュー、統合テスト、Ollama、GPU、キャッシュ、backend、認可境界を確認するとき。

## Do not read this when
- 構築済み環境での具体的なテスト・Ruff・mypy の実行手順だけを確認したいときは、repository local の run-cmoc-tests skill を読む。
- CLI の具体的な挙動や出力仕様を確認したいときは、app_spec 配下を読む。

## hash
- 3168391ca2cada110d5557bab2d03d5cda1bd52571b8762039c35b92c3bc20e9
