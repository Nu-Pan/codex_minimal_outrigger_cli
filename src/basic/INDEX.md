# `__init__.py`

## Summary
- `basic.*` の互換 import を維持するための入口。実体の実装や正本型を複製せず、`basic` という公開面だけを残している。

## Read this when
- `basic.*` 参照を残す必要があるか、削除できるかを判断したいとき。
- 利用者向け公開面の移行先を確認したいとき。
- 互換 import の維持条件や廃止条件を確認したいとき。

## Do not read this when
- `basic.acp`、`basic.path_model`、`basic.struct_doc` の個別実装や再公開内容を確認したいときは、各モジュールを直接読む。
- ACP 基本型や path model の正本仕様そのものを確認したいときは、`basic` ではなく正本側を読む。

## hash
- 8a9d153c30f1ec0c568fd2702b1580077d56f027401c802ee1cca9b03f7b76bb

# `acp.py`

## Summary
- oracle 側で定義された ACP 型を realization 側から再公開する互換層。型定義自体は保持せず、既存の `basic.acp` 参照を維持するための入口である。

## Read this when
- ACP 型の import 経路、`basic.acp` 参照、または realization 側の公開面を変更・調査するとき
- oracle 側の ACP 型と realization 側の再公開関係を確認するとき

## Do not read this when
- ACP 型の正本定義や仕様を確認したいときは、直接 oracle 側の定義を読む
- ACP 型や `basic.acp` の参照経路に関係しない処理を変更・調査するとき

## hash
- b6c1a325e0018a7ea29e9f189cdea64a1bf8ad87c15afcbd45cd971c888337fb

# `path_model.py`

## Summary
- `oracle.other.path_model` の公開 path model をそのまま再公開する薄い中継層。`basic.path_model` を参照している利用者や、公開面を通じて path model を取り込む変更のときに読む。
- 中身の実装差ではなく、公開名の維持が目的なので、実体の生成方法や内部の path 変換ロジックを追う必要はない。

## Read this when
- `basic.path_model` 経由の公開名が必要なとき
- 再公開される `RootPathPlaceHolder` と path 解決関数の公開関係を確認したいとき
- `basic.path_model` を直接使う既存利用者の互換性を扱うとき

## Do not read this when
- path 解決の本体仕様や変換規則を確認したいときは、正本側の実装を見る
- `basic.path_model` を使わない新規コードの配置先を探しているだけなら、ここは読む必要がない
- 公開名の一覧だけを知りたい場合は、実体側や利用箇所を優先して読む

## hash
- 04ccbdd9d67b1290d840fdc1d4a8b3ff576ff7ddf0efee21717a188214d79784

# `struct_doc.py`

## Summary
- `oracle.other.struct_doc` の構造化文書 API を `basic` 側から再公開する入口。実装本体はここに置かず、既存の公開名を維持しながら利用者が `StructDoc` 系と `render_as_markdown` を引けるようにする。

## Read this when
- `basic.struct_doc` という公開名で構造化文書の型やレンダラを使う先を探しているとき。
- `basic` 側の公開 API から、構造化文書の実体がどこから供給されるかを確認したいとき。

## Do not read this when
- 構造化文書のレンダリング規則や型の制約そのものを知りたいときは、再公開先ではなく `oracle.other.struct_doc` を読む。
- `basic.struct_doc` を残す必要性や削除条件を確認したいだけなら、この入口ではなく参照元の利用箇所を読む。

## hash
- 0397791c0dc37c51edd489ea3dd01470322afc79499e4a5ddf069f9785bd13f9
