# `apply_behavior.md`

## Summary
- cmoc realization refactor で、修正点リスト後の独立した作業計画立案や、所見の並列列挙・所見単位の修正を採用しなかった理由を説明する代替案検討記録。
- 実装状態との乖離、所見の重複や False-Positive、ファイル間依存、文脈分断を避けるため、永続的な調査要求に従って file 単位で調査と反映を進める現行方式に至った判断の根拠を確認できる。

## Read this when
- realization refactor の調査・修正フローを設計または変更する際に、計画立案の独立化や所見調査の並列化を採用しない判断理由を確認したいとき。
- 所見単位の修正、ファイル単位の処理、調査と反映の順序に関する設計上のトレードオフを検討するとき。
- realization refactor の前身となった orchestration との違いや、現行方式へ移行した理由を調べるとき。

## Do not read this when
- realization refactor の現行仕様や処理手順そのものを確認したいときは、正本である realization_refactor の仕様を直接読む。
- 特定の実装ファイルの具体的な不具合、修正内容、所見の詳細を調査するときは、この判断記録ではなく対象ファイルや対応する調査記録を読む。
- 一般的な作業計画の立案方法や並列処理の設計を検討しているだけで、cmoc realization refactor の採用判断を確認する必要がないとき。

## hash
- feb3514ab820c4b2b2323737a480acb41f0bd6aaecb280583faedf0233cc7a5f

# `file_access_policy_violation_post_validation.md`

## Summary
- file access policy 違反の事後検査と自動リカバリーを断念した経緯を記録し、並列編集による false-positive などの問題と関連仕様を削除した判断を確認するための資料。

## Read this when
- file access policy 違反の事後検査・自動リカバリー案がなぜ断念されたかを調査するとき
- agent call の差分を正確に判定できなかった事例や、関連仕様を削除した経緯を確認するとき

## Do not read this when
- 現行の agent call 差分検証の仕様や実装を確認・変更するとき
- file access policy 自体の現行定義を確認するとき

## hash
- 385aa0a3b0190a2f4460e451a34e37e7b95178eb8e07614ca2146fc82ffa52bd

# `gitignore_to_permission_profile.md`

## Summary
- `.gitignore` 対象を permission profile の例外として動的に扱う案の採否、想定していた用途、断念理由を確認するための記録。
- `.gitignore` と permission profile の記法上の非互換性や、動的生成禁止という正本方針の経緯を調べる際の入口。

## Read this when
- `.gitignore` の除外対象を agent の読み書き権限へ反映する設計や、permission profile の動的生成案を検討・再評価するとき。
- この代替案が採用されなかった理由や、ディレクトリ限定指定・柔軟なパターン指定の非互換性を確認するとき。

## Do not read this when
- 現行の permission profile の仕様や動的生成禁止の正式な判断を確認することが目的で、正本仕様を直接参照できるとき。
- `.gitignore` や permission profile と無関係な読み書き制限、または個別の `__pycache__` の扱いだけを調べるとき。

## hash
- fd7e8ab368bd5a1429571454da71973f34c65523a3480778ccc37fa5245b7def

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
- 作業計画レビュー方式を採用しなかった当時の評価と判断を記録する文書。人間が望む成果物を oracle に定義し、AI がレビューと実装を担う役割分担の考え方、および人間と AI の共同作業に関する制約を確認するための入口。

## Read this when
- tgbt plan や /plan のような作業計画レビューを導入・評価する理由を確認したいとき
- 成果物起点の oracle review 方式を採用した背景や、当時の AI への委任範囲の評価を調べるとき
- 人間と AI の役割分担や、AI の生産速度が共同作業に与える問題意識を確認したいとき

## Do not read this when
- 現在の oracle review の仕様・判断・代替案を確認したいとき
- 具体的な作業計画の作成方法や、計画レビューの実行手順を知りたいとき
- 当時の採用理由ではなく、実装や運用の具体的な手順を確認したいとき

## hash
- 091551bc712f8f2521559295791c6e3328bd4127c772a2f489c6349d7a4c9a18
