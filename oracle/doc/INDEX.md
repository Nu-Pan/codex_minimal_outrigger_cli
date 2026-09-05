# `app_spec`

## Summary
- cmoc の CLI・セッション・feedback・oracle／realization・ログ・通知など、アプリケーション全体の正本仕様を分野別に参照する入口。個別仕様の責務境界と、関連する下位文書へ進むためのルーティング情報を提供する。

## Read this when
- cmoc のアプリケーション仕様を調査し、対象分野に対応する正本仕様を選ぶとき
- CLI 実行、session／run lifecycle、feedback、ログ、通知、oracle／realization、INDEX.md 運用などの共通仕様の入口を探すとき
- 個別仕様間の参照関係や、共通契約と下位仕様の責務分担を確認するとき

## Do not read this when
- 特定の仕様本文、実装、テスト、設定スキーマの詳細が既に特定できているときは、対応する個別対象を直接読む
- INDEX.md の生成規則そのものだけを確認するときは indexing の仕様を直接読む
- 特定サブコマンドや個別機能の挙動だけを確認するときは、該当する下位仕様を直接読む

## hash
- 7d13b700c48e1556bb3c6964e41f06b70364be965971ac085dcc554ae119e254

# `branch_model.md`

## Summary
- cmoc の session・run が利用する branch、commit、linked worktree の役割と関係を定義するモデル。通常の git branch との区別、分岐元・統合先、run の隔離方法を確認するための入口。

## Read this when
- session fork や run の branch 構成、分岐元・統合先 commit、run worktree の位置づけを確認するとき
- cmoc 管理 branch と通常の local・remote-tracking branch の違い、または session と run の隔離関係を扱うとき
- run の差分検査、apply の追従対象、join の no-op 条件を含む commit の意味を確認するとき

## Do not read this when
- 個別の CLI サブコマンドの実行手順や state・report の詳細を確認したいとき
- oracle の変更内容や realization の実装責務を確認したいとき
- branch、commit、worktree の関係ではなく、git 一般の操作方法だけを調べるとき

## hash
- 2acd7424aee437c67f38a81333bef36915ec27f659402c48fa745ab596010e7b

# `considered_alternative`

## Summary
- cmoc の設計・運用で検討したが採用しなかった代替案を記録する資料群への入口。現行方針との違いや不採用理由を確認するための上位ルーティング対象。

## Read this when
- 現行仕様ではなく、作業フロー、アクセス制御、記憶、oracle review などに関する過去の代替案と、その採否理由を調べるとき。
- 複数の不採用案を比較し、cmoc が採用した設計判断の背景を確認するとき。

## Do not read this when
- 現行の実装方法、アクセス制御、refactor state、feedback 処理などの正本仕様を確認したいとき。
- 特定の代替案の詳細ではなく、採用済みの CLI 挙動やテスト内容を調べたいとき。

## hash
- f488f904c483ea51c8b0dae8971eeb56b2299b80f6aa29129650dec08027d65f

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
