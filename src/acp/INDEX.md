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
- ACP builder の realization 側入口をまとめる階層。正本実装を oracle 側に置いたまま既存の公開 import path を維持する互換境界と、apply・review・session・TUI・indexing 各領域への委譲入口を扱う。
- この階層の主な役割は、旧来参照から正本側 builder 実装へ到達できるようにすること、および apply fork や review oracle、session join、TUI 起動パラメータ、indexing 互換公開面の下位領域へ進むための案内である。

## Read this when
- ACP builder の realization 側で、公開済み参照経路と oracle 側 builder 実装の対応関係を確認したいとき。
- apply・review・session・TUI・indexing のどの builder 領域へ進むべきかを、realization 側の入口から切り分けたいとき。
- 既存の builder import path を残す理由、正本側への委譲境界、互換入口の削除条件を確認したいとき。
- apply fork の agent call parameter 構築、review oracle 向け builder 再公開、session join 入口、TUI 起動パラメータ、indexing 互換公開面の所在を探しているとき。

## Do not read this when
- ACP builder の prompt 本文、出力 schema、モデル選択、file access mode、判定基準などの正本仕様を確認したいとき。対応する oracle 側の builder や JSON 定義を読む。
- apply fork、review oracle、session join、TUI、indexing の具体的な処理ロジックや入出力仕様をすでに特定しているとき。該当する下位領域または正本側実装へ直接進む。
- CLI コマンド全体の制御フロー、fork 作成、git 操作、画面描画、キー操作、状態管理など builder 以外の挙動を調べたいとき。
- AgentCallParameter 型、path model、model class、reasoning effort、file access mode enum など、builder 領域に限らない共通型や共通仕様そのものを調べたいとき。

## hash
- 919d783ca312c9e813bd57d97a75ff8b7d5410d3f184e2cbca45d466c877207d
