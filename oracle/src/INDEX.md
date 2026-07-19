# `oracle`

## Summary
- oracle の設定・パス解決・規範データ構造・構造化文書レンダリングを担う実装群をまとめたディレクトリ。cmoc 固有設定、ルートパスモデル、標準文書の構造化、Markdown 変換、cmoc_ref 検証の実装への入口を提供する。
- ACP builder、prompt builder など、エージェント呼び出し条件やプロンプト構築を支える下位実装への入口を含む。

## Read this when
- cmoc の設定値、既定値、Codex・Ollama・oracle review の制御を確認・変更するとき。
- プレースホルダを含むパス解決、cmoc・repo・run・work ルートの探索を調査するとき。
- 規範文書のデータ構造、構造化文書の Markdown レンダリング、cmoc_ref 検証を調査するとき。
- ACP builder や prompt builder の共通設定、agent call 構築条件、プロンプト部品の担当箇所を特定するとき。

## Do not read this when
- CLI 機能の具体的な実装や入出力処理だけを調査するとき。
- エージェント呼び出しの実行本体や、生成済みの INDEX.md・oracle file・realization file などの成果物を確認するとき。
- 個別ファイルの実装詳細や schema の内容が既に特定できており、その本文だけを確認すればよいとき。

## hash
- 524a86d3b9ca9913986844c5586e48a69c50bc65e664a29ee8e2f702ef6f159f
