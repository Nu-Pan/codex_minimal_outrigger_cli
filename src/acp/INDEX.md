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
- ACP builder の互換入口をまとめるパッケージ。oracle 実装を `acp.builder` 配下から再公開し、既存の builder import 経路を維持する。共通の code fence 補正、indexing・oracle・realization・session・TUI adapter、quota probe fallback への入口を含む。

## Read this when
- `acp.builder` 配下の互換 package 構成や、既存 import 経路から canonical 実装へ接続する責務を確認するとき。
- ACP builder の共通 prompt 境界補正、indexing・oracle・realization・session・TUI adapter、または quota probe の互換入口を調査・変更するとき。

## Do not read this when
- canonical な oracle builder 実装や正本仕様を変更・調査するときは、対応する oracle 側の対象を直接読む。
- 個別 adapter の実装詳細を確認するときは、該当する下位ディレクトリまたはファイルを直接読む。
- builder の利用箇所、TUI 本体、CLI、fork 処理など、`acp.builder` の互換入口自体に関係しない処理を調査するとき。

## hash
- bf73347b67314c4562a375173d8bb34d2826e1aba84e38fb5d448f698ed0f061
