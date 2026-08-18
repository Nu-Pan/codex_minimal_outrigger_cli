# `edit`

## Summary
- `fork` は現時点で本文ファイルを含まない空のディレクトリで、将来ファイルが追加された場合に内容や用途を確認するための入口です。
- `launch_exec.py` は `cmoc oracle edit` が起動する本命 agent と仕様削減 agent の `codex exec` パラメータを構築します。oracle 編集の起動条件、prompt 構成、権限・作業ルート・モデル・推論強度・初回 indexing 設定を確認または変更するときの入口です。prompt の共通構造は `complete_prompt`、agent call の基本型は `oracle.acp_builder.basic`、編集対象の仕様は対象 oracle file を直接確認します。

## Read this when
- `cmoc oracle edit` の agent call 起動パラメータや oracle 編集用 prompt の埋め込み指示・アクセス権限・作業ディレクトリ・indexing 設定を調査または変更するとき。
- `fork` 配下にファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- oracle file 編集用 prompt の共通構造だけを確認したいときは `complete_prompt` を直接読む。
- agent call の基本的な型や enum だけを確認したいときは `oracle.acp_builder.basic` を直接読む。
- oracle file の編集対象や仕様そのものを確認したいときは、起動パラメータ定義ではなく対象の oracle file を直接読む。
- `fork` 配下の具体的なファイルを直接確認できるときは、空ディレクトリの案内だけを読む必要はない。

## hash
- ad854f6ac6efbc1450c078ed5c12a136fec21efc91c4626b3dda4327dd238a1b

# `investigation`

## Summary
- `cmoc oracle investigation` の調査担当 TUI を起動するための入口。ユーザー指示を調査対象として完全プロンプトに組み込み、oracle 専用の読み取り専用設定、モデル、推論強度、作業ディレクトリ、インデックス事前処理を含む起動パラメータを構築する。

## Read this when
- oracle investigation の調査起動を変更・確認するとき
- ユーザー指示から調査用完全プロンプトと TUI 起動設定がどう構成されるかを確認するとき

## Do not read this when
- 完全プロンプトの共通生成規則だけを確認したいときは、プロンプト構築側を直接読む
- ACP の基本パラメータ型やリポジトリパス解決だけを確認したいときは、それぞれの定義元を直接読む

## hash
- b3d2f2eed082196703d0a1d75e6f337485d09a9dd9022d400667b06280e3bc93

# `review`

## Summary
- oracle review の所見生成・検証・判定・統合に用いる JSON Schema と agent call 構築実装をまとめたディレクトリ。各ファイルは、所見の列挙、妥当性の擁護・反証、採否判定、重複や矛盾の整理という個別処理への入口を提供する。

## Read this when
- oracle review で新規所見を列挙するとき
- 既存所見の妥当性を擁護または反証する理由を生成するとき
- 個別所見の採否判定や所見リストの統合処理を確認・変更するとき
- これらの agent call の prompt、Structured Output schema、モデルや worktree などの起動設定を確認するとき

## Do not read this when
- oracle review の全体実行制御や所見の保存処理だけを確認するとき
- レビュー対象の oracle file や realization の内容そのものを調査するとき
- 共通の prompt 生成、agent call 型、パスコンテキストの仕様を確認するとき
- 個別処理の出力項目や JSON schema だけを確認するときは、対応する schema ファイルを直接読むとき

## hash
- df2e0b8568bae112a72d581d9a410d8c0ae47af313470a9574814c45f899fb0b
