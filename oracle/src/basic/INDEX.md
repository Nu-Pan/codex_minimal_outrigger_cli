# `acp.py`

## Summary

- `<cmoc-root>/oracle/src/basic/acp.py` は、AI コーディングエージェント呼び出し用の共通型を定義するファイルです。
- `ModelClass`、`ReasoningEffort`、`FileAccessMode` の列挙型と、これらを束ねる `AgentCallParameter` を提供します。
- backend 実装への具体的なモデル名解決は担当せず、cmoc 上の論理的な呼び出し条件を表現するための基盤です。

## Read this when

- AI コーディングエージェントのモデル選択、推論強度、ファイルアクセスモード、prompt、structured output schema の扱いを確認したいとき。
- `ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameter` の定義や役割を把握したいとき。
- cmoc 上の論理的な呼び出し条件だけを整理したいとき。
- このファイルの個別定義を読む前に、共通の入れ物と列挙型の役割を先に把握したいとき。

## Do not read this when

- バックエンド受理可能なモデル名への解決や、実装側の対応表を確認したいとき。
- `path_model.py`、`standard.py`、`struct_doc.py` など別の共通基盤だけを追いたいとき。
- すでに `ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameter` の役割が分かっていて、このファイル本体を直接確認したいとき。
- AI コーディングエージェント呼び出しではなく、設定や文書レンダリングの仕様を追いたいとき。

## hash

- 899055a64c6c21d9e062970ffb35779c7d1eafeb41fb77388c18af2455faf171

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
- `Standard` は見出し、対象、背景、要求、判定基準、例示をまとめ、各フィールドの型や空配列を検証します。
- `Requirement` は `必須` / `禁止` / `推奨` / `許容` のラベルと本文を持つ凍結 dataclass です。
- `standard_to_struct_doc()` は `Standard` を階層化された `StructDoc` に整形して、markdown 出力や文書組み立てへ渡せる形にします。

## Read this when

- `Standard` と `Requirement` の定義、入力検証、各フィールドの役割を確認したいとき。
- `oracle` 配下で新しい標準文書や標準断片を追加・修正するとき。
- `standard_to_struct_doc()` で `Standard` を `StructDoc` に変換する流れを把握したいとき。
- `<work-root>/oracle/src/acp/prompt_parts` などで共通の標準フォーマットを使う前に、対象・背景・要求・判定基準・例示の構造を整理したいとき。

## Do not read this when

- `Standard`、`Requirement`、`standard_to_struct_doc()` の役割がすでに分かっていて、このファイル本体を直接確認したいとき。
- `StructDoc` の実装や markdown レンダリングだけを確認したいとき。
- パス解決や root token の扱いだけを確認したいとき。
- 個別の `oracle` 標準文書や prompt 断片だけを読み、この共通定義は不要なとき。

## hash

- 548458cf7c69648918ee1e06bf58430ff24cd1023476aa3e0cc2bd6297c083c3

# `struct_doc.py`

## Summary

- この `<cmoc-root>/oracle/src/basic/struct_doc.py` は、階層構造を持つ文章を `StructDoc` として保持し、markdown にレンダリングするための共通ヘルパーです。
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

- 395c731db73411b43b15d1bfda78b11293da74b06f9d5b35ceec78bec69ee227
