# `acp.py`

## Summary

- この `basic` ディレクトリのルーティング文書で、`acp.py`、`path_model.py`、`standard.py`、`struct_doc.py` への入口です。
- `acp.py` は AI コーディングエージェント呼び出し用の共通型を、`path_model.py` は root token 付きパス解決を、`standard.py` は標準表現を、`struct_doc.py` は階層文書の markdown レンダリングを案内します。
- この階層は、cmoc の共通基盤をまとめて扱うための目次です。

## Read this when

- `<work-root>/oracle/src/basic` 配下で、どの基盤ファイルから読むべきか整理したいとき。
- `BackendType`、`ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameter` の所在を確認したいとき。
- `<cmoc-root>` / `/<repo-root>` / `<run-root>` / `<work-root>` の解決規則や、標準表現、StructDoc の役割をまとめて把握したいとき。
- この階層の下位 `INDEX.md` や個別ファイルへ進む前に、役割分担を先に整理したいとき。

## Do not read this when

- すでに読む対象が `acp.py`、`path_model.py`、`standard.py`、`struct_doc.py` のいずれかに決まっていて、この目次を経由する必要がないとき。
- `BackendType`、`ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameter` の定義内容を直接確認したいとき。
- パス解決、標準表現、StructDoc のうち、個別機能だけを直接確認したいとき。
- `oracle` 全体の別ルートや開発規約だけを確認したいとき。

## hash

- f5779d476de953b93122d973246f48e8485f33a55644887d93fe0b15957c138f

# `path_model.py`

## Summary

- `<cmoc-root>/oracle/src/utils/path_model.py` は、cmoc のパス表記と root token 解決を扱うユーティリティです。
- `RootToken` で `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` を定義し、文字列や `Path` から実パスへ変換します。
- 逆変換として、実パスを root token 表記に戻す `resolve_token_path()` も提供します。

## Read this when

- `<cmoc-root>/oracle/src/utils/path_model.py` の役割と、`RootToken` による root 解決の入口を把握したいとき。
- ルートトークン付きの相対パスを絶対パスへ解決したいとき。
- 実パスを `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` 表記へ戻す方法を確認したいとき。
- 各 root token の違いと使い分けを整理したいとき。

## Do not read this when

- `RootToken` と `resolve_real_path()` の役割がすでに分かっていて、このファイル本体を直接確認したいとき。
- パス解決ではなく、`standard.py` や `struct_doc.py` など別の `utils` 基盤を探しているとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の定義ではなく、別の oracle 文書や開発規約だけを確認したいとき。

## hash

- 027714ffb8df9a610273154c3576c6f114050fedcea38cd005f3fc034aec3519

# `standard.py`

## Summary

- この `standard.py` は、`oracle` 文書で共通に使う標準表現を定義し、`Standard` と `Requirement` を `StructDoc` へ変換する入口です。
- `Standard` は見出し・対象・背景・要求・判定基準・例示をまとめ、入力の型や空配列を検証します。
- `Requirement` は `必須` / `禁止` / `推奨` / `許容` のラベルと本文を持つ凍結 dataclass です。
- `standard_to_struct_doc()` は `Standard` を階層化された `StructDoc` に整形して、markdown 出力や文書組み立てに渡せる形へ変換します。

## Read this when

- `oracle` 配下の標準文書を新規追加・修正するとき。
- `Standard` と `Requirement` の役割、または `StructDoc` への変換経路を確認したいとき。
- `basic.standard` を利用する実装やテストを書く前に、共通の標準フォーマットを把握したいとき。
- `oracle` の各種 `*_standard.py` がどの共通基盤を使うか追いたいとき。

## Do not read this when

- `Standard`、`Requirement`、`standard_to_struct_doc()` の役割がすでに分かっていて、このファイル本体を直接確認したいとき。
- `StructDoc` の実装や markdown レンダリングだけを確認したいとき。
- パス解決や root token の扱いだけを確認したいとき。
- 個別の仕様本文だけを読み、`standard.py` の共通定義は不要なとき。

## hash

- dfda5b72a8ee44107a9f085d7e21e6c2baa30cbf1ef9836ce48d1ed8f31b6e68

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
