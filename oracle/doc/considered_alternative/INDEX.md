# `apply_behavior.md`

## Summary
- cmoc realization refactor で採用しなかった作業方式と、その不採用理由を記録する文書。事前の作業計画立案や、所見の並列リストアップ・所見単位の修正を避け、永続的な調査要求に従ってファイル単位で調査と反映を進める現行方針との違いを確認するための入口。

## Read this when
- cmoc realization refactor の作業フローや調査・修正単位の設計理由を確認するとき
- 事前計画方式、並列所見調査、ダーティフラグ方式を採用しなかった背景を調べるとき
- 現行の investigation_required の責務と、一時的な queue 管理方式との違いを確認するとき

## Do not read this when
- 具体的な realization file の修正方法や実装責務を確認したいとき
- 現行 refactor state の定義や運用仕様を直接確認したいとき
- 単に対象ファイルの実装内容やテスト内容を調べたいとき

## hash
- 4ae063e03f4cee3284619dd468f190be9b8260cf5aaac9493faab0d08024688b

# `file_access_policy_violation_post_validation.md`

## Summary
- agent call 後の差分に対する file access policy 違反の事後検査と、違反時の別 agent call によるリカバリー案を記録した検討資料です。false-positive、並列 agent 間の差分誤判定、`.gitignore` 系の扱い、agent call 起因差分の特定困難性を理由に案を断念し、関連仕様を削除した経緯を確認するための入口です。

## Read this when
- file access policy の事後検査や、違反検出後の自動リカバリー案を再検討するとき
- この方式を断念した理由や、過去に削除された仕様の背景を確認するとき
- 並列 agent による差分の誤検出、`.gitignore` の検査対象定義、agent call 起因差分の特定可能性を調査するとき

## Do not read this when
- 現行の file access policy や実装上の責務を確認したいとき
- 実際のアクセス制御・検査処理の仕様やコードを変更するとき
- この検討案の断念経緯ではなく、現在採用されている仕様を確認したいとき

## hash
- b03169145359e5a6b4136d7bd26d9335a9a7ee8f3d06fc03a56f478eebca8486

# `gitignore_to_permission_profile.md`

## Summary
- `.gitignore` の除外判定を permission profile の読み書き例外へ変換する案を検討した記録。記法の非互換性により採用せず、現行のアクセス制限は別の正本仕様に従う方針と、変換を実行時分岐や fallback に使わない判断を示す。

## Read this when
- `.gitignore` と permission profile の連携案、その採否理由、または除外ファイルを自由に扱う例外規則の検討経緯を確認するとき。

## Do not read this when
- 現行のファイルアクセス制限そのものを確認・変更するとき。指定された正本仕様を直接読むべきである。
- .gitignore の現在の除外パターンや、実行時のアクセス制御を実装・調査するとき。

## hash
- b30df9818914933f918982f74982684bbcc96a7ef97e7c179756ad599e7d3601

# `memory_alternative.md`

## Summary
- AI に実行結果の振り返りから kaizen を作らせ、それを後続の Codex CLI 実行へ自動注入する設計を cmoc が採用しない理由を説明する正本仕様断片。
- 検証・整理・人間の採用判断を経ない AI-generated kaizen は、仕様、ログ、失敗分析、思い込みが混ざった曖昧な準仕様レイヤーになり、oracle とは別の暗黙仕様を生むため避けるべきだと位置づける。
- cmoc が目指すべき方向を、AI に暗黙記憶を持たせることではなく、INDEX、oracle、ログ、実行成果物を通じて必要情報へ明示的に到達できる状態にすることとして示す。

## Read this when
- AI-generated kaizen、memory、振り返り結果、改善案を次回以降の実行コンテキストへ自動で引き継ぐ機能を検討しているとき。
- Codex CLI 呼び出しに継続的な指示、学習結果、失敗原因分析、過去の対処を自動注入する状態管理を追加すべきか判断するとき。
- oracle 以外の場所に蓄積される暗黙の仕様や準仕様レイヤーが、cmoc の仕様単一性や追跡可能性を壊さないか確認したいとき。
- cmoc における情報到達の方針として、永続的な AI 記憶ではなく、INDEX、oracle、ログ、実行成果物の整備を優先する根拠を確認したいとき。

## Do not read this when
- 個別の kaizen 文面の書き方、レビュー観点、改善提案の内容そのものを設計したいだけで、自動的な次回実行への注入可否を扱わないとき。
- INDEX、oracle、ログ、実行成果物の具体的な形式や配置、生成手順を確認したいとき。
- Codex CLI 本体の memory 機能の詳細仕様や操作方法を調べたいとき。
- 一時的な実行ログ、成果物、明示入力を今回限りの判断材料として読む処理を検討しており、継続的な暗黙記憶や自動注入を追加しないことが明らかなとき。

## hash
- 5ef1ea0577ef57db18994f2e242ebf091720662552e236911b3608f9b8431527

# `oracle_review.md`

## Summary
- 通常の workload と独立した oracle file の網羅検査・Markdown レポート作成を行う `cmoc oracle review` を採用しない判断と、その理由を示す文書。
- 意図的な未定義部分との境界が曖昧になり、根拠の薄い修正反復によって oracle file が過剰に詳細化・肥大化するリスクを説明する。
- 通常の workload で解消できない問題を feedback observation として報告する代替方針と、潜在的な問題を残す不確実性を許容する判断を示す。

## Read this when
- `cmoc oracle review` の提供可否や、oracle file の網羅検査を採用しない設計判断を確認するとき。
- 通常の workload における oracle file の調査と、解消できない問題の feedback observation 報告との境界を確認するとき。
- oracle file を疎に保ちつつ実装可能な安定状態を優先する方針を確認するとき。

## Do not read this when
- `cmoc feedback report` の具体的な処理手順や自動修正条件を確認したいときは、feedback report の正本を直接読む。
- agent による feedback observation の報告基準を確認したいときは、feedback observation の正本を直接読む。
- 通常の workload における個別の oracle file の内容や実装詳細だけを確認したいとき。

## hash
- 94dadc3181ebca75170b8ee418395e9d736cef7ea77eed49d78eb53d5f0e6230

# `working_plan_review.md`

## Summary
- AI に作業計画を出させて人間がレビューする方式を採用しなかった理由を説明する、設計上の不採用案メモ。
- 人間が最終成果物に関心を持つ一方で、実装・設計の細部には介助が必要になるという前提から、人間と AI が同じ作業計画を共同管理する方式の問題を整理している。
- 代替として、人間が正本仕様断片を編集し、AI がその実装可能性をレビューして実装を追従させる方式を採用した背景を示す。

## Read this when
- AI に計画を書かせて人間がレビューする workflow を採用しない理由を確認したいとき。
- 人間が oracle を編集し、AI が実装可能性を評価する方式の設計意図を確認したいとき。
- 人間の want、AI の実装追従、作業計画レビューの責務分担を比較して判断したいとき。

## Do not read this when
- oracle file と realization file の一般的な定義や責務を確認したいだけのとき。
- 個別コマンドの入出力仕様、実装手順、テスト仕様を探しているとき。
- 採用済み workflow の操作方法や CLI の具体的な挙動を確認したいとき。

## hash
- f67c8c03a7304771c90eedfba5756a287112ba4a325f5a8c3d56a93f92c5d96d
