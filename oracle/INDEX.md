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
- agent call の共通パラメータ型とファイルアクセスモード、および quota probe・indexing・feedback・oracle・realization・session・TUI など用途別 builder の入口。
- prompt の構成・policy・placeholder・エディタ入力を組み立てる部品と、agent call 用 Structured Output schema の定義。
- 設定値、作業ディレクトリや repository・run のルート解決、root placeholder、構造化文書の Markdown レンダリングを担う基盤実装。

## Read this when
- agent call の共通設定、アクセスモード、作業ディレクトリ、モデルや並列実行に関する実装を確認するとき。
- 特定用途の agent call builder、prompt policy・部品、Structured Output schema、feedback 入力契約の入口を探すとき。
- agent call で使うパスの導出・placeholder 解決や、構造化文書を Markdown 化する処理を確認するとき。

## Do not read this when
- 特定の agent call の prompt、出力契約、または個別業務処理の詳細だけを確認したいときは、該当する下位対象を直接読む。
- oracle・realization・feedback・session などの具体的な業務処理や保存手順だけを調べたいとき。
- Codex CLI 自体の実行挙動や、永続化設定ファイルを人手で編集する方法だけを確認したいとき。

## hash
- 8e9d32dcf135652a9dedc21690ecf798e779d58df42e49b33a1de9abf876b830
