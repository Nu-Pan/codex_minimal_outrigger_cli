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
- ACP builder 群の realization 側入口であり、oracle 側 builder を正本に保ちながら旧 import 経路を維持する互換層と、runtime 用の一部 builder をまとめる。
- apply、review、session、TUI、indexing などの builder 領域について、canonical oracle 実装への中継、realization 側公開型への適合、既存 caller 移行までの互換維持を扱う。
- quota availability probe のように通常実行ではなく runtime 制御のための最小 AgentCallParameter を組み立てる builder も含む。

## Read this when
- ACP builder の旧 import 経路が oracle 側 canonical 実装や互換入口へどう接続されるかを調べるとき。
- apply fork、review、session、TUI、indexing など、用途別の agent call parameter builder 入口や互換 package の読む先を選びたいとき。
- oracle 側 builder の戻り値を realization 側の公開型や runtime path に適合させる境界を確認または変更するとき。
- 既存 caller を canonical import path へ移行する作業で、互換入口を残す理由、公開面維持、削除条件を確認したいとき。
- quota waiting が使う Codex 呼び出し用の最小 AgentCallParameter 構成を調べたいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したい場合は、対応する oracle 側 builder や oracle file を読む。
- apply、review、session、TUI など各機能の実行フロー、UI、branch 操作、finding 処理など builder 以外の本体挙動を調べたい場合は、それぞれの実装領域へ進む。
- AgentCallParameter の公開型、path model、git helper、file access mode など共通基盤だけを調べたい場合は、それぞれの定義元を読む。
- 新しい公開 API や新規 import 経路を設計したいだけの場合は、互換維持層ではなく canonical な公開面や設計対象を読む。

## hash
- 5c1968a3bd20d62f94b7c8204d160cf4b4a68d53b0fdb400aeb9e61082ce511d
