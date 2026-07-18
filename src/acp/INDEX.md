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
- acp.builder の互換入口と builder 群をまとめる realization package。oracle builder への委譲を保ちながら、apply・indexing・oracle・session・tui など各用途の builder 入口と、quota probe の互換 fallback を提供する。

## Read this when
- acp.builder 配下の builder package 構成、互換 import 経路、canonical な oracle builder への委譲先を確認するとき
- apply、oracle、session、TUI、indexing、quota probe の builder 入口や parameter 構築を変更するとき

## Do not read this when
- 各 builder の canonical な正本仕様や実装詳細を確認するときは、対応する oracle 側または下位の直接対象を読む
- builder 以外の CLI 実装、TUI 本体、ループ制御や state 遷移を調査するとき

## hash
- ce3f9352c26195212dff470429bf5335334aea69b7f833699a7e23b1d7a3ed09
