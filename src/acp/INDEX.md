# `__init__.py`

## Summary
- `acp` 互換の公開入口を扱う。`acp.*` を利用している既存参照を、`oracle.*` または実体モジュールへ移す必要があるときに読む。

## Read this when
- `acp` という公開名を残すべきか、削除できるかを判断したいとき。
- 既存の利用者向け参照を壊さずに、`oracle` 側の実体へ切り替える導線を確認したいとき。

## Do not read this when
- `acp` 配下の具体的な実装内容や移行先の詳細を知りたいだけなら、直接その実体モジュールを読む。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変えたいだけならここではない。

## hash
- fe0939ab61e919bfb5ae35264e02859ee36efb102a15498d95fcbd45f9670e76

# `builder`

## Summary
- 対象ディレクトリは、ACP builder の realization 側入口をまとめる層です。既存の `acp.builder.*` import 互換を維持しつつ、apply・indexing・quota probe・review・session・TUI などの各領域を下位要素へ振り分けます。

## Read this when
- ACP builder の互換 import 経路、canonical/oracle builder への委譲、または下位 builder package の入口を確認するとき。
- 対象ディレクトリ直下の builder 機能の追加・変更・削除に伴い、どの下位要素へ進むべきか判断するとき。

## Do not read this when
- 個別 builder の詳細な prompt・schema・処理仕様を確認したいときは、該当する下位 package または oracle 側実装を直接読む。
- TUI の画面挙動、apply fork のループ制御、session の状態遷移など、builder 入口以外の責務を調べるときは対応する実装箇所へ直接進む。
- 対象ディレクトリに新たな通常ファイルがないかを確認するだけの場合は、本文ではなくディレクトリ構成を確認する。

## hash
- 73190804eb843eab784b4f8260f3e42ced60cbf2f93215b21b9721343b26dcd4
