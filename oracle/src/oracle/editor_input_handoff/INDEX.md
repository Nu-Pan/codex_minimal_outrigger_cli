# `body.py`

## Summary
- 項目別の依頼内容と検証済みの送信元情報から、editor work file を置換する Markdown 本文を構築する正本実装です。必須項目の検証、任意の oracle 参照の整形、送信元識別情報の配置、見出し順序とレンダリングを確認するときの入口になります。

## Read this when
- editor input handoff の本文生成、必須項目の空値扱い、oracle 参照の挿入、または送信元情報の出力形式を変更・確認するとき。
- handoff 本文の正確な見出し・順序・項目表記を、仕様から実装へ追跡するとき。

## Do not read this when
- handoff の入力 schema、送信元情報のデータ供給・検証、または agent-facing MCP の受付処理だけを調査するときは、それぞれの専用 oracle source や仕様を直接読む。
- editor work file の target routing、待機 lifecycle、最終読み取り、または Codex TUI への注入手順だけを調査するとき。

## hash
- 92d68f381f9124196075afccf753cab24f47dc0effeaa46913cf6858da50fd4a

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
