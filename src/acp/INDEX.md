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
- acp builder 配下の realization 側互換入口を束ねるディレクトリ。oracle 側 canonical builder を正本に保ちながら、旧 acp.builder 系 import path、module alias、薄い wrapper、正本側欠落時の限定 fallback を扱う。
- apply、review、session、tui、indexing、quota probe などの agent call parameter builder について、既存参照を oracle 側実装へ中継し、realization 側公開型への適応や互換削除条件を確認する入口になる。

## Read this when
- acp.builder.* の旧 import 互換性、再公開 module、module alias、package path 接続を確認したいとき。
- agent call parameter builder が oracle 側 canonical 実装をどう呼び出し、必要に応じて realization 側公開型や既存公開名へどう適応するかを調べるとき。
- apply、review、session、tui、indexing、quota probe の builder 互換層を残す理由や削除条件を確認したいとき。
- 正本側 builder 欠落時の quota probe fallback など、この階層に限った一時的な互換実装の所在を探すとき。

## Do not read this when
- 各 builder の正本仕様、prompt、parameter 生成内容、人間意図を確認したい場合は、対応する oracle 側 canonical 実装や oracle file を読む。
- cmoc apply fork、review、session、TUI など各機能全体の実行フロー、CLI 引数処理、runtime path、git 操作を調べたい場合は、それぞれの上位実装や呼び出し元を読む。
- AgentCallParameter の公開型、汎用 git helper、path model、quota 管理、INDEX.md 生成仕様など builder 互換入口以外の共通概念を調べたいだけの場合。
- 新規機能の通常実装場所を探しており、既存 acp.builder import surface の維持や移行に関係しない場合。

## hash
- 21f1e423075dab393715a7f463f99193ee7bfc44251267059c8fccfa8f4ab13d
