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
- ACP builder 領域の realization 側入口。正本側 builder 実装への import 互換経路を提供する薄い公開境界を中心に、apply、indexing、review、session、TUI など用途別の下位領域へ分岐する。
- この階層は多くの場合、builder の実処理本体ではなく、正本側定義・生成結果・schema 連携を realization implementation 側から参照できる形に接続する場所である。
- 下位領域には、apply fork 用パラメータ生成と structured output schema 連携、indexing の互換入口、review finding 系 builder の再公開と一部 prompt 補正、session join への入口、TUI 起動パラメータの互換調整が含まれる。

## Read this when
- ACP builder 全体のうち、どの下位領域へ進むべきかを最初に切り分けたいとき。
- realization 側の builder package が正本側 builder 構造とどのように import 互換を保っているか確認したいとき。
- apply fork、indexing、review finding、session join、TUI 起動パラメータのいずれかに関わる builder の所在を探したいとき。
- builder 実装が独自処理を持つのか、正本側実装の再公開・包み直し・実行側契約への小さな補正なのかを見分けたいとき。

## Do not read this when
- 各 builder の具体的な生成アルゴリズム、prompt 構成、判定基準、入出力仕様を詳しく理解したいとき。その場合は対応する正本側実装や仕様断片を読む。
- CLI コマンド全体の制御フロー、git 操作、差分適用、TUI の画面描画やイベントループなど、builder 境界の外側の処理を調べたいとき。
- repo root 解決、path model、AgentCallParameter、enum、Structured Output schema そのものなど、共通基礎定義を確認したいとき。
- 互換 import 経路や realization 側 adapter の確認が不要で、実処理本体だけを変更したいとき。

## hash
- dd39ba0533c427921d57f5f568ac20d6d52c281f17eeee5a94d7757f84d08e6a
