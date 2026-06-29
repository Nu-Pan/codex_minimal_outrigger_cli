# `__init__.py`

## Summary
- oracle.acp_builder を既存の acp.builder 参照から利用できるようにするための互換入口。正本実装を oracle 側に置いたまま、公開済み参照経路を維持する役割を持つ。
- 互換維持のためだけに残される薄い入口であり、削除条件は realization 側と利用者向け公開面の双方から acp.builder.* 参照がなくなること。

## Read this when
- acp.builder.* 参照が残っている理由や、oracle.acp_builder との互換関係を確認したいとき。
- acp.builder 系の公開入口を削除・移動・置換してよいか判断したいとき。
- realization 側の互換コードについて、残す理由と削除条件を確認したいとき。

## Do not read this when
- oracle.acp_builder の具体的な実装内容や builder の本体仕様を調べたいとき。
- acp.builder.* 以外の ACP 関連モジュールの責務や挙動を調べたいとき。
- 互換入口ではなく、新規機能の実装場所やテスト対象を探しているとき。

## hash
- bce540ff289ae7f7f8c83e9796e27376d4c6313646e45756110fa755ab94158c

# `apply`

## Summary
- apply 系の agent call parameter builder への入口となる領域。package 初期化要素と、fork 適用で使う builder 群への下位入口を含み、実処理は主に下位の個別 builder 領域に委ねる。
- realization 側から oracle 側 builder を利用するための互換 package として位置づけられ、apply 系の処理準備を調べる際に、まず package 構造と下位領域の分担を見分けるための階層である。

## Read this when
- apply 系の agent call parameter builder がどの下位領域に分かれているかを確認したいとき。
- apply builder 領域が oracle 側の package 構造に対応する互換 packageとして置かれているか確認したいとき。
- fork 適用に関する agent 呼び出し準備、oracle builder への委譲、realization 側 parameter 型への適合を調べる入口を探しているとき。
- 変更要約、ファイル単位所見列挙、所見適用など、apply fork の個別 agent 呼び出し準備へ進む前に上位の配置を確認したいとき。

## Do not read this when
- apply fork の具体的な builder 実装や repo root 解決、oracle import 経路補正、parameter 型変換を直接調べたいときは、下位の fork 用 builder 領域へ進む。
- apply fork コマンド全体の制御フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理を調べたいときは、コマンド実装や上位の apply fork 実装へ進む。
- agent prompt、出力条件、変更要約や所見処理の正本仕様を確認したいときは、委譲先の oracle 側 builder または正本仕様断片を読む。
- package 初期化の互換性メモだけで十分な場合を除き、この階層自体には公開 API や具体的な適用ロジックの定義を期待しない。

## hash
- 701ec977b0f06fbfb6f6a79d4e93b731b69f1160c2dc4895c4de00ac87f32c96

# `indexing`

## Summary
- 正本側に置かれた indexing 関連実装を、既存の公開参照から到達できるようにする互換入口をまとめる領域。実処理や仕様本体ではなく、旧来の import 経路を壊さないための薄い再公開境界を担う。
- 互換コードを残す理由、正本側実装との対応、削除できる条件を確認するための入口であり、indexing の生成処理・探索処理・データ構造そのものはこの領域の責務ではない。

## Read this when
- 旧来の公開名や import 経路が、正本側の indexing 実装へどのように接続されているか確認したいとき。
- 正本側へ実装を集約しつつ、既存利用者や残存参照を壊さないための互換公開面を確認したいとき。
- 互換入口を残す理由、削除条件、残存参照の有無に関わる変更を検討しているとき。
- 公開参照の維持または廃止に伴い、再公開先の正本側実装との対応関係を確認したいとき。

## Do not read this when
- indexing の具体的な生成処理、探索処理、データ構造、入出力仕様を確認したいとき。実体を持つ正本側実装を読む。
- インデックスエントリーの型・関数・挙動そのものを確認したいとき。再公開先の正本側実装を読む。
- 新しい indexing 機能を追加または変更したいとき。互換入口ではなく処理本体の実装側を読む。
- 互換参照の削除条件や再公開先ではなく、正本仕様全体を確認したいとき。該当する正本側の本文を読む。

## hash
- 0ab736b2c29b4ef0eadf9408768a9f99642c5d3d95caecb6c4def825217c487a

# `quota_probe.py`

## Summary
- quota availability probe のために、既存の agent call parameter から probe 用の ACP を組み立てる小さな builder。model class、reasoning effort、file access mode は元の値を引き継ぎ、自然言語 prompt を持たない空 stdin の probe に限定して stdin と追加入力を空扱いにする。
- 現行 oracle src に同用途の builder が存在しないための adapter であり、同用途の oracle 側 builder が追加されたら削除する前提を docstring に持つ。

## Read this when
- quota availability probe 実行時に渡す agent call parameter の組み立て内容を確認または変更したいとき。
- probe では base parameter のどの項目を引き継ぎ、どの項目を空にするかを確認したいとき。
- 自然言語 prompt を持たない空 stdin の probe という制約、またはこの adapter の削除条件を確認したいとき。

## Do not read this when
- 通常の prompt 付き Codex 実行や、一般的な ACP builder の仕様・実装を探しているとき。
- quota availability の判定ロジック、実行結果の解釈、または quota 不足時の制御フローを確認したいとき。
- oracle 側の正本仕様や prompt 標準そのものを確認したいとき。

## hash
- 8c4351eae4b30619b8338cc6c2cbc0170b8f28574ca95d18c8a81cb1bbc2e49d

# `review`

## Summary
- review builder 領域の realization 側 package で、正本側 review oracle builder との互換 import 境界と、旧経路から正本側実装へ委譲する薄い入口を扱う。
- review finding の列挙・判定・challenger validation は実装本体ではなく再公開層として置かれ、merge finding と finding advocate validation では正本側 builder の生成結果を保ちながら prompt 内の oracle root 表記だけを補正する。

## Read this when
- review builder 領域で、正本側 review oracle builder に対応する realization 側 package や旧 import 経路の互換境界を確認したいとき。
- review oracle builder 周辺の処理が、この領域の実装本体なのか、正本側実装への委譲または最小 wrapper なのかを切り分けたいとき。
- review oracle merge finding や finding advocate validation の AgentCallParameter 生成で、正本側 builder への委譲と prompt 内 oracle root 表記補正の有無を確認したいとき。
- package としての互換性や import 経路の成立だけを確認したいとき。

## Do not read this when
- review finding の列挙・判定・検証そのものの正本仕様、出力内容、検出ロジック、評価ロジックを調べたいとき。
- AgentCallParameter の共通型、model、reasoning、file access、structured output schema などの基礎定義を調べたいとき。
- review oracle 以外の builder、CLI 表示、テスト方針、または互換 import と prompt 表記補正に関係しない review 機能全般を調べたいとき。
- review builder の新しい判定ロジックや検証処理を追加・変更する実装本体を探しているとき。

## hash
- b5982b09e4ce2166f96a96ee67c2e95418af42cdfc1006f94bbe53b9ce6eef84

# `session`

## Summary
- ACP builder の session 領域で、oracle 側と同じ package 構造を実装側に成立させるための互換入口を扱う階層。
- この階層自体は session builder の実処理を担う場所ではなく、実体を持たない package 初期化と、session join 配下の互換境界へ進むための入口として位置づけられる。

## Read this when
- ACP builder の session 領域が oracle 側の package 構造とどう対応しているかを確認したいとき。
- session 領域が import 可能な package として存在する理由を確認したいとき。
- session join 配下へ進む前に、この領域が実処理ではなく互換 package 境界を扱う場所かどうかを見分けたいとき。

## Do not read this when
- session builder の具体的な処理、状態管理、入出力変換、関数、クラス、定数を調べたいとき。
- session join の衝突解決ロジックや判定内容など、実体を持つ処理を確認したいとき。
- oracle 側の正本仕様や互換対象そのものを確認したいとき。

## hash
- 8c4fa4ee9bc1e65c70dcc8ff005ed00bb8e4079aff3755b9674a92cfef3a0446

# `tui`

## Summary
- ACP builder の TUI 関連公開 import path を、正本側の実装へ中継する互換層をまとめる階層。TUI 起動パラメータ生成と resolve-parameter builder の既存参照を維持し、TUI 向け file access mode tuple も公開する。
- ここにある実装は TUI の画面処理や builder の正本ロジック本体ではなく、realization 側または利用者向け公開面に残る既存 import 経路を成立させるための再公開・委譲を担う。

## Read this when
- ACP builder の TUI 関連 API を既存の公開 import path から使えるように保っている互換層を確認したいとき。
- TUI 起動パラメータ生成や resolve-parameter builder が、realization 側から oracle 側の canonical 実装へどう接続されているかを確認したいとき。
- TUI 向け import surface で公開される file access mode の選択肢や、builder 関数の再公開範囲を確認したいとき。
- 正本側 import path への移行に伴い、この互換層を削除できる条件を調べたいとき。

## Do not read this when
- TUI 起動パラメータや resolve-parameter builder の実際の組み立て仕様を確認したいとき。ここではなく oracle 側の canonical 実装を読む。
- TUI の表示、イベント処理、画面構成、入力操作などの UI 本体実装を調べたいとき。
- AgentCallParameter や FileAccessMode の型定義・意味を確認したいとき。ここでは型や列挙値を利用・公開するだけで、定義本体は別の基本モジュールが担う。
- TUI 以外の ACP builder 経路、または UI 非依存の parameter 構築全般を調べたいとき。

## hash
- 3d3ccc7c3599265b864d6f03f95716c3677e3806db42b4c7e7371a7a4440e6f2
