# `doc`

## Summary
- cmoc のアプリケーション仕様断片を集約するディレクトリ。CLI サブコマンド、Codex/Ollama 連携、ログ、エラー処理、状態管理、run isolation、branch・session 境界、利用手順などの正本仕様を選ぶ入口であり、個別仕様の確認は下位文書へ進む。

## Read this when
- cmoc の個別機能やサブコマンドの仕様を調査・実装・レビューするとき。
- CLI 実行、Codex 呼び出し、managed Ollama、ログ、状態管理、run isolation、INDEX 生成などの正本文書を選ぶとき。
- 利用手順や共通のアプリケーション動作を確認するとき。

## Do not read this when
- INDEX.md の生成・更新ルールだけを確認したいとき。
- Python 開発環境、設計、テスト実行規則を確認したいとき。
- 特定文書の内容が明らかな場合や、既存実装の詳細を確認したい場合。

## hash
- 0ecff0c69f6bf3dfee5008048b179561739edaa82d48748d33ddcc38bdd6a6ee

# `src`

## Summary
- ACP builder の agent call パラメータ、prompt builder の構成・依存注入、設定・ルートパス解決、規範文書や構造化 markdown を扱う共通 oracle src の領域。個別サブディレクトリの仕様・実装へ進むための入口。

## Read this when
- agent call のモデル、推論強度、ファイルアクセス、Structured Output、作業ディレクトリの型を確認するとき。
- prompt の組み立て、standard・プレースホルダ・ファイルアクセス規則・routing rule の注入を調査するとき。
- cmoc 設定、ループ回数、JSON 保存、ルートパスプレースホルダ解決、構造化 markdown の検査・レンダリングを確認するとき。
- 個別実装を読む前に、ACP builder、prompt builder、その他の共通基盤のどこへ進むべきか判断するとき。

## Do not read this when
- 個別サブコマンドの実行フロー、CLI 入出力、ファイル探索、生成物の保存処理を調査するとき。
- 個別の oracle file や realization file の具体的な仕様・実装を確認するとき。
- 下位ディレクトリの責務が明確で、共通の agent call、prompt、設定、パス、構造化文書基盤を確認する必要がないとき。

## hash
- 653d8ccb890d140a59a10aad0e8996dca6bbccecc3405aa44c76baa19f0965f3
