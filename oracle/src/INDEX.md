# `oracle`

## Summary
- AI コーディングエージェント呼び出しに関する共通パラメータ型、アクセスモード、用途別 builder への入口を扱う。
- quota probe、indexing、feedback、oracle、realization、session、TUI などの agent call 構築設定を確認するための上位入口。
- prompt、Structured Output schema、作業ディレクトリ、editor input handoff、indexing preflight の設定を確認できる。

## Read this when
- agent call の共通設定や用途別 builder の入口を確認するとき。
- oracle・realization を含む用途別 agent call の構築責務を確認するとき。
- agent call に渡す prompt、Structured Output schema、cwd、editor input handoff、indexing preflight の設定を調べるとき。

## Do not read this when
- 特定の agent call の prompt や出力契約の詳細を確認したいときは、該当する下位対象を直接読む。
- agent call の共通実行処理や Codex CLI の実際の挙動を調査するとき。
- oracle・realization file の具体的な内容や編集手順、feedback issue の保存・受付処理だけを確認したいとき。

## hash
- aa94f446acda9d09a6b113733de829f22cff0883329d72265fb3490619d43682
