# `app_spec`

## Summary
- cmoc のアプリケーション挙動仕様を集約する正本文書群。CLI 自動補完、Codex 呼び出し、ログ・エラー処理、doctor preprocess、feedback、prompt、session/run、サブコマンド、通知などの個別仕様への入口を提供する。実装・テスト・仕様適合性確認では、対象機能に対応する下位仕様へ進むために読む。

## Read this when
- cmoc の利用者向け挙動仕様、共通実行契約、サブコマンド lifecycle、feedback、prompt、session/run、通知の正本を探すとき
- 複数のアプリケーション仕様にまたがる責務境界や、適切な下位仕様の入口を確認するとき

## Do not read this when
- 特定機能の詳細仕様が明らかな場合は、このディレクトリ全体ではなく対応する個別仕様を直接読む
- 実装コード、realization の具体的挙動、テスト実行手順、開発環境の規則だけを確認するとき

## hash
- 29dedadc8cee1a001c2eeaae72c4bfad7199c630f26874948696ab93e661b3e3

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
