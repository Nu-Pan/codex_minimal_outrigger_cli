# `__init__.py`

## Summary
- oracle src 側の acp 実装と互換の import 経路を提供するためのパッケージ入口。
- 実処理や公開 API の定義ではなく、acp 名前空間を import 対象として成立させるための最小の入口として位置づけられる。

## Read this when
- acp パッケージ自体の import 入口が必要か、または oracle src 互換の import 経路が存在するかを確認したいとき。
- acp 配下の実装を読む前に、パッケージ入口の責務が実処理ではなく互換 import の提供に限られていることを確認したいとき。

## Do not read this when
- acp の具体的な処理内容、データ構造、関数、クラスの挙動を調べたいとき。
- oracle src の仕様断片そのもの、または acp 以外の import 互換入口を調べたいとき。

## hash
- a4fa2404d751d07495abc462d628458a8e48984730fe92845a6644bfa89ef089

# `builder`

## Summary
- ACP builder の realization implementation 側入口であり、正本側 builder 実装を実行側の import 経路から利用するための互換 package 群を束ねる。
- この領域は builder 処理の正本実装そのものではなく、apply fork、review oracle、session join、TUI、indexing などの各 builder 領域へ進むための境界として位置づけられる。
- 多くの下位要素は oracle 側実体の再公開または薄い adapter であり、一部では実行時契約に合わせた最小限の補正や runtime 側 parameter への橋渡しを扱う。

## Read this when
- ACP builder 関連機能を realization implementation 側からどの import 経路で参照できるか確認したいとき。
- apply fork、review oracle、session join、TUI、indexing など、どの builder 領域へ進むべきかを切り分けたいとき。
- 正本側 builder 実装と realization 側 package 構造の対応関係や、互換入口・薄い adapter の有無を確認したいとき。
- repository root 解決、oracle src import 準備、runtime 側 AgentCallParameter への橋渡し、または実行時契約に合わせた小さな補正が builder 境界で行われるかを探しているとき。

## Do not read this when
- 各 builder の prompt 本文、Structured Output schema、model 設定、reasoning effort、file access mode などの正本仕様を確認したいとき。その場合は対応する oracle 側の仕様文書または実装を読む。
- builder の具体的な生成処理、変換ロジック、判定基準、データ構造、公開関数・クラスの詳細を理解したいとき。その場合は該当する下位の実装本体または委譲先を読む。
- apply fork 全体、review workflow、TUI 起動後の画面処理、session join の制御など、builder 境界より外側の orchestration や UI 本体を調べたいとき。
- path model、AgentCallParameter、基本 enum、repository root 解決そのものなど、builder から参照される基礎定義の意味を確認したいとき。

## hash
- 4b2f77a48d5d74f0d3eab7cf6c3066b886ed9492b74f35eb62736e9e5fea8b6a
