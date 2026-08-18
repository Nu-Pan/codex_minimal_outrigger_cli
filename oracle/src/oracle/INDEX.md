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
- oracle/src/oracle/other は、cmoc の共通データモデルと文書・パス処理の実装をまとめたディレクトリ。設定モデルは `cmoc_config.py`、agent call のルートパスと placeholder 解決は `path_model.py`、構造化ノードから Markdown を生成する処理は `struct_doc.py` が入口になる。

## Read this when
- cmoc の設定モデル、Codex CLI や oracle review の設定を確認・変更するとき
- `{{repo-root}}`・`{{work-root}}`・`{{run-root}}`・`{{cmoc-root}}` の解決、agent call のパスコンテキスト、実パスとの相互変換を確認・変更するとき
- 見出し、タグブロック、コードブロック、規定文などの構造化ノードを Markdown へレンダリングする処理を確認・変更するとき
- 上記の共通モデルやヘルパーを横断して、複数の下位実装の関係を確認するとき

## Do not read this when
- Codex CLI の呼び出し処理や個別 CLI 機能の責務だけを確認したいとき
- oracle review の所見生成・マージ・検証ロジックそのものを確認したいとき
- 構造化文書を利用する上位のプロンプト生成処理だけを確認したいとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認したいとき

## hash
- 65f0c439824955801a77b6e5742e2fcaf02fa3fc5721a195558e975306fc4462

# `prompt_builder`

## Summary
- prompt_builder は、agent 向け完全プロンプトとエディタ入力用初期文面を構築する実装群である。placeholder 定義、プロンプト部品、policy の統合を扱う。
- basic.py は、placeholder 名と置換先の文字列または Path を対応付ける型定義を提供する。
- complete_prompt.py は、基礎規定、選択された policy、追加文面、目的、placeholder 定義を順序付けて完全プロンプトへ統合する。policy や構造化文書要素の具体的内容は下位対象が担う。
- editor_input.py は、エディタ経由で入力するプロンプトの初期表示文面を構築する。記入案内と、入力内容を注入する完全プロンプトのテンプレートを HTML コメント内へ配置する。
- parts は、oracle と realization の役割・分類・配置規則を説明するプロンプト部品をまとめる。個別の基本説明を確認するときの入口である。
- policy は、ファイルアクセス、oracle・realization の扱い、レビュー、routing、handoff など、agent call に条件付きで注入する規定文面をまとめる。特定の規定の内容や生成処理を確認するときの入口である。

## Read this when
- agent 向け完全プロンプトの構成順、policy の選択・統合、placeholder の競合処理を確認または変更するときは complete_prompt.py を読む。
- placeholder の型や、文字列と Path を混在させる定義を確認するときは basic.py を読む。
- エディタ入力ファイルの案内、HTML コメントの範囲、prompt template の注入方法を確認または変更するときは editor_input.py を読む。
- oracle と realization の分類や基本説明を確認するときは parts を読む。
- agent call に注入する特定の作業規定を確認するときは policy を読む。

## Do not read this when
- 特定の policy の詳細だけを調べる場合は complete_prompt.py ではなく policy 配下の該当実装を直接読む。
- oracle・realization の具体的な分類説明だけを調べる場合は complete_prompt.py ではなく parts 配下の実装を直接読む。
- 構造化文書要素そのもののデータ構造やレンダリング規則を調べる場合は、このディレクトリではなくインポート元の実装を読む。
- agent call 側で summary、goal、file access mode、各 policy フラグを決める規則を調べる場合は、呼び出し側の実装を読む。
- placeholder を使わない処理や、prompt builder 外の設定値の表現だけを確認する場合は basic.py を読む必要はない。

## hash
- f08a78d04bb5e83002ca43f4474fb6b412f97d2914342a424c52d3f93f5af794
