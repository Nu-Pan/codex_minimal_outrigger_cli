# `app_spec`

## Summary
- cmoc のアプリケーション挙動を定める正本仕様群です。ファイル分類、session/run、agent 呼び出し、入力引き渡し、ログ・エラー・通知、indexing・feedback などの共通契約と、個別コマンド仕様を含みます。

## Read this when
- 複数のコマンドに関わる挙動や共通契約を調査・変更するとき。
- CLI 全体の操作フローや、状態管理・Codex 呼び出し・報告に関する仕様上の責務を確認するとき。

## Do not read this when
- 特定コマンドだけの動作を調べるときは、そのコマンドの仕様へ直接進んでください。
- 正確な prompt 文面、schema、または委譲された構築処理を調べるときは、該当仕様が示す定義元を参照してください。

## hash
- 208343bcdfa39294530b76cb0823dec0d01957b6e813b431105b10e6f6bdf2db

# `branch_model.md`

## Summary
- cmoc が session と run を管理する際の Git branch、commit、worktree の役割と相互関係を定義する。
- session/run の分岐元・merge 先、命名、対象範囲、run worktree の位置づけを確認するための入口。

## Read this when
- session branch と run branch の関係、分岐元や merge 先を確認するとき。
- fork/join に関わる commit の定義や、join が no-op となる条件を確認するとき。
- run worktree の役割や、管理対象 branch 上の変更範囲を判断するとき。

## Do not read this when
- 特定サブコマンドの手順、入出力、失敗時の動作を調べるときは、そのコマンドの仕様を直接読む。
- 実装方法やテストの内容を調べるときは、該当する実装またはテストを直接読む。

## hash
- d043bb04484e4c8b1c47fbaf83d5e776f1c0e1a2d180e01ee2788e2fb23251aa

# `considered_alternative`

## Summary
- 複数の過去の不採用案について、判断理由や当時のトレードオフを記録する資料群。現行仕様ではなく、採否の背景をたどる入口。
- realization refactor、差分の事後検査、permission profile の動的生成、AI の改善案の自動引き継ぎ、oracle や作業計画のレビュー方式などを扱う。

## Read this when
- 機能に関して検討された代替案が採用されなかった理由や、判断時の制約・トレードオフを確認するとき。
- 複数の不採用判断に共通する背景をたどるとき。

## Do not read this when
- 現行仕様や現行挙動の確認・変更・実装をするときは、該当する正本仕様を直接読む。
- 特定の不採用案の理由だけを調べる場合は、該当する資料を直接読む。
- 過去の代替案の採否理由が関係しない作業では参照不要。

## hash
- 8f1609bbacffd65e7eedc6cffe9ac52710be176773c393d128c0f025f82ba759

# `dev_rule`

## Summary
- cmoc の開発環境構築、コード設計・コーディング規則、テストの要件と実行手順を扱う。開発作業の進め方や実装品質を確認するときの入口であり、製品の機能仕様を定める文書群ではない。

## Read this when
- Python 環境の構築、依存関係の追加、pip 操作の条件を確認するとき。
- CLI の構成や共通機能の置き場所、型・import・docstring・コメントなどの実装規則を確認するとき。
- テストの対象や実経路統合テストの要件を定めるとき、またはテスト・品質検査の選択、実行、完了判定、結果報告を行うとき。

## Do not read this when
- cmoc の利用者向け機能が満たすべき振る舞いを判断するときは、開発規約ではなく該当する機能仕様を参照する。
- 構築済み環境でテストや品質検査を実行・報告するだけなら、環境構築や一般的な実装規則まで読む必要はなく、その実行手順を直接確認する。

## hash
- cd7d23c93d085767e759f358baa2c54a3fe075d0b4d1f0a1418d18cc3074c443
