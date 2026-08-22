# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータ定義と、oracle・realization・feedback・indexing・session・tui・quota probe 用途別 builder の入口をまとめるディレクトリ。
- basic.py はモデルクラス、推論強度、ファイルアクセスモード、prompt、Structured Output schema、cwd、indexing preflight を含む AgentCallParameter 契約を定義する。
- 下位ディレクトリでは、用途ごとの prompt・アクセス制約・モデル設定・出力 schema を構築する。oracle review、realization の apply/refactor、feedback issue 判定、INDEX.md エントリー生成、session join の conflict 解消、TUI 起動を扱う。

## Read this when
- AgentCallParameter の共通契約や論理的なモデル・推論・ファイルアクセス設定を確認するとき
- 特定の cmoc 機能に対応する agent call builder の所在と、下位の用途別定義へ進む入口を判断するとき
- oracle、realization、feedback、indexing、session join、tui の agent call の prompt・起動設定・Structured Output 契約を横断して調査するとき

## Do not read this when
- 特定用途の prompt 構築や実行制御だけを確認したいときは、対応する下位ディレクトリまたは builder を直接読むとき
- 実際のモデル名やバックエンド固有の解決処理を確認したいときは realization 側の実装を読むとき
- Codex CLI の sandbox や oracle・realization の正本仕様を確認したいときは、対応する oracle 文書を読むとき

## hash
- e7dd952adee515b5bed502af055695f4d777bd687a79431fed01d6cad5d814b4

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
- 対象ディレクトリは、cmoc の設定モデル、パスモデル、構造化 Markdown 文書ノードの実装を扱う。設定項目や既定値、root placeholder と worktree/repository root の解決、文書ノードの Markdown レンダリング規則を確認するための入口である。

## Read this when
- cmoc の設定項目・既定値・シリアライズ構造を変更または確認するとき
- root placeholder、agent call の作業ルート、worktree/repository root の解決規則を確認するとき
- 構造化文書ノードや参照タグを Markdown にレンダリングする挙動を変更または確認するとき

## Do not read this when
- Codex CLI の呼び出し処理や個別 CLI 機能の実装責務を確認したいとき
- oracle review のレビュー処理や所見生成ロジックを確認したいとき
- 設定ファイルの保存内容や人手による調整結果だけを確認したいとき
- Markdown 以外の文書形式や、個別機能におけるパスモデルの利用挙動だけを確認したいとき

## hash
- b97eefaa4d29d7835c2033b91e430e3593bcd5c68643fbc6ef124e09507994df

# `prompt_builder`

## Summary
- prompt-builder 配下の prompt 構築関連ファイルを、役割と探索条件付きで案内するルーティング入口。
- basic.py はプレースホルダ名と文字列・実パスの置換先を表す型定義を扱う。
- complete_prompt.py は policy、prompt、placeholder 定義を統合して完全な agent prompt を構築する中心実装を扱う。
- editor_input.py はエディタ経由で入力するユーザー向け初期文面とテンプレート埋め込みを扱う。
- parts は oracle／realization の分類概念と uncategorised file の判定規則を説明する prompt-builder 部品を扱う。
- policy は agent call 共通の各種 policy 定義と、その責務・確認入口を扱う。

## Read this when
- プレースホルダの型や置換先の表現を確認したいときは basic.py。
- 完全な agent prompt の構築順序、構成要素、policy の追加条件、placeholder の競合処理を確認したいときは complete_prompt.py。
- エディタ入力ファイルの初期文面、記入案内、テンプレートや HTML コメントの構成を確認したいときは editor_input.py。
- oracle／realization の概念、分類、work-root の埋め込み、uncategorised file の判定規則を確認したいときは parts。
- agent call の共通 policy、ファイルアクセス、feedback 報告、INDEX.md、oracle／realization の扱いを確認したいときは policy。

## Do not read this when
- 個別 policy の本文や生成ロジックだけを確認したい場合は policy 配下の該当ファイルを直接読む。
- prompt 本文の生成手順や置換ロジックの詳細だけを確認したい場合は complete_prompt.py。
- placeholder の型だけを確認したい場合は basic.py、実際の値や path context の定義だけを確認したい場合は別の担当実装を読む。
- エディタ入力の初期文面ではなく、完全 prompt 全体や別経路の入力処理を調査する場合は editor_input.py ではなく担当実装を読む。
- oracle／realization の具体的な仕様、実装、テスト内容を確認する場合は parts ではなく該当する oracle／realization ファイルを直接読む。
- prompt-builder の policy 以外の実装やテストの具体的内容を確認する場合は policy ではなく該当対象へ直接進む。

## hash
- 89a1135b95eda3e9a3f7f8578bd8d70535b32fc2fb8e3e00f09e2567d21227fa
