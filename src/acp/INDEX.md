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
- ACP builder の realization 側公開面をまとめる階層。正本側にある builder 実装への薄い互換入口、再公開、委譲、暫定 adapter を配置し、既存の参照経路を維持する役割を持つ。
- 実処理の本体や正本仕様を置く場所ではなく、apply fork、indexing、review、session、TUI、quota probe などの agent call parameter 構築経路について、realization 側から正本側または暫定実装へ進むための入口になる。
- 多くの下位要素は、正本側実装との対応関係、既存 import path を残す理由、互換層を削除できる条件を確認するための案内点として位置づけられる。

## Read this when
- ACP builder の realization 側に残る公開 import path や互換入口が、正本側 builder 実装へどのように接続されているか確認したいとき。
- agent call parameter builder のうち、apply fork、review oracle、session join、TUI 起動・resolve、indexing 公開面、quota availability probe のどの下位領域へ進むべきか切り分けたいとき。
- 正本側へ実装を集約した後も既存参照を壊さないために残された再公開・委譲・adapter の理由や削除条件を確認したいとき。
- oracle package を通常 import できない配置での fallback、正本側戻り値を realization 側型として扱う適合、prompt 内表記の一時補正、probe prompt の runtime 外出しなど、互換境界に関わる処理の所在を探したいとき。

## Do not read this when
- ACP builder の正本仕様、prompt 内容、structured output schema、AgentCallParameter の本来の組み立て規則を確認したいとき。正本側の対応する builder 実装や仕様文書を読む。
- 個別の生成処理、探索処理、状態管理、UI 表示、CLI 制御、git 操作、fork 適用処理など、agent call parameter 構築入口を越えた実処理を調べたいとき。
- AgentCallParameter、FileAccessMode、model class、reasoning effort、repo root 解決などの共通型や基本仕様を確認したいとき。定義元の基本モジュールや正本側本文を読む。
- 新しい builder ロジックや正本仕様を追加・変更したいとき。互換層ではなく、実体を持つ正本側または該当する処理本体へ進む。

## hash
- 359718fc6ed3b1c1e0d43b653f151a5c07aa84acaf02274f0d176710f72b510e
