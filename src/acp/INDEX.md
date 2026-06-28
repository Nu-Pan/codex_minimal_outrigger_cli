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
- ACP builder の realization implementation を束ねる領域。正本側 builder 実装への互換 import 境界を中心に、apply、indexing、review、session、TUI など用途別 builder 領域へ進むための入口になる。
- この階層の多くは処理本体ではなく oracle 側実装や正本側 package 構造を src 側の import 経路から参照できるようにする薄い公開境界であり、一部の下位領域では agent call parameter 構築や TUI 用候補値の接続も扱う。

## Read this when
- ACP builder まわりで、src 側の package 構成が oracle 側 builder 名前空間や正本側実装とどう対応しているかを把握したいとき。
- apply、indexing、review、session、TUI のどの builder 領域へ進むべきかを切り分けたいとき。
- builder 関連の import 互換入口、再エクスポート境界、公開 package の有無を確認したいとき。
- apply fork の agent call parameter 構築、review finding 入口、session join 入口、TUI 起動・パラメータ解決入口など、builder 用途別の入口を探したいとき。

## Do not read this when
- builder の具体的な生成処理、prompt 構成、判定ロジック、データ構造、入出力仕様を直接調べたいとき。その場合は下位の該当領域または正本側実装を読む。
- oracle 側の正本仕様断片、prompt、review standard、realization standard、path model、基本定義そのものを確認したいとき。
- apply fork 全体の実行制御、git 操作、作業ディレクトリ管理、レポート保存など、agent call parameter 構築以外の処理を調べたいとき。
- ACP builder 以外の CLI ルーティング、公開 API、テスト、または生成済み成果物の内容を探しているとき。

## hash
- e218865cb3af55057423a53f2a3dcbb8f8a46c3ae6dde049efb5d73efec01b1a
