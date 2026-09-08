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
- agent call の共通パラメータと用途別 ACP builder をまとめる領域。quota probe、session join、TUI、indexing、oracle、realization、feedback の構築入口を扱う。
- agent へ渡す prompt を組み立てる領域。基本 prompt、policy、parts、editor input handoff、oracle・realization 関連の指示を扱う。
- agent call を支える補助モデルの領域。パス解決、cmoc 設定、構造化文書、エディタ入力上書き、feedback reporter input を扱う。

## Read this when
- agent call の共通入力契約や file access mode を確認するとき。
- 用途別の ACP builder の入口を探すとき。
- prompt の基本構成、policy、parts、または editor input handoff の構築責務を確認するとき。
- パス placeholder の解決、cmoc 設定、構造化文書のモデルを確認するとき。
- feedback issue の報告入力や remediation 用の agent call 契約を確認するとき。

## Do not read this when
- 特定用途の prompt や Structured Output schema の詳細だけを確認したいときは、該当する下位ディレクトリまたは schema を直接読むとき。
- agent call の実行処理や Codex CLI の実際の挙動を調査したいとき。
- 設定保存、feedback 受付、oracle・realization の編集など、個別処理の実装だけを確認したいとき。

## hash
- eeb1fd7c1517b91faeca8d03ef33dd814546fe673b79bbec66e144013544ea78
