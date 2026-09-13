# File Access Policy Violation Post Validation

本書は、file access policy 違反の事後検査と自動リカバリーを断念した当時の記録である。現行の差分検証の範囲は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「agent call の差分検証」を正本とする。

## やりたかったこと

- cmoc が agent call による差分を事後検査し、file access policy への違反がないか確認する
- 事後検査で違反が見つかった場合、cmoc は別の agent call でリカバリーを試みる

## 断念した理由

- false-positive による cmoc の停止が相次いだ
- 例えば、単一の `{{run-root}}` を並列 agent で編集すると、互いの差分を violation と判定してしまう
- また、`.gitignore` 系を検査対象に含めない方針が realization file にうまく反映されず、oracle file への定義が必要かを検討していた
- これらの経験から、「agent call が発生させた差分」を正確に判定すること自体に疑問が残った
- 当時は新たな違反を見ていなかったため、一旦断念し、それらの仕様を git commit hash 49ef351d687235a0e8ea2dc9e3eb2dc7ab8ae852 で削除した
