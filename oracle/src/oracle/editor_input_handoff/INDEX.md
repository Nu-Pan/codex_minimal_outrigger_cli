# `body.py`

## Summary
- 検証済みの editor input 項目と送信元 TUI process 情報から、受信側へ渡す Markdown 本文全体を構築する正本実装。任意の背景情報・oracle 参照を省略可能な章として配置し、送信元識別子と絶対ログパスを記録する。

## Read this when
- editor input handoff の本文構成、項目の配置、任意項目や oracle 参照の扱いを確認したいとき。
- 送信元 TUI process の識別情報を本文へ引き渡す処理や、入力本文中のコメント開始記号の扱いを確認したいとき。

## Do not read this when
- 送信元情報の型、不足値、ログパスの絶対パス検証を確認したいときは、同階層の source.py を直接読む。
- MCP tool input の検証済み項目や許可されるフィールド構造を確認したいときは、同階層の overwrite_input.json を直接読む。
- editor input handoff の意味仕様や TUI/MCP の呼び出し制御を確認したいときは、参照される oracle 文書または呼び出し側実装を直接読む。

## hash
- 551f441e7b828986223438685bad190bfe801889c2dce883accfe01a211379b4

# `overwrite_input.json`

## Summary
- 対象は oracle/editor_input_handoff における overwrite_input の入力データを定義する JSON ファイルで、編集対象の入力を上書きするために渡す値を扱う。
- 同階層の実装・仕様ファイルを横断して概要を確認したい場合ではなく、overwrite_input の入力形式や上書き操作への受け渡し条件を確認する際の入口となる。

## Read this when
- 編集対象の入力を上書きする処理へ渡される JSON 入力の構造や値を確認するとき。
- editor_input_handoff の中で、追加入力や別のハンドオフ形式ではなく overwrite_input の扱いを調べるとき。

## Do not read this when
- 入力上書きの実際の実装手順や実行時挙動を確認したい場合は、対応する realization 実装やテストを直接読むとき。
- editor_input_handoff 全体の責務や他の入力形式との関係だけを知りたい場合は、上位の仕様・案内対象から読み始めるとき。

## hash
- 740bd6adb777e14fe1f704c1c40e9f9d897eb1a3bd1ef783d887c2219aa8003a

# `source.py`

## Summary
- MCP呼び出し元へ渡すエディタ入力の送信元情報を、不変なデータ構造として定義する。識別子の空白値と、サブコマンドログパスの絶対パス性を生成・補完なしで検証する送信元情報の入口。

## Read this when
- エディタ入力引き継ぎで保持する送信元識別子やサブコマンドログパスの構造・入力検証を確認または変更するとき

## Do not read this when
- エディタ入力引き継ぎ全体の意味仕様や呼び出し元・利用先の処理を確認するとき。まず関連する仕様文書や利用側の実装を直接読むべき場合

## hash
- 0e2bdf5cf9b9de75d852ce8c8730bbebf89251fd72d48cfea31886189c0342c1
