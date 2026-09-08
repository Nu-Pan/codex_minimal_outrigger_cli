# `doc`

## Summary
- cmoc の正本仕様・開発規則・設計判断資料を、branch model、app_spec、dev_rule、considered_alternative の領域別に案内する文書群への入口。
- CLI 実行、session/run、Codex CLI、ログ、feedback、oracle/realization、状態管理などの実行契約は app_spec 配下へ、Python 開発・設計・テスト・環境規則は dev_rule 配下へ進む。
- 採用しなかった設計案やその理由を確認する場合は considered_alternative 配下へ、session・run の branch、commit、worktree の関係を確認する場合は branch_model.md へ進む。

## Read this when
- cmoc の正本仕様、開発規則、branch・commit・worktree のモデル、または不採用設計の資料がどの領域にあるかを判断するとき。
- CLI 実行や session/run のライフサイクル、Codex CLI 呼び出し、ログ、feedback、oracle/realization の仕様入口を探すとき。
- Python 開発、CLI 設計、開発環境、テスト要件・実行手順の正本文書を探すとき。
- 現行仕様ではなく、過去に検討された代替案や不採用理由を確認するとき。

## Do not read this when
- 特定の CLI 実行契約、状態遷移、prompt、Structured Output、ログ、feedback、テスト規則などの詳細が分かっており、対応する app_spec または dev_rule の個別文書を直接読めるとき。
- branch・commit・worktree の具体的な関係が明確で、branch_model.md だけを直接確認すればよいとき。
- 不採用案の具体的な判断理由が明確で、considered_alternative 配下の該当文書を直接確認するとき。
- 実装コード、oracle file、realization file、または INDEX.md の本文だけを確認したいとき。

## hash
- 4c30d2cb31c3c9e0eb77b8752114ccdea843f2e37d92d406dba2443aeaaf314f

# `src`

## Summary
- cmoc の agent call に渡すパラメータ、ファイルアクセスモード、実行先コンテキストを定義する実装領域。
- agent call の用途別に、oracle・realization の編集、レビュー、適用、所見処理、feedback、indexing、session join、TUI などの prompt と Structured Output 契約を構成する。
- prompt の共通規定、oracle・realization の基本説明、routing、設定、パス解決、構造化文書のレンダリングを下位実装へ提供する入口。

## Read this when
- cmoc の agent call の入力パラメータ、ファイルアクセスモード、Structured Output schema、実行コンテキストの構成を確認するとき。
- oracle・realization の編集・レビュー・適用、feedback remediation、index entry 生成、session join、TUI など特定用途の agent call がどの prompt builder と結び付くかを調べるとき。
- 複数の agent call に共通する prompt policy、oracle・realization の基本知識、routing、path model、設定モデル、構造化文書の生成処理を確認するとき。

## Do not read this when
- oracle file や realization file の人間向け正本仕様そのものを確認するときは、対応する仕様文書または対象ファイルを直接読む。
- 特定用途の prompt、出力契約、または実行処理だけを確認したいときは、該当する用途別の下位領域へ直接進む。
- Codex CLI や agent call の共通実行機構そのものの実際の挙動を確認したいときは、実行機構側の実装や仕様を直接読む。

## hash
- 6681788c2c01203045116d052623f65b8c0336cd9c5b8ed7227731ec1ca20372
