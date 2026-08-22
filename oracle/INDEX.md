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
- cmoc の oracle source を構成する実装・設定・agent call 定義の領域。`acp_builder`、`feedback`、`other`、`prompt_builder` の各下位領域へ進むための入口であり、agent 呼び出しパラメータ、feedback 入力契約、設定・パス・構造化文書モデル、完全 prompt と各種 policy の実装を扱う。

## Read this when
- cmoc の oracle source 内で調査・変更すべき責務が `acp_builder`、`feedback`、`other`、`prompt_builder` のどれに属するか判断するとき
- agent call 構築、feedback reporter 入力契約、設定・パス・文書モデル、prompt policy の実装群を横断して確認するとき

## Do not read this when
- 対象の下位ディレクトリが特定できており、その具体的な実装・スキーマ・prompt 定義を直接確認すればよいとき
- oracle の正本仕様、realization 実装、通常の CLI 実行や TUI 表示の挙動を確認するとき
- 下位要素の具体的な責務や Structured Output の詳細を確認したいときは、対応する `acp_builder`、`feedback`、`other`、`prompt_builder` の下位対象を直接読む

## hash
- 3c98367bc4b6c3b8e635a5495ad2371534398c1af7ae4b830ff72eb40cad265c
