# `apply_behavior.md`

## Summary
- realization refactorで採用しなかった二つの進め方（事前の作業計画立案、所見の並列リストアップ）と、その不採用理由を説明する文書。現行の永続的な調査要求に従うファイル単位の調査・反映方式との違いを確認するための入口。

## Read this when
- realization refactorの作業フロー設計で、修正点確定後の独立した計画立案を採用しない理由を確認したいとき。
- 所見を先に並列収集してから所見単位で修正する方式と、現行のfile単位の調査・反映方式の違いを確認したいとき。

## Do not read this when
- 現行realization refactorの具体的な実装仕様や状態管理の定義を確認したいとき。
- oracle fileまたはrealization fileの個別の修正内容・所見を直接確認すべきとき。

## hash
- 75826a26abd23751d9e74980ff58a58f419472e9d085b0ef5eca57227f6960c0

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
- .gitignore の除外判定を permission profile に変換して例外的な読み書きを許可する案の検討結果を記録する文書。採用しなかった理由と、記法互換性の具体的な制約を確認するための入口。

## Read this when
- .gitignore を利用して Codex CLI の permission profile を動的生成する案を検討・評価するとき。
- git 追跡対象外ファイルを通常のアクセス制限の例外として扱う設計の背景や不採用理由を確認するとき。

## Do not read this when
- 現行のファイルアクセス制限の正本仕様や実装を確認するときは、permission profile の正本・実装対象を直接読む。
- .gitignore の一般的な構文や git の追跡除外動作だけを調べるとき。

## hash
- 043c7f3a7187986053ccac79f76718ead5448f728287b5bb77dc0e0bceda37f5

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
- AI に作業計画を作成・レビューさせる方式を採用せず、人間が oracle に want を明文化し、AI が実装可能性を確認して実装へ追従させる方針の背景を説明する文書。
- 人間と AI の共同作業における速度差と、人間が実装・設計へ介助的に関与せざるを得ない事情を踏まえ、`cmoc eval-oracle` を中心とした開発スタイルの選択理由を示す。

## Read this when
- `tgbt plan` や `/plan` による作業計画レビューを採用しない理由を確認したいとき。
- oracle を人間が編集し、AI が実装を追従させる開発方針の背景や、`cmoc eval-oracle` の位置づけを理解したいとき。

## Do not read this when
- 具体的な oracle の内容、実装手順、または CLI の操作方法を確認したいとき。
- 作業計画そのものの作成・レビューや、個別の実装判断を行うとき。

## hash
- b77118d588434b7038abe6c86e38acd6fc563eb52ca325508f0422c04e999c5f
