# `edit`

## Summary
- oracle 編集フローに関する起動定義を扱うディレクトリです。空の `fork` と、`cmoc oracle edit` の2段階 agent call の固定パラメータを構築する `launch_exec.py` を入口として、oracle 編集の起動条件や編集・仕様削減フローの設定を確認します。

## Read this when
- `cmoc oracle edit` の本命編集呼び出しまたは成功後の仕様削減呼び出しの起動パラメータを変更・確認するとき。
- ユーザー指示、oracle 専用ファイルアクセス、完全 prompt の保存、推論設定、インデックス事前処理の組み合わせを確認するとき。
- このディレクトリに追加されたファイルの内容や用途を確認するとき。

## Do not read this when
- oracle file の具体的な編集規則や正本仕様そのものを確認したいときは、関連する oracle file を直接読む。
- `codex exec` の一般的な実行機構や共通データ型を確認したいときは、共通実装や prompt builder を直接読む。
- このディレクトリ配下の具体的なファイルを直接確認できるとき。

## hash
- c90bd10a113230da106132b4a51fd62339b459c35acee3274633fb5d50ab30e2

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
