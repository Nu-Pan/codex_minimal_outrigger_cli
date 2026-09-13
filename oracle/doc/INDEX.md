# `app_spec`

## Summary
- cmoc のアプリケーション仕様群を横断する目次。自動補完、Codex CLI 実行、ログ・エラー処理、feedback、session/run lifecycle、サブコマンド、通知などの正本仕様への入口を提供する。
- 個別仕様の責務や参照境界を把握し、実装・変更・レビュー時に適切な下位仕様へ進むための階層入口。

## Read this when
- cmoc のアプリケーション仕様全体から、確認すべき正本仕様や関連する仕様領域を判断したいとき
- CLI 実行、サブコマンド、session/run、feedback、ログ、通知、自動補完などの共通契約を調査・変更するとき
- 複数の仕様領域にまたがる処理の責務分担や参照先を確認するとき

## Do not read this when
- 特定の機能の詳細な要求、正確な field・型・prompt・schema、または実装 API だけを確認したいときは、該当する下位仕様や正本実装を直接読む
- INDEX.md の生成手順、一般的な開発環境、または対象仕様と無関係な実装詳細だけを確認したいとき

## hash
- 6afabbfd1c5abf76051c988ee8e8676137f32357712dfd6c8d3b4e14e4469941

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
- cmoc の設計・運用上の代替案を比較検討した記録群。realization refactor の調査・修正単位、file access policy 違反対応、permission profile の動的生成、AI-generated kaizen の自動注入、oracle review、作業計画レビューを採用しなかった理由と、現在の方針へ至った判断材料への入口を提供する。

## Read this when
- cmoc の調査・修正フローや権限管理、明示的な情報伝達、oracle と feedback observation の役割分担について、過去の代替案と採否理由を確認したいとき。
- realization refactor における file 単位の処理、並列編集・事後検査の扱い、作業計画レビューの導入可否など、設計上のトレードオフを再評価するとき。
- 現行仕様を読む前に、関連する設計判断の背景や不採用となった方式の問題点を把握したいとき。

## Do not read this when
- 現行仕様、処理手順、差分検証、permission profile、feedback report、feedback observation の正式な定義を確認・変更するときは、それぞれの正本仕様を直接読む。
- 特定の実装不具合、個別の所見、実際の kaizen・oracle・ログ・成果物の内容を調査するときは、該当する実装や記録を直接読む。
- cmoc と無関係な一般的な計画立案、並列処理、記憶機構、ファイル権限の設計だけを検討しているとき。

## hash
- 6d984c323206ea2495118aec7539f6628376a35f314ba33ac406919e9e5fd9db

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
