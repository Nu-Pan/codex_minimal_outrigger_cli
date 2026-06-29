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
- ACP apply builder 領域の package 入口と、apply fork 系 agent call parameter builder 群へのルーティングを担う階層。package 初期化要素は互換 package としての存在確認に限られ、具体的な builder 実装は下位の apply fork 系領域にまとまる。
- apply fork 系では、変更要約、ファイル単位所見列挙、所見適用などの agent call parameter 構築入口を扱い、realization 側から oracle 側 builder へ委譲する adapter 群と共通 helper へ進むための入口になる。

## Read this when
- ACP apply builder 領域で、package 初期化要素だけを確認すればよいのか、apply fork 系 builder 群へ進むべきかを切り分けたいとき。
- `cmoc apply fork` 用の agent call parameter builder について、変更要約、ファイル単位所見列挙、所見適用などの用途別入口を探したいとき。
- oracle 側 ACP builder と runtime 側実行コードの境界、特に oracle src import 準備や parameter adapter の責務を確認する入口を探しているとき。

## Do not read this when
- apply builder の具体的な処理、変換、適用ロジック、公開関数、クラス、入出力仕様、エラー処理を直接確認したいとき。その場合は下位の実装本体へ進む。
- prompt 本文、出力 schema、モデル選択、file access mode などの正本仕様を確認したいとき。その場合は委譲先の oracle 側 builder や JSON 定義を読む。
- `cmoc apply fork` 全体の制御フロー、fork 作成、git 操作、CLI 引数処理だけを調べたいとき。その場合は上位の command 実装を読む。
- repository root 解決や path model の仕様、AgentCallParameter や enum 型そのものの定義を確認したいとき。その場合は対応する basic 側の定義へ直接進む。

## hash
- 0f6d505f49ddf8483c37dd4b68ef451cbc88dfd2e5caca055afa5ce79fc71936

# `indexing`

## Summary
- ACP builder の indexing 領域に置かれた realization 側の互換入口で、oracle 側にある実体を src 側の import 経路から参照できるようにするための薄いパッケージである。
- この階層自体は indexing の生成処理やデータ構造の実装本体ではなく、対応する oracle 名前空間への公開経路を保つための最小構成を扱う。

## Read this when
- ACP builder indexing 関連の import 経路が realization 側から利用できるか確認したいとき。
- src 側の indexing パッケージが oracle 側の定義を独自実装せず再公開しているかを確認したいとき。
- indexing 領域で、実装本体ではなく oracle 側との互換パッケージ入口を調べたいとき。

## Do not read this when
- indexing の具体的なデータ構造、バリデーション、生成ロジック、制御フローを調べたいとき。
- oracle 側にある index_entry の正本定義や具体的な挙動を確認したいとき。
- ACP builder 全体の処理連携やテスト対象を探しており、import 互換入口の確認が不要なとき。

## hash
- b1c27037bb29a9905c86985af10e1e43d0645d58d8167683cce83634f51a3ab7

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
