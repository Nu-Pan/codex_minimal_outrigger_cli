# `doc`

## Summary
- `oracle/doc` 配下の正本仕様・開発ルール・検討資料を横断的に案内する上位入口。CLI、session/run、branch、開発環境、設計、テスト、代替案の確認先を目的別に示す。

## Read this when
- cmoc の正本仕様や開発ルールについて、複数領域にまたがる入口または適切な下位文書を判断するとき。
- CLI の実行・状態管理・branch/worktree・Python 開発・テストなどの領域横断的な責務や参照先を確認するとき。
- 現行仕様ではなく、採用しなかった設計案や判断背景を調べる必要があるとき。

## Do not read this when
- 特定の仕様本文、branch model、個別の Python・CLI・テスト規則、実装、テスト、prompt builder、schema、サブコマンドの詳細だけを確認したいときは、該当する下位対象を直接読む。
- INDEX.md の生成規則、raw observation や repository-local feedback state など、対象が明確な個別仕様だけを確認したいときは対応する下位仕様を直接読む。

## hash
- b9753729b5779d0e24331153e745177369a0382affde9e1c43b47cbb7d440e87

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
