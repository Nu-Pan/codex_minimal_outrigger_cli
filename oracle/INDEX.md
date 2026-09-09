# `doc`

## Summary
- cmoc の正本文書・開発規則・branch model・設計上の不採用案を、アプリケーション仕様、開発ルール、branch 関係、検討資料の責務別に振り分ける文書群への入口。現行仕様と実装に追従する規則、または過去の設計判断の背景を参照する際の起点となる。

## Read this when
- cmoc の仕様・開発規則・branch model・設計判断の背景のうち、どの文書群を読むべきか切り分けるとき。
- 複数の領域にまたがる調査や変更で、現行の正本仕様、開発上の規則、Git の概念、採用しなかった案の境界を確認するとき。

## Do not read this when
- 参照対象の仕様文書、開発規則、branch model、または検討資料がすでに特定できており、その本文だけを確認したいとき。
- 実装コード、個別の oracle／realization file、または特定 agent call の厳密な builder・schema を直接調べるとき。

## hash
- b3d44843265139beb73a7d08bfd6c1ff3a64b164c740395084b0a596820926ba

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
