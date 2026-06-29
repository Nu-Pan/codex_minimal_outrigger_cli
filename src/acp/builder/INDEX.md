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
- apply builder 全体の realization 側入口をまとめる package。package 初期化要素と fork 系 builder 群への入口を持ち、oracle 側 apply builder 構造との対応、および apply fork 用 agent call parameter 構築の委譲境界を案内する。
- この階層の実体は、apply builder 領域を package として扱うための薄い入口と、apply fork の変更要約・ファイル単位所見列挙・所見適用に関する runtime 側 builder adapter 群で構成される。

## Read this when
- realization 側で apply builder のどの下位領域へ進むべきかを判断したいとき。
- apply builder 領域が oracle 側 package 構造とどのように対応しているかを確認したいとき。
- apply fork 系で agent call parameter を構築する入口、または oracle 側 builder への委譲境界を探しているとき。
- 変更要約、ファイル単位所見列挙、所見適用のいずれかに関する apply fork builder の所在を確認したいとき。

## Do not read this when
- apply fork の prompt 本文、出力 schema、モデル選択、file access mode などの正本仕様を確認したいとき。対応する oracle 側の builder や JSON 定義を読む。
- apply fork コマンド全体の制御フロー、fork 作成、git 操作、CLI 引数処理を調べたいとき。上位の command 実装や git 操作側を読む。
- repo root 解決、path model、runtime 側 agent call parameter 型や enum 型そのものの定義を確認したいとき。この階層はそれらの定義を所有しない。
- apply builder の具体的な下位実装をすでに特定しているとき。該当する下位 package または実装本体へ直接進む。

## hash
- 76a64d34039072e53ac312248ce5182a9ac5ee9c9ab220c88de3559663a4a5ec

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

# `review`

## Summary
- review builder 領域の realization 側 package。上位からこの領域を package として扱うための入口と、review oracle 機能へ到達する互換 import 境界をまとめる。
- 主な内容は、oracle 側の finding 列挙・判定・統合・advocate/challenger 検証実装の再公開または薄い adapter であり、一部で oracle 側 prompt placeholder 表記を実行側で許容される範囲に補正する。

## Read this when
- realization 側の review builder から review oracle の finding 列挙・判定・統合・検証機能へ到達する import 経路を確認したいとき。
- review builder 領域が独自の主要ロジックを持つのか、oracle 側実装への互換入口や薄い adapter に留まるのかを切り分けたいとき。
- merge finding や finding advocate 検証に関する prompt placeholder typo 補正が、realization 側のどの境界で行われるかを確認したいとき。
- review oracle 関連の互換 import path や package 境界を変更・削除してよいか判断したいとき。

## Do not read this when
- review oracle の正本仕様、prompt 本文、Structured Output schema、model 設定、reasoning effort、file access mode を確認したいとき。その場合は oracle 側の仕様文書または実装へ進む。
- finding 列挙・判定・統合・検証の具体的なアルゴリズム、入出力、判定基準を理解したいとき。その場合は委譲先の oracle 側実装へ進む。
- review workflow 全体の制御、CLI 入出力、レビュー結果の検証観点、または review oracle 以外の builder 処理を調べたいとき。
- package 初期化や互換 import 境界ではなく、公開 API の詳細実装、関数・クラス・定数の新規定義、または再公開ではない処理本体を探しているとき。

## hash
- 06dfadc2e53290eb8b873bc7cfd7da1313017e9edda7d7f26300d12a5fa1339d

# `session`

## Summary
- ACP builder の session 領域における realization 側の入口を扱う階層。正本側 package 構造との import 経路互換を成立させ、session join 領域への委譲入口を下位に持つ。
- この階層自体は session builder の具体的な処理実体を持たず、package としての成立、および join 領域へ進むための境界として位置づけられる。

## Read this when
- ACP builder の session 領域で、realization 側の package 構成が正本側とどう対応しているか確認したいとき。
- session join の競合解決機能へ進む前に、session 領域全体の入口と下位領域の位置づけを把握したいとき。
- この階層が処理実体ではなく、互換 package と下位委譲入口を束ねる場所であることを確認したいとき。

## Do not read this when
- session builder の具体的な処理、状態管理、入出力変換、判定条件を調べたいとき。より直接の実装または正本側の対応箇所を読む。
- session join の具体的な分岐、データ構造、入出力仕様を調べたいとき。下位の対応領域または正本側実装を読む。
- ACP builder 全体の設計や session 以外の領域を調べたいとき。より上位または該当領域の対象を読む。
- oracle 側の正本仕様そのものを確認したいとき。この階層は realization 側の互換境界であり、正本仕様本文ではない。

## hash
- 2c93bf1bba91509e81b2885c63b2b7c6cddd88d36fb0023de9e342fb0c09d71b

# `tui`

## Summary
- ACP builder の TUI 関連 realization package で、正本側にある TUI 起動パラメータ生成と TUI パラメータ解決を既存 import path から参照できるようにする互換入口をまとめる階層。
- この階層自体は TUI 画面やイベント処理の本体ではなく、oracle 側の実装・基本定義の列挙値を realization 側の公開面へ薄く接続する役割を持つ。

## Read this when
- ACP builder の TUI 関連 import path が、正本側の対応 package や関数と互換になるよう用意されているか確認したいとき。
- TUI 起動パラメータ生成関数や TUI パラメータ解決関数が、realization implementation 側からどの入口で再公開されているか確認したいとき。
- TUI で扱うファイルアクセスモード候補が、基本定義の列挙値から組み立てられている接続部分を確認したいとき。
- TUI 関連の互換用 import path を削除・変更できるか、その接続先や削除条件を確認したいとき。

## Do not read this when
- TUI 起動パラメータ生成や TUI パラメータ解決の具体的な正本仕様・処理内容を確認したいときは、oracle 側の実体を読む。
- TUI の画面構成、入力処理、イベント処理、表示制御などの本体実装を調べたいときは、それらを直接実装する対象へ進む。
- ファイルアクセスモード自体の定義や意味を確認したいときは、基本定義側の列挙値を読む。
- 新しい公開 API、CLI の利用方法、または利用者向けの公開面全体を調べたいときは、その公開面を定義している対象を読む。

## hash
- 93af006861378091a3c7ebdc1df93776c2cc057b1c561b96b2b60c5da4a9d167
