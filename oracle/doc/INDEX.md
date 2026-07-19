# `app_spec`

## Summary
- cmoc のアプリケーション仕様を収録するディレクトリ。CLI 補完、ログ、エラー処理、プロンプト、managed ollama、session/run、サブコマンドなど、利用者向け挙動と主要 workflow の正本仕様を扱う。個別仕様の確認では、該当する仕様ファイルまたはサブコマンド仕様へ進む入口となる。

## Read this when
- cmoc の利用者向け挙動、CLI 実行条件、出力・ログ、状態管理、プロンプト、サービス管理、session/run、サブコマンドの正本仕様の所在を確認するとき。
- 複数のアプリケーション仕様にまたがる workflow や、どの個別仕様を読むべきか判断するとき。

## Do not read this when
- 具体的な機能の詳細仕様が特定できる場合は、このディレクトリ全体ではなく対応する個別仕様ファイルを直接読む。
- 開発環境、設計・テスト規則、oracle/realization の共通定義、または具体的な実装詳細だけを確認するとき。

## hash
- 2da92451d745246352797e3a2bae34d705875532d2e75afb53a3882712b561ea

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
- cmoc の開発規則に関する正本ドキュメント群。Python コーディング、CLI の設計・配置、開発環境、realization test の方針を確認するための入口。

## Read this when
- Python 実装の書き方や命名・型ヒント・import 方針を確認するとき。
- CLI のエントリーポイント、サブコマンド、共有処理の配置を判断するとき。
- Python/venv、依存関係、ファイル命名など開発環境の運用を確認するとき。
- pytest、Real Codex CLI 結合、テスト環境隔離、検証範囲など realization test の方針を確認するとき。

## Do not read this when
- 個別機能やコマンドの挙動仕様を確認したいときは、対象機能の oracle doc を直接読む。
- 個別モジュールの実装詳細を確認したいときは、その実装本文を読む。
- INDEX.md の読み方やルーティング方針を確認したいときは、専用の routing 文書を読む。

## hash
- 2eadee0de716c3689527ae67aef5aeae48aedf5689c90b9bc197be8d5fa9cc60
