# `doc`

## Summary
- cmoc のアプリケーション仕様、開発ルール、設計判断の背景を目的別に案内する `oracle/doc` 配下の正本文書群への入口。
- CLI・TUI・session/run・feedback・oracle・realization・ログ・通知などの現行仕様はアプリケーション仕様群へ、Python・CLI・環境・テストの規則は開発ルール群へ進む。
- 採用されなかった設計案や判断理由を確認する場合は、検討資料群へ進む。

## Read this when
- cmoc の正本仕様や開発規則について、最初に読む文書群と適用範囲を判断するとき。
- CLI、TUI、session/run、feedback、oracle・realization、ログ、通知などのアプリケーション仕様の入口を探すとき。
- Python 実装、CLI 設計、開発環境、テスト要件・実行手順の正本規則の入口を探すとき。
- 現行仕様ではなく、不採用案や設計判断の背景を確認するとき。

## Do not read this when
- すでに目的の個別仕様本文や開発規則が特定できており、その対象を直接読めば足りるとき。
- 実装、テスト、状態管理、アクセス制限、feedback処理などの具体的な内容だけを確認したいとき。
- 個別の git 操作手順や、LLM・Codex CLI・model provider 自体の一般的な正しさだけを確認したいとき。

## hash
- 64da91043f46efd3d3614fe4cca9824eaa06d7b82a5143d5abed6c40514bc79a

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
