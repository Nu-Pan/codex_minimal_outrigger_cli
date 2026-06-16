# `path_model.py`

## Summary

- `<cmoc-root>/oracle/src/utils/path_model.py` は、cmoc のパス表記と root token 解決を扱うユーティリティです。
- `RootToken` で `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` を定義し、文字列や `Path` から実パスへ変換します。
- 逆変換として、実パスを root token 表記に戻す `resolve_token_path()` も提供します。

## Read this when

- `<cmoc-root>/oracle/src/utils/path_model.py` の `RootToken` と各 root 解決処理の役割を把握したいとき。
- ルートトークン付きの相対パスを絶対パスへ解決したいとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の違いと使い分けを確認したいとき。

## Do not read this when

- `RootToken` や `resolve_real_path()` の実装をすでに把握していて、このファイル本体を直接確認するとき。
- パス解決ではなく、`StructDoc` や `standard.py` など別の `utils` 基盤を探しているとき。
- root token の定義ではなく、`oracle` 配下の個別仕様や開発規約だけを確認したいとき。

## hash

- da048fc9cbd327d4867d675e9377f9692a49de6ccf38ec008eebb0a91ebdd7ad

# `standard.py`

## Summary

- `<cmoc-root>/oracle/src/utils/standard.py` は、oracle 文書で共通に使う標準表現を定義し、`Standard` と `Requirement` を `StructDoc` へ変換する入口です。
- `Standard` は見出し・対象・背景・要求・判定基準・例示をまとめ、入力の型や空配列を検証します。
- `Requirement` は `必須` / `禁止` / `推奨` / `許容` のラベルと本文を持つ凍結 dataclass です。
- `standard_to_struct_doc()` は `Standard` を階層化された `StructDoc` に整形して、markdown 出力や文書組み立てに渡せる形へ変換します。

## Read this when

- `oracle` 配下の標準文書を新規追加・修正するとき。
- `Standard` と `Requirement` の役割、または `StructDoc` への変換経路を確認したいとき。
- `oracle.src.utils.standard` を利用する実装やテストを書く前に、共通の標準フォーマットを把握したいとき。
- `oracle` の各種 `*_standard.py` がどの共通基盤を使うか追いたいとき。

## Do not read this when

- `Standard`、`Requirement`、`standard_to_struct_doc()` の役割がすでに分かっていて、このファイル本体を直接確認するとき。
- `StructDoc` の実装や markdown レンダリングだけを確認したいとき。
- パス解決や root token の扱いだけを確認したいとき。
- 個別の仕様本文だけを読み、`standard.py` の共通定義は不要なとき。

## hash

- f1c731a2f6faf2a326e85a6d9f2fdd0adb0d1fd5f46e515b6e7146a997bd7a4d

# `struct_doc.py`

## Summary

- `<cmoc-root>/oracle/src/utils/struct_doc.py` は、階層構造を持つ文章を `StructDoc` として保持し、markdown にレンダリングするための共通ヘルパーです。
- 見出しを再帰的に組み立てる `render_as_markdown()` と、三重クォート文字列のインデントを整える `ntqs()` を提供します。
- prompt 生成や標準文書の組み立てで `StructDoc` を使うときの、共通基盤の入口です。

## Read this when

- 階層構造を持つ文章を `StructDoc` で表現し、markdown に出力したいとき。
- `render_as_markdown()` の見出し階層の生成方法や、`ntqs()` の改行・インデント正規化の挙動を確認したいとき。
- `standard.py` や prompt_builder 配下から `StructDoc` を使う前に、共通表現の仕様を把握したいとき。
- `StructDoc` を使う新しいヘルパーを追加・修正する前に、既存の共通基盤を確認したいとき。

## Do not read this when

- `StructDoc` の使い方がすでに分かっていて、`struct_doc.py` の実装を直接確認したいとき。
- `path_model.py` や `standard.py` だけを個別に確認したいとき。
- 個別の prompt 文書やレビュー規約を追っていて、共通の markdown レンダリング基盤は不要なとき。

## hash

- e32829336f19e839e8f0cbc28fae24d48d58413d451b04ad36f07345f47022fc
