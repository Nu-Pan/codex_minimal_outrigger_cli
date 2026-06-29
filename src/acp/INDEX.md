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
- ACP builder に関する realization 側の入口を束ねる領域。正本側 builder 実装への薄い互換入口と、apply・indexing・review・session・TUI 各領域への導線を持つ。
- 主な責務は、既存 import path を壊さず正本側実装へ接続すること、apply fork や review oracle などの下位 builder adapter へ進むための境界を示すこと、互換入口を残す理由と削除条件を確認できるようにすること。

## Read this when
- realization 側の ACP builder から、apply・indexing・review・session・TUI のどの下位領域へ進むべきか判断したいとき。
- 既存の acp.builder 系 import path が、正本側 builder 実装や同名 package 構造とどのように対応しているか確認したいとき。
- 互換入口を維持・削除・移動してよいか、残存参照や正本側への委譲境界を起点に調べたいとき。
- apply fork の agent call parameter 構築、review oracle 実行用 parameter 生成、TUI parameter 関連再公開など、builder adapter の所在を探し始めるとき。

## Do not read this when
- 正本側 builder の具体的な仕様、prompt 本文、structured output schema、モデル選択、file access mode などを確認したいとき。対応する oracle 側の本文を読む。
- apply fork や review oracle の具体的な関数・クラス・制御フローがすでに分かっているとき。該当する下位領域または実装本体へ直接進む。
- CLI コマンド全体の制御フロー、fork 作成、git 操作、引数処理、TUI 画面やイベント処理など、builder adapter 以外の実体を調べたいとき。
- AgentCallParameter 型、path model、基本列挙値などの共通定義そのものを確認したいとき。この領域はそれらの定義を所有しない。

## hash
- d947a0e831c8ed3bb5ad7fb5325eb27c4acbdce7c2e2fa2f3a510f139028d7f8
