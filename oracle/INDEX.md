# `doc`

## Summary
- cmoc の正本文書群への入口。アプリケーション挙動、session／run の branch 分離モデル、不採用案の背景、開発ルールを案内し、仕様・設計・実装判断の確認先を振り分ける。

## Read this when
- cmoc の機能仕様や状態遷移、branch・worktree 分離モデル、設計上の不採用案、実装・環境・テストの開発ルールを確認するとき。
- 具体的な個別仕様や開発規則へ進む前に、どの正本文書を読むべきか判断するとき。

## Do not read this when
- 実装コードやテストコードの具体的な挙動を確認する場合は、対象の realization file やテストを直接読む。
- 個別仕様、開発環境、テスト要件など対象文書が特定できている場合は、このディレクトリの概要ではなく該当する文書を直接読む。
- INDEX.md の生成・更新規則だけを確認する場合は、indexing の仕様を読む。

## hash
- ec0406de238d8dbe405be191223f06cfa9130d01345cedd0f966687c1b437f13

# `src`

## Summary
- AI コーディングエージェント呼び出しのパラメータと、用途別の prompt 起動定義を扱う実装領域。
- agent call に共通する prompt 構築、ファイルアクセス、routing、oracle・realization、feedback、editor input handoff の規定を組み立てる。
- 設定値、パスコンテキスト、構造化文書の Markdown レンダリングなど、prompt と agent call を支える基盤を提供する。
- oracle review、realization の適用・リファクタ、session join、TUI、feedback issue 検証など、処理段階ごとの agent call 定義へ進む入口となる。

## Read this when
- agent call の起動パラメータ、prompt 本文、Structured Output schema、ファイルアクセスモードの実装を確認するとき。
- prompt に共通規定や個別ポリシーを組み込む方法、placeholder とパス解決、構造化文書のレンダリングを調べるとき。
- oracle review、realization、feedback、session join、TUI などの用途別 agent call 実装の配置と責務を特定するとき。

## Do not read this when
- Codex CLI の実行処理やサブコマンド全体の業務ロジックを調べたいとき。
- 正本となる意味仕様や agent call の運用要件を確認したいとき。
- 特定の用途別 agent call の詳細だけを確認したい場合は、この領域全体ではなく対応する下位領域へ直接進むとき。

## hash
- 1b15b9c3fb0dc58061ed11cf1f967195e8f05b2d76e4953c3127561b31f6c955
