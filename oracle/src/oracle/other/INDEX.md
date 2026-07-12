# `cmoc_config.py`

## Summary
- `CmocConfig` 系の永続設定を扱う入口。リポジトリごとに変わる cmoc の挙動設定、Codex CLI 向けモデル対応、`cmoc apply fork` と `cmoc review oracle` の個別設定、json への保存方針を確認したいときに読む。
- この設定の直下で、どの項目が既定値として固定され、どの項目を人間が調整する前提かを把握するための案内に向く。

## Read this when
- cmoc のリポジトリ別設定を追加・変更したい。
- Codex CLI 向けのモデル名や reasoning effort の対応を確認したい。
- `cmoc apply fork` や `cmoc review oracle` の既定動作を調べたい。
- 設定の json 永続化や enum の value 化の扱いを確認したい。

## Do not read this when
- `cmoc` のコマンド実装や各サブコマンドの処理手順を追いたい。
- 設定の読み書きロジックそのものや保存先の実装詳細を探したい。
- 個別の UI・出力・テストの挙動を見たい。
- この設定に含まれない他の永続状態や別機能の設定を探したい。

## hash
- 5f4ca222620328fcea1e325566bb80a9d5cb0a39c6f72ad42821d539cf2d3564

# `path_model.py`

## Summary
- `oracle/src/oracle/other/path_model.py` の、`{{cmoc-root}}`・`{{repo-root}}`・`{{run-root}}`・`{{work-root}}` の解決規則と、実パスとプレースホルダ表記の相互変換を扱う入口。パス解決の境界条件や例外を確認したいときに読む。

## Read this when
- ルートパスプレースホルダの意味や解決方法を変えるとき
- 絶対パス・相対パス・プレースホルダ付きパスの受け入れ条件を確認したいとき
- `work-root` / `repo-root` / `run-root` / `cmoc-root` の見つけ方や失敗時挙動を調べたいとき
- 実パスをプレースホルダ表記へ戻す変換の仕様を確認したいとき

## Do not read this when
- CLI のサブコマンド全体や他の設定モデルを探したいとき
- 個別コマンドの入出力や業務ロジックを確認したいとき
- パス解決以外の共通ユーティリティや別の `oracle/other` ファイルを見たいとき

## hash
- a3d1106f01ca2a08139a30ecb7f60467f1f40b8071f1cf99cd77897d53dca932

# `standard.py`

## Summary
- `Standard` と `Requirement` の定義、および `standard_to_struct_doc` を扱う。規範文書の見出し・背景・要求・判断例をどの形で保持し、`StructDoc` に落とすかを読む入口にする。

## Read this when
- 規範を表すデータ構造の必須項目や検証条件を確認したいとき。
- `Requirement` のラベル制約や、`examples` に何を書いてよいかの境界を確認したいとき。
- `Standard` を `StructDoc` に変換する際の章立てや、どのフィールドが出力に使われるかを確認したいとき。

## Do not read this when
- `oracle file` 全体の命名規則や配置方針を知りたいだけのときは、より上位の oracle 標準文書を読む。
- `StructDoc` 自体の仕様や実装詳細を知りたいだけのときは、このファイルではなく `StructDoc` の定義元を読む。
- この定義を使う個別の標準文書の内容を確認したいときは、各標準文書を直接読む。

## hash
- d19edf009065fcbd4a29ea2693bccd0f09a9860ab31fba30d25aaaa1f0108eaf

# `struct_doc.py`

## Summary
- 階層付きの markdown 文書を組み立ててレンダリングするための基盤。見出し深さの自動決定、`cmoc_block` と `cmoc_ref` の整合性検査、コードブロックや文字列本文の正規化を扱う。
- `StructDoc` / `StructBlock` / `StructCodeBlock` の構造や、レンダリング前検査・改行圧縮・インデント正規化の振る舞いを確認したいときに読む。

## Read this when
- markdown 生成時の見出し階層、ブロック参照の検証、コードブロックの埋め込み方針を変えたい。
- `cmoc_ref` の解決条件や `cmoc_block` の重複検出、空行圧縮の境界を確認したい。
- 構造化文書のノード型や、文字列本文の正規化方法を追いたい。

## Do not read this when
- 単なる CLI 入出力や他サブコマンドのルーティングを見たい。
- markdown 以外の汎用テキスト処理や別フォーマットのレンダリングを探している。
- 構造化文書の仕様そのものを読むだけなら、根拠として近接する正本仕様断片の方が直接的だが、この実装の詳細挙動だけを見たいわけではない。

## hash
- fbb3959c4420a6d1ec2b263170dcc6b478bef13c1007507b957cc6c2f8a4f198
