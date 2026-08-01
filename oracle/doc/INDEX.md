# `app_spec`

## Summary
- cmoc の CLI、Codex 呼び出し、ログ、doctor、INDEX 生成、prompt、run/session lifecycle、サブコマンドなどの正本仕様を収録する app_spec の入口。個別機能の仕様を探し、関連する oracle doc へ進むために読む。

## Read this when
- cmoc の機能仕様や共通仕様の正本文書を探すとき
- CLI 補完、Codex 呼び出し、ログ、doctor、prompt、run/session、サブコマンド、INDEX 更新の仕様を確認するとき
- 対象機能に対応する個別の oracle doc を特定するとき

## Do not read this when
- 特定の仕様文書が既に分かっており、その本文だけを確認すればよいとき
- 実装構造、テスト手順、開発環境など、対応する realization code・realization test・dev_rule の文書を直接読むべきとき
- 一般的な Codex CLI、model provider、認証、推論品質など cmoc の正本仕様外の事項を調査するとき

## hash
- 22d1f862e9753f1dc2d3fd865638ef972ee78cdd1e9f89268c38bf58fae51152

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
- cmoc の開発規約を扱うディレクトリ。Python コーディング、CLI の設計・実装配置、開発環境、pytest による realization test の規約を確認するための入口。各規約の詳細は用途に応じた個別文書で確認する。

## Read this when
- Python 実装の命名・責務・型ヒント・import・docstring・コメントを確認するとき。
- CLI のエントリーポイント、サブコマンド、共有処理の配置方針を確認するとき。
- Python/venv・依存関係・ファイル形式などの開発環境ルールを確認するとき。
- pytest、実経路統合テスト、GPU test、cache、timeout などのテスト規約を確認するとき。

## Do not read this when
- 個別機能や CLI の具体的な挙動・出力仕様を確認したいとき。
- README だけで足りる一般的な利用方法を確認したいとき。
- 既存の INDEX.md のルーティングだけを更新したいとき。

## hash
- a1c4a09fee986b0f4fd273d2cab6a7a54416595437dc16acddbcacc63cfcc4b7
