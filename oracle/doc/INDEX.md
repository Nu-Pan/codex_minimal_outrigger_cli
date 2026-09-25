# `app_spec`

## Summary
- cmoc の利用方法とアプリケーション動作を定める oracle 仕様群。実行、状態、エラー、報告などの共通契約と、機能別仕様への入口を示す。
- oracle と realization の責務や列挙、インデクシング、session と run、feedback、エディタ連携、通知などを扱う。個別コマンド固有の詳細は、そのコマンドの仕様に委ねる。

## Read this when
- 複数の機能に関わる cmoc の動作や、Codex 呼び出し、ファイルアクセス、エラー処理、報告、中断などの共通規則を確認・変更するとき。
- oracle と realization の扱い、session と run の状態、feedback、インデクシングなど、機能をまたぐ契約を調べるとき。
- cmoc の利用方法や workload の選び方を確認し、関連する機能別仕様への入口を探すとき。

## Do not read this when
- 質問が単一コマンド固有の引数、手順、処理、報告に限られるときは、そのコマンドの仕様から確認する。共通契約が関係する場合に限り、こちらも参照する。
- 関心が仕様の解釈ではなく、特定の実装箇所やテストの構成だけにあるときは、対応する実装またはテストの本文を確認する。

## hash
- d3cc7c10d272f95a4e35d30cfdfba7212372d8a5661ea9e9ae0d2c4572048189

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
