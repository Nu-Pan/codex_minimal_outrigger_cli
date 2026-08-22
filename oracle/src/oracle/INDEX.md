# `acp_builder`

## Summary
- AIコーディングエージェント呼び出しの共通パラメータ定義と、用途別の agent call 構築実装を扱うディレクトリ。indexing、oracle、quota probe、realization、session、TUI の prompt、起動条件、アクセスモード、作業ディレクトリ、Structured Output 契約へ進む入口となる。

## Read this when
- AgentCallParameter の共通契約、モデル、推論強度、ファイルアクセス、prompt、Structured Output schema、cwd、preflight 設定を確認するとき
- INDEX.md エントリー生成、oracle の用途別 agent call、Codex CLI quota probe、realization の追従・refactor、session join の conflict 解消、cmoc tui の起動設定を調査・変更するとき
- 用途別 agent call の prompt、起動条件、権限、出力契約の入口を特定するとき

## Do not read this when
- 既存 INDEX.md のルーティング内容だけを確認したいとき
- モデル名やバックエンド固有の解決処理、共通 prompt 生成、path model、構造化文書などの共通仕様だけを確認したいときは、それぞれの定義元を直接読む
- realization の通常の implementation・test・ancillary、session join の通常処理、TUI の画面表示や対話操作など、個別の実行処理を確認したいとき
- 具体的な issue 内容、report cut reference、raw log、個別のレビュー対象や所見判定など、用途別定義の範囲外のデータや処理を調べるとき

## hash
- be850c993e27a952760282e707918a5ae57d677bcd25dd0a0139f3d21cae5ff5

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
- プロンプト構築に関する共通部品と入口をまとめたディレクトリ。placeholder の型、完全 prompt の組み立て、エディタ入力文面、oracle・realization の説明部品、各種 policy prompt を扱う。個別実装や規定の詳細へ進むための入口となる。

## Read this when
- 完全 prompt の構造や placeholder 統合規則を確認したいとき。
- oracle・realization の分類や責務説明を prompt に組み込む処理を調査するとき。
- agent call に適用する policy prompt の生成内容や責務分担を確認したいとき。
- エディタ経由の入力文面や、構造化された prompt 部品の組み立てを変更するとき。

## Do not read this when
- 個別 policy の具体的な規定だけを確認したいときは、対応する policy モジュールを直接読む。
- prompt-builder の共通型や構造化ドキュメント要素の定義だけを確認したいときは、それぞれの定義元を直接読む。
- 具体的な CLI や agent call の利用動作だけを調査したいときは、呼び出し側を直接読む。
- 個別の oracle・realization ファイルの仕様や実装内容を確認したいときは、対象ファイルを直接読む。

## hash
- 4e6a03a5605200fa0e54f50bc0e96b04c6c11b001a2cd78edf1c77021429a139
