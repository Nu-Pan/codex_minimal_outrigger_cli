# `apply_behavior.md`

## Summary
- `cmoc realization refactor` で不採用となった先行計画立案と並列の所見列挙・個別修正案、その不採用理由を記録する設計判断の背景資料。現行手順の正本ではない。

## Read this when
- realization refactor で先行計画立案や並列の所見列挙を採用しなかった理由を確認するとき。

## Do not read this when
- realization refactor の現行状態、調査対象の選択、処理単位、完了条件を実装・変更・確認するときは、正本の `oracle/doc/app_spec/sub_command/realization_refactor.md` を直接読む。

## hash
- 4ca1f0d162961d203941966401a55acccf672c043dd5dc0f51e24487e8cd8322

# `file_access_policy_violation_post_validation.md`

## Summary
- agent call の差分を事後検査し、違反時に自動リカバリーする案を断念した経緯と、その判断の背景を記録する。現行仕様ではなく、過去の検討理由を確認するための資料。

## Read this when
- 事後検査と自動リカバリーを採用しなかった経緯や、並列編集時の誤検知・差分の帰属に関する懸念を調べるとき。

## Do not read this when
- 現行の差分検証や file access policy の要件を確認・変更するときは、正本仕様の「agent call の差分検証」を直接読む。過去の検討経緯が不要な場合も参照不要。

## hash
- aa4e46f7fa5ff8935ccf8bccc7747ee27928538a2c397ad21e9cf05288f20c03

# `gitignore_to_permission_profile.md`

## Summary
- .gitignore の無視判定から permission profile を動的生成する案の採否と断念理由を記録した文書です。現行ルールではなく、その代替案を採用しなかった背景を確認する入口です。

## Read this when
- 無視対象ファイルを permission profile の例外として扱う案が、なぜ採用されなかったかを調べるとき。

## Do not read this when
- 現行の permission profile の制約を確認するときは、正本仕様を直接参照してください。
- permission profile の動的生成案に関係しない .gitignore の挙動を調べるとき。

## hash
- 987eb09968e110f446ed1d4ba07c5ed1edec235bc979c1b816138f8ab088b763

# `memory_alternative.md`

## Summary
- cmoc が AI 生成の改善案を後続の Codex CLI 呼び出しへ自動注入しない理由を説明する。明示的で追跡可能な情報を重視する設計と、自動注入による誤診断の固定化や古い助言の混入などの懸念を扱う。

## Read this when
- cmoc で AI 生成の改善案や記憶を実行間で引き継ぐ設計の判断理由・トレードオフを確認するとき。

## Do not read this when
- 自動注入の規範的なルールや feedback 全体の共通原則を確認するときは、正本の oracle/doc/app_spec/feedback.md を読む。
- feedback の収集・状態管理・report の具体的な仕様や、Codex CLI 自体の memory 機能の詳細を調べるとき。

## hash
- bc32ac25bcf7c60c60e815650fbac349db3b1b4f55f6c615396792c6681fafb5

# `oracle_review.md`

## Summary
- oracle file のスナップショットを網羅検査する独立コマンドを採用しない判断と、その理由を説明する。通常の workload で問題を見つけた場合の報告との境界や、代替方針を確認するための入口。

## Read this when
- oracle file 専用の網羅検査を提供しない理由や、その判断で許容する不確実性を確認するとき。
- 通常の workload における問題報告が、独立した網羅検査の代替としてどこまで扱われるかを確認するとき。

## Do not read this when
- 問題報告の基準を確認するときは、報告基準を定める正本を直接読む。
- `cmoc feedback report` の処理内容を確認するときは、そのサブコマンドの正本を直接読む。
- 別の機能や代替案の不採用理由を調べており、oracle file の網羅検査の判断が関係しないとき。

## hash
- 7587831208609b406e33647005fd1d5f34560e7c301828947c12adc83bd1b3a9

# `working_plan_review.md`

## Summary
- AI に作業計画を書かせて人間がレビューする方式を採用せず、望む成果物を oracle に記し AI がレビューと実装を進める方式を選んだ当時の評価を記録する。
- 現行の oracle review 方針ではなく、その判断に至った背景をたどるための資料。

## Read this when
- 作業計画レビュー方式を採用しなかった当時の理由や、人間と AI の役割分担の考え方を確認するとき。

## Do not read this when
- 現在の oracle review の扱いや判断を確認するときは、現行の扱いを記す oracle review の資料を読む。

## hash
- f02f409e012460c1b72522890ce3ad4b903a1a441f5ff232243c120ba0142af2
