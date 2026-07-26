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
- ACP builder の realization adapter と互換入口をまとめたディレクトリ。canonical な oracle builder への接続、Markdown code fence 補正、index・session・TUI・quota probe・realization・oracle command builder の各 adapter を扱う。下位要素から用途別の互換入口や builder adapter の実装へ進める。

## Read this when
- acp.builder 配下の互換 import 経路、canonical oracle 実装との接続、または builder adapter 全体の構成を調査・変更するとき。
- index、session、TUI、quota probe、realization、oracle command builder の parameter・prompt・fork 連携を確認するとき。
- 動的 Markdown code fence の補正や prompt 内での保護処理の入口を探すとき。

## Do not read this when
- canonical な oracle builder の仕様・実装や具体的な prompt 内容を確認するときは、oracle 側の対象を直接読む。
- TUI の画面構成、workload の処理本体、または builder adapter の利用箇所だけを調査するときは、対応する実装・参照元を直接読む。
- レビュー用の生成キャッシュだけを調査するときは、対応するキャッシュ対象を直接読む。

## hash
- 16998dfb32ed797374b6542d993442644c2550c55d125966b0cd10e74d1ae805
