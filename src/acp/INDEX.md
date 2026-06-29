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
- ACP builder 領域の realization 側公開入口を束ねる階層。正本側実装を既存の import 経路から利用できるようにする互換境界を中心に、apply fork、review oracle、session join、TUI パラメータ、indexing 関連の下位入口へ進むための案内を担う。
- この階層の主な役割は builder 本体仕様や処理本体を所有することではなく、oracle 側に置かれた正本実装との対応関係、既存参照経路の維持、互換入口の削除可否、下位領域への委譲境界を確認するための入口になること。

## Read this when
- ACP builder の realization 側 import path が、oracle 側の builder 実装や正本 package 構造へどのように接続されているか確認したいとき。
- 既存の ACP builder 公開入口や互換 package を削除・移動・置換してよいか判断するために、残す理由や削除条件を確認したいとき。
- apply fork、review oracle、session join、TUI パラメータ、indexing のいずれかに関する builder 入口の所在を、この階層から切り分けたいとき。
- realization 側が独自処理を持つ箇所と、oracle 側 builder へ薄く委譲または再公開しているだけの箇所を区別したいとき。

## Do not read this when
- ACP builder の prompt 本文、structured output schema、モデル選択、file access mode などの正本仕様を確認したいとき。対応する oracle 側の本文を読む。
- apply、review、session、TUI、indexing の具体的な処理内容や判定基準、入出力仕様を調べたいとき。互換入口ではなく、委譲先の正本実装またはより直接の下位実装へ進む。
- CLI 全体の制御フロー、fork 作成、git 操作、状態管理、共通型定義、path model などを調べたいとき。この階層はそれらの責務を所有しない。
- 新規機能の実装場所やテスト対象を探しており、既存 import path 互換や oracle 側への接続関係が主題ではないとき。

## hash
- d76a837643de314a4b49b67f51757cdd04b9b17494549d139181bc2de376475f
