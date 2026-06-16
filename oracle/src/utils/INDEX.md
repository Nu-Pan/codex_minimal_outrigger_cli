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

- `resolve_real_path()` などの呼び先がすでに分かっていて、このファイルを直接確認するとき。
- パス表記規則ではなく、`StructDoc` など別の `<work-root>/oracle/src/utils` 基盤を探しているとき。
- root token の定義ではなく、`oracle` 配下の個別仕様や開発規約を確認したいとき。

## hash

- e7c36dedf9b965debff58914874f07bebbe9ea10ad0b5e06db4504593e962db1

# `standard.py`

## Summary

- `<cmoc-root>/oracle/src/utils/standard.py` は、標準の共通表現を定義し、`Standard` と `Requirement` を `StructDoc` に変換するための入口です。
- このモジュールは、oracle 文書群で共通に使う標準フォーマットの基盤をまとめます。
- 標準定義そのものを読む前に、共通データ構造と変換関数の役割を確認するための目次です。

## Read this when

- `Standard` と `Requirement` の役割、および標準定義を `StructDoc` に変換する流れを把握したいとき。
- `oracle` 配下の標準文書を追加・修正する前に、共通の標準表現を確認したいとき。
- `oracle.src.utils.standard` を呼び出す側の実装やテストを読む前に、共通ユーティリティの入口を整理したいとき。
- `oracle` 配下の各種 `*_standard.py` がどの共通基盤を使っているか確認したいとき。

## Do not read this when

- `Standard`、`Requirement`、`standard_to_struct_doc()` の定義がすでに分かっていて、このファイル本体を直接確認するとき。
- `StructDoc` の実装や markdown レンダリングだけを確認したいとき。
- パス解決や root token の扱いを確認したいだけで、`standard.py` は不要なとき。

## hash

- 3f3b52d6376cbe9a2898c1f1c8c8186b9f5c9bda18a40d3f1ddae48e8832f803

# `struct_doc.py`

## Summary

- `<cmoc-root>/oracle/src/utils/struct_doc.py` は、階層構造を持つ文章を `StructDoc` として保持し、markdown にレンダリングする共通ヘルパーです。
- 見出しを再帰的に組み立てる `render_as_markdown()` と、三重クォート文字列のインデントを整える `ntqs()` を提供します。
- prompt 生成や標準文書の組み立てで `StructDoc` を使うときの、共通基盤の入口です。

## Read this when

- 階層化された文章を `StructDoc` で表現し、markdown 出力したいとき。
- `render_as_markdown()` の見出し階層や、`ntqs()` の改行・インデント正規化の挙動を確認したいとき。
- `<work-root>/oracle/src/utils/standard.py` や prompt_builder 配下から `StructDoc` を使う前に、共通表現の仕様を把握したいとき。
- `StructDoc` を使う新しいヘルパーを追加・修正する前に、既存の共通基盤を確認したいとき。

## Do not read this when

- 既に `StructDoc` の使い方が分かっていて、`struct_doc.py` のコード本体を直接確認するとき。
- `path_model.py` だけ、または `standard.py` だけを個別に確認したいとき。
- markdown の共通化ではなく、個別の prompt 文書やレビュー規約だけを追いたいとき。

## hash

- db91b79116cc87a37124cc214cd697e91182656d38b2f33dcabb792cd38e8e10
