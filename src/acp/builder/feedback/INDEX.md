# `__init__.py`

## Summary
- feedback の issue 正規化・検証に対応する builder adapter パッケージ。対応する oracle 実装を起点に、feedback の normalize／verify 処理を確認する際の入口となる。

## Read this when
- feedback issue の normalization または verification に関する builder adapter の構成を確認するとき
- 対応する oracle の normalize_issue／verify_issue 実装との対応関係を確認するとき

## Do not read this when
- feedback 以外の builder adapter を調べるとき
- 正規化・検証処理そのものの詳細を確認する場合は、対応する oracle file を直接読む

## hash
- 5be652524e2cf162bcb1e9f7afa2fb8fff79cfa9828f6648565cc06ee9728f4c

# `normalize_issue.py`

## Summary
- feedback issue の同一性判断用 canonical builder を再公開する realization adapter。oracle builder が生成する AgentCallParameter を基に、Structured Output schema と重複する new 判定用の prompt 指示だけを除去する。

## Read this when
- feedback issue の normalize 処理へ渡す AgentCallParameter の生成経路や、canonical prompt の重複指示補正を確認するとき。

## Do not read this when
- feedback issue の同一性判断ロジックそのもの、Structured Output schema の定義、または oracle builder の正本仕様を確認したいとき。これらは対応する oracle file や canonical builder を直接読む。

## hash
- 8990916ccd631feb12ea3af9224a9e2e8aa7559f58777b73ddb05b73aae0809d

# `verify_issue.py`

## Summary
- 対象は feedback issue verification 用の realization adapter で、oracle の canonical builder を呼び出し、実運用向け AgentCallParameter の prompt を補正して再公開する。
- canonical prompt 内の Structured Output schema と重複する verdict 指示を検出し、該当する human action の指示行だけを除去する責務を持つ。

## Read this when
- feedback issue verification の AgentCallParameter を構築する実装や、canonical builder の prompt を実運用向けに補正する処理を確認するとき。
- schema と prompt の verdict 指示の重複を除去する挙動や、その適用対象を確認するとき。

## Do not read this when
- feedback issue verification 以外の builder や一般的な prompt 生成の責務を調べるとき。
- verdict 条件そのものの正本仕様や schema 定義を確認したいときは、対応する oracle file または Structured Output schema を直接読む。

## hash
- 277ec2a8e40d229cb223f35f9d958f73b5e79fbfd46a44a298557e2d2dd98c94
