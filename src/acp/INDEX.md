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
- Agent call parameter builder 群の実装側入口。正本側 builder を既存の公開参照経路から利用できるようにする互換 package 群と、quota availability probe 用の最小 parameter builder を含む。
- 主な責務は、旧来の import surface 維持、正本側実装への委譲、TUI resolve parameter schema など実行時入力に必要な限定的補正、apply・review・session・indexing・TUI 各 builder 領域へのルーティングである。
- この階層自体は多くの場合、処理本体や正本仕様ではなく互換境界であり、具体的な builder 実装・prompt・schema・制御ロジックは下位領域または正本側実装へ進むための入口として扱う。

## Read this when
- agent call parameter builder の実装側 package 構造と、正本側 builder への委譲関係を確認したいとき。
- 既存の公開参照経路や import surface が残っている理由、削除条件、canonical な正本側 path への移行可否を判断したいとき。
- apply fork、review oracle、session join、indexing、TUI 起動・resolve parameter などの builder 領域のうち、どの下位領域へ進むべきか見分けたいとき。
- Codex quota availability probe の agent call parameter が、通常設定から何を引き継ぎ、どの入力を固定するか確認・変更したいとき。
- 正本側 prompt や実装を保持したまま、realization 側で必要な互換再公開、placeholder 補正、runtime schema 差し替えの境界を確認したいとき。

## Do not read this when
- agent call parameter builder の正本 prompt、出力条件、schema、具体的な値の組み立て仕様を確認したいときは、対応する正本側実装または正本仕様断片を読む。
- apply fork コマンド全体の制御フロー、branch 操作、diff 生成、CLI 引数処理、状態管理を調べたいときは、コマンド実装や上位の apply fork 実装を読む。
- review finding の判定仕様、検出ロジック、統合ロジック、CLI 表示、テスト方針を調べたいときは、review の処理本体や正本側仕様を読む。
- TUI 画面描画、イベント処理、端末 UI の挙動、sandbox profile 生成、writable roots、cwd 選択など runtime 側の詳細を調べたいときは、TUI runtime や起動処理の実装を読む。
- indexing の生成処理、探索処理、データ構造、入出力仕様そのものを変更・確認したいときは、互換入口ではなく実体を持つ正本側実装を読む。

## hash
- d7c75dedac85c9cdedb8e1d9196e043ca2014103f635404c660664dfb679fe48
