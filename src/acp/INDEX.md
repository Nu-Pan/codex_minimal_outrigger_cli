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
- ACP builder の realization adapter と互換 import 入口をまとめるパッケージ。`oracle.acp_builder` の canonical builder を `acp.builder` 配下から再公開し、既存 caller の参照経路を維持する。
- 配下には feedback、indexing、oracle command、realization、session、TUI、quota probe、および共通 builder 関連の入口があり、個別 builder の adapter 構成や canonical 実装への委譲関係を確認するための上位入口となる。
- oracle edit・investigation の TUI builder adapter では repository path と editor input directory の準備を行い、それ以外の多くの builder は正本関数を互換経路から再公開する。

## Read this when
- ACP builder 全体の adapter 構成、互換 import 方針、canonical `oracle.acp_builder` への委譲関係を確認するとき。
- feedback issue、index entry、quota probe、session join、TUI 起動、oracle command、realization apply/refactor の builder 入口を特定するとき。
- 特定の下位 builder を読む前に、その機能が互換 adapter、realization adapter、または oracle command adapter のどの領域に属するかを判断するとき。

## Do not read this when
- 特定 builder の具体的な prompt、入力検証、出力仕様、または処理ロジックを確認するときは、対応する canonical oracle 実装や下位ファイルを直接読む。
- builder の利用箇所、CLI command の業務ロジック、または利用者向け公開面を調査するときは、各参照元や CLI 実装を直接読む。
- 共通 prompt 整形や review finding 処理など、配下にある特定領域の詳細だけを調べる場合は、この上位入口から総当たりせず該当する下位対象へ進む。

## hash
- 204b79bcea13ed3fd218a6010e30b529da65c3fad9848c5589f0ad04d5d4bd37
