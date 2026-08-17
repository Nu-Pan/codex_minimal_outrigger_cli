# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの AgentCallParameter を構築する定義を集約する領域です。共通パラメータ契約に加え、indexing、feedback、realization、session、tui、oracle の各処理向けに、prompt、ファイルアクセスモード、モデル・推論設定、Structured Output、作業ディレクトリ、indexing preflight の構成を定義します。
- 個別処理の agent call 設定を調査・変更するときの入口であり、共通のパラメータ型は直下の定義、処理別の prompt と schema は対応する下位ディレクトリへ進んで確認します。

## Read this when
- 特定の cmoc 処理がどのような agent call パラメータと完全 prompt を構築するかを調査・変更するとき
- agent call のモデルクラス、推論強度、ファイルアクセス制御、Structured Output、cwd、indexing preflight の設定箇所を特定するとき
- 処理別の agent call builder を横断して、oracle・realization・feedback などの設定責務の分割を確認するとき

## Do not read this when
- agent call の実行制御や終了結果の処理を調査するときは、呼び出し側または実行処理を直接読む
- モデル名や Codex CLI sandbox の具体的な解決仕様を確認するときは、realization 実装または指定された oracle 文書を読む
- 個別の Structured Output schema、prompt の詳細、または対象処理の通常フローだけを調査するときは、対応する下位要素を直接読む

## hash
- e6e88ad08d1c68b9f12d7ce007246a19da65ae8c10753ac1d6ccfa748b645c9a

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
- cmoc の補助的な正本モデルをまとめるディレクトリ。リポジトリ固有設定、agent call における root placeholder と Git worktree のパス解決、構造化文書の Markdown レンダリングを扱う。各機能の共通モデルや変換規則を確認する際の入口であり、個別機能の呼び出し側実装やテストの詳細は下位の対応対象へ進む。

## Read this when
- cmoc の設定モデル、Codex CLI 向け設定、oracle review のループ上限、設定の JSON/TOML 表現を確認・変更するとき
- agent call の cwd から work root・repository root を導出する規則や、root placeholder と実パスの相互変換を確認・変更するとき
- StructDoc・StructBlock・StructCodeBlock の構造、見出し深度、cmoc ブロック、コードフェンス、空行・インデントの Markdown レンダリングを確認・変更するとき

## Do not read this when
- Codex CLI の呼び出し処理や個別 CLI 機能の責務を確認するとき
- oracle review の所見生成・マージ・検証処理や、動的プロンプト全体の仕様を確認するとき
- 設定ファイルの実際の保存内容、人間による調整結果、テストの期待値や実行方法だけを確認するとき

## hash
- fb3acd148a4beb55757989a58afce272b0ea3a5b8315b45c563a4378e1ddb4ce

# `prompt_builder`

## Summary
- agent 呼び出しへ渡すプロンプトを構築する領域。プレースホルダ型、完全プロンプトの統合順序、エディタ入力の初期文面、oracle/realization の基本説明、作業種別ごとの policy 文面を扱う。
- 完全プロンプト全体の構成や複数 policy の組み込み条件を確認するときの入口であり、個別 policy や prompt builder 部品の詳細を調べる場合は対応する下位対象へ進む。

## Read this when
- agent 呼び出しへ渡すプロンプトの構成要素、配置順、目的や追加文面の統合方法を変更・確認するとき
- プレースホルダ定義の統合、同名定義の競合検査、path context 由来の値の扱いを調査するとき
- エディタ経由の入力テンプレートや、oracle/realization の基本説明を変更・確認するとき
- oracle、realization、file access、routing、feedback、review、INDEX.md 生成など、作業種別 policy の責務や適用条件を調査するとき

## Do not read this when
- 特定の policy の文面や単一 builder の実装詳細だけを確認したい場合は、該当する下位対象を直接読む
- StructDoc など構造化文書の型・レンダリング仕様、path context の定義、または agent 呼び出し処理そのものを調べる場合
- 生成済みプロンプトの個別出力だけを確認すれば足りる場合

## hash
- bd5ee5f8801782311f1cec036fe22005b04e7b0f89ac9d210deaeabc3a05ad45
