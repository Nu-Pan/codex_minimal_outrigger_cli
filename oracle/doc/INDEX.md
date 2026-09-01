# `app_spec`

## Summary
- cmoc のアプリケーション仕様を、CLI 実行、workflow、state、feedback、Codex 呼び出し、通知、文書分類などの個別仕様へ案内する正本仕様群の入口。
- 各仕様書の責務と適用条件を確認し、対象の挙動や実装に対応する下位仕様へ進むために使用する。

## Read this when
- cmoc のアプリケーション挙動に関する正本仕様を探すとき
- CLI、session／run、feedback、Codex CLI、ログ、通知、editor input、INDEX.md などの個別仕様の入口を判断するとき
- 複数の仕様書にまたがる責務の所在や、共通仕様と個別仕様の境界を確認するとき

## Do not read this when
- 特定の仕様書の詳細な挙動、field、prompt、schema、実装規則だけを確認したいときは、該当する個別仕様書または委譲先を直接読む
- アプリケーション仕様に関係しない開発環境、設計、テスト実行などの内部開発規則だけを確認したいとき
- 実装やテストの具体的なコードを調査するときは、routing 後に対象ファイルを直接読む

## hash
- 548fa2350bff66ad10100eefccd206da3a4309e7107e353cb1920e0be05cffdc

# `branch_model.md`

## Summary
- cmoc が session と run を git branch・commit・worktree で隔離するモデルを定義する正本文書。各管理対象の命名、分岐元・統合先、run の差分検査に用いる commit、run 用 worktree の関係を確認する入口。

## Read this when
- session fork や run の branch 分岐・統合、run worktree の作成、または関連する commit 名・役割を実装・変更・調査するとき。
- cmoc 管理 branch と通常の local branch・remote-tracking branch の境界を確認するとき。

## Do not read this when
- branch model の具体的な CLI 入出力契約だけを確認する場合は、該当する CLI 仕様を直接読む。
- git 操作を伴わない workload の実行内容や report の詳細仕様だけを確認する場合は、各機能の仕様・実装文書を直接読む。

## hash
- c40f58b39046604d613c84f9bd18f7a9688be81e5c3b97293298f685511debdd

# `considered_alternative`

## Summary
- cmoc realization refactorで採用しなかった作業方式と、その不採用理由を確認するための検討資料群。現行のファイル単位の調査・反映方針との違いを把握する入口。
- agent call後のfile access policy違反の事後検査と自動リカバリー案を断念した経緯を確認する資料。誤検出や差分帰属の困難性を扱う。
- .gitignoreの除外判定をpermission profileの例外へ変換する案と、その記法非互換性による不採用理由を確認する資料。
- AI-generated kaizenや継続的な暗黙記憶を次回のCodex CLI実行へ注入しない設計理由と、INDEX・oracle・ログ・成果物による明示的な情報到達方針を確認する資料。
- oracle fileの網羅的レビュー機能を採用せず、feedback observation/reportで人間対応が必要な問題を扱う方針を確認する資料。
- AIに作業計画を作成させて人間がレビューする方式を採用せず、人間がoracleを編集しAIが実装可能性を確認する責務分担を採用した背景を確認する資料。

## Read this when
- cmoc realization refactorの作業フロー、調査単位、修正単位の設計理由を確認するとき。
- file access policy違反の事後検査、自動リカバリー、並列agentによる誤検出の検討経緯を調べるとき。
- .gitignoreとpermission profileの連携案や、除外ファイルの例外規則を検討するとき。
- AI-generated kaizen、memory、過去の失敗分析や改善案を後続実行へ自動注入する設計の採否を判断するとき。
- oracle reviewを提供しない理由や、feedback observation/reportによる人間への問題報告の流れを確認するとき。
- AI主導の作業計画レビュー方式と、人間によるoracle編集・AIによる実装追従の責務分担を比較するとき。

## Do not read this when
- 具体的なrealization fileの修正方法、実装責務、現行refactor state、対象ファイルの実装・テスト内容を確認したいとき。
- 現行のfile access policy、アクセス制御・検査処理、または現在採用されている仕様を確認・変更するとき。
- 現行の.gitignoreパターンや実行時アクセス制御を調査・実装するとき。
- 個別のkaizen文面、レビュー観点、INDEX・oracle・ログ・成果物の具体形式、またはCodex CLI本体のmemory機能を調べるとき。
- oracle file自体の正本内容、feedback observation/reportの正本仕様、通常workloadの具体的な実装・運用手順を確認するとき。
- oracleとrealizationの一般定義、個別コマンドの仕様・実装手順・テスト仕様、採用済みworkflowの具体的操作を確認するとき。

## hash
- f547b1f8191281da475eecf2949bb09d20ade64b9fde5b9d5990c97510bc872c

# `dev_rule`

## Summary
- cmoc の開発ルール文書群への入口。Python の書き方、CLI の責務配置、開発環境、テスト要件、テスト実行手順を、それぞれの正本文書へ振り分けて確認できる。
- 実装・環境構築・テストに関する判断で、コーディング規則、CLI 構成、依存関係、テストの意味要件、または検査実行手順のどれを確認すべきかを選ぶための案内を担う。

## Read this when
- Python 実装の命名、型ヒント、import、docstring、コメント、ログなどの記述規則を確認するとき
- CLI のエントリーポイント、サブコマンド、共有処理の配置と責務境界を判断するとき
- Python 仮想環境、依存関係、pip 操作、実行環境の前提を確認するとき
- テストの検証要件、隔離、Fake Codex CLI、実経路統合テストの条件を確認するとき
- 構築済み環境で focused test、品質検査、通常の pytest、実経路統合テストを選択・実行・判定するとき

## Do not read this when
- 特定機能の挙動や出力など、アプリケーション仕様そのものを確認したいとき
- 実装やテストの責務・配置を個別に判断するときは、対応する正本文書を直接確認するとき
- テストの意味上の要件を確認するときは test_rule.md を直接読むとき
- Python 環境の新規構築、依存関係の追加、pip 操作を確認するときは development_environment.md を直接読むとき
- 単に実装上の問題や期待値の意味を調査し、文書の実行手順を必要としないとき

## hash
- a9eb031831fbfcc2aae337585c7e2af5d64d5a4aa2137ecc1f49137f43e2175d
