# `acp_builder`

## Summary
- AIコーディングエージェント呼び出し用の論理モデル、推論強度、ファイルアクセス、プロンプト、Structured Output schema、作業ディレクトリなどの AgentCallParameter 定義を扱うディレクトリ。feedback、indexing、oracle、realization、session、tui など用途別の agent call 構築定義への入口を提供する。

## Read this when
- agent call の共通パラメータ契約やモデル・推論・ファイルアクセス設定を確認するとき
- feedback issue 判定、INDEX.md エントリー生成、oracle 操作、realization 反映・refactor、session conflict 解消、TUI、quota probe の起動設定や出力契約を調査・変更するとき

## Do not read this when
- 実際のモデル名やバックエンド固有の解決処理を確認するとき
- oracle や realization の正本仕様・具体的な実装やテストを確認するとき
- 共通 prompt 生成、CLI のサブコマンド解析、TUI の画面処理など、このディレクトリの用途別 agent call 定義に直接属さない処理を確認するとき

## hash
- e83d8d3998bbc8c030f56d4faa50269583ee65f4dff52ea22c6dad15f891a9a7

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
- agent 向けプロンプトを構築する実装群の入口。完全プロンプトの全体構成、エディタ入力用の初期文面、placeholder の共通表現、oracle・realization の説明部品、各種 prompt policy を扱う。個別の構築規則や policy 内容を確認するときは、該当する下位モジュールへ進む。

## Read this when
- agent call 用プロンプトの構築順序や全体構成を調べるとき
- エディタ入力の初期文面やテンプレート埋め込みを確認するとき
- placeholder の値表現や統合規則を確認するとき
- oracle・realization の説明文や分類規則を確認するとき
- agent call に適用する各種 policy の内容・生成方法を確認するとき

## Do not read this when
- 個別の oracle 文書・実装・テストの具体的内容を確認したいとき
- prompt builder を利用する側の呼び出し規則や引数決定方法を調べるとき
- 構造化ドキュメント要素のデータ構造や Markdown レンダリング仕様だけを確認したいとき
- プロンプト本文の生成や placeholder を使わない別処理を調べるとき

## hash
- 93d9c2f8799d33b0d9690fcd6c5934e8e4fcdefe4b27c909d74d22b749e67c3f
