# `doc`

## Summary
- cmoc の正本仕様と開発ルールを収録するドキュメント領域。アプリケーション共通仕様、branch・commit・worktree のモデル、不採用案、Python・CLI・環境・テストに関する開発規約への入口を提供する。
- 共通契約や複数サブコマンドにまたがる仕様は `app_spec`、branch や worktree の関係は `branch_model.md`、不採用案の背景は `considered_alternative`、実装・環境・テストの規約は `dev_rule` へ進む。

## Read this when
- cmoc の正本仕様や開発ルールの対象領域を特定し、適切な下位文書への入口を選ぶとき
- アプリケーション共通契約、branch・commit・worktree、設計上の不採用案、Python・CLI・環境・テスト規約を調査・変更・レビューするとき

## Do not read this when
- 特定サブコマンドや個別仕様の内容が明確で、対応する下位文書を直接読めるとき
- 実装コード、realization、テスト対象、開発環境、テスト実行手順など専用の対象を直接確認するとき
- INDEX.md の生成・更新処理自体を調べるときは、indexing の正本仕様を直接読む

## hash
- d5cd194fe37ff810e996d87837f1dfefb47da6c2f4c3220beb57553115cf0a9a

# `src`

## Summary
- `oracle/src` は、cmoc の agent call 構築と prompt 構築を実装する source 層の最上位入口。
- agent call の論理パラメータ、モデル・推論強度・ファイルアクセス、quota probe などは `acp_builder` 配下で扱う。
- feedback の入力契約は `feedback`、設定・モデル対応・パス解決・構造化文書は `other`、prompt の組み立てと各種ポリシー文面は `prompt_builder` 配下で扱う。
- 具体的な処理やデータ構造を調べる場合は、責務を特定した下位領域または実装ファイルへ進むための入口として用いる。

## Read this when
- cmoc の agent call 構築、prompt 構築、feedback 入力契約、設定・パス・構造化文書の実装領域を特定するとき
- `oracle/src` 配下で、`acp_builder`、`feedback`、`other`、`prompt_builder` のどこを読むべきか判断するとき
- source 実装の責務分担や、関連する下位対象への入口を確認するとき

## Do not read this when
- 具体的な処理やデータ構造が既に特定できており、対応する下位領域または実装ファイルを直接読めるとき
- oracle の正本仕様・実装構築定義全体を調べる必要がなく、通常の CLI 実行制御や別のドキュメント領域を直接調べるとき

## hash
- afffa11cc3f1a1aa2190fc16d9040518f5684caeb5e2317353197e770fae4d2e
