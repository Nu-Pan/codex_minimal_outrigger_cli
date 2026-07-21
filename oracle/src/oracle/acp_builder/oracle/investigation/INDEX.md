# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用の TUI 起動パラメータを構築する実装。oracle file 調査向けの完全プロンプトを生成・ログ保存し、固定モデル・推論設定・oracle 読み取り権限・インデックス事前処理を指定した起動情報を返す。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件、調査プロンプトの構成、または editor_input ログ保存を変更・確認するとき。

## Do not read this when
- oracle 調査プロンプトの共通生成規則を変更するときは、まず共通 prompt builder を読む。
- TUI 起動後の agent 実行処理や oracle file の内容を調査するときは、対応する実行処理または oracle file を直接読む。

## hash
- 9552559b62db3840667f4ae02001c9aebae4356f91092f7ea48acc2af0d1a879
