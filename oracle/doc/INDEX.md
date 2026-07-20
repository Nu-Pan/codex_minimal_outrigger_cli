# `app_spec`

## Summary
- cmoc のアプリケーション仕様をまとめた oracle 文書群。CLI 自動補完、Codex 呼び出し・provider 設定、ログ、doctor preprocess、エラー処理、プロンプト、run/session lifecycle、サブコマンド、中断処理、標準 workflow などの正本仕様へ進むための入口。

## Read this when
- cmoc の利用者向け挙動、共通仕様、CLI 呼び出し、状態管理、ログ、プロンプト、run/session lifecycle を実装・検証するとき
- 対象機能に対応する個別仕様文書を選び、仕様上の責務や制約を確認したいとき

## Do not read this when
- 対象が特定の realization code または realization test の内部実装だけであるとき
- 一般的な開発環境・設計・テスト手順を確認したいときは、対応する開発規約を直接読む

## hash
- 5c2c236902481e52c10a217fde3bd6e7fcfa9bf5e28d91865167b7e24b6d0a5e

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
- cmoc の開発規約をまとめた oracle doc 群。Python コーディング、CLI の責務配置、開発環境、pytest による realization test の方針を確認するための入口。

## Read this when
- Python 実装の書き方や命名・型ヒント・コメント規則を確認したいとき。
- CLI のエントリーポイント、サブコマンド、共有処理の配置方針を判断したいとき。
- Python/venv、依存関係、ファイル命名などの開発環境ルールを確認したいとき。
- pytest、実経路統合テスト、test-local Ollama、キャッシュ隔離などのテスト規約を確認したいとき。

## Do not read this when
- 個別機能や CLI の具体的な挙動・出力仕様を確認したいときは、app_spec 配下の対応する oracle doc を読む。
- 個別モジュールの実装詳細を確認したいときは、対応する realization implementation を直接読む。
- INDEX.md の読み方やルーティング方針を確認したいときは、別の routing 文書を読む。

## hash
- 1432317a33591d4375f1ae8f4fd20238371162235a3687052f18c53ee7d0be72
