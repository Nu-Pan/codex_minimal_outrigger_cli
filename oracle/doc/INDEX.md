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
- cmoc が採用しなかった設計案や作業方式を記録し、現行方針との違いと不採用理由を確認するための検討資料群。
- refactor の作業フロー、file access policy、.gitignore 連携、AI-generated memory、oracle review、working plan review などの設計判断を扱う。

## Read this when
- cmoc の設計案や作業方式が不採用となった理由を確認するとき
- refactor の調査・修正単位、アクセス制御、永続的な AI 記憶、oracle 検査、作業計画レビューの採否を調べるとき
- 採用済み方針と過去の代替案の境界や設計意図を確認するとき

## Do not read this when
- 現行のアクセス制御、refactor state、feedback 報告、oracle や realization の仕様を確認したいとき
- 具体的な realization file の実装方法、CLI の入出力、テスト内容を調べたいとき
- 採用済み workflow の操作方法や実装責務を直接確認したいとき

## hash
- 9b342c36d29ca53f24b8fc2150e30340840913bf1d2deec724c22a615f5332bb

# `dev_rule`

## Summary
- Python 実装規約、CLI の配置・責務分担、開発環境、テスト規則・実行手順を扱う開発ルール文書群への入口。実装方針から環境操作、テスト検証まで、開発時の判断基準を確認できる。

## Read this when
- Python 実装の命名、型ヒント、import、docstring、コメント、公開範囲、変更規模を確認するとき。
- CLI のエントリーポイント、サブコマンド、共有処理の配置や責務分担を判断するとき。
- Python 環境の構築、依存関係追加、pip 操作、実行環境の前提を確認するとき。
- テストの意味上の要件、実経路統合テスト、Fake Codex CLI、または品質検査の実行・完了判定・報告手順を確認するとき。

## Do not read this when
- 個別の realization 実装やテストの具体的な内容を理解したいときは、対応する本文を直接読む。
- CLI の具体的な挙動や出力内容の正本仕様を確認したいときは、app_spec 配下を読む。
- Codex の model provider の責務境界や quota 待機・再開規則を確認したいときは、指定された codex_model_provider.md または codex_exec_rule.md を直接読む。

## hash
- debf67359ab8bb2979d8fb2c946f26531b153aa8b7d8dd7bbbfc32fc4f4105b2
