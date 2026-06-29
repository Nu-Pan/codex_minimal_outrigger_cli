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
- ACP builder の realization implementation 領域で、agent call parameter 構築に関わる下位領域への入口になる。正本側実装を実行側 import 経路へ接続する互換境界を中心に、apply fork 用の呼び出しパラメータ構築、review 系 builder の再公開と一部補正、session join への入口、TUI 起動用パラメータ調整、indexing 関連の互換入口を束ねる。
- この領域では、正本側の prompt builder や builder 実装を再利用しながら、実行側 package から参照できる公開経路を用意する。実処理を持つ箇所と、正本側 API を薄く再公開するだけの箇所が混在するため、下位領域を選ぶための分岐点として扱う。

## Read this when
- agent を呼び出すための model、reasoning effort、file access mode、prompt、Structured Output schema などの ACP builder 実装または公開入口を探したいとき。
- apply fork、review、session、TUI、indexing のどの builder 領域へ進むべきかを切り分けたいとき。
- realization 側の package が、正本側 builder 実装や定義をどの import 経路で公開しているか確認したいとき。
- 正本側実装を再公開するだけの互換入口と、realization 側で追加の調整を行う builder 実装との境界を把握したいとき。
- TUI 起動時の ACP 調整、review advocate 検証時の prompt 表記補正、apply fork の各段階の呼び出しパラメータ構築など、実行側での接続・補正箇所を探したいとき。

## Do not read this when
- builder の正本仕様断片、prompt 断片、review standard、realization standard、path model など、人間所有の仕様本文そのものを確認したいとき。
- fork 作成、git 操作、作業ディレクトリ管理、レポート保存、CLI サブコマンドルーティングなど、builder が生成した ACP を使う側の実行制御を調べたいとき。
- TUI の画面描画、入力処理、イベントループなど、起動後の UI 本体の挙動を調べたいとき。
- finding の列挙・判定・結合・検証、indexing、session join などの具体的なアルゴリズムや正本側の入出力仕様を理解したいとき。
- 生成済みの変更要約、所見、レポートなど、agent call parameter 構築結果ではなく実行後データの内容だけを読みたいとき。
- model class、reasoning effort、file access mode、Structured Output schema などの共通定義自体を確認したいとき。

## hash
- 3994b17896fc58db5fd68a715ae543e6b446d39030d573991c3b52834a1f3dce
