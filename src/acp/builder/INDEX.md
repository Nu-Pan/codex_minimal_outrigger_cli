# `__init__.py`

## Summary
- `oracle.acp_builder` を `acp.builder` として参照できるようにする互換用の公開入口。実処理を持つ実装本体ではなく、既存の import 経路を保つための薄い窓口として位置づけられる。

## Read this when
- `acp.builder` 経由の import 互換性や公開入口の有無を確認したいとき。
- `oracle.acp_builder` 側の機能を、別名のモジュール経路から公開しているかを確認したいとき。

## Do not read this when
- builder の具体的な生成処理、関数、クラス、制御ロジックを調べたいとき。その場合は実体側の実装を読む。
- 互換入口ではなく、新しい builder 機能の仕様や挙動を確認したいとき。

## hash
- 9e834d7b4a4868035265a9b1d6e846ff32541555482bed155e7bbf15576d4932

# `apply`

## Summary
- apply builder 領域の realization 側 package。oracle 側の apply builder package と対応する互換 package として成立し、下位に apply fork 系の agent call parameter builder 群への入口を持つ。
- この領域では、apply fork の各段階で使う agent 呼び出しパラメータ生成について、realization 側から oracle 側 builder へ委譲し、repository root 解決、oracle src import 準備、runtime 側 parameter への橋渡しを扱う。

## Read this when
- apply builder 領域が oracle 側 package 構造とどう対応しているかを確認したいとき。
- apply fork 系の agent call parameter builder へ進む入口を探しているとき。
- apply fork 系 builder で、realization 側から oracle 側 builder へどう委譲されるか、repository root 解決や oracle src import 準備をどこから確認するか判断したいとき。
- 変更要約、ファイル単位の所見列挙、検出済み所見の適用に対応する agent 呼び出しパラメータ生成箇所を探しているとき。

## Do not read this when
- apply builder の具体的な変換・適用ロジックや公開関数・クラスの詳細だけを調べたいときは、該当する実装本体へ直接進む。
- apply fork の prompt 本文、JSON schema、モデル選択、file access mode などの正本仕様を確認したいときは、対応する oracle 側 builder や schema を読む。
- apply fork 全体の制御フロー、fork 作成、git 操作、実行 orchestration を調べたいときは、上位の apply fork 実装へ進む。
- repository root 解決そのものの仕様、path model、AgentCallParameter や enum 型の定義を調べたいときは、それぞれの基本定義側を読む。
- apply fork 以外の apply 系 command や、所見の検出・分類・生成ロジックを調べたいだけのとき。

## hash
- 30a141b5c106ba2f0181deead440ccdfb91d81c9dfc10a1ba0ae9f295bfeb9d5

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
- ACP builder の TUI 関連呼び出しパラメータを、正本側の定義から realization implementation 側へ接続する薄い package。
- TUI 起動用パラメータでは正本側の構築結果を再利用しつつ、起動時に消費しない Structured Output schema path を実行時契約に合わせて無効化する。
- TUI のパラメータ解決入口と、TUI で提示するファイルアクセスモード候補を基本定義の列挙値から参照できるようにする。

## Read this when
- TUI 起動または TUI パラメータ解決に使う AgentCallParameter が realization implementation 側でどう公開されているか確認したいとき。
- TUI 起動処理が存在しない Structured Output schema path を公開しないようにしている互換調整を確認・変更したいとき。
- TUI で扱うファイルアクセスモード候補が基本定義の列挙値と同期しているか確認したいとき。
- 正本側の ACP builder TUI 実装を、実行側 package から import できる形に接続する箇所を探しているとき。

## Do not read this when
- TUI の画面描画、入力処理、イベントループなど、起動後の TUI 本体の挙動を調べたいとき。
- パラメータ構築や解決の正本仕様断片そのものを確認したいとき。
- Structured Output を実際に消費する agent call や JSON schema の内容を調べたいとき。
- ファイルアクセスモード自体の意味や基本定義を確認したいとき。

## hash
- 01df73688f2bfcdab47931ac7ccc89582b5f9b15e5a365a1351fe5e278d86ad6
