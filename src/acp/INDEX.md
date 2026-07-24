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
- ACP builder の互換入口と各種 builder adapter をまとめるパッケージ。oracle 実装への委譲、prompt の code fence 補正、oracle・realization・TUI・session・indexing 関連の互換 import 経路、quota probe の fallback を扱う下位要素への入口となる。

## Read this when
- acp.builder 配下の builder 互換層全体の構成や、どの下位パッケージ・モジュールへ進むべきかを確認するとき。
- canonical な oracle builder と既存の acp.builder.* import 経路の接続、互換層の整理条件を調査するとき。
- ACP builder 共通の prompt 境界補正、quota probe、oracle・realization・TUI・session・indexing builder の入口を横断して確認するとき。

## Do not read this when
- 個別 builder の具体的な生成ロジックや挙動を変更・調査するときは、対応する下位パッケージまたはモジュールを直接読む。
- canonical な oracle 実装や正本 prompt 仕様を確認するときは、oracle 側の対象を直接読む。
- ACP builder を利用する CLI、TUI、その他の呼び出し元の公開面を調査するときは、各利用箇所を直接読む。

## hash
- 3d013770d0176712c97ac8e8dec4f29ccf78fb96229595dd0b4ff0c38ddbbf4b
