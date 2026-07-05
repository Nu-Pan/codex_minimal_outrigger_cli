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
- ACP builder 領域の入口。oracle 側 builder を正本として扱いながら、realization 側の既存 import 経路や公開型へ接続する互換層と、apply fork・quota probe・review・session・TUI など用途別の agent call parameter 構築入口をまとめる。
- 主な責務は、旧 import path の維持、canonical/oracle 実装への再 export、oracle builder 生成結果の最小適応、fallback や既知補正の境界管理であり、prompt 本文や各機能本体の実行処理そのものは扱わない。

## Read this when
- ACP builder 全体で、oracle 側実装を正本にしつつ realization 側の既存参照をどう成立させているかを確認したいとき。
- acp.builder 系の旧 import 経路、互換 package、再 export、module alias、canonical 実装への中継を調べたいとき。
- apply fork、quota probe、review、session、TUI 起動などの agent call parameter 構築入口を探しており、どの下位領域へ進むべきか判断したいとき。
- 既存 caller を canonical path へ移行する作業で、互換入口を残す理由、削除条件、公開面維持の範囲を確認したいとき。
- oracle builder の戻り値を realization 側公開型や runtime path に接続する境界、または既知 placeholder/typo 補正や fallback のような最小適応層を確認したいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいだけなら、対応する oracle 側 builder や oracle doc を読む。
- apply、review、session、TUI など各機能本体の実行フロー、UI、branch 操作、diff 生成、CLI 引数処理を調べたい場合は、それぞれの実装領域へ進む。
- AgentCallParameter、model class、reasoning effort、file access mode、path model、git helper などの基礎型や共通処理を確認したいだけなら、それらの定義元を読む。
- 個別 builder の具体的な変換処理、探索処理、データ構造、入出力仕様を確認したい場合は、その処理を持つ下位 module または canonical 実装を読む。
- 新しい公開 API や新規 import 経路を設計したいだけで、旧 import 互換や既存 caller 移行に関係しない場合は、公開面の定義元や対象機能の設計箇所を読む。

## hash
- 286ab0829950b9bc5a6b8739224eb651153b65c6557e4efa846b2367f5eae824
