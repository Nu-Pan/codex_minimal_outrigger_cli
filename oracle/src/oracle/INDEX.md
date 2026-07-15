# `acp_builder`

## Summary
- `oracle.acp_builder` の共通型と、各サブコマンド別の Agent 呼び出しパラメータ組み立て入口を束ねる上位ルーティング対象。ここでは個別の prompt 本文や schema の詳細ではなく、どの用途でどの下位領域へ進むかを判断する。
- 共通の `AgentCallParameter`、モデル類型、推論強度、ファイルアクセス方針の定義を確認したいときはここから `basic.py` 側へ進む。
- `cmoc apply`、`cmoc indexing`、`cmoc review`、`cmoc session join`、`cmoc tui` のいずれかについて、対応する agent call の正本を探すときはここから各サブディレクトリへ進む。

## Read this when
- ACP builder 全体で共通する呼び出しパラメータの型や既定値を確認したいとき。
- 特定サブコマンドの prompt 生成や Structured Output 入口を探していて、まず担当領域を切り分けたいとき。
- 共通定義とサブコマンド別定義のどちらを読むべきかを、責務分担から判断したいとき。

## Do not read this when
- 個別サブコマンドの prompt 本文、出力契約、実行条件を確認したいときは、対応する下位ディレクトリを直接読む。
- ファイルアクセス規則や prompt ビルダーの共通規約そのものを確認したいときは、ここではなくその定義元を読む。
- Agent 呼び出しの実行フロー全体や CLI 側の制御を追いたいときは、ここではなく上位の実行側を読む。

## hash
- 4323b3d146b309af6a4578e7c607511aa05ba282520d6968f2f2c40d1e882f71

# `other`

## Summary
- `cmoc_config.py`: `cmoc` の repo 固有設定をまとめる定義。設定値の既定、JSON 永続化時の扱い、Enum 系の value 化、`codex`・`apply fork`・`review oracle` 向けの個別設定を読む入口。
- `path_model.py`: `{{cmoc-root}}` `{{repo-root}}` `{{run-root}}` `{{work-root}}` の解決規則と、実パスとプレースホルダ表記の相互変換を扱う。
- `standard.py`: `Standard` と `Requirement` の共通表現、およびそれを `StructDoc` に変換する基盤を扱う。個別の標準定義そのものではない。
- `struct_doc.py`: 階層化された文章を markdown にレンダリングする処理をまとめる。見出し深さ、自動整形、`cmoc_block`/`cmoc_ref` の検査を扱う。

## Read this when
- `cmoc` の設定項目を追加・変更・削除したい。
- 設定の JSON 保存形式や、Enum をどう直列化するかを確認したい。
- `codex`、`cmoc apply fork`、`cmoc review oracle` に関わる既定値や repo ごとの振る舞いを見たい。
- プレースホルダ付きパスを実パスへ解決する規則、または実パスをプレースホルダ表記へ戻す規則を確認したい。
- `{{cmoc-root}}` `{{repo-root}}` `{{run-root}}` `{{work-root}}` の判定条件を確認したい。
- 標準文を新しく定義したい、または既存の標準定義がどう組み立てられるかを確認したい。
- `Requirement` のラベルや、標準を `StructDoc` に落とす変換結果に影響する変更を入れたい。
- 構造化された文書オブジェクトから markdown を生成したい。
- 見出し深さの決め方、参照先ブロックの欠落検査、重複 block id 検査、コードブロック本文の正規化を変えたい.

## Do not read this when
- CLI の入出力やコマンド実行の詳細だけを知りたいなら、各サブコマンドや実行処理側を読む。
- 設定の生成・同期の手順だけを知りたいなら、doctor や永続化周辺の仕様を読む。
- `cmoc` 全体の利用手順や一般的な動作を知りたいだけなら、設定定義そのものではなく上位の app spec を読む。
- 単なる文字列整形や一般的な CLI ルーティングだけを確認したいなら `path_model.py` は読まない。
- パス解決以外の設定、コマンド体系、実行フローを確認したいなら `path_model.py` は読まない。
- 個別の標準内容や判定基準を読みたいだけなら、各 standard の定義ファイルを直接読む。
- `StructDoc` のレンダリングや cmoc ブロックの検査だけを追いたいなら `struct_doc.py` を読む。
- 単なる自由形式の markdown 編集ルールを探しているだけなら `struct_doc.py` は読まない。
- 構造化文書の組み立てや他の prompt builder の責務を見たいだけなら、そちらを先に読む。

## hash
- cbb2834f649fa9396dcaa2ea58071b2357fdc32656cf64f1e809d95eb2128d01

# `prompt_builder`

## Summary
- `basic.py` は、プレースホルダ名と置換先値を共通の型で扱うための定義。置換対象の表現をそろえたいときだけ読む。
- `complete_prompt.py` は、完全なプロンプトの組み立て順と、静的・動的要素や各種標準文の注入条件をまとめる入口。プロンプト全体の構成や注入順を変えるときに読む。
- `parts` は、oracle/realization の基本説明、各種標準、アクセス規則、ルーティング規則など、個別の規範文を組み立てる入口群。どの規範を先に読むべきかを絞りたいときに読む。

## Read this when
- プレースホルダの型や、文字列と `Path` を混在させる置換対象の表現を確認したいとき。
- agent call に渡す完全なプロンプトの構成順、固定案内、静的・動的プロンプトの分け方、標準文の注入条件を見直したいとき。
- oracle/realization の基本定義や、各種標準・規則のどれを読むべきかを絞り込みたいとき。

## Do not read this when
- プロンプト本文の生成手順や置換ロジックの詳細だけを知りたいときは、実装側を読む。
- 個別の標準文そのものの内容だけを変えたいときは、対応する `parts` 側を直接読む。
- プレースホルダを使わない処理や、別の設定値の表現だけを確認したいときは、この下ではなく該当する別対象を読む。

## hash
- ec2c4a04062c9b5b62de4087e27684fbd4234fea8afd15f18dc2f912c233dd74
