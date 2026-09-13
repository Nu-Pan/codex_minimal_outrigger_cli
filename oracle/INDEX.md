# `doc`

## Summary
- cmoc のアプリケーション仕様を収録する正本文書群への入口。CLI 共通規約、サブコマンド、session・run lifecycle、feedback、ログ、通知、エディタ入力など、アプリケーション全体の責務と境界を確認できる。

## Read this when
- cmoc のアプリケーションレベルの正本仕様を探しており、複数機能にまたがる責務分担や参照先を確認するとき。
- CLI 実行、workflow、session／editing run、feedback、出力・ログ、通知、自動補完、prompt editor などの仕様を確認・変更するとき。
- 個別機能の詳細仕様へ進む前に、共通契約や機能間の境界を把握するとき。

## Do not read this when
- 個別の実装 module、テスト、実行結果、診断ログそのものを調査・変更するとき。
- 特定の schema、prompt literal、設定 field、内部 API など、より詳細な正本を直接確認すべきとき。
- 一般的な開発手順や、アプリケーション仕様に関係しない資料だけを探しているとき。

## hash
- 33f39c95c9671dfcdaa987e3a36b11185c6a02fcdc8fc82ff6bfc0d7a67765c2

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
