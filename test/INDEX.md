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

# `test_basic_and_cli.py`

## Summary

- basic/config/runtime/CLI の主要 realization 挙動を検証するテスト群です。
- path token 解決、config 既定値と永続化、stdout structured error、completion probe の副作用回避、work root 実行検査、`.cmoc` ignore 保証、Codex 呼び出し前 indexing、INDEX entry 並列生成、apply fork 編集禁止差分検査、最小 apply state schema、apply join 想定外差分判定、session fork 状態ファイル、review report frontmatter 生成を扱います。
- prompt 部品以外の共通基盤と CLI 境界の回帰確認入口です。

## Read this when

- path model、config JSON、runtime/stdout error、completion probe、work root 実行検査、`.cmoc` ignore、Codex 呼び出し前 indexing、INDEX entry 並列生成、apply fork 編集禁止差分検査、最小 apply state schema、apply join 想定外差分判定、session/review CLI と review report のテスト観点を確認したいとき。
- `src/main.py` や `src/cmoc_runtime.py` を変更した後に、どの CLI 挙動が検証されているか把握したいとき。
- 一時 git repository を使う CLI テストの作り方を確認したいとき。

## Do not read this when

- prompt 部品の StructDoc 生成と Markdown 表現だけを確認したいとき。
- 個別の prompt builder や Structured Output schema の内容を直接追いたいとき。
- CLI ではなく oracle/src と同形の純粋関数だけを確認したいとき。

## hash

- 19d21ac286d881e1fbeeb7e7096702a407270ec9503786fa7ac28f6011f2a33c
