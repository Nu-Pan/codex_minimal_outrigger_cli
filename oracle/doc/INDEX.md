# `app_spec`

## Summary
- cmoc の利用方法と、コマンドをまたぐ共通動作を定めるアプリケーション仕様群です。Codex 呼び出し、session と編集 run、入出力、障害処理、feedback、indexing、oracle と realization の責務などを扱います。
- コマンド固有の契約は専用の仕様群に分かれており、共通規則とコマンド固有規則が交わる箇所を調べる入口です。

## Read this when
- 複数のコマンドに関わる挙動や共通機構を変更・調査するとき。Codex CLI の実行、session と run の lifecycle、ログ、中断、障害回復などの共通契約を確認します。
- 共通規則と特定コマンドの規則のどちらが対象かを判断するとき、またはコマンド固有仕様から参照される共通契約を追うとき。
- oracle doc、oracle src、realization の責務や、対象ファイルの分類・列挙の意味を確認するとき。

## Do not read this when
- 一つのコマンドの引数、事前条件、固有の処理順、report、結果だけを確認する場合は、そのコマンドの仕様へ直接進みます。
- 定義済みの要求に対する実装の具体的な状態やテスト結果だけを調べる場合は、該当する実装またはテストを直接確認します。
- 正確な構造、値、生成文面が別の正本へ委譲されている場合は、その定義元を直接読みます。

## hash
- 8c49c2b255b9af722cfc07f6083e1214dd7bd9ebb54dfdae0064e526169e845d

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
