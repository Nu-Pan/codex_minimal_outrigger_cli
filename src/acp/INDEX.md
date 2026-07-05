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
- ACP builder 領域全体の入口で、oracle 側 builder を正本に保ちながら既存の acp.builder 系 import 経路を維持する互換層をまとめる。
- apply、review、session、tui など個別 builder 領域へのルーティングと、旧公開名前空間から canonical oracle 実装または realization 側適応層へ接続する境界を確認する起点になる。
- 実際の prompt、parameter 構築仕様、finding 処理、TUI 本体挙動などはここではなく、対象ごとの oracle 実装または個別 module に委ねる。

## Read this when
- acp.builder 配下の旧 import path 互換が、oracle 側 canonical 実装や realization 側 wrapper へどう接続されるかを俯瞰したいとき。
- apply fork、review、session、tui、quota probe、indexing などの builder 互換入口のうち、どの下位領域を読むべきか判断したいとき。
- oracle src を正本に保ちつつ realization 側で path 接続、module alias、返却型適応、最小補正を行う境界を確認したいとき。
- acp.builder 系の互換 package や再公開 module を削除または移行する作業で、残す理由や削除条件を調べ始めるとき。

## Do not read this when
- oracle 側 builder の正本仕様、prompt 本文、parameter 生成内容を確認したいだけなら、対応する oracle 側 builder を直接読む。
- apply、review、session、TUI など各機能の実行フローや本体挙動を調べたい場合は、それぞれの実装領域へ進む。
- AgentCallParameter 型、path model、git helper、file access mode など ACP builder 以外の共通基盤を確認したい場合は、その定義元を読む。
- 特定の変換処理、wrapper の詳細挙動、既知 typo 補正、runtime path 接続などを変更する場合は、該当する個別 module または下位 package を読む。

## hash
- e6655cc76801aede8a22b3b91dd714f3c3b1c2146b66314cdf4a8b2d8b18b1ad
