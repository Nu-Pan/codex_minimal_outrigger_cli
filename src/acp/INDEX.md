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
- ACP builder 群の realization 側における互換入口をまとめる領域。正本側に置かれた builder 実装を既存の公開参照経路から利用できるようにし、薄い package 境界・再公開・委譲・一部の適合処理を担う。
- 扱う範囲は、変更要約や所見処理、インデックス生成関連、レビュー用所見処理、セッション結合、TUI 起動・解決パラメータなどの AgentCallParameter 構築入口である。実処理や正本仕様の本体ではなく、正本側 builder へ進むための realization 側接続点として位置づく。
- 互換入口を残す理由、正本側 package 構造との対応、既存 import path の維持、正本側戻り値を realization 側型として扱う境界、削除可能条件を確認するための上位入口になる。

## Read this when
- ACP builder の realization 側で、既存の公開参照経路が正本側 builder 実装へどのように接続されているか把握したいとき。
- 変更要約、ファイル単位所見、所見適用、インデックス関連、レビュー用 finding 処理、セッション結合、TUI 用パラメータ生成のうち、どの下位領域へ進むべきか選びたいとき。
- 正本側へ実装を集約しつつ、既存利用者や残存参照を壊さないための互換 package、再公開、委譲境界を確認したいとき。
- oracle 側 builder を通常 import できない配置での import path fallback、正本側生成結果への realization 側適合、または prompt 内の oracle root 表記補正など、realization 側の薄い補正境界の所在を探したいとき。
- 互換入口を削除・移動・置換してよいか、残存参照や利用者向け公開面との関係から判断したいとき。

## Do not read this when
- AgentCallParameter builder の正本仕様、プロンプト内容、出力条件、型定義、モデル選択、reasoning effort、file access mode の意味そのものを確認したいとき。対応する正本側本文または基本定義を読む。
- 各 builder の具体的な生成処理、探索処理、判定条件、データ構造、入出力変換、検証規則を調べたいとき。互換入口ではなく処理本体または正本側実装を読む。
- ACP builder 以外の CLI 制御、fork 適用、git 操作、作業レポート生成、TUI 表示・イベント処理・対話フローを調べたいとき。該当する機能本体の領域を読む。
- 新規機能の実装場所やテスト対象を探しているだけで、既存公開参照経路の維持、正本側への委譲、互換層の削除条件に関心がないとき。

## hash
- 8fdac0ac0aaa17e13c185bd22ab3452995dd35c13b41e46dd1924630a800ca04
