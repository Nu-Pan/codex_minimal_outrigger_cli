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
- .gitignore の ignore 判定結果を permission profile の例外的な読み書き許可へ動的変換する案について、採用しなかった判断と検討理由を記録する oracle 文書。
- gitignore と permission profile の記法差により、ディレクトリ限定指定や `?`・文字クラスなどを正確に変換できないことを根拠に、案を断念した経緯を扱う。

## Read this when
- .gitignore の無視対象を permission profile の読み書き例外として扱う設計案の採否を確認するとき。
- git check-ignore の結果を Codex CLI の permission profile に反映する案の問題点を調べるとき。
- ignore 対象の削除・編集許可を権限規則へ変換する代替設計を検討するとき。

## Do not read this when
- 現行の permission profile の不使用・動的生成禁止という正本仕様を確認したいときは、codex_exec_rule.md を直接読む。
- .gitignore の現在のパターンや実際の ignore 判定を確認したいときは、.gitignore と git check-ignore の結果を直接調べる。
- permission profile の具体的な設定方法や実装を確認したいとき。

## hash
- 987eb09968e110f446ed1d4ba07c5ed1edec235bc979c1b816138f8ab088b763

# `memory_alternative.md`

## Summary
- AI-generated kaizen を後続の Codex CLI 実行へ自動注入しない判断理由を説明する文書。仕様・入力・ログ・成果物を明示的に参照可能に保ち、未検証の AI 改善案を暗黙の記憶や準仕様として蓄積しない方針を扱う。

## Read this when
- AI-generated kaizen やメモリ機構を次回実行へ自動反映する設計の是非を検討するとき。
- 誤診断の永続化、古い制約の混入、仕様とログの混同といった自動注入のリスクを確認したいとき。

## Do not read this when
- 現在の共通原則そのものを確認したいときは、正本である feedback 仕様を直接読むべき。
- Codex CLI のメモリ機構の具体的な実装や運用手順を確認したいとき。

## hash
- bc32ac25bcf7c60c60e815650fbac349db3b1b4f55f6c615396792c6681fafb5

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
- 作業計画レビューを採用しなかった当時の判断記録。AI に計画を書かせて人間が監督する方式ではなく、人間が望む成果物を oracle に定義し、AI がレビューと実装を追従させる方式を選んだ理由、AI への委任範囲、共同作業上の懸念を扱う。

## Read this when
- `tgbt plan` や `/plan` のような計画レビュー機能を採用しなかった理由を確認したいとき。
- 成果物を起点にした人間と AI の役割分担や、当時の AI 委任可能範囲の評価を確認したいとき。

## Do not read this when
- 現在の oracle review の判断や代替手段を確認したいときは、`oracle_review.md` を直接読むとき。
- 具体的な作業計画の内容や実装手順を確認したいとき。

## hash
- f02f409e012460c1b72522890ce3ad4b903a1a441f5ff232243c120ba0142af2
