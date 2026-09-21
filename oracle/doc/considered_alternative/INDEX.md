# `apply_behavior.md`

## Summary
- `cmoc realization refactor` で採用しなかった作業計画立案と並列所見リストアップ方式、その不採用理由を記録する設計判断メモ。
- 現行の調査要求と処理単位を定義する正本仕様へ進む前に、代替案の比較や判断背景を確認するための入口。

## Read this when
- realization refactor の作業計画を独立させなかった理由を確認したいとき。
- 所見調査・修正をファイル単位で進める方式を採用した背景や、並列リストアップ方式の問題点を確認したいとき。
- 現行の refactor state や refactor loop を読む前に、採用判断の背景を把握したいとき。

## Do not read this when
- realization refactor の現行の調査要求・状態遷移・処理ループを確認したいときは、本文が参照する正本仕様を直接読むべきです。
- apply 操作の一般的な利用方法や実装の詳細を確認したいとき。
- 代替案の不採用理由や設計判断の経緯を必要としないとき。

## hash
- 4ca1f0d162961d203941966401a55acccf672c043dd5dc0f51e24487e8cd8322

# `file_access_policy_violation_post_validation.md`

## Summary
- ファイルアクセス方針違反の事後検査と自動リカバリーを検討したが、並列編集による誤検知などの理由で断念した経緯を記録する文書。
- 現行の差分検証仕様ではなく、過去の代替案の問題点や採用されなかった理由を確認するための記録。

## Read this when
- ファイルアクセス方針違反の事後検査や自動リカバリー案を再評価するとき。
- 並列 agent による差分の帰属判定や、gitignore 系ファイルを含む検証範囲の課題を調べるとき。

## Do not read this when
- 現行の agent call 差分検証の仕様を確認するときは、正本である codex_exec_rule.md を直接読む。
- 現在発生している違反の具体的な調査・修正方法を確認するとき。

## hash
- aa4e46f7fa5ff8935ccf8bccc7747ee27928538a2c397ad21e9cf05288f20c03

# `gitignore_to_permission_profile.md`

## Summary
- .gitignore の無視対象を permission profile の例外的な読み書き許可へ動的変換する案について、採用しなかった結果と具体的な検討内容を記録する文書。
- permission profile と .gitignore の記法に互換性がなく、ディレクトリ限定指定や一部のパターンを正確に表現できないため、変換案を断念した理由を確認できる。

## Read this when
- .gitignore の判定結果を permission profile の読み書き規則へ反映する設計や、その採否理由を確認するとき。
- git ignore 対象の削除・編集許可を permission profile の例外として扱う案を検討するとき。

## Do not read this when
- 現行の permission profile の仕様や禁止事項を確認したいときは、正本である codex_exec_rule.md を直接読む。
- .gitignore の現在のパターンや実際の ignore 判定を調べるときは、リポジトリの .gitignore と git check-ignore の結果を直接確認する。
- permission profile の具体的な設定方法や実装を知りたいとき。

## hash
- 3c40d786231e0fbca364c00b33e64be3dc52eb5513092ced7eb7f87915ade183

# `memory_alternative.md`

## Summary
- AI-generated kaizenを次回のCodex CLI実行へ自動注入しない方針と、その理由を説明する代替案文書。仕様・ログ・成果物を明示的に参照可能に保つ考え方、誤診断の永続化や古い知見の混入などの懸念を扱う。

## Read this when
- AI生成の改善案やmemory機構を後続実行へ自動反映する設計を検討・評価するとき
- kaizenの自動注入を採用しない理由や、oracleを正本として明示的な情報到達を重視する方針を確認するとき

## Do not read this when
- 実際のkaizen生成・保存・注入処理の実装を確認したいときは、対応する実装や正本仕様を直接読む
- INDEX、oracle、ログ、実行成果物の一般的な運用方法だけを確認したいとき
- memory機構以外の代替案や、具体的なCodex CLI本体の仕様を調べるとき

## hash
- 9fd9192b4cfdeb2473e0118c22cc359ab7946d7612dd311c94ba04ef7bc6285b

# `oracle_review.md`

## Summary
- `cmoc oracle review` を提供しない判断と、その理由を記録する文書。oracle file の網羅検査が未定義部分と問題の境界を曖昧にし、過剰な詳細化を招く点を説明する。
- 通常の workload で解消できない問題は feedback observation として報告し、実装側で安全に解決できる問題を先に自動修正する代替方針と、その正本への入口を示す。

## Read this when
- oracle file の独立した網羅レビュー機能を採用しない理由を確認するとき
- oracle の問題を通常の workload や feedback observation で扱う境界を判断するとき
- `cmoc oracle review` と `cmoc feedback report` の役割の違いを確認するとき

## Do not read this when
- 通常の workload で必要な oracle file の内容や調査手順を確認したいとき
- feedback observation の報告基準や `cmoc feedback report` の詳細な正本仕様を直接確認したいとき
- 実装可能な機能やコマンドの具体的な仕様を確認したいとき

## hash
- 7587831208609b406e33647005fd1d5f34560e7c301828947c12adc83bd1b3a9

# `working_plan_review.md`

## Summary
- 作業計画レビュー方式を採用しなかった理由と、成果物を oracle に記述して AI が実装を追従する方式を採用した当時の判断を記録する文書。AI に任せられる範囲や、人間と AI の共同作業に対する評価も扱う。

## Read this when
- 作業計画を AI に作成させて人間がレビューする方式の不採用理由を確認したいとき。
- oracle を成果物要求の起点とする役割分担や、当時の AI 活用方針の判断根拠を確認したいとき。

## Do not read this when
- 現在の oracle review の扱いを確認したいときは、本文が案内する oracle_review.md を直接読む。
- 具体的な作業計画や実装手順を確認したいとき。

## hash
- 772ace41faee7031fefb2aa3d1734311f9cf9e0254b832b7522ce2808b1e78ac
