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
- ACP builder 領域の realization 側入口を束ねる階層。正本実装を oracle 側に置いたまま既存の公開 import path を維持する互換 package 群と、apply fork 向け agent call parameter 構築など一部 runtime 側 builder adapter への入口を扱う。
- 主な範囲は、apply、review、session、TUI、indexing などの builder 領域へのルーティングであり、多くは oracle 側実装や正本定義への薄い再公開・委譲境界として位置づけられる。
- この階層自体は各 builder の正本仕様や詳細アルゴリズムの置き場ではなく、realization implementation 側からどの互換入口・下位領域へ進むべきかを切り分けるための起点である。

## Read this when
- realization 側で ACP builder 関連の import path、互換 package、oracle 側実装への委譲境界を確認したいとき。
- apply、review、session、TUI、indexing のいずれの builder 領域へ進むべきか、上位から入口を判断したいとき。
- 正本実装が oracle 側にある機能について、既存の acp builder 系公開経路を残している理由や削除可否を確認したいとき。
- apply fork の変更要約・ファイル単位所見列挙・所見適用、review oracle 機能、session join、TUI パラメータ生成・解決、indexing 互換入口の所在を大まかに切り分けたいとき。

## Do not read this when
- 各 builder の prompt 本文、Structured Output schema、model 設定、reasoning effort、file access mode などの正本仕様を確認したいとき。その場合は oracle 側の対応する仕様文書または実装を読む。
- finding 列挙・判定・統合・検証、indexing 生成、session join、TUI パラメータ解決などの具体的な処理内容やアルゴリズムを理解したいとき。委譲先の oracle 側実装またはより直接の下位実装を読む。
- ACP builder ではなく、CLI コマンド全体の制御フロー、fork 作成、git 操作、引数処理、画面イベント処理、基本 enum・path model・runtime 型定義を調べたいとき。
- 互換 import 境界や公開経路の確認ではなく、新規機能の本体実装場所、利用者向け API 全体、またはテスト対象を探しているとき。

## hash
- e559e4f4130f61d45a3702620cd4db703895c40255e2611c84f1bc81bcef5f37
