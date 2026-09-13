# `apply_behavior.md`

## Summary
- cmoc realization refactor で採用しなかった事前計画・並列所見調査の理由を記録する補足資料。現行の file 単位の調査・反映方式を理解するための背景情報への入口。

## Read this when
- realization refactor の処理単位やループ設計について、事前計画や所見単位の並列処理を採用しなかった判断理由を確認したいとき。
- 現行方式が、実装中の状態変化・依存関係・重複所見・文脈分断などをどう考慮した結果かを調べるとき。

## Do not read this when
- realization refactor の現行仕様、refactor state、refactor loop の具体的な動作を確認したいときは、正本仕様を直接読む。
- 実際の実装箇所を修正・調査するときに、採用済みの処理手順だけが必要な場合。

## hash
- f4ca37fd0290a0c54ec62aa1a9a83f23dd83e7ef0562faa4ff58afc8864cd9fd

# `file_access_policy_violation_post_validation.md`

## Summary
- agent call 後の差分を検査して file access policy 違反を検出し、違反時に別の agent call でリカバリーする案を、false-positive などの理由で断念した経緯を記録する検討資料。

## Read this when
- file access policy 違反の事後検査や、違反検出後の自動リカバリー案を調査するとき。
- 並列 agent による差分の誤検出、`.gitignore` 系の扱い、agent call 起因の差分判定の難しさを確認するとき。

## Do not read this when
- 現行の file access policy や実装仕様を確認・変更するとき。
- 過去の断念理由ではなく、現在の検査処理やリカバリー処理の詳細を直接調べるとき。

## hash
- 6ca39e6855f9add5db8cb57a495360d319e2e83f99e9bb194b51126cb4138d59

# `gitignore_to_permission_profile.md`

## Summary
- .gitignore の除外判定を permission profile の読み書き例外へ変換する案について、採用しなかった理由と実行時利用を禁じる判断を記録する。

## Read this when
- .gitignore 対象を permission profile の例外として扱う設計や、両者の記法互換性を検討するとき。
- 現行のファイルアクセス制限を正本仕様に従わせ、この変換案を fallback や実行時分岐に使わない理由を確認するとき。

## Do not read this when
- 現行の permission profile やファイルアクセス制限の具体的な仕様を確認したいとき。
- .gitignore の一般的な記法や git 追跡対象外ファイルの扱いを直接調べるとき。

## hash
- b25695a7bfeafd936275ec65ae35b32df87b0cb6a195e9b22003c08302edd9e2

# `memory_alternative.md`

## Summary
- AI-generated kaizen を後続の Codex CLI 実行へ自動注入しない理由を整理した検討資料。暗黙の準仕様化、誤診断の永続化、oracle との仕様単一性の損失、古い情報の混入を避け、仕様・入力・ログ・成果物・INDEX・oracle による明示的な情報到達を重視する。

## Read this when
- AI-generated kaizen や AI の振り返り結果を次回以降の実行コンテキストへ自動反映する仕組みの採否を検討するとき
- cmoc に暗黙記憶や memory 系の仕組みを導入することの問題点を確認するとき
- oracle を正本仕様断片として維持し、実行の根拠を明示情報に限定する方針を確認するとき

## Do not read this when
- 実際の kaizen、oracle、ログ、実行成果物の内容や更新手順を確認したいとき
- Codex CLI 本体の memory 機能の具体的な仕様や利用方法を調べたいとき
- AI-generated kaizen の自動注入以外の実装方式や個別の実行障害を直接調査するとき

## hash
- bdf5f8772491fd718cde867cc852b43c14722dbb097400a776dd3396450a65eb

# `oracle_review.md`

## Summary
- `cmoc oracle review` を採用しない判断の理由と、その代替として通常 workload の範囲外の問題を feedback observation として報告する方針を示す文書。

## Read this when
- `cmoc oracle review` の不採用理由や、oracle file の網羅検査を提供しない設計判断を確認するとき。
- 通常の workload における oracle file 調査と、解消できない問題の feedback report への引き継ぎ方針を確認するとき。

## Do not read this when
- `cmoc feedback report` の具体的な処理仕様や自動修正条件を確認したいときは、feedback_report の正本を直接読む。
- agent による feedback observation の報告基準を確認したいときは、feedback_observation の正本を直接読む。
- 通常の workload に必要な個別の oracle file の内容や実装責務を調べるとき。

## hash
- 85eff2dc068f2ad2f8e8b693036af18e0c41551c0ec0754ce18e8311739b946e

# `working_plan_review.md`

## Summary
- 作業計画レビューを採用しなかった理由と、その代替として人間が oracle を編集し AI が実装を追従する方式を採用した判断を記録する文書。

## Read this when
- `tgbt plan` や `/plan` のような計画レビューの導入理由・不採用理由を確認したいとき。
- 人間と AI の役割分担、および oracle 中心の開発方針に至った評価を確認したいとき。

## Do not read this when
- 現在の oracle review の具体的な扱いや判断を確認したいときは、案内されている oracle review の文書を直接読むべき場合。
- 作業計画の作成・実施手順そのものを確認したいとき。

## hash
- 86f703748490a2b583c7663810655d2414fc22290edf44a7cad32981be3dbcf0
