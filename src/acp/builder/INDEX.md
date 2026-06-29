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
- apply builder 領域の realization 側 package。apply 系 agent call parameter 構築に関する互換入口をまとめ、oracle 側 package との対応を保ちながら、apply fork 向け builder 群への入口を提供する。
- この階層自体は薄い package 境界であり、実処理は下位領域が担う。特に apply fork では oracle 側 builder への委譲、oracle src import path の準備、repo root 由来の fallback、oracle parameter から realization 側 agent call parameter への適合処理を扱う。

## Read this when
- apply builder 領域が oracle 側 package 構造とどう対応するかを確認したいとき。
- apply 系の agent call parameter builder のうち、apply fork 向けの変更要約、ファイル単位所見列挙、所見適用の入口を選びたいとき。
- oracle 側 builder を realization 側から呼び出す境界や、oracle 側戻り値を realization 側型として扱う適合処理の所在を確認したいとき。
- oracle package を通常 import できない配置で、repo root 由来の候補から oracle src を import path に追加する fallback を調べたいとき。

## Do not read this when
- apply builder の具体的な処理や agent call parameter 構築ロジックを確認したいとき。この階層の package 初期化部分ではなく、該当する下位実装を読む。
- apply fork のプロンプト内容、出力条件、agent call parameter の正本仕様そのものを確認したいとき。realization 側の薄い委譲実装ではなく、対応する oracle 側本文を読む。
- apply fork 全体の CLI 制御、fork 適用処理、git 操作、作業レポート生成フローを調べたいとき。この領域は agent call parameter 構築の入口と共通境界に限られる。
- repo root 解決仕様、ACP 型の定義・検証規則、oracle 側 builder 本体の詳細を確認したいとき。それぞれの定義元や委譲先を読む。

## hash
- 6c0c8d0dd7e34017f6fd337be982bfc258fc5deb27e06becc8f3d7a11b42e98a

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
- review builder 領域の realization 側 package 入口。review oracle 向け builder について、package 初期化と、正本側実装を再公開または最小限に補正する互換層への入口をまとめる。
- この階層自体は review 判定ロジックや正本仕様断片を持つ場所ではなく、realization 側 import path から oracle.acp_builder.review 由来の機能へ到達するための薄い境界として位置づく。

## Read this when
- realization 側で review builder の package や import 経路が成立しているかを確認したいとき。
- review oracle の finding 列挙・判定・統合・検証用パラメータ生成が、realization 側からどの入口を通って正本側実装へ委譲されるかを確認したいとき。
- 正本側 builder の返却値に対して、realization 側が oracle root 表記の typo 補正など最小限の調整だけを行う箇所を探したいとき。
- この階層に独自の review 判定処理があるのか、互換名前空間または正本側実装の再公開に留まるのかを切り分けたいとき。

## Do not read this when
- review oracle の finding 列挙・判定・統合・検証ロジックそのもの、判定基準、prompt 本文、structured output schema を理解したいとき。
- 正本仕様断片としての review builder や review oracle の要求を調べたいとき。
- AgentCallParameter 型、model class、reasoning effort、file access mode、アクセス設定など、review builder に限らない共通仕様を調べたいとき。
- review oracle 以外の builder、CLI 入出力、テスト観点、または review 全体のユーザー向け挙動を調べているとき。

## hash
- f720b3653b3fd22299182fbaf3c90acb2246003b449790e14f0dd7afc084084d

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
- ACP builder の TUI 起動・resolve parameter 構築に関する realization 側の互換入口をまとめる階層。正本側の TUI builder 実装へ処理を委譲しつつ、既存の公開 import path を維持する。
- 対話的な TUI 起動では AgentCallParameter から Structured Output schema 指定を外す差分を扱い、resolve parameter 構築関数と TUI で選べるファイルアクセスモード候補を正本側定義から公開する。

## Read this when
- ACP builder の TUI 関連公開入口が、正本側実装へどのように接続されているかを確認したいとき。
- TUI 起動用 AgentCallParameter の生成経路、または対話的な TUI 起動で Structured Output schema を渡さない理由を確認したいとき。
- TUI ビルダー層から resolve parameter 構築関数やファイルアクセスモード候補へ到達する import 境界を確認したいとき。
- 正本側との互換 import path を維持する理由や削除条件が、TUI 起動パラメータの公開面にどう関係するかを調べるとき。

## Do not read this when
- TUI の画面描画、キー操作、入力処理、対話フローなど、対話 UI 本体の挙動を調べたいとき。
- TUI 起動パラメータや resolve parameter の正本仕様、具体的な引数組み立て、検証処理を確認したいだけのとき。この階層ではなく委譲先の正本側実装を読む。
- Structured Output schema を要求する非 TUI 起動や index entry 生成など、schema 付き AgentCallParameter の挙動を調べたいとき。
- ファイルアクセスモード enum 自体の定義や各モードの意味を確認したいとき。この階層は正本側定義から候補集合を公開するだけを扱う。

## hash
- cc9d5fc6cfc2286f721f05a6da86a2b65c56b0789f704e9478e76083f84da07d
