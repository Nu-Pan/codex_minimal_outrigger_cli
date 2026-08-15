# `edit`

## Summary
- `cmoc oracle edit` における本命 agent call と、成功後の仕様削減 agent call の起動パラメータ構築を扱うディレクトリです。ユーザー指示の prompt 組み込み、oracle-only の書き込み範囲、モデル・推論設定、作業ディレクトリ、Structured Output、索引付け前処理など、oracle 編集起動の具体的な設定を確認する入口になります。配下には現時点で本文ファイルを含まない空の領域もあります。

## Read this when
- `cmoc oracle edit` の本命または仕様削減 agent call の起動パラメータを変更・確認するとき
- oracle 編集用 prompt の構成、ユーザー指示の埋め込み、ファイルアクセスモード、起動前索引付け設定を確認するとき
- 本命成功後の仕様削減 call に渡す参照境界や、既存未コミット差分の扱いを確認するとき

## Do not read this when
- oracle file の編集ルールや仕様削減そのものの正本規範を確認する場合
- 一般的な agent call パラメータや共通 prompt 構築の挙動だけを確認する場合
- `cmoc oracle edit` 以外のコマンドの起動パラメータを確認する場合

## hash
- d545d4ae86932f4ac05a41e1a58013be44e8fc203295e054dc7b66e027481ac6

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
