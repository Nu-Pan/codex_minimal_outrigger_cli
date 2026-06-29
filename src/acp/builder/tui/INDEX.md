# `__init__.py`

## Summary
- 正本側の ACP builder TUI パッケージとの互換性を示すだけの package 初期化地点。具体的な処理や公開オブジェクトは持たず、この階層が互換 package として存在する理由を示す。

## Read this when
- ACP builder の TUI 関連 package が、正本側の対応 package と互換の入口として用意されているかを確認したいとき。
- この package 初期化地点自体に、追加の初期化処理、公開 import、互換性説明があるかを確認したいとき。

## Do not read this when
- TUI の構築処理、画面制御、入出力処理などの実装内容を調べたいとき。
- 正本仕様断片そのもの、または互換先の詳細な挙動を確認したいとき。
- 関数、クラス、定数、CLI 動作などの具体的な公開面を探しているとき。

## hash
- 0a593accdb428d084c035fe120f2a06b5788abb28e112e72252680ca369fb14d

# `launch_tui.py`

## Summary
- TUI 起動パラメータ生成関数の実体を oracle 側に置いたまま、既存の公開 import path から同じ関数を参照できるようにする互換用モジュール。
- realization 側や利用者向け公開面に残っている既存参照を維持するための薄い再 export であり、TUI 起動パラメータの仕様や組み立てロジック自体は持たない。

## Read this when
- TUI 起動パラメータ生成関数の import 経路、公開面との互換性、または oracle 側実装への接続を確認したいとき。
- 既存の公開 import path を削除・移動・置換してよいか判断するために、互換コードを残す理由と削除条件を確認したいとき。
- TUI builder 周辺で、realization 側から oracle 側の TUI 起動パラメータ正本へどのように委譲しているかを確認したいとき。

## Do not read this when
- TUI 起動パラメータの具体的な構造、値、生成ロジックの正本を確認したいとき。この対象は再 export だけを担うため、oracle 側の実体を読む。
- TUI 画面の描画、イベント処理、ユーザー操作、または端末 UI の挙動を調べたいとき。
- 互換 import path ではなく、新しい起動仕様や利用者向け CLI 挙動そのものを設計・確認したいとき。

## hash
- 23d4d93c40bb8191cb1d3b58b15845e17afca479d63366ca50c92836df1b6091

# `resolve_parameter.py`

## Summary
- TUI の resolve-parameter builder について、既存の TUI 側 import surface を保つための互換モジュール。prompt 構築は oracle 側の正本 builder に委譲し、戻り値の Structured Output schema path だけを realization 側の整合 schema へ差し替える。
- oracle 側 schema の `required` と `properties` が file access profile について食い違う間、TUI runtime が実際に読む `file_access_profile.value.{oracle,realization,index}` 形式を検証可能にする境界として位置づけられる。

## Read this when
- TUI 側から resolve-parameter builder を import している既存コードの互換性を確認・変更するとき。
- TUI resolve parameter の prompt は oracle 側へ委譲しつつ、Structured Output schema だけ realization 側で補正している理由を確認するとき。
- canonical な oracle 側 builder への移行に伴い、この互換モジュールを削除できる条件を確認するとき。

## Do not read this when
- resolve-parameter builder の実際の prompt 組み立て処理や正本仕様を確認したいとき。この対象は prompt 生成を oracle 側へ委譲するため、canonical な builder 実装を読む方が直接的。
- ファイルアクセスプロファイル自体の定義や意味を確認したいとき。この対象は TUI resolve 用 schema の接続だけを担う。
- TUI 以外の ACP builder import 経路や UI 非依存の parameter 構築を調べたいとき。

## hash
- 3d226f80d42a0ac3d7551617d002af4d355b8d3c2077fd8e8dc52f9ef8f0c929

# `resolve_parameter.json`

## Summary
- TUI resolve parameter の realization 側 Structured Output schema。TUI runtime が解釈する `file_access_profile.value.{oracle,realization,index}` と標準 prompt 注入フラグを、理由付きの JSON object として検証する。
- oracle 側 schema の field 構成が runtime 入力形式と食い違う間、`acp.builder.tui.resolve_parameter` wrapper から参照される補正 schema として使われる。

## Read this when
- `cmoc tui` の resolve parameter 結果として Codex に返させる JSON 形、特に `file_access_profile` と標準 prompt 注入フラグの schema を確認・変更するとき。
- TUI resolve parameter の Structured Output 検証が、oracle 側 schema ではなく realization 側 schema を使う理由を確認するとき。

## Do not read this when
- TUI resolve parameter の prompt 本文やパラメータ選定方針そのものを確認したいとき。その場合は oracle 側 builder と prompt 仕様を読む。
- Codex CLI 起動時の sandbox profile 生成、writable roots、cwd 選択など runtime 変換を調べたいとき。

## hash
- 1f277462bbae21469b8ef7bf246d5ce6845882a781799429c114c5273a8ea51d
