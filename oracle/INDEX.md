# `doc`

## Summary
- cmoc のアプリケーション仕様断片をまとめたディレクトリ。CLI の補完・通常実行・サブコマンド、ログとエラー処理、セッション状態、run 隔離、Codex CLI 呼び出し、managed ollama などの個別仕様へ進む入口。

## Read this when
- cmoc の利用者向け挙動、CLI 実行条件、状態遷移、ログ・エラー処理、agent call、managed ollama の仕様を確認するとき。
- 複数のアプリケーション仕様候補から、対象機能に対応する正本仕様断片を選ぶとき。

## Do not read this when
- INDEX.md の自動生成・更新規則だけを確認したいとき。
- Python 実行環境、設計ルール、テスト手順など開発規則だけを確認したいとき。
- 個別仕様が明らかで、対象ファイルへ直接アクセスすれば足りるとき。

## hash
- de45440fefb270c49b4c914d7cbaa34ed23e56aa27574c630ab877d9eb2482ad

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
