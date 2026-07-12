# `__init__.py`

## Summary
- oracle src 側の acp builder 実装を複製せず、既存の `acp.*` import 参照を維持するための互換入口。実体は別 module 側に置き、この対象は移行期間中の公開 import 面を保つ役割に限定される。

## Read this when
- `acp.*` 参照を `oracle.*` または実体 module へ移行する作業で、互換入口を残す理由や削除条件を確認したいとき。
- realization 側または利用者向け公開面に残る `acp.*` import の扱いを判断したいとき。
- oracle src 由来の acp builder 互換 import がどこで維持されているかを確認したいとき。

## Do not read this when
- acp builder の実装内容や生成処理そのものを調べたいとき。この対象は実体を持たない互換入口なので、実装本体へ進む。
- 新しい acp 機能や API 仕様を追加する場所を探しているとき。この対象は互換維持専用であり、機能追加の入口ではない。
- `acp.*` 参照がすでに全公開面と realization 側から消えていることだけを確認済みで、互換入口の詳細を読む必要がないとき。

## hash
- 9376c267fa8194d94f175e9895f353889128d4ce8fff592333bfe1d50f96077f

# `builder`

## Summary
- `acp.builder` 配下の公開入口を束ねる上位ディレクトリ。個別の builder 実装を直接読む前に、どの下位パッケージへ進むかを選ぶためのルーティング地点として扱う。
- ここでは共通の builder 入口、互換公開面、サブパッケージ境界を確認する。実処理そのものは各下位モジュールに分かれる。

## Read this when
- `acp.builder.*` のどの領域へ進むべきか判断したいとき。
- 上位の builder 公開面と、下位の個別実装の境界を確認したいとき。
- 互換入口や共通 builder の有無を見て、読むべきサブパッケージを絞りたいとき。

## Do not read this when
- 個別の parameter builder、変換処理、実行ロジックの詳細を知りたいときは、対応する下位モジュールを読む。
- 特定の公開面だけを確認したいときは、この上位ディレクトリではなく該当サブパッケージを直接読む。
- `oracle` 側の正本仕様そのものを確認したいときは、この realization 側の入口ではなく oracle 側を読む。

## hash
- 26d4ed6063d73b90d7edc2a352566ccd83e00ba6d68480bdfdb039e2bd61f312
