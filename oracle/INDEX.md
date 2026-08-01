# `doc`

## Summary
- cmoc の正本仕様ドキュメントを収録する入口。CLI、Codex 呼び出し、ログ、doctor、prompt、run/session lifecycle、branch model、INDEX 生成、開発規約などの個別仕様を探す際に、機能仕様または開発規約の文書へ進むために読む。

## Read this when
- cmoc の機能・共通仕様を確認し、対応する oracle doc を特定するとき
- branch・commit・worktree、session・run の関係やライフサイクルを確認するとき
- Python 開発、CLI 設計、開発環境、pytest などの開発規約を確認するとき
- 採用されなかった設計案や作業方式の背景を調査するとき

## Do not read this when
- 特定の仕様文書や開発規約文書が既に分かっており、その本文だけを確認すればよいとき
- 実装構造、テスト実装、一般的な Codex CLI や model provider の仕様を直接調査するとき
- 既存の INDEX.md のルーティングだけを更新するとき

## hash
- 561d1321fc7b134c6afb2fdc4ef7a6288a2fc62d4bfec4d829876068a0438129

# `src`

## Summary
- AIエージェント呼び出し用パラメータの正本ソースを扱うディレクトリ。ACP設定、パスモデル、設定モデル、構造化Markdown、完全プロンプト、各種規範プロンプト、INDEX生成、oracle review、realization操作、session join、TUI起動の実装入口を含む。

## Read this when
- agent callのモデル・推論・ファイルアクセス設定やパラメータ構築を調査・変更するとき
- agent callのcwd、worktree、repo root、placeholderなどのパス解決を調査・変更するとき
- 完全プロンプト、エディタ初期文面、規範注入、StructDocのMarkdown化を調査・変更するとき
- INDEX生成、oracle review、realization適用・refactor、session join、TUI起動のprompt構築を調査・変更するとき

## Do not read this when
- realization側のCLI実装や実行フローだけを調査・変更するとき
- oracleドキュメント本文や個別規範の内容だけを確認するとき
- ACPのモデル・推論値そのものの利用箇所や、設定ファイルの生成・同期処理だけを調査するとき

## hash
- 15a2b0a78fabdb3e363407ec80b26fdbd569f82f65e894a4a1562dce8f875c23
