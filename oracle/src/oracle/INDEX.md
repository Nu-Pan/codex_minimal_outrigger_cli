# `acp_builder`

## Summary
- AIコーディングエージェント呼び出しのパラメータ契約と、indexing・oracle・realization・session・tui など各用途別の AgentCallParameter 構築定義を扱うディレクトリ。モデル、推論強度、ファイルアクセス、prompt、Structured Output schema、cwd、preflight などの用途別設定を確認する入口であり、具体的な処理は対応する下位定義へ進む。

## Read this when
- 特定用途の agent call の起動パラメータ、prompt、アクセス範囲、cwd、モデル設定、Structured Output 契約の所在を判断するとき
- indexing、oracle、realization、session、tui などの agent call 構築定義を横断して調査・変更するとき

## Do not read this when
- AgentCallParameter や prompt rendering などの共通仕様を確認したいとき
- oracle や realization の正本ファイル、通常の CLI 動作、TUI の画面表示、具体的な処理実装を調べるとき
- 対象用途の具体的な prompt・実装・出力 schema が特定できている場合は、対応する下位ファイルを直接読むとき

## hash
- 49461539615e06edb22f938557755d61e38e7b236814c6243cad6bdb34960d30

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
- prompt-builder 配下の実装群を、agent 向けプロンプトの構造化・初期入力・共通説明部品・各種 policy の生成責務ごとに案内する入口。placeholder の型定義、完全プロンプトの集約、エディタ入力文面、oracle/realization 説明部品、policy 群を扱う。
- `basic.py` は placeholder 名と実パス・文字列を対応付ける型定義、`complete_prompt.py` は基礎規定や条件付き policy、追加プロンプト、目的、placeholder 定義を最終プロンプトへ集約する実装を扱う。
- `editor_input.py` はエディタ経由のユーザー入力ファイルの初期文面とテンプレート埋め込み、`parts` は oracle/realization の概念・分類説明、`policy` はファイルアクセスや routing、feedback、conflict resolution、handoff、INDEX.md エントリー生成などの規定生成を扱う。

## Read this when
- agent 呼び出し向けの完全プロンプトの構成順序、条件付き policy の組み込み、placeholder の統合や競合処理を確認したいときは `complete_prompt.py` から確認する。
- エディタ入力ファイルの初期表示、記入案内、構造化見出し・タグブロック、完全プロンプトのテンプレート埋め込みを確認したいときは `editor_input.py` を読む。
- oracle と realization の責務・分類、work-root を用いたパス説明、uncategorised file の分類規則を確認したいときは `parts` を読む。
- agent call に注入される個別 policy の定義や、routing・feedback・handoff・conflict resolution・INDEX.md エントリー生成の規定を確認したいときは `policy` を読む。
- placeholder の名前と置換先を共通の型で扱う意味だけを確認したいときは `basic.py` を読む。

## Do not read this when
- 特定の policy 本文の詳細、個別の oracle/realization ファイル、実装コードやテストの内容を確認したいだけのときは、対応する定義元を直接読む。
- 構造化ドキュメント要素の定義や Markdown レンダリング仕様そのものを確認したいときは、`editor_input.py` ではなくインポート元の実装を読む。
- 生成済みプロンプトの解釈・実行や agent 呼び出しの実行制御を確認したいときは、prompt-builder 配下ではなく呼び出し側・実行側の対象を読む。
- prompt builder と無関係な CLI 機能やデータモデル、個別ファイルの具体的な仕様を調べるときは、このディレクトリを入口にしない。

## hash
- fdab3bfcdff4f339ee01336815b1a54e11372dde4fd65b87cfe6013af5288493
