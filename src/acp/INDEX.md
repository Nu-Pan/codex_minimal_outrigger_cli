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
- ACP builder の realization adapter と互換 import 入口を収めるディレクトリ。oracle.acp_builder の canonical builder を acp.builder 配下から再公開し、既存 caller の import 経路を維持する。
- feedback・indexing・oracle・quota probe・realization・session・TUI の用途別 builder 入口を含む。oracle edit／investigation の一部では、正本 builder の呼び出し前に runtime directory を準備する adapter も提供する。
- 個別 builder の prompt 仕様や本体ロジックではなく、互換公開、canonical 実装への委譲、realization からの接続を確認するための上位入口。

## Read this when
- acp.builder 配下の builder adapter 全体の構成、canonical な oracle.acp_builder への委譲関係、または既存 import 経路の維持・削除条件を確認するとき
- feedback issue の normalization／verification、index entry、quota availability probe、session join conflict resolution、TUI 起動の builder 入口を探すとき
- cmoc oracle edit／investigation／review または realization apply／refactor fork の builder adapter へ進む入口を確認するとき

## Do not read this when
- canonical builder の prompt 構築、入力検証、出力仕様、または具体的な処理ロジックを調査・変更するときは、対応する oracle.acp_builder 側の対象を直接読む
- acp.builder の builder を利用する CLI・realization・利用者向け公開面の挙動を調査するときは、各呼び出し元や利用側の対象を直接読む
- builder 共通の処理や、個別の edit・investigation・review・apply・refactor・session の詳細実装だけを確認したいときは、該当する下位対象へ直接進む

## hash
- db6081bf8fa7696d03ad0fe17c11fac169ef41814a13900670c7591aad25702b
