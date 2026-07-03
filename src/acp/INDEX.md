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
- ACP builder 関連の realization 実装をまとめる領域。oracle 側 builder を正本として参照しながら、既存の acp.builder 系 import 経路を維持する互換入口と、quota probe や TUI 起動など一部の realization 側 builder を扱う。
- apply、review、session、indexing、tui などの用途別 builder package への入口になり、canonical oracle 実装への委譲、旧公開名の維持、realization 側公開型への最小適応が必要な箇所を切り分ける。

## Read this when
- acp.builder 配下の旧 import path 互換が、oracle 側 canonical 実装や realization 側 wrapper にどう接続されるかを調べたいとき。
- apply fork、review、session、indexing、TUI、quota probe など、用途別 ACP builder の入口や読むべき下位領域を選びたいとき。
- oracle 側 builder を正本に保ちながら realization 側で package path、module alias、戻り値変換、既知表記補正を行う境界を確認したいとき。
- 既存 caller を canonical import path へ移行する作業で、互換 package や再公開 module の削除条件を確認したいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したい場合は、対応する oracle 側 builder や oracle doc を読む。
- apply、review、session、TUI など各機能の実行フロー、CLI 引数処理、UI 処理、branch 操作、finding 処理を調べたい場合は、それぞれの機能実装へ進む。
- AgentCallParameter の公開型、path model、git helper、file access mode など builder 共通外の基礎構造を調べたい場合は、該当する共通実装を読む。
- 新しい公開 API や新規 import 経路を設計したいだけの場合は、互換入口ではなく canonical な定義元や設計対象を読む。

## hash
- d73a20e3637bd8206627a39c4b2c8e380367afd26573f7b9a8216aaf9a0bc30f
