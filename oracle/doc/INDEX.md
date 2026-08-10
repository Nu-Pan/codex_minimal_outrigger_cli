# `app_spec`

## Summary
- cmoc の CLI、workflow、feedback、ログ、Codex CLI 呼び出し、Windows toast 通知などに関する正本仕様をまとめたディレクトリ。個別仕様へ進むための入口として、各機能の責務境界・挙動・制約を扱う。

## Read this when
- cmoc のサブコマンドや共通 lifecycle の仕様を確認・変更するとき
- Codex CLI 呼び出し、prompt、feedback、ログ、通知、自動補完の仕様を確認するとき
- run・session・state・エラー処理・中断などの共通ルールを確認するとき
- INDEX.md の自動生成や oracle／realization の列挙規則を確認するとき

## Do not read this when
- 特定仕様の実装配置やテスト実行方法だけを調べるときは、対応する realization implementation、realization test、または開発ルールへ直接進む
- 個別機能の詳細ではなく、一般的な利用手順だけを確認するときは利用手順書へ直接進む
- 対象ディレクトリに含まれない provider 固有の稼働、認証、推論品質、外部サービスの詳細を調査するとき

## hash
- c79f358b52e51549b525e213dd9cee22576a2afd235a04755a37782aed4b62f7

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
- cmoc の開発規則を定める正本仕様群への入口。Python コーディング、CLI 設計、開発環境、テスト要件、テスト実行・品質検査の各領域を扱い、作業内容に応じて個別文書へ分岐する。

## Read this when
- Python 実装の規則、CLI の設計責務、開発環境や依存関係、realization test の要件、または test と品質検査の実行手順を確認するとき
- cmoc の実装・テスト作業で、適用すべき正本仕様の入口を判断するとき

## Do not read this when
- CLI の具体的な挙動や出力仕様を確認するときは、app_spec 配下の該当文書を直接読む
- 個別の実装規則だけを確認するときは、コーディング規則の文書を直接読む
- テストの意味要件だけを確認するときは、テスト規則の文書を直接読む
- 構築済み環境でのテスト選択・実行・完了判定だけを確認するときは、テスト実行手順の文書を直接読む
- Python 環境の構築、依存関係追加、pip 操作だけを確認するときは、開発環境の文書を直接読む

## hash
- e56b2fe9c76c29fabba93b9c167539407454585fd9045d783db221f7bf21f2e8
