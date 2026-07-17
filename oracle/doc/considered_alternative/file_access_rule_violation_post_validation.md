# File Access Rule Violation Post Validation

## やりたかったこと

- agent call が発生させた差分内容にたいして、file access rule に違反していないか、cmoc が事後検査を行う
- 事後検査の結果違反が見つかった場合、cmoc は別の agent call でリカバリーを試みる

## 断念した理由

- false-positive による cmoc の停止が相次いだ
- e.g. 単一の `{{run-root}}` を並列 agent で編集した際にお互いがの差分を violation 扱いしてしまう
- e.g. gitginore 系は検査対象に含まないのだが、その事が realization file 上うまく反映されない (oracle file で定義を書くべきか)
- そもそも「agent call が発生させた差分」を正確に判定するのがむりなのでは、という感じ。
- 新なる違反を見たこと無いので、一旦断念し、それらの仕様を git commit hash 49ef351d687235a0e8ea2dc9e3eb2dc7ab8ae852 で削除した
