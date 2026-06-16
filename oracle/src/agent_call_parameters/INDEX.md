# `prompt_builder`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameters/prompt_builder/oracles_standards.py` は、oracle file 向けの standards を `StructDoc` にまとめる入口です。
- このモジュールは、`oracle standards` の内容を prompt 用の構造化文書として組み立てる役割を持ちます。
- 同階層で確認すべき中心ファイルはこの `oracles_standards.py` です。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameters/prompt_builder/oracles_standards.py` が何を組み立てるモジュールか確認したいとき。
- `Standard` と `Requirement` を使って oracle file 向けの規範をどう StructDoc 化しているか追いたいとき。
- oracle file の認知負荷最小化、正本仕様断片、未定義部分の扱い、文字数最小化、矛盾回避、用語統一、命名、ベストプラクティスとの優先関係、goal/non-goal の整理方針を確認したいとき。

## Do not read this when

- `oracles_standards.py` の内容がすでに分かっていて、この階層の目次を経由せず直接確認するとき。
- `oracle` 配下の自然言語仕様や他の `INDEX.md` を確認したいだけで、このモジュールは不要なとき。
- Structured Output schema や実装本体ではなく、別の prompt builder モジュールを探しているとき。

## hash

- 2d5895a798f053b073ad31c8cc929ceae176c59364e907bcd4dc4b32fedcabcd
