# `app_spec`

## Summary
- cmoc の正本仕様文書を集約するディレクトリ。CLI 自動補完、Codex CLI 呼び出し、ログ、doctor preprocess、プロンプト、run・session lifecycle、サブコマンドなどの仕様確認における入口であり、各機能の詳細は対応する文書または下位ディレクトリへ進む。

## Read this when
- cmoc の正本仕様を横断的に探すとき
- CLI 起動、Codex CLI 呼び出し、ログ、プロンプト、run・session、サブコマンドの仕様上の入口を確認するとき
- 複数の機能に共通する仕様文書の所在を判断するとき

## Do not read this when
- 特定の機能の詳細仕様が明らかな場合は、対応する個別文書または下位ディレクトリへ直接進むとき
- realization の実装・テストの詳細だけを調査するとき
- cmoc の一般的な利用手順だけを確認するときは、利用手順書を直接読むとき

## hash
- 2579b005fcf0c94abd6b2867658d412f63a22b0d7ae022874630128bcc77807f

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
- Python 実装のコーディング規則、CLI の設計・配置方針、開発環境の運用ルール、pytest による realization test 規約をまとめた開発ルール文書群。実装・テスト・環境設定に関する判断の入口。

## Read this when
- cmoc の Python 実装方針、型ヒント、import、docstring、コメント、命名を確認するとき。
- CLI のエントリーポイント、サブコマンド、共有モジュールの責務や配置を決めるとき。
- Python、venv、依存関係、ファイル命名・エンコードなど開発環境のルールを確認するとき。
- realization test の追加・変更・レビュー、実経路統合テストや GPU test の実行条件を確認するとき。

## Do not read this when
- 個別機能や CLI の具体的な挙動・出力仕様を確認するときは、対象機能の oracle doc を直接読む。
- 個別モジュールの実装詳細を確認するときは、その realization code を読む。
- INDEX.md の読み方やルーティング方針自体を確認するときは、対応する routing 文書を読む。
- 一般的な利用方法だけを確認する場合は、README などの利用者向け文書を優先する。

## hash
- 17eeb3926e0e5d1fd2b71d2a19bc50fab24083ae35e7b5612a6c65e333d67346
