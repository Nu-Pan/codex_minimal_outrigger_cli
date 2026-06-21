# `test_prompt_parts.py`

## Summary

- prompt 部品の StructDoc 生成と markdown 表現を検証するテスト群です。
- 各標準断片が期待どおりの見出し・文言を持つかを確認し、完全な prompt への含有条件も押さえます。
- index entry 標準、apply review 標準、review oracle 標準の主要な出力規則を回帰テストする入口です。

## Read this when

- prompt 断片の組み立て結果や markdown レンダリングの期待値を確認したいとき。
- 完全な prompt に各標準断片が条件付きで含まれるか、既定では含まれないかを確認したいとき。
- index entry や review 標準のような共通プロンプト部品を変更した後に、回帰確認の観点を把握したいとき。

## Do not read this when

- 個別の prompt 断片の実装内容だけを確認したいとき。
- `complete_prompt` 以外の別フローや別階層のテストを探しているとき。
- このファイルで検証している包含条件やレンダリング結果がすでに分かっていて、直接本体や関連テストへ進むとき。

## hash

- 5d7c302901b2feee319c7f721f1b30ba4982d5c51a7aa732bb18ceaaf81eba47
