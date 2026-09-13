# `app_spec`

## Summary
- cmoc のアプリケーション仕様を収録する oracle doc 群。CLI の共通実行規約、サブコマンド、session・run lifecycle、feedback、ログ、通知、エディタ入力など、アプリケーション全体の責務と境界を確認するための入口。

## Read this when
- cmoc のアプリケーションレベルの正本仕様を探しており、複数の機能にまたがる責務分担や参照先を確認したいとき
- CLI 実行、workflow、session／editing run、feedback、出力・ログ、通知、自動補完、prompt editor などの仕様を確認・変更するとき
- 対象機能の詳細仕様へ進む前に、共通契約や機能間の境界を把握したいとき

## Do not read this when
- 個別の実装 module、テスト、実行結果、診断ログそのものを調査・変更したいとき
- 特定の schema、prompt literal、設定 field、内部 API など、本文が委譲する詳細の正本を直接確認すべきとき
- 一般的な開発手順だけを確認したいときや、アプリケーション仕様に関係しない資料を探しているとき

## hash
- 832156c4e4eedb60f50b77630fa7622a95c82f15437c9e75a6d8309b31967729

# `branch_model.md`

## Summary
- cmoc における session・run の branch、commit、worktree の役割と関係を定義する正本文書。
- branch の作成元・命名・統合先、commit の fork/join、run worktree の分離条件を確認する入口。

## Read this when
- session fork、run の開始・分離・join、apply の追従対象、run report の commit 基準を扱うとき。
- cmoc 管理 branch と通常の git branch、session home branch の意味を区別する必要があるとき。
- branch・commit・linked worktree の用語や対応関係を確認するとき。

## Do not read this when
- run state や report の状態遷移そのものを確認したいとき。
- oracle の変更手順や設計責務、test の実行規則を直接確認したいとき。
- 個別の git 操作手順だけを知りたいときで、branch model の用語上の判断を必要としない場合。

## hash
- 955dd077586a6c946e3573d1b1bbde073736e4f7325fbd93ed6c09a3862fc858

# `considered_alternative`

## Summary
- cmoc の設計検討で不採用となった代替案と、その判断理由を記録する補足資料群への入口。現行の仕様や実装ではなく、現在の方式を選んだ背景を扱う。

## Read this when
- 事前計画、所見単位の並列処理、事後検査、自動リカバリー、.gitignore 連携、AI-generated kaizen の自動注入、oracle review、作業計画レビューなどの不採用理由を確認したいとき。
- 現行方式が、状態変化・依存関係・誤検出・暗黙の準仕様化・情報の鮮度・人間と AI の役割分担をどう評価して選ばれたかを調べるとき。

## Do not read this when
- 現行の仕様、実装済みの処理手順、permission profile、feedback report、feedback observation、oracle、ログ、成果物の具体的な扱いを確認したいときは、それぞれの正本仕様や実装箇所を直接読む。
- 不採用案の背景ではなく、現在採用されている機能の利用方法や個別の障害対応だけを調べるとき。

## hash
- 5afa9314ec4f58e1359ac273ff335f483f6e9d9bbc9c2b7022a4cf4c001ac19c

# `dev_rule`

## Summary
- cmoc の開発規約群への入口。Python 実装のコーディング、CLI の責務分担と共通機能の配置、開発環境の構築、テストの意味要件・実行手順を扱う。

## Read this when
- cmoc の Python 実装や CLI 構成を新規作成・変更・レビューし、命名・型注釈・責務分担・共通機能の配置を判断するとき。
- 開発環境や依存関係を構築・変更するとき。
- pytest・Ruff・mypy・実経路統合テストの対象、実行条件、完了判定、または realization test の検証要件を確認するとき。

## Do not read this when
- cmoc の機能仕様や利用手順そのものを確認したいとき。
- 構築済み環境での通常の検査手順だけを確認したい場合は、テスト実行手順の対象を直接読むとき。
- 実装規則ではなくテスト固有の意味要件だけを確認したい場合は、テスト規約の対象を直接読むとき。
- Python 環境の構築や依存関係の変更を伴わない通常の開発作業では、開発環境の対象を読む必要がないとき。

## hash
- a075a93a49793f0fcae674074efb36753c7eb1dba5fbc16071c8061f18435a8e
