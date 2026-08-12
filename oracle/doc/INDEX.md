# `app_spec`

## Summary
- cmoc のアプリケーション仕様を集約するディレクトリ。CLI 自動補完、Codex 実行・provider 設定、ログ、doctor preprocess、feedback、prompt、run／session、サブコマンド中断、利用手順、Windows toast 通知などの正本仕様を扱う。各仕様の責務と適用範囲を確認し、実装・変更・レビュー時に該当する下位文書へ進むための入口である。

## Read this when
- cmoc のアプリケーション挙動に関する正本仕様を探すとき
- CLI、Codex 呼び出し、ログ、feedback、prompt、run／session、通知、サブコマンドの仕様から読むべき下位文書を選ぶとき
- 複数のアプリケーション仕様が関係する変更やレビューで、仕様の分担と境界を確認するとき

## Do not read this when
- 実装ファイルやテストの具体的な挙動だけを確認する場合
- 特定の仕様文書が既に判明しており、その本文を直接確認すれば足りる場合
- 開発環境、設計ルール、テスト実行手順など、アプリケーション仕様以外のリポジトリ運用を確認する場合

## hash
- fdf762a6a6298d9ca93d3067a32190c82fba309093774684d4953363c9d0491b

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
- cmoc の開発ルールに関する正本文書群への入口。Python コーディング規約、CLI の設計・実装配置、開発環境、テスト要件、テスト実行・品質検査の手順を扱い、実装・環境構築・テスト関連の判断に応じて各文書へ進むための領域。

## Read this when
- cmoc の Python 実装を作成・変更・レビューし、コーディング規約や型・命名・入出力方針を確認するとき
- CLI のエントリーポイント、サブコマンド、共有処理の責務や配置を判断するとき
- Python 環境の構築、依存関係の追加、pip 操作、実行環境の前提を確認するとき
- realization test の意味要件、隔離、実経路統合テスト、Fake Codex CLI の適用条件を確認するとき
- 既存環境で focused/full test、品質検査、実経路統合テストの実行・判定・報告手順を確認するとき

## Do not read this when
- テストの意味上の要件だけを確認する場合は、テスト要件を定める文書へ直接進む
- テストや品質検査の実行手順だけを確認する場合は、テスト実行手順を定める文書へ直接進む
- CLI の挙動や出力内容そのものを確認する場合は、アプリケーション仕様の文書へ直接進む

## hash
- 56b4ef90349ea3545524ad8783ffba1ae66060c50c4d829d418330365923484d
