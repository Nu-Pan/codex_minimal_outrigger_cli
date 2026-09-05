# `doc`

## Summary
- cmoc の正本仕様・設計判断・開発規則を、アプリケーション挙動、branch model、採用しなかった代替案、Python 実装・環境・テスト規則の領域別に参照するための上位入口。対象分野に応じて下位文書群へ進む判断基準を提供する。

## Read this when
- cmoc の仕様、設計、開発ルールを調査し、どの文書群を起点に読むべきか判断するとき
- CLI、session・run、feedback、ログ、通知、oracle／realization などのアプリケーション挙動を確認するとき
- Python 実装、CLI の責務分担、開発環境、テストの規則を確認するとき
- 現行仕様ではなく、採用しなかった設計案や不採用理由を調べるとき
- branch、commit、worktree の役割と session・run の隔離関係を確認するとき

## Do not read this when
- 確認対象のアプリケーション仕様、branch model、開発規則、または代替案の本文が既に特定できているときは、対応する個別文書を直接読む
- 特定サブコマンドの挙動、個別の agent call 規則、feedback の詳細、oracle／realization のファイル単位の責務を調べるときは、該当する下位仕様を直接読む
- Python の具体的な実装や realization test の具体的な内容を理解したいときは、対応する実装・テスト対象を直接読む
- INDEX.md の生成・更新規則だけを確認するときは、indexing に対応する仕様を直接読む

## hash
- d1d459fce84a0443e81986e6b5f81467e4424dc148bf46d106a9e6488c7939c9

# `src`

## Summary
- Codex CLI を用いる cmoc の実装層で、agent call のパラメータ構築、prompt と policy の生成、パス・構造化文書・設定の共通処理を担う。
- quota probe、indexing、feedback、oracle、realization、session、TUI などの用途別 call builder と、editor input handoff や feedback reporter の入力契約を提供する。
- oracle と realization の扱い、ファイルアクセス制約、routing、Structured Output 連携を組み合わせて、用途ごとの agent call を構成する入口となる。

## Read this when
- cmoc の agent call 構築における共通パラメータ、prompt、policy、パス解決、構造化文書処理の責務分担を確認するとき。
- quota probe、indexing、feedback、oracle、realization、session、TUI の用途別 agent call builder や、editor input handoff・feedback reporter の入力契約を探すとき。
- oracle・realization の正本責務、ファイルアクセスモード、INDEX.md routing、Structured Output を agent call に組み込む方法を調べるとき。

## Do not read this when
- 特定用途の prompt、出力契約、起動パラメータの詳細だけを確認したいときは、該当する用途別 builder と schema を直接読む。
- agent call の実行処理や Codex CLI の実際の挙動を調べるときは、実行層や対応する外部仕様を直接確認する。
- oracle・realization・feedback の意味仕様、保存・受付処理、または個別の入力契約だけを調べるときは、それぞれの正本仕様や専用入力定義を直接読む。

## hash
- 39340166c0e1059ce1115273520875a712f43899db4538a882ffbf0de62d8b98
