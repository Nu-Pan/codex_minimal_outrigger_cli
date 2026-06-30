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
- Codex quota availability probe に使う最小限の agent call parameter を組み立てる実装。通常の呼び出し設定から model class、reasoning effort、profile を引き継ぎつつ、意味のある作業を依頼しない固定 prompt の probe 呼び出しを作る。

## Read this when
- Codex quota availability probe の agent call parameter がどの設定を引き継ぎ、どの入力を固定するか確認したいとき。
- quota availability probe の prompt、作業依頼の有無、または Codex CLI 呼び出し時の最小パラメータ構成を変更するとき。
- Codex CLI 実行ルールに対応する probe 用 parameter builder の実装箇所を探しているとき。

## Do not read this when
- quota availability probe の実行タイミング、プロセス起動、CODEX_HOME、profile、cwd の適用処理を確認したいだけのとき。
- agent call parameter 型そのものの定義や通常の parameter builder 全般を確認したいとき。
- Codex CLI 実行ルールの正本仕様断片を確認したいとき。

## hash
- 10efcfba9e5fde341cf5938462b2719a485ee5de2495db23651d7b5f9d53a153

# `review`

## Summary
- レビュー用 AgentCallParameter builder 領域のうち、互換 package 初期化と review oracle 関連 builder の互換 import 層をまとめる階層。主に旧来の realization 側 import 経路から canonical oracle 側実装へ委譲する入口であり、正本仕様や実処理本体ではなく、互換名前空間・移行中の import 経路・限定的な prompt placeholder 補正の境界を確認するための場所。

## Read this when
- review builder 領域で、oracle 側 package と対応する realization 側 package の互換 import 経路が成立しているか確認したいとき。
- レビュー oracle finding の列挙・判定・検証・統合 builder について、旧来の呼び出し経路が canonical oracle 側へどう委譲されているか調べたいとき。
- 互換 import 層を削除できるか、または呼び出し元を canonical oracle path へ移行すべきか判断したいとき。
- oracle src 由来 prompt の既知 placeholder 表記補正が、どの範囲で静的 prompt にだけ適用され、動的入力を保持しているか確認・変更したいとき。

## Do not read this when
- review builder の具体的な処理本体、関数、クラス、出力、制御フローを調べたいとき。
- レビュー finding の判定仕様、検出ロジック、正本 prompt、schema そのものを調べたいとき。
- AgentCallParameter の型、model、reasoning、profile、schema 指定の一般仕様を確認したいとき。
- 互換 import 経路や placeholder 補正と無関係な review 機能全般、CLI 表示、テスト方針を調べたいとき。

## hash
- 332200c050599cc766823f835aaa4ee6697948e6ea885ef80efce02f04f2c635

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
- ACP builder の TUI 互換 package。正本側の TUI 起動パラメータ生成や resolve-parameter builder を既存 import path から参照できるようにする薄い再公開層で、TUI 画面制御や builder 本体の実装は担わない。
- TUI 関連の公開 import surface、oracle 側実装への委譲、利用者向けに公開される file access mode 選択肢を確認する入口。

## Read this when
- ACP builder の TUI 関連 import path が正本側実装と互換に保たれているか確認したいとき。
- TUI 起動パラメータ生成関数や resolve-parameter builder が、既存公開面から oracle 側の canonical 実装へどのように接続されているか確認したいとき。
- TUI 側の互換モジュールを削除・移動・置換してよいか判断するため、残している理由や削除条件を確認したいとき。
- TUI の import surface で公開される file access mode の選択肢を確認したいとき。

## Do not read this when
- TUI 起動パラメータや resolve-parameter builder の具体的な仕様、値、組み立てロジックを確認したいとき。ここは再公開層なので oracle 側の実体を読む方が直接的。
- TUI 画面の描画、イベント処理、ユーザー操作、端末 UI の挙動を調べたいとき。
- FileAccessMode 自体の定義や意味を確認したいとき。ここは利用可能な列挙値を公開するだけで、mode 定義は別の基本モジュールが担う。
- TUI 以外の ACP builder import 経路、UI 非依存の parameter 構築、または CLI 挙動そのものを設計・確認したいとき。

## hash
- a06d2b1249b5b845e565d0103b984f0eb0d68abddfcfa4ebfbb78c018b939b4e
