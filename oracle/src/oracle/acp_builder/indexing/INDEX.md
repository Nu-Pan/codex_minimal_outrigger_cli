# `index_entry.json`

## Summary
- インデクシングで生成する INDEX.md エントリーについて、agent の結果を機械的に受け入れるための契約を定める。エントリーの意味要件や生成指示ではなく、出力の受け入れ条件を確認する入口。

## Read this when
- 生成 agent の返すエントリーについて、機械的な受け入れ条件を変更・確認するとき。
- 出力の検証失敗を調べ、生成指示と受け入れ条件のどちらを確認すべきか切り分けるとき。

## Do not read this when
- エントリーに記載する内容の意味要件を変更するときは、インデクシングの正本仕様を直接確認する。
- 生成指示の文面、参照対象、呼び出し設定を変更するときは、agent call の構築定義を直接確認する。

## hash
- 03e00cc984eeca5067e5dbe49c481a91c135c6aa06a633d90cc5a69c3ad05735

# `index_entry.py`

## Summary
- cmoc indexing の目次エントリー生成用 agent call について、対象パスに応じた prompt と起動パラメータを組み立てる。
- 読み取り専用で既存 INDEX.md を参照しない生成依頼を構成し、indexing 自身への自動 preflight を無効にする。

## Read this when
- 個別の目次エントリー生成 call の指示内容、対象パスの渡し方、cwd、アクセスモード、自動 preflight 設定を変更するとき。
- indexing 自身を実行する agent call の起動条件を確認するとき。

## Do not read this when
- 共通 prompt の組み立てや共有ポリシーの内容を変更するときは、prompt builder 側の定義を読む。
- 目次生成対象の列挙、処理順序、並列化、ハッシュ検査、INDEX.md の更新やコミットを調べるときは、indexing の仕様または実行側を読む。
- Codex のモデルや推論設定を変更するときは、call 種別ごとの設定を読む。
- INDEX.md の意味や運用規則を確認するときは、indexing の仕様を読む。

## hash
- 1710918437f23582a6330d74bc56eee15fb0ba844cd4554d26c34a3b8a69fecf
