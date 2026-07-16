# `doc`

## Summary
- cmoc のアプリケーション仕様断片を収めるディレクトリ。CLI 補完、ログ、doctor、provider、run isolation、session 状態、サブコマンド、利用手順など、個別機能と共通実行規則の正本仕様への入口を提供する。
- branch と worktree による session・run の境界、採用しなかった設計案、Python 実装・CLI 構成・テストの開発規則も含む。各対象の詳細確認が必要なときに下位文書へ進むためのルーティング起点である。

## Read this when
- cmoc の CLI 挙動、サブコマンド、実行前処理、状態管理、ログ、agent call、Ollama provider、run isolation の仕様を調べるとき。
- session や run の branch・worktree 境界を確認するとき。
- 採用しなかった設計案や、Python 実装・CLI 構成・テストの共通規則を確認するとき。
- 複数のアプリケーション仕様から、作業対象に直接関係する下位文書を選ぶ必要があるとき。

## Do not read this when
- INDEX.md の生成・更新規則だけを確認したいときは、インデクシング仕様を直接読む。
- git、branch、状態ファイルなどの基礎概念だけを確認したいときは、対応する基礎仕様を直接読む。
- 特定仕様の詳細が明らかな場合は、このディレクトリ全体ではなく該当する下位文書へ直接進む。
- 現行仕様や実装・テストの詳細ではなく、採用しなかった設計案だけを確認したい場合は、代替案の文書へ直接進む。

## hash
- 8d657280fdeda08a6076c678db43ed549981cdb47bd1b57b9959d1cc83b68634

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
