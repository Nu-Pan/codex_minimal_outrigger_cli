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
- oracle の agent call パラメータ、prompt と policy の構築、プレースホルダ定義、ファイルアクセス制約、パスコンテキスト解決を担う実装領域。
- 構造化文書モデルと Markdown レンダリング、editor input handoff、TUI・oracle・realization・feedback・indexing など各処理の呼び出しパラメータ構築への下位入口。

## Read this when
- oracle の agent call 構築定義や Codex CLI 起動パラメータを確認するとき。
- prompt の部品、policy、placeholder、ファイルアクセスモード、routing、feedback reporting の生成を調べるとき。
- agent call の cwd・repo/work/run root 解決や、構造化文書のモデルと Markdown レンダリングを確認するとき。
- editor 経由の入力 handoff、TUI、oracle 編集・調査、realization、feedback、indexing の呼び出し定義を探すとき。

## Do not read this when
- oracle 正本ファイルの具体的な内容や編集手順を確認したいときは、該当する正本ファイルまたは専用処理を直接読む。
- realization の実装本体、feedback の収集・受付処理、または Codex CLI の共通実行挙動だけを調べるとき。

## hash
- eeb1fd7c1517b91faeca8d03ef33dd814546fe673b79bbec66e144013544ea78
