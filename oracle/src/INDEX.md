# `oracle`

## Summary
- cmoc の oracle 実装を構成するサブ領域への入口。ACP 呼び出し構築、設定・パス・規範文書・Markdown 変換、プロンプト構築と標準ルール部品を扱う。各責務の詳細は acp_builder、other、prompt_builder 配下へ進んで確認する。

## Read this when
- oracle 実装の責務分担や、ACP builder・設定／パス／規範文書・prompt builder のどの領域を読むべきか判断するとき。
- 複数の oracle 実装領域にまたがる agent call、設定、パス、規範文書、プロンプト生成の連携を調査するとき。

## Do not read this when
- 実際の CLI 実行経路、agent 呼び出しの実行処理、TUI 画面処理、個別の oracle file や realization file の内容だけを調査するとき。
- 既存の共通実装や個別定義を直接確認すべき場合は、該当する下位ディレクトリまたは定義元へ進むとき。

## hash
- b35c35c9e1252090fe293667d8ca39a40def9ec3f0cbfc9a27fded1ce6d35232
