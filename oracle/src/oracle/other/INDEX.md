# `cmoc_config.py`

## Summary
- `cmoc` のリポジトリ固有設定をまとめる定義。設定項目の既定値、JSON 永続化時の扱い、Enum 系の value 化、`codex`・`apply fork`・`review oracle` 向けの個別設定を扱う。

## Read this when
- `cmoc` の設定項目を追加・変更・削除したいとき。
- 設定の JSON 保存形式や、Enum をどう直列化するかを確認したいとき。
- `codex`、`cmoc apply fork`、`cmoc review oracle` に関わる既定値や repo ごとの振る舞いを見たいとき。

## Do not read this when
- CLI の入出力やコマンド実行の詳細を知りたいだけなら、各サブコマンドや実行処理側を読む。
- 設定の生成・同期の手順だけを知りたいなら、doctor や永続化周辺の仕様を読む。
- `cmoc` 全体の利用手順や一般的な動作を知りたいだけなら、設定定義そのものではなく上位の app spec を読む。

## hash
- 520f4b5d648b84e5622f2ea1d45fc76ae39997ea4e01070e9dcd44126da47045

# `path_model.py`

## Summary
- `{{work-root}}/oracle/src/oracle/other/path_model.py` は、`{{cmoc-root}}` `{{repo-root}}` `{{run-root}}` `{{work-root}}` の解決規則と、実パスとプレースホルダ表記の相互変換を定義する。パス解決ロジックや新しいルート表記の扱いを確認したいときに読む。

## Read this when
- プレースホルダ付きパスを実パスへ解決する規則を確認したいとき
- 実パスをプレースホルダ表記へ戻す規則を確認したいとき
- `{{cmoc-root}}` `{{repo-root}}` `{{run-root}}` `{{work-root}}` の判定条件を確認したいとき

## Do not read this when
- 単なる文字列整形や一般的な CLI ルーティングだけを確認したいとき
- パス解決以外の設定、コマンド体系、実行フローを確認したいとき
- 既存の INDEX.md エントリー文言の編集方針だけを見たいとき

## hash
- 7e7ab0726d9a013ff720de44e556898a5693c9d7d55b9ea8da57d5ebba716bc6

# `standard.py`

## Summary
- `Standard` と `Requirement` の共通表現、およびそれを `StructDoc` に変換する最小の基盤を定義している。個別の標準文そのものではなく、標準定義の器と変換規約を扱う層への入口として使う。

## Read this when
- 標準文を新しく定義するとき、または既存の標準定義がどういう構造で組み立てられるかを確認したいとき。
- `Requirement` のラベルや、標準を `StructDoc` に落とす変換結果に影響する変更を入れるとき。
- 標準定義の入力検証や、空の `examples` をどう扱うかを確認したいとき。

## Do not read this when
- 個別の標準内容や判定基準を読みたいだけなら、各 standard の定義ファイルを直接読む。
- `StructDoc` のレンダリングや cmoc ブロックの検査を追いたいだけなら、`struct_doc` 側を読む。
- 標準の利用先のプロンプト生成やテンプレート文面を調整したいだけなら、この基盤ではなく上位の prompt builder 側を読む。

## hash
- 9c61e023928041aed3c4b1970c0e47858a81542e7c898449904f335fc2cb73f8

# `struct_doc.py`

## Summary
- 階層化された文章構造を markdown に変換する処理をまとめる。見出し深さの自動計算、`cmoc_block` の包み込み、`cmoc_ref` の参照検査、コードブロック文字列の整形を扱う。
- 構造化された文章を組み立てる側で、レンダリング前の参照整合性や空行の詰め方まで含めて確認したいときに読む。

## Read this when
- 構造化された文書オブジェクトから markdown を生成したい。
- 見出し深さの決め方、参照先ブロックの欠落検査、重複 block id 検査、コードブロック本文の正規化を変更したい。

## Do not read this when
- 単なる自由形式の markdown 編集ルールを探しているだけなら読まない。
- 構造化文書の組み立てや他の prompt builder の責務を見たいだけなら、そちらの対象を先に読む。

## hash
- b126653e743ce1796dcd1fc60e51289674d8225734b5705c6863adb555e5433b
