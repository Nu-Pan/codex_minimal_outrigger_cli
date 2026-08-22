# `acp_builder`

## Summary
- AIエージェント呼び出し用の AgentCallParameter 定義と、用途別の起動設定・プロンプト・Structured Output 契約をまとめるディレクトリ。共通パラメータ、feedback issue 判定、INDEX.md エントリー生成、oracle の edit/investigation/review、quota probe、realization、session conflict 解消、TUI 起動の各入口を扱う。

## Read this when
- AIエージェント呼び出しのモデル、推論強度、ファイルアクセス、cwd、prompt、preflight、Structured Output 設定を用途別に確認・変更するとき
- oracle、realization、indexing、feedback、session、tui など特定の agent call 経路の起動条件や責務の入口を探すとき
- 用途別の AgentCallParameter や出力契約のどの下位対象を読むべきか判断するとき

## Do not read this when
- 具体的な realization 実装・テスト、oracle file の正本仕様、既存 INDEX.md の内容、TUI の画面表示など、起動パラメータ以外の実体を確認するとき
- 共通の prompt 構築、パス解決、AgentCallParameter 型、構造化文書レンダリングの実装を直接確認したいとき
- 特定の下位処理の詳細な prompt、実装、出力 schema が既に分かっており、その対象を直接読む方が適切なとき

## hash
- bb6bc93774a13f548f61085450eaf0c36013f2fa89d2a717d745ee22efb7fdb8

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
- `oracle/src/oracle/prompt_builder` は、agent call に渡すプロンプトを組み立てる実装の入口である。プレースホルダー型、完全プロンプトの統合、エディタ入力文面、oracle／realization の説明部品、各種 prompt policy builder を扱う。
- 完全プロンプトの構成、policy の統合、placeholder 定義の競合処理を確認・変更するときは `complete_prompt.py` を読む。
- プレースホルダー名と実パス・文字列の対応型を確認するときは `basic.py` を読む。
- エディタ経由のユーザー入力ファイルの初期表示文面やテンプレート埋め込みを確認するときは `editor_input.py` を読む。
- oracle／realization の説明、分類規則、work-root の埋め込みを確認するときは `parts` を読む。
- agent call に適用される policy の種類や、file access・feedback reporting・INDEX.md ルーティングなどの規定生成を確認するときは `policy` を読む。

## Read this when
- agent call 用プロンプトの組み立てや、prompt-builder の責務分担を調査・変更するとき。
- 完全プロンプトへ policy、補助プロンプト、目的、placeholder 定義を組み込む経路を確認するとき。
- oracle／realization の説明や分類規則を prompt-builder 側で確認するとき。
- agent call 向けの共通または個別 policy の生成方法を確認するとき。

## Do not read this when
- 個別の oracle 文書・実装・テストの内容を確認したいだけのとき。
- Structured Document の要素定義やレンダリング仕様そのものを確認したいとき。
- prompt-builder を利用して生成された最終プロンプトの内容だけを確認したいときは、呼び出し元または生成対象を直接読む。

## hash
- 32d0e60edb774a6984bbb467e24f5742423716521629fd772c5c8e32ce548777
