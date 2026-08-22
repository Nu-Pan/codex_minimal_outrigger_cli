# `app_spec`

## Summary
- cmoc のアプリケーション正本仕様を収録するディレクトリ。共通契約、Codex 呼び出し、ログ・エラー、feedback、session/run、prompt、通知、補完、indexing などの横断仕様を扱う。
- サブコマンド固有の引数、前提条件、処理手順、状態遷移、report、終了契約は `sub_command` 配下の各仕様へ進むための入口を提供する。
- 実装・変更・レビューで正本仕様の責務境界や共通規則を確認する場合は本ディレクトリから該当する共通仕様またはサブコマンド仕様を選ぶ。

## Read this when
- cmoc の共通アプリケーション仕様、正本文書間の責務分担、または複数サブコマンドにまたがる契約を確認するとき
- Codex CLI 呼び出し、prompt 構築、console・ログ・report、エラー処理、feedback、session/run、通知、自動補完、indexing の仕様を実装・変更・レビューするとき
- 特定の cmoc サブコマンドの引数、前提条件、処理手順、状態遷移、report、終了結果を確認するとき

## Do not read this when
- 個別サブコマンドの仕様が特定できている場合は、`sub_command` 配下の対応する仕様を直接読む
- 実装コード、realization file、テスト規約、開発環境、テスト実行手順だけを確認する場合は、それぞれの専用文書や実装・テスト対象を直接読む
- INDEX.md の生成・更新処理そのものだけを確認する場合は、indexing の正本仕様を直接読む

## hash
- eac50434d393eb175a358588faa8546cd8f3a677354102007a36b6a735f1ed82

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
- cmoc の設計・リファクタで採用しなかった作業方式や仕様案を記録する検討資料群。事前計画、並列所見管理、事後アクセス違反検査、`.gitignore` 連携、AI-generated memory などの不採用理由を確認するための入口であり、採用済みの現行仕様や具体的な実装手順の正本ではない。

## Read this when
- cmoc realization の作業フローや調査単位について、採用しなかった代替案とその理由を比較するとき
- AI による作業計画・memory の自動継承や、アクセス制御の事後検査、`.gitignore` 連携案の採否背景を調査するとき
- 現行設計が特定の代替方式を採用しなかった根拠を確認したいとき

## Do not read this when
- 現行のアクセス制御、refactor state、oracle、realization の仕様を確認・変更するとき
- 具体的な realization file の実装方法、CLI の挙動、テスト手順を調べるとき
- 採用済み workflow の操作方法や現在の実行結果だけを確認したいとき

## hash
- 2306639b6cb9d46169d1e0614cafd6a1ff50856b67ccfe5f40849ae09d0cd405

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
