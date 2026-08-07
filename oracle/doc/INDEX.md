# `app_spec`

## Summary
- cmoc のアプリケーション仕様を集約するディレクトリ。CLI の補完、実行規約、ログ、doctor preprocess、feedback、prompt、session/run、subcommand など、利用者向け挙動と横断的な運用契約を定義する正本仕様群を扱う。個別仕様やサブコマンド仕様へ進むための入口となる。

## Read this when
- cmoc の利用者向け挙動、CLI 実行契約、ログ、feedback、prompt、session/run、またはサブコマンドの正本仕様を調査・実装・変更するとき
- 複数のアプリケーション仕様の責務境界や、共通処理と個別コマンドの関係を確認するとき

## Do not read this when
- 特定仕様の詳細だけを確認する場合は、該当する個別仕様本文へ直接進むとき
- 実装配置、開発環境、テスト実行手順、または個別 builder の実装詳細だけを確認するときは、対応する設計規約・開発規約・realization file を読むとき

## hash
- 92df768ac0489c72cf4ac5d1efe44cf8ffa4898974fafc14de5ea15fe0c1f617

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
- cmoc の Python 開発に関する正本仕様をまとめたディレクトリ。コーディング規則、CLI 設計、開発環境、テスト規則、テスト実行手順を扱い、実装・環境構築・テスト関連の判断における入口となる。

## Read this when
- Python 実装の作成・修正・レビューで、命名、型ヒント、import、docstring、コメント、ログの規則を確認するとき。
- CLI のエントリーポイント、サブコマンド、共有モジュールの配置や責務分担を決めるとき。
- Python 環境の構築、依存関係追加、pip 操作の手順を確認するとき。
- テストの追加・変更・レビューで、検証対象、実経路統合、Ollama、GPU、cache、backend 制約を確認するとき。
- pytest、Ruff、mypy、GPU test などの選択・実行・完了判定・結果報告を行うとき。

## Do not read this when
- CLI の利用者向け挙動や出力形式など、アプリケーション仕様そのものを確認するときは app_spec 配下を直接読む。
- テストの意味上の要件ではなく、構築済み環境でのテスト実行手順だけを確認するときは test_execution.md を直接読む。
- Python 環境の新規構築、依存関係追加、pip 操作だけを確認するときは development_environment.md を直接読む。
- Python の文法、型ヒント、docstring、コメントの書き方だけを確認するときは coding_rule.md を直接読む。
- CLI の実装配置方針だけを確認するときは design_rule.md を直接読む。
- テスト固有の作成・変更要件だけを確認するときは test_rule.md を直接読む。

## hash
- d5d9bb89ee7d975c11d125df48b4eb78f7b43da0e926f53fd25b9f558b62b113
