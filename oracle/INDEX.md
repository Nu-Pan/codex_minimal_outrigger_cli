# `doc`

## Summary
- cmoc のアプリケーション仕様断片をまとめるディレクトリ。CLI 補完、Codex 呼び出し、ログ、前処理、プロンプト、実行隔離、session 状態、branch/run 境界、サブコマンドなどの正本仕様文書への入口。
- 設計上の代替案や開発規則も含み、目的に応じて個別の仕様文書・設計判断メモ・開発規則へ進むために使う。

## Read this when
- cmoc の個別機能またはサブコマンドの正本仕様を確認・変更するとき。
- CLI 補完、Codex 呼び出し、ログ、前処理、プロンプト生成、実行隔離、session 状態、branch/run 境界を調べるとき。
- cmoc の設計で採用しなかった代替案や、Python・CLI・テストの共通開発規則を確認するとき。
- app_spec 内の具体的な仕様文書やサブコマンド仕様の入口を選ぶ必要があるとき。

## Do not read this when
- INDEX.md の自動生成・更新規則だけを確認したいとき。
- リポジトリ全体の共通運用前提だけを確認したいとき。
- 特定文書の本文や実装の詳細が既に明らかな単純な作業で、個別の対象を直接読めるとき。
- 現行仕様・実装・テストの詳細ではなく、採用しなかった設計案だけを確認したい場合は、該当する設計判断メモを直接読むとき。

## hash
- 1eb27c0d9a3f194641e66f9490100b9a47b2b48bfac9e7d302874635a08170db

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
