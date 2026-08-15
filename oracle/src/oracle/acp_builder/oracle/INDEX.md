# `edit`

## Summary
- oracle file 編集用の agent call 起動処理を配置するディレクトリです。対話型 TUI の起動パラメータや、編集用 prompt を構築・保存する実装への入口になります。現時点では空のサブディレクトリと、`cmoc oracle edit` の起動パラメータを構築する実装を含みます。

## Read this when
- `cmoc oracle edit` の TUI 起動条件、起動パラメータ、oracle file 編集用 prompt の構築または保存方法を確認・変更するとき。
- oracle 編集 agent call のモデル、推論強度、アクセスモード、作業ディレクトリ、indexing preflight の責務を確認するとき。
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- oracle 編集用 prompt の共通構築規則だけを確認したいときは、prompt builder の実装を直接読む。
- agent call の基本型やアクセスモードの定義だけを確認したいときは、acp builder の基本型定義を直接読む。
- oracle 編集処理の実行本体や TUI UI 自体を調査するときは、それぞれの実装入口へ直接進む。
- このディレクトリ配下の具体的なファイルを直接確認できるときは、ディレクトリ入口を読む必要はありません。

## hash
- ee0fc09fe5574d1bfdb10201b5c6008822b9bdfe4ff76c2737ad9182b2c5277d

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動に必要な固定パラメータと完全プロンプトを構築する入口。ユーザー指示や調査範囲を組み込み、リポジトリルートを作業ディレクトリとして確定し、ログ保存から Codex CLI 起動パラメータ返却までを扱う。共通プロンプト構成、パス解決、ACP 基本型は下位の実装対象へ案内する。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件、モデル・推論設定、ファイルアクセスモード、作業ディレクトリを確認するとき。
- oracle 調査用完全プロンプトへのユーザー指示、調査範囲、目標、ルーティング規則の組み込み方を確認するとき。
- 完全プロンプトのログ保存から TUI 起動パラメータ返却までの処理を追跡するとき。

## Do not read this when
- 一般的な完全プロンプトの構築規則だけを確認する場合。
- エージェント呼び出しパラメータの型や列挙値の定義だけを確認する場合。
- リポジトリルートやエージェント作業パスの解決だけを確認する場合。

## hash
- 653fcb8b663407a6719785b89bf0696112bc449cd7694997749e9df06c0249a2

# `review`

## Summary
- このディレクトリは、oracle review における所見の列挙、妥当性理由・反証理由の検証、採否判定、所見の統合に使う Structured Output schema と agent call 定義をまとめた領域です。各ファイルは、所見処理の契約確認と、その契約に対応する prompt・実行条件の調査への入口になります。

## Read this when
- oracle review の所見を生成・検証・判定・統合する処理の入出力契約を確認するとき
- 所見処理用 agent call の prompt、読み取り範囲、worktree、モデル設定、実行条件を確認または変更するとき
- 所見の妥当性を支持・反証する理由や、重複・矛盾を整理する処理の構造を調査するとき

## Do not read this when
- oracle review の所見処理以外の agent call やサブコマンドを調査するとき
- レビュー対象の oracle file や実装そのものの仕様を確認するときは、対象の仕様・実装ファイルを直接読むとき
- 個別の Structured Output schema や prompt 定義だけを確認すれば足りる場合は、対応するファイルへ直接進むとき

## hash
- c12f226d38c2018bd916db5f72029ff4c27c95e5c4c5da145e936965cb0b3327
