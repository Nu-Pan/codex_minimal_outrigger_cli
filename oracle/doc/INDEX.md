# `app_spec`

## Summary
- cmoc アプリケーションの正本仕様をまとめる入口で、利用方法、実行・ログ、session/run lifecycle、feedback、Codex 呼び出し、通知、サブコマンド固有仕様などを扱う。
- 共通契約や横断的な挙動を確認したい場合は app_spec から入り、個別 workload の詳細は配下の sub_command 仕様へ進む。

## Read this when
- cmoc のユーザー向け workflow、共通実行規則、状態管理、ログ・通知、feedback、または複数サブコマンドにまたがる仕様を確認・変更するとき。
- どのサブコマンド仕様や共通契約を参照すべきかを判断するとき。

## Do not read this when
- 特定サブコマンドの実行条件や成果物だけを確認したい場合は、app_spec/sub_command 配下の該当仕様を直接読む。
- 実装上の正確なデータ構造やアルゴリズムが必要な場合は、仕様が委譲している oracle/src の対象を読む。
- 実装・テストの現在の挙動だけを調べる場合は、対応する src または test の対象を直接読む。

## hash
- 4c983fd40b90d76ca5695082fc0a4e3223ac4c0cbc85c1ee2cb2e04d69af641a

# `branch_model.md`

## Summary
- cmoc が session と run を隔離・統合するための branch、commit、worktree の正本モデルを定義する。session/run branch の作成元・命名・対応関係、fork/join commit、run worktree の配置と no-op join の扱いを確認する入口である。

## Read this when
- session fork や run の開始・join・apply における branch、commit、worktree の関係を確認したいとき。
- run の差分検査や report がどの fork commit を基準にすべきか確認したいとき。
- session branch と run branch の命名、分岐元、merge 先を確認したいとき。

## Do not read this when
- 個別サブコマンドの実装手順や CLI 入出力を確認したいとき。
- run state や report の項目定義そのものを確認したいときは、それらを直接定義する仕様へ進むべきである。

## hash
- d043bb04484e4c8b1c47fbaf83d5e776f1c0e1a2d180e01ee2788e2fb23251aa

# `considered_alternative`

## Summary
- 採用しなかった設計案と、その判断理由を記録する正本仕様文書群。実装仕様そのものではなく、現行方式に至った比較検討の経緯を確認するための入口。

## Read this when
- 現行の実装方式が、代替案をなぜ採用しなかった結果なのか確認したいとき。
- 作業計画レビュー、oracle review、差分事後検証、動的 permission profile、AI-generated kaizen、自動並列調査などの採否判断を調べるとき。
- 現行仕様への変更を検討し、過去の不採用理由や想定されたトレードオフを確認するとき。

## Do not read this when
- 現行仕様や実装手順そのものを確認したいときは、各文書が参照する app_spec の正本を直接読む。
- 特定の不採用案だけを調べる場合は、このディレクトリ全体ではなく該当する個別文書を直接読む。
- 採用判断の経緯や代替案との比較が不要な通常の実装・利用では読む必要がない。

## hash
- d5ff4d46d2ecc3fe4a53566128e71edb8d7ef4d72dfd707c9662ac283ca06535

# `dev_rule`

## Summary
- cmoc の開発規則をまとめた正本文書群への入口で、設計・コーディング・テスト実装・テスト実行・開発環境の各規約を扱う。
- CLI の責務分割や共通機能の配置、Python の型・docstring・命名規則など、実装構造とコード品質の判断基準を確認できる。
- pytest によるテスト実装要件、実経路統合テスト、構築済み環境での検査手順、完了判定、Python 環境構築条件を確認できる。

## Read this when
- cmoc の実装構造、CLI とサブコマンドの責務分割、共通機能の配置を決めるとき。
- Python コードの型注釈、docstring、import、コメント、命名、非公開識別子の規約を確認するとき。
- テストの意味上の要件や実経路統合テストの扱いを確認するとき。
- pytest・Ruff・mypy の選択、実行、完了判定、結果報告の手順を確認するとき。
- Python 仮想環境の構築、依存関係追加、pip 操作、開発環境の前提を確認するとき。

## Do not read this when
- 個別の実装やテストの具体的な挙動を確認する場合は、まず対応する src または test の対象へ直接進むとき。
- 既存環境で単にテストを実行するだけで、実行手順がすでに明らかな場合は development_environment.md へ直接進む必要がないとき。
- アプリケーション仕様や Codex CLI 呼び出し規約そのものを確認する場合は、対応する oracle/doc/app_spec の正本へ直接進むとき.

## hash
- 42c32e9799374c2242c1bd735dff6a0ee22e14afe6db2d1c15093788d7a2a557
