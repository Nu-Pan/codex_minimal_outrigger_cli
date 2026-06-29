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
- ACP の agent call parameter builder 群への realization 側入口をまとめる階層。多くは oracle 側にある正本 builder 実装への互換 import 境界や薄い再公開層であり、既存の公開参照経路を維持しながら apply、indexing、review、session、TUI、quota probe などの builder 領域へ分岐する。
- この階層自体は各 builder の正本仕様や詳細な組み立てロジックを担う場所ではなく、realization 側から oracle 側 builder を利用するための互換 package 構造、委譲境界、削除条件、最小 wrapper の所在を見分けるための入口である。

## Read this when
- ACP builder の公開 import path や旧参照経路が、oracle 側の正本実装へどのように接続されているか確認したいとき。
- apply、indexing、review、session、TUI、quota probe など、agent call parameter builder の領域分担を上位から把握し、次に読む下位領域を選びたいとき。
- realization 側に残る互換入口、再公開層、最小 wrapper を残す理由や削除条件を確認したいとき。
- 正本側 builder への委譲、公開面の維持、prompt 表記補正、realization 側 parameter 型への適合など、builder 周辺の互換境界を調べる入口を探しているとき。

## Do not read this when
- 各 agent call parameter builder の具体的な prompt、parameter 組み立て、repo root 解決、型変換、検証ロジックを直接確認したいときは、該当する下位領域または oracle 側の正本実装を読む。
- apply fork、review、session、TUI などのコマンド全体の制御フロー、UI 処理、状態管理、branch 操作、diff 生成、CLI 引数処理を調べたいときは、それぞれの実処理を担う実装領域へ進む。
- AgentCallParameter、FileAccessMode、model、reasoning、file access、structured output schema などの共通型や基礎定義を確認したいときは、基本モジュールを読む。
- 互換 import 境界や builder 入口ではなく、正本仕様断片そのもの、または新規機能の実装場所やテスト対象を探しているときは、該当する oracle 側本文、実装本体、またはテスト領域を読む。

## hash
- 5329091959e2c2c0b06f0ba6ec00d4d8266f84ac67cecf414e426289679c0a1d
