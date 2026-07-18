# `app_spec`

## Summary
- cmoc のアプリケーション仕様を定める oracle doc ディレクトリ。CLI の補完、ログ、エラー処理、doctor 前処理、managed ollama、Codex CLI 呼び出し、プロンプト、セッション状態、run 隔離、各サブコマンドなどの正本仕様への入口を提供する。

## Read this when
- cmoc の利用者向け挙動、CLI 共通規則、サブコマンドの実行条件や状態遷移を確認するとき。
- managed ollama、Codex CLI、プロンプト生成、ログ、エラー処理、session/run、INDEX.md 更新の仕様を調査・変更するとき。
- 個別のアプリケーション仕様文書を探す入口が必要なとき。

## Do not read this when
- Python の開発環境、設計ルール、テストルールなど開発手順だけを確認したいとき。
- 特定仕様の実装詳細だけを確認したい場合に、対象文書が直接特定できているとき。
- cmoc のアプリケーション挙動や正本仕様と無関係な一般的な調査を行うとき。

## hash
- 9f2aee3e47e4e3e28ecdc424d76154974a7df4ae8a82c6e9061b2edfa3fc559c

# `branch_model.md`

## Summary
- cmoc における branch・commit・worktree の用語と関係を定義する正本文書。session、run、realization の分岐・統合、および関連する命名規則と責務を確認する入口。

## Read this when
- cmoc の session fork/join、run fork/join、realization apply/refactor の branch 運用を変更・実装・レビューするとき
- cmoc 管理 branch、commit、linked worktree の用語や命名規則を確認するとき

## Do not read this when
- branch 運用ではなく、CLI サブコマンド固有の処理仕様や realization 実装の詳細を確認するとき
- 一般的な Git 操作や repository の既定 branch の情報だけを確認したいとき

## hash
- f5a4f62d0ed0f74d970962ad9b460fe72c29d1fedfa72a0e77fd88f9a3c7df70

# `considered_alternative`

## Summary
- cmoc realization refactor で採用しなかった作業方式・設計案と、その不採用理由を記録する文書群。現行仕様や実装の入口ではなく、過去の判断経緯を確認するための参照先。

## Read this when
- refactor の作業フロー、事後検査、permission profile 連携、AI-generated memory、作業計画レビューなど、不採用案の背景や採否理由を確認するとき。
- oracle と realization の責務分担や、採用済み workflow の設計判断に至った経緯を調べるとき。

## Do not read this when
- 現在の実装手順、file access rule、差分検査、CLI 挙動、正本仕様を確認・変更するとき。
- 採用済みの workflow や具体的な実装・テスト対象を調査するとき。

## hash
- ced5ab864d5828938ecc62365eb3fa96cfe8f948cb1ca21c60dc592bbd746106

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
