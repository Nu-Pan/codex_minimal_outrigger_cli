# `__init__.py`

## Summary
- oracle 系サブコマンドをまとめる package の境界を示す。oracle サブコマンド群への入口として扱う。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。

## Do not read this when
- 個別の oracle サブコマンド実装の詳細を確認するとき。

## hash
- 2c8110c7811042f7162e1264e7027bb2d801f4687eb66f48f1668402c8eeb0df

# `edit`

## Summary
- 編集関連の実装ファイルを含まない空のディレクトリです。現時点で下位要素へのルーティング先はありません。

## Read this when
- このディレクトリに編集関連ファイルが追加されたか確認するとき。

## Do not read this when
- Oracle サブコマンドの実装を調査するとき。親ディレクトリの実装ファイルを直接確認してください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `edit.py`

## Summary
- `cmoc oracle edit` サブコマンドの実行入口と本体を担い、エディタ入力・prompt 構築・indexing・起動前提の検査を経て、固定設定の Codex exec を最大 2 回直列実行し、各回の状態を primary report に反映する。
- oracle file の編集処理そのものや prompt の定義ではなく、CLI runtime の実行順序、main worktree・active session の前提検査、2 回の agent call の制御を確認したい場合の入口である。

## Read this when
- `cmoc oracle edit` の実行フロー、agent call の回数・順序、1 回目失敗時の扱いを確認したいとき。
- oracle 編集指示の入力確定から indexing、起動前提検査、primary report の agent call 状態更新までの CLI 統合を調べるとき。
- main worktree と `cmoc/session/` の active session を要求する起動条件を確認または変更するとき。

## Do not read this when
- oracle edit に渡す prompt の正本仕様や編集境界を確認したいだけなら、`oracle/doc/app_spec/oracle_edit.md` と対応する builder を直接読むとき。
- エディタ入力の保存・抽出・cleanup の共通 lifecycle を調べる場合は、`commons.prompt_editor_input` を直接読むとき。
- oracle investigation の read-only TUI フローを調べる場合や、Codex exec の一般的な起動実装を調べる場合は、それぞれの専用実装を直接読むとき。

## hash
- 4e7890ad56ee0266c7c51d1f8051116de45af4f2936826ddae91b64ee3b1cc4a

# `investigation.py`

## Summary
- `cmoc oracle investigation` の CLI 実行入口と本体を提供する。インデックス前処理・実行状態管理を設定し、oracle 調査指示の編集用プロンプトを準備・収集したうえで、調査契約付きの read-only Codex TUI を起動する。

## Read this when
- `cmoc oracle investigation` の実行手順、調査指示の入力編集、または Codex TUI 起動までの流れを確認・変更するとき。

## Do not read this when
- oracle investigation 用の起動パラメータ生成規則だけを確認したいときは、`acp/builder/oracle/investigation` 配下を直接読む。
- 共通の CLI ランタイム、プロンプト編集、またはインデックス前処理の実装だけを確認したいときは、それぞれの共通モジュールを直接読む。
- `cmoc oracle edit` の処理や oracle ファイル編集の挙動を確認したいとき。

## hash
- fb938a9e9ec720dedab2b1590703d0fa62e7affbff17538db7703020ea386b0f
