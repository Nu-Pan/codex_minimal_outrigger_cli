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
- ACP builder 領域の realization implementation 側入口。正本側の ACP builder 実装や package 構造を、実行側の import 経路から利用できるようにする互換境界を中心に扱う。
- apply、review、session、indexing、TUI などの下位 builder 領域へ進むための入口であり、多くは正本側実装の再公開または薄い調整を担う。
- 実処理本体を持つ領域と、互換 package として正本側へ委譲するだけの領域が混在するため、どの builder 領域へ進むべきかを切り分ける案内点として位置づけられる。

## Read this when
- ACP builder 全体の realization 側 package 構成と、正本側 builder 実装への import 互換境界を把握したいとき。
- apply、review、session、indexing、TUI の各 builder 領域のうち、どの下位領域が目的に近いかを選びたいとき。
- agent 呼び出しパラメータ、prompt 構築、Structured Output schema、file access mode、model class などがどの builder 領域で扱われるかを大まかに切り分けたいとき。
- 正本側実装を realization implementation 側から再公開しているだけの領域と、実行時契約に合わせた薄い補正を行う領域の境界を確認したいとき。

## Do not read this when
- 個別 builder の具体的な生成処理、prompt 内容、判定ロジック、入出力仕様を調べたいとき。その場合は該当する下位領域または委譲先の正本側実装を読む。
- fork 作成、作業ディレクトリ管理、git 操作、CLI 入出力、レポート保存など、builder 呼び出し後の実行制御を調べたいとき。
- oracle file の正本仕様断片そのもの、review standard、path model、基本定義の意味を確認したいとき。該当する oracle 側の本文を読む。
- TUI の画面描画、入力処理、イベントループ、agent 応答の解釈・表示・永続化など、builder 以外の実処理を調べたいとき。

## hash
- f414b92a0ccc847f573423fdb890da9419132a336cf92c49efced08fc9185710
