# `doc`

## Summary
- cmoc のアプリケーション仕様、設計判断資料、開発ルールを横断して参照するための上位入口。
- 自動補完、Codex CLI、provider、ログ、状態管理、feedback、run/session、サブコマンド、割り込み、通知などの個別仕様へ進むための構成を示す。
- session・run の branch、commit、worktree の関係を確認する仕様への入口を含む。
- 採用しなかった設計案やその理由を確認する検討資料への入口を含む。
- Python 実装、CLI 設計、開発環境、テストの規則を目的別の下位文書へ案内する入口を含む。

## Read this when
- cmoc のアプリケーション仕様について、複数の機能領域にまたがる正本仕様の所在や参照入口を判断するとき
- 自動補完、Codex CLI 呼び出し、provider、ログ、feedback、state、editor input、run/session、サブコマンド、割り込み、timestamp、通知などの仕様から読む対象を選ぶとき
- session fork、run の開始・分離・join、apply の追従対象、run report の commit 基準を確認するとき
- branch・commit・linked worktree の役割や、cmoc 管理 branch と通常の git branch を区別するとき
- 不採用となった設計案の理由や、設計判断の背景を調べるとき
- Python 実装、CLI 設計、開発環境、テストについて、確認すべき開発ルールの領域を判断するとき

## Do not read this when
- 単一の機能やサブコマンドの具体的な挙動、状態 schema、prompt、実装、または exact な契約を直接確認したいときは該当する個別仕様を読む
- run state や report の状態遷移そのものを確認したいときは該当する状態仕様を読む
- oracle の変更手順や設計責務、test の実行規則を直接確認したいときは該当する個別仕様を読む
- 現行の正本仕様や具体的な実装を確認したいときに、採用しなかった設計案の資料を読む
- 特定の Python コーディング規則、CLI 設計規則、開発環境、テスト要件、またはテスト実行手順が明確な場合は該当する下位文書を直接読む
- INDEX.md の生成規則や routing 情報の一般規約だけを確認したいときは indexing の仕様を読む
- 対象仕様群に含まれない実装コード、実行結果、診断ログだけを調べるとき

## hash
- 747ab3a417cefc4688c8f2ec7801768e03e22d6e56d5e24f51252864f426adb7

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
