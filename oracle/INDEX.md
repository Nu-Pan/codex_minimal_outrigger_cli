# `doc`

## Summary
- cmoc のアプリケーション仕様、開発規約、branch・commit・worktree model、設計上の代替案を扱う正本文書群への入口。機能仕様と開発・運用上の共通判断を、担当文書ごとに切り分けて参照するための文書群。

## Read this when
- cmoc の仕様調査で、アプリケーション機能、開発規約、session・run の branch model、または過去の設計判断のどの文書から確認を始めるか判断するとき。
- 現行仕様の責務分担、実装・テスト規約、run の分離と統合、採用・不採用となった設計案の背景を確認するとき。

## Do not read this when
- 単一機能の詳細な実行手順、入力 schema、実装挙動、テスト固有要件だけを確認したいときは、対応する個別の正本仕様や実装を直接読む。
- INDEX.md の自動生成規則、oracle・feedback・ログなど個別領域の正式な定義だけを確認したいときは、該当する正本仕様を直接読む。
- ファイル列挙やハッシュ計算など、文書の意味や責務分担を必要としない機械的処理だけを行うとき。

## hash
- 8ef4acfec44388ae113e9bf3d2ff76eb468f6785e10b83792f66da167868e7ad

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
