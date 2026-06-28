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
- ACP builder 全体の realization 側入口をまとめる領域。apply、indexing、review、session、tui などの下位 builder 領域へ進むための分岐点であり、正本側 package 構造との import 経路互換や再エクスポート境界を扱う。
- この階層自体は多くの具体的な生成処理を直接持つ場所ではなく、正本側実装または下位領域へ到達するための薄い公開入口として位置づけられる。

## Read this when
- ACP builder のどの下位領域を読むべきか、apply、indexing、review、session、tui の入口を切り分けたいとき。
- src 側の ACP builder package が、正本側 builder package とどのように対応し、互換 import 経路を保っているか確認したいとき。
- agent call parameter builder 群のうち、apply 作業、indexing、review、session join、TUI のどこへ進むべきかを判断したいとき。
- 正本側実装を runtime import しない realization 実装境界と、正本側実装を再公開する互換 shim の境界を見分けたいとき。

## Do not read this when
- apply、indexing、review、session、tui の具体的な処理、関数、クラス、prompt、schema、制御フローを調べたいとき。その場合は該当する下位領域または正本側実装を読む。
- fork 作成、branch 操作、commit 操作、作業ディレクトリ管理、レポート保存など、ACP builder の外側にある実行制御や git 副作用を追いたいとき。
- oracle file、realization file、path model、work-root、run-root などの基本概念そのものを確認したいとき。
- 正本仕様断片そのもの、または oracle 側の文書・実装・テストを根拠として読むべき作業をしているとき。

## hash
- 402c8a7da54531c900ba821494c18280060733c22b702b9b244b7fe10de0e6a2
