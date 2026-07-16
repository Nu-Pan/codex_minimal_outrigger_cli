# `app_spec`

## Summary
- cmoc のアプリケーション仕様断片を集約するディレクトリ。CLI の補完、ログ、エラー処理、Codex/Ollama 連携、セッション状態、run 隔離、利用手順、サブコマンド仕様など、個別機能の正本仕様を読むための入口。

## Read this when
- cmoc の個別機能やサブコマンドの仕様を調査・実装・レビューするとき。
- CLI 実行、Codex 呼び出し、managed Ollama、ログ、状態管理、run isolation、INDEX 生成などの正本文書を選ぶとき。
- 利用手順や共通のアプリケーション動作を確認するとき。

## Do not read this when
- INDEX.md の生成・更新ルールだけを確認したいときは、indexing の仕様を直接読む。
- Python 開発環境、設計、テスト実行規則を確認したいときは、対応する dev_rule の oracle doc を読む。
- 特定文書の内容が明らかな場合は、このディレクトリ全体ではなく該当する仕様ファイルへ直接進む。

## hash
- d521072671354a78f4a8f082e7ea3b0518341e5fc252def25ce72bdddfb0c320

# `branch_model.md`

## Summary
- cmoc が session と run の境界をどう切るかを定める。どの branch や worktree が誰の作業領域か、session fork/join と各サブコマンドの run fork/join を扱う文脈で読む。

## Read this when
- session の開始・終了で branch の生成や merge の扱いを決めたいとき
- apply や review などの run がどの branch と worktree を使うか確認したいとき
- cmoc 管理対象の branch 名や commit 名の責務境界を確認したいとき

## Do not read this when
- 個別サブコマンドの入出力や実行手順だけを知りたいとき
- branch 名や worktree 名の具体的な生成規則ではなく、内部実装の詳細を詰めたいとき
- cmoc 以外の通常の git 運用やリポジトリ本流の方針だけを確認したいとき

## hash
- e48fc3d9371ee9b4c447d06cdcb12a96f006afa581263ea87bd285118a7a60ed

# `considered_alternative`

## Summary
- `cmoc` の設計で採用しなかった代替案と、その不採用理由を記録した設計判断メモ群。apply の orchestration、事後検査、permission profile 連携、AI-generated memory、作業計画レビューなどの背景を確認するための入口であり、現行仕様や実装そのものを扱う場所ではない。

## Read this when
- `cmoc apply` の不採用 orchestration 案や、所見調査・並列化・作業計画・状態管理を避けた理由を確認するとき。
- file access rule の事後検査案や `.gitignore` と permission profile の連携案の採否を調べるとき。
- AI-generated kaizen や継続的 memory の自動注入を採用しない設計意図を確認するとき。
- AI 作業計画を人間がレビューする workflow ではなく、人間が oracle を編集し AI が実装を追従させる方式を採用した背景を確認するとき。

## Do not read this when
- `cmoc apply` などの現行の実行手順、CLI 入出力、状態ファイル、テスト期待値を確認するとき。
- 現在の file access rule、差分検査、permission profile の仕様や実装を調べるとき。
- oracle file・realization file・INDEX.md の一般的な定義や記述規則を確認するとき。
- 採用済み workflow の操作方法や、個別機能の実装・テスト仕様を直接確認したいとき。

## hash
- 2eaef6ba625b805a5335e7f4ed166148fe03f84fac754f6e59a849b6ed892226

# `dev_rule`

## Summary
- cmoc の開発規約をまとめた oracle doc 群。Python コーディング、CLI の設計・配置、開発環境、pytest による realization test の方針を確認する入口。

## Read this when
- Python 実装の書き方、型ヒント、import、docstring、コメント、命名規則を確認したいとき。
- CLI のエントリーポイント、サブコマンド、共有処理の配置や責務分担を判断したいとき。
- Python・venv・依存関係・ファイル命名などの開発環境ルールを確認したいとき。
- realization test の配置、検証範囲、隔離環境、Codex CLI や ollama の使い分けを確認したいとき。

## Do not read this when
- 個別機能や CLI の挙動・出力仕様を確認したいときは、対象機能の oracle doc を直接読む。
- 既存モジュールの実装詳細を知りたいときは、その realization code を直接読む。
- INDEX.md の読み方やルーティング方針を確認したいときは、別の routing 文書を読む。

## hash
- 3e49c9637bd1f2f7bf758fdd01682f362e3973d6450d144d7d5592277ccb8768
