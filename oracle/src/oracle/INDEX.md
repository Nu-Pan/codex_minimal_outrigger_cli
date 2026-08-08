# `acp_builder`

## Summary
- 対象ディレクトリには、各種 cmoc フローで AI Agent 呼び出しに使う正本ソースが配置されている。共通の呼び出しパラメータ定義、feedback・indexing・oracle・realization・session・tui など用途別の prompt／起動設定、Structured Output schema の定義が下位要素への入口となる。

## Read this when
- cmoc の特定フローで使われる AI Agent 呼び出しの prompt、モデル・推論設定、アクセス権限、作業ディレクトリ、実行前設定を調査・変更するとき。
- Agent call の出力契約や用途別の Structured Output schema の定義を確認するとき。
- 共通パラメータ定義または feedback、indexing、oracle、realization、session、tui の呼び出し設定の入口を探すとき。

## Do not read this when
- 通常の realization 実装・テストや CLI／TUI の実行フローそのものを調査するときは、対応する realization 側または呼び出し側を直接読む。
- 正本仕様そのもの、Codex CLI sandbox・permission profile の一般規則、共通 prompt 構築の詳細だけを調査するときは、それぞれの専用仕様・実装を直接読む。
- 特定用途の prompt や schema 以外の agent call を調査するときは、該当する下位ディレクトリまたは共通定義を直接読む。

## hash
- b035301cb336018a668b3f20fcad66aa0c4fc4ddf0a8ec9c30a1d86b6b47e214

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- cmoc の設定・パス解決・規範・構造化文書を扱う基礎モデル群を収録するディレクトリ。設定値や root 導出、Standard の文書化、Markdown 構造化処理の実装へ進む入口となる。

## Read this when
- CmocConfig の設定項目や永続化構造を確認するとき
- agent call の cwd・root・placeholder に関するパス解決を調査するとき
- Standard や Requirement のモデル、または構造化 Markdown 生成の基盤を確認するとき

## Do not read this when
- CLI サブコマンドの実行フローや設定ファイル同期など、利用側の処理だけを調査するとき
- ModelClass、ReasoningEffort、StructDoc など個別モデル自身の定義だけを確認するとき
- 個別の規範本文、テスト、開発環境の実行手順を確認するとき

## hash
- cc3b77dc08ddbb1b12d585f5e63b2630c6e225539a7714dd86f54d66fd8d2db0

# `prompt_builder`

## Summary
- エージェント用プロンプトを構成する部品群をまとめるディレクトリ。oracle・realization 規範、アクセス制約、ルーティング、feedback 報告などの共通規則を扱い、個別の prompt builder 部品へ進む入口となる。

## Read this when
- プロンプトに組み込む共通規則の責務や適用条件を確認・変更するとき。
- oracle・realization、ファイルアクセス、ルーティング、feedback 報告に関する prompt builder 部品を選ぶとき。

## Do not read this when
- プロンプト全体の組み立て順序やプレースホルダ定義を確認したいときは、親ディレクトリの中核ビルダーや型定義を直接読む。
- エージェント入力の初期テンプレートや記入ガイドラインを確認したいときは、入力生成側を直接読む。
- 特定の共通規則の実装詳細を確認したいときは、配下の対応する部品へ直接進む。

## hash
- 0fd5b32e6b44d4663af557871612c48d95454a28f294959882cc86cd37d48583
