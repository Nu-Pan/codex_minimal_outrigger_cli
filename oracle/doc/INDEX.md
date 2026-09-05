# `app_spec`

## Summary
- cmoc のアプリケーション挙動に関する正本仕様を集約し、共通 lifecycle・実行境界・ログ・状態管理・feedback と、各サブコマンド固有の契約への入口を提供する。
- 共通仕様は、Codex CLI 呼び出し、自動補完、doctor 前処理、editor input、run/session 隔離、エラー・中断・通知、oracle／realization 分類などの横断的な責務を扱う。
- サブコマンド仕様は、doctor、editing run、feedback report、indexing、oracle edit／investigation、realization apply／refactor、session 操作、TUI の個別挙動を定義する。

## Read this when
- cmoc のアプリケーション仕様を実装・変更・レビューし、共通仕様と個別サブコマンド仕様のどこから確認を始めるか判断するとき。
- 複数の実行経路にまたがる状態遷移、出力・ログ、Codex CLI 呼び出し、feedback、run/session lifecycle の契約を確認するとき。
- 特定サブコマンドの目的、事前条件、処理手順、結果、状態更新、report または終了条件を正本仕様で確認するとき。

## Do not read this when
- 単一の実装ファイル、test、schema、または既存状態データの具体的内容だけを調べるときは、その対象を直接読むとき。
- 個別仕様の詳細を確認する目的で、共通仕様群全体や対象外のサブコマンド仕様を読む必要がないとき。
- INDEX.md の生成・更新規則そのものを確認するときは、インデクシング運用の正本仕様を直接読むとき。

## hash
- d58e508e4055a557ae8341c6ab968715f25575495a37793328400cd3d97153c0

# `branch_model.md`

## Summary
- cmoc の session・run を隔離して管理する branch、commit、linked worktree のモデルを定義する。
- session と run の分岐元・統合先、各 branch の用途、run 差分を識別する commit、および run worktree の関係を確認するための入口。

## Read this when
- session fork、run の隔離、run join、差分検査、report の commit 基準を扱うとき。
- cmoc 管理 branch と通常の local branch・remote-tracking branch の区別を確認するとき。
- run の linked worktree の配置や、session home branch への統合関係を確認するとき。

## Do not read this when
- branch・commit・worktree の運用モデルを扱わず、個別サブコマンドの実装手順や CLI 入出力だけを確認したいとき。
- run state や report の具体的な形式だけを確認する場合。

## hash
- 0ded198aa853368ff378bf1184aaeaa04caad22fa5ef2c6e74a38c6ff413f291

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
