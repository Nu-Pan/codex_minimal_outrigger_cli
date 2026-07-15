# `doc`

## Summary
- cmoc のアプリケーション仕様断片を集約するディレクトリ。CLI 共通基盤、実行環境、ログ、状態管理、プロンプト、run 隔離、session、サブコマンド仕様など、機能別の正本文書へ進むための入口。
- branch と worktree による session/run の境界、採用しなかった設計案、Python 開発規則など、アプリケーション仕様を横断して確認する文書も含む。

## Read this when
- cmoc のアプリケーション仕様から、対象機能の正本文書やサブコマンド仕様を探すとき。
- CLI 共通基盤、session/run、branch、設計判断、Python 開発規則など複数領域にまたがる仕様の入口を確認するとき。
- 現在の採用仕様だけでなく、不採用案の理由や開発時の共通規則を確認するとき。

## Do not read this when
- 実装コードやテストコードの具体的な挙動を確認するときは、対応する src または test 配下を読む。
- 対象機能の仕様が明確な場合は、このディレクトリ全体ではなく該当する個別文書へ直接進む。
- oracle と realization の一般定義や記述標準、INDEX.md の生成・更新規則だけを確認するときは、それぞれの専用文書を読む。

## hash
- 361092b8354964e4c2bfb12ec1f9cc5e8def8ad81957dfd7ea8a892552634a87

# `src`

## Summary
- ACP builder の呼び出し設定・用途別 Structured Output 契約、設定／パス／構造化文書モデル、prompt 合成と規範文面の正本ソースを扱うディレクトリ。下位の acp_builder、other、prompt_builder から個別領域へ進む入口。

## Read this when
- agent 呼び出しパラメータ、モデル・推論設定、ファイルアクセスモード、Structured Output schema の正本を確認・変更するとき。
- cmoc の設定、ルートパス解決、構造化 markdown、Standard モデルの正本を確認するとき。
- oracle／realization／review／index の規範や、それらを prompt に組み込む処理を確認するとき。

## Do not read this when
- サブコマンドの実行フロー、CLI 入出力、差分適用、競合解消の realization 実装を調査するとき。
- prompt の合成順序や個別タスクの実行制御だけを調査するときは、下位の prompt_builder または該当する acp_builder の個別ファイルへ直接進む。
- 個別の oracle 文書、realization 側の実装・テスト本文だけを確認するとき。

## hash
- 14478f6f2108d1e6eefa8d00598fda26d557c34b54aff984bb23baa0ccd39e41
