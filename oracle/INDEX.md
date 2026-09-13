# `doc`

## Summary
- cmoc の正本仕様・設計判断記録・開発規約を、責務別に参照するための文書群への入口。
- app spec、branch・commit・worktree のモデル、過去の代替案と採否理由、Python・CLI・開発環境・テストの規約を扱う。
- 機能仕様や開発作業の詳細を確認する際に、共通仕様と専門文書の境界を判断して適切な対象へ進むための上位ルーティング対象。

## Read this when
- cmoc の正本仕様、設計判断の背景、branch・commit・worktree の関係、または開発・テスト規約の参照先を選びたいとき。
- CLI 機能、session・run、権限管理、feedback、実装、開発環境、テストなど複数の責務にまたがる文書の境界を把握したいとき。
- 個別文書を読む前に、app spec と開発規約・設計判断記録の役割分担を確認したいとき。

## Do not read this when
- 特定機能の詳細仕様、個別の git 操作、実装 module、設定 field・型・schema、prompt 文面、またはテスト固有の意味要件が明らかで、対応する専門文書を直接確認できるとき。
- 実際の実装不具合、個別の所見、ログ、成果物、kaizen、oracle、feedback observation の内容を調査するとき。
- INDEX.md の生成規則や既存の目次内容だけを確認したいとき。

## hash
- 91170ac54c6125eb9167e75dc74450f730aec78fc96aa0bd783ee5036b89a093

# `src`

## Summary
- cmoc の AI コーディングエージェント呼び出しを構築する Python 実装群への入口。共通の呼び出しパラメータとファイルアクセスモード、用途別の agent call 設定、完全 prompt の組み立て、構造化出力、各種ポリシーを扱う。
- quota probe、INDEX.md エントリー生成、feedback issue の正規化・修正、oracle 調査・編集、realization 追従、session join の競合解消、TUI 起動など、個別機能の呼び出し構築へ進む起点。
- パスコンテキスト、設定モデル、構造化文書の Markdown 化、prompt の部品化と editor input handoff など、agent call 構築を支える共通処理を提供する。

## Read this when
- AI コーディングエージェント呼び出しのパラメータ、論理的なファイルアクセスモード、起動 cwd、Structured Output、editor input handoff、または indexing preflight の設定を確認するとき。
- cmoc の quota、indexing、feedback、oracle、realization、session join、TUI のいずれかに対応する agent call の prompt や起動条件を調べるとき。
- 完全 prompt の構成、用途別ポリシーの注入、placeholder の解決、または構造化文書のレンダリング経路を追うとき。

## Do not read this when
- ファイルアクセスモードや agent call の意味仕様そのものを確認したいときは、参照される正本仕様を直接読む。
- 個別 agent call の実行処理、Codex CLI のプロセス制御、通常の Git 差分処理、feedback の受付・候補 issue 管理、または oracle／realization file の具体的内容だけを調べるとき。
- INDEX.md のルーティング規則や oracle／realization の正本上の責務だけを確認したいときは、対応する仕様または下位の専用対象へ直接進む。

## hash
- 6a849be36944f6154ca91cce923cbbd5dea9fb4f61a17e9a836495325c077aba
