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
- agent call parameter builder 群の realization 側入口を扱う階層。主に oracle 側 builder を正本に保ちながら、旧来の acp.builder 系 import path を維持する互換 wrapper、再公開 package、薄い adapter を収める。
- apply、review、session、tui、indexing などの builder 領域について、canonical oracle 実装への接続、realization 側公開型への最小変換、互換入口の残存理由や削除条件を確認する起点になる。
- quota 回復確認用のように oracle 側 builder を持たない realization-only の最小 builder も含む。

## Read this when
- acp.builder.* の旧 import path 互換性、module alias、再公開入口、削除条件を確認したいとき。
- apply fork、review、session、TUI、indexing などの agent call parameter builder が oracle 側実装へどう接続されるかを調べるとき。
- oracle 側 builder の生成結果を realization 側公開型や既存 caller 向け import surface にどう適応しているか確認・変更したいとき。
- quota availability probe や quota 回復確認用の最小 agent call parameter builder を確認・変更したいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容などの正本仕様や人間意図を確認したい場合は、対応する oracle 側 builder を読む。
- apply fork、review、session、TUI など各機能全体の実行フロー、CLI 引数処理、状態操作、画面構成を調べたい場合は、それぞれの上位実装や呼び出し元を読む。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、path model、git helper などの共通型・共通処理そのものを調べたい場合は、該当する共通実装を読む。
- 新規機能の通常実装場所を探しているだけで、既存 import 互換や builder 入口に関係しない場合は、対象機能の実装階層へ直接進む。

## hash
- 845925685c57b83232fa0fbf4a31a8883694585c57ae1b80a871e1df3349a33d
