# `acp_builder`

## Summary
- AI コーディングエージェント呼び出し用の oracle src を収める領域。共通の呼び出しパラメータ定義に加え、TUI、indexing、feedback、oracle 各処理、realization 追従、session join の prompt・実行条件・Structured Output 契約を構築する実装への入口。
- 配下の各サブディレクトリは用途別の agent call builder と schema をまとめており、対象コマンドの起動パラメータや prompt 構成を調査するときに、該当する下位領域へ進む。

## Read this when
- AI エージェント呼び出しの共通パラメータ、モデル区分、推論強度、ファイルアクセスモード、作業ディレクトリ、indexing preflight の定義を確認するとき。
- 特定の cmoc サブコマンドに対応する agent call の prompt、実行条件、Structured Output schema の構築箇所を特定するとき。
- TUI、indexing、feedback、oracle、realization、session join のいずれかの agent call builder を変更・調査するとき。

## Do not read this when
- 実際の cmoc サブコマンドの実行フローや agent call の起動処理そのものを調査するときは、呼び出し側や実行基盤を直接読む。
- prompt の共通構造・レンダリング仕様だけを確認するときは、共通 prompt builder を直接読む。
- 個別の oracle file、realization file、Git 操作、レビュー基準の内容を確認するときは、それぞれの対象ファイルや正本仕様を直接読む。

## hash
- f3216980016e702b4d2b2d26542dd692239b2b6d24c6079c1a9653808c09fc86

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
- cmoc の oracle src にある共通基盤を扱うディレクトリ。リポジトリ設定、root と worktree のパス導出、Standard/Requirement の規範モデル、StructDoc の Markdown 変換と検証を提供し、それぞれの実装を読むための入口になる。

## Read this when
- cmoc の共通設定や Codex CLI・oracle review の設定構造を確認するとき。
- agent call の cwd、各種 root、placeholder、worktree 境界の導出やパス変換を調査するとき。
- Standard/Requirement のモデルや StructDoc の構造化・Markdown 変換・参照検証を確認するとき。

## Do not read this when
- 個別の CLI サブコマンド、agent call の具体的なプロンプト生成、または共通モデルを利用する呼び出し側だけを調査するとき。
- 永続化された設定 JSON の生成・同期・doctor の実装、列挙値の定義、個別の規範本文、既存テスト、開発環境の実行手順を直接確認するとき。

## hash
- 858d9da7a853f45063fa924c2c396aa54e1546f33a28a1268d283fb4834dba05

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
