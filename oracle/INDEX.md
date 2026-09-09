# `doc`

## Summary
- cmoc のアプリケーション仕様、開発ルール、branch・worktree モデル、採用しなかった設計案を確認するための仕様・設計資料群の入口。現行仕様の個別契約、開発規則、branch 関係、設計判断の背景へ目的別に進む。

## Read this when
- cmoc のアプリケーション仕様や開発ルールを調べ、個別の正本文書へ進む前の参照先を判断したいとき。
- session・run の branch・commit・worktree 関係、または採用しなかった設計案の背景を確認したいとき。

## Do not read this when
- 確認対象の仕様・開発規則・branch model・検討資料がすでに特定できており、その本文だけを読む場合。
- 実装コード、realization file、oracle、個別 builder・schema、または具体的な git 操作手順を直接確認したい場合。

## hash
- 859f07827ddc65323578d5f68da3450dc9d5702c223b783518a07a4f7fdbd597

# `src`

## Summary
- AI コーディングエージェント呼び出しを支える oracle パッケージの実装ソースへの入口。
- agent call パラメータ、パスモデル、構造化文書、prompt 構築、用途別 builder など、呼び出し設定と入力文面を組み立てる処理を扱う。
- quota probe、indexing、feedback、oracle・realization・session・TUI の各呼び出し経路や、editor input handoff の実装を下位対象から辿れる。

## Read this when
- agent call の共通パラメータ、ファイルアクセスモード、agent call の cwd、worktree パス、placeholder 解決を調べるとき。
- 構造化された prompt の組み立て、policy の注入、placeholder の統合、editor 経由入力の初期文面を調べるとき。
- 用途別の Codex CLI 呼び出し builder や quota probe、indexing、feedback、session、TUI の実装経路を確認するとき。

## Do not read this when
- 特定用途の prompt や policy の本文だけを確認したいときは、prompt_builder 配下の該当対象を直接読む。
- oracle・realization・feedback の個別処理や、session・TUI の具体的な起動処理だけを確認したいときは、それぞれの下位対象を直接読む。
- Codex CLI の実行結果処理や、正本仕様・実装の適合性を確認したいときは、この実装入口ではなく該当する実行処理または仕様対象を読む。

## hash
- bf60aa7791a88cc168d94bc736b1151e2068727c0ff41d63b1ade7ad33c4de7f
