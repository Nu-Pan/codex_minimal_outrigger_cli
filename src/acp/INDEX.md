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
- ACP builder の realization adapter と互換入口をまとめるパッケージ。canonical な oracle builder を再公開し、既存 import 経路を維持する。
- 動的 prompt section の Markdown code fence 保護、feedback・index・session・quota probe の互換 adapter、realization apply/refactor と oracle edit/investigation/review の builder 接続を下位要素へ案内する入口。

## Read this when
- ACP builder の adapter 配置、canonical oracle builder への委譲、既存 `acp.builder.*` import 経路を調査するとき
- 動的な diff・JSON・finding・対象本文を prompt に埋め込む際の code fence 保護の実装箇所を探すとき
- realization apply/refactor または oracle edit/investigation/review の builder adapter の下位実装へ進むとき
- feedback・index・session・quota probe の互換入口や optional builder fallback の責務を確認するとき

## Do not read this when
- canonical oracle builder の prompt 内容、Structured Output schema、判定基準を確認するときは対応する oracle 側の実装や仕様を直接読む
- ACP builder の利用箇所や利用者向け公開面を調査するときは各呼び出し元・公開面を直接読む
- builder と無関係な ACP 実行処理、realization 本体、TUI 起動処理そのものを調査するときは対応する実装へ直接進む

## hash
- 7ca5d1d61f975b2e7ffe24aecde2a730d81ade65b6743aa2eaba9fdf203958d0
