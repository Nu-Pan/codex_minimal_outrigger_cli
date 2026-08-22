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
- oracle と realization の基本概念・分類規則を説明する prompt-builder 部品、各種 prompt policy の構築定義、完全プロンプト生成、エディタ入力初期文面、プレースホルダ型定義を扱うディレクトリ。個別実装の責務を確認するための入口として、parts・policy と各 Python モジュールを参照する。

## Read this when
- oracle／realization の責務境界、分類条件、配置パス、work-root の扱いを確認するとき
- agent prompt に組み込む policy の責務や生成内容、関連する横断的な規定の入口を探すとき
- 完全プロンプトの構成順序、policy の統合条件、placeholder 定義の重複・競合処理を確認するとき
- エディタ経由のユーザー入力ファイルの初期文面やテンプレート埋め込みを確認するとき
- placeholder 名と文字列・Path の置換先を共通表現で扱う型を確認するとき

## Do not read this when
- 個別の oracle／realization 文書・実装・テストの内容そのものを確認したいとき
- 具体的な policy 本文だけ、または prompt 本文の生成手順・置換ロジックだけを確認したいときは、担当する下位モジュールを直接読む
- 構造化ドキュメント要素の定義や Markdown レンダリング仕様だけを確認したいときは、担当する struct_doc 実装を直接読む
- placeholder を使わない処理や、別の設定値の表現だけを確認したいとき

## hash
- ed572460c99cbdb992642de2a2f34027071e3418c44104928df9934146f660fb
