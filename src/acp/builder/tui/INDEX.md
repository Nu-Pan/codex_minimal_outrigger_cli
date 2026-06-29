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
- TUI 起動用の AgentCallParameter builder を公開する薄い realization 実装。oracle 側の builder 結果を再利用しつつ、TUI 起動では Structured Output を使わないため、存在しない schema path を公開しないよう `structured_output_schema_path` だけを実行時に無効化する。

## Read this when
- TUI 起動用の AgentCallParameter の組み立て結果、とくに Structured Output schema path の扱いを確認・変更したいとき。
- oracle 側の TUI 起動 parameter 定義と realization 側の実行時契約の差分を調べたいとき。
- TUI 起動処理が存在しない Structured Output schema を参照しないようにする互換処理の根拠を確認したいとき。

## Do not read this when
- TUI の画面描画、入力処理、イベントループなど、起動後の TUI 本体の挙動を調べたいとき。
- Structured Output を消費する agent call や JSON schema の内容を調べたいとき。
- oracle 側の正本仕様断片そのものを確認したいとき。

## hash
- 4ec0ac51241993677a09a6e26d9752464337332b6f6156de3352c0203793f960

# `resolve_parameter.py`

## Summary
- TUI 向けのパラメータ解決機能を正本側実装から公開し、TUI で扱うファイルアクセスモードの選択肢を基本定義の列挙値から組み立てる薄い realization 実装。
- 独自の解決ロジックを持つ入口ではなく、正本側の TUI パラメータ解決と基本定義の列挙値を、実装側から参照できる形に接続する役割を持つ。

## Read this when
- TUI のパラメータ解決を realization implementation 側でどこから import しているか確認したいとき。
- TUI で提示・利用するファイルアクセスモードの候補が、基本定義の列挙値と同期しているか確認したいとき。
- 正本側の TUI パラメータ解決実装を realization 側へ露出する接続部分を変更・確認したいとき。

## Do not read this when
- パラメータ解決の具体的な仕様や処理内容を確認したいときは、正本側の TUI パラメータ解決実装を読む。
- ファイルアクセスモード自体の定義や意味を確認したいときは、基本定義側の列挙値を読む。
- TUI 全体の画面構成、入力フロー、表示処理を調べたいだけなら、より直接それらを実装する対象を読む。

## hash
- c5a764ce2693eef8273489b9de5d8f063ec7dcd7e72609d239251b54dc4554bd
