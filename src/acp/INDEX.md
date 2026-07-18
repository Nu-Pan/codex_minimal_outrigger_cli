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
- ACP builder の realization 側入口をまとめるパッケージ。canonical な oracle builder への委譲、既存 `acp.builder.*` import の互換維持、TUI・oracle review/edit・apply fork・session join・indexing・quota probe の parameter builder を扱う。各サブパッケージが機能別の実装入口となる。

## Read this when
- ACP parameter builder の realization 側入口、canonical builder への委譲、互換 import 経路を調査・変更するとき。
- TUI、oracle edit/review、apply fork、session join、indexing、quota probe のいずれかの builder を探すとき。

## Do not read this when
- canonical な builder の仕様や実装内容を確認したいときは、対応する `oracle.acp_builder` 側を読む。
- CLI のループ制御、state 遷移、TUI 起動後の処理など、builder parameter 構築以外の挙動を調査するときは、対応する上位実装を直接読む。

## hash
- 9639a6d764d311dcc41f5a792de4f2d6d06b0a51eaf952c750cdd70fe55365a5
