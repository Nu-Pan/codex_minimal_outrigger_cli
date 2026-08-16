# File Access Policy Violation Post Validation

## やりたかったこと

- agent call が発生させた差分に対して、file access policy に違反していないか、cmoc が事後検査を行う
- 事後検査の結果違反が見つかった場合、cmoc は別の agent call でリカバリーを試みる

## 断念した理由

- false-positive による cmoc の停止が相次いだ
- e.g. 単一の `{{run-root}}` を並列 agent で編集した際に、お互いの差分を violation 扱いしてしまう
- e.g. `.gitignore` 系は検査対象に含まないが、そのことが realization file 上でうまく反映されない（oracle file で定義を書くべきか）
- そもそも「agent call が発生させた差分」を正確に判定するのは難しいのではないか
- 新たな違反を見ていないため、一旦断念し、それらの仕様を git commit hash 49ef351d687235a0e8ea2dc9e3eb2dc7ab8ae852 で削除した
