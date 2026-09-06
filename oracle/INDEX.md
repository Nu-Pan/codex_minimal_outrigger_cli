# `doc`

## Summary
- cmoc のアプリケーション仕様、開発ルール、session・run の branch model、設計上の検討資料を目的別に案内する正本文書群の入口。現行仕様と開発規則を横断して参照する際の起点となる。

## Read this when
- cmoc のアプリケーション挙動や開発ルールについて、複数領域にまたがる正本仕様の参照先を選ぶとき
- session・run の branch・commit・worktree 関係を確認するとき
- 現行仕様ではなく、不採用案や設計判断の背景を調べるとき

## Do not read this when
- 特定のサブ文書や実装ファイルが直接の参照先として明確なとき
- 具体的な状態遷移、CLI 操作、Python 規約、テスト要件・実行手順などを直接確認したいとき
- 現行仕様ではなく、設計上の代替案や不採用理由を調べる必要がないとき

## hash
- 7471aab60cda425c9f1441fe82cd4ab4cc1e169a9c46bf3d068622af066a133f

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
