# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの構築定義を集約する領域。共通の呼び出しパラメータ、quota probe、feedback 判定、INDEX エントリー生成、oracle 操作、realization 適用・レビュー、session conflict 解消、TUI 起動を扱う。用途別の prompt、Structured Output schema、モデル・推論強度、ファイルアクセスモード、作業ディレクトリ、indexing preflight の設定を確認するための上位入口で、具体的な挙動は各下位領域へ進む。

## Read this when
- 特定の agent call の用途が複数領域にまたがり、まず呼び出し構築定義の下位入口を選ぶとき
- agent call の共通パラメータ契約と、用途別の起動設定の配置を把握するとき
- oracle、realization、feedback、indexing、session、TUI の agent call 構築定義を横断して確認・変更するとき

## Do not read this when
- 特定の agent call の実装や Structured Output schema が明確で、対応する下位ファイルを直接読めるとき
- prompt の共通生成規則、agent call の実行処理、バックエンド固有のモデル解決、またはファイルアクセス規則の正本だけを確認するとき
- 対象となる oracle file、realization file、feedback state、または INDEX.md の実際の内容を調査するとき

## hash
- 3f9984abfb6b79736583aa2275bd489db7d42a8444d51bd8b8ec0d89ecd7b703

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
- cmoc の設定、パス解決、標準定義、構造化 Markdown 生成という、oracle 実装を支える共通モデル群の入口。設定値や agent call の root context、instruction 標準の合成、StructDoc のレンダリングを扱う対象へ進む際に読む。

## Read this when
- cmoc のリポジトリ固有設定、Codex CLI 設定、oracle review のループ設定を確認・変更するとき。
- agent call の work root・repository root、root placeholder、実パスとの相互変換や Git worktree 探索を調査するとき。
- agent 向け標準の検証・合成・決定的順序・instruction 文面化を確認するとき。
- 構造化文書を Markdown に変換する見出し、cmoc_block／cmoc_ref、コードブロック、参照検証の挙動を確認するとき。

## Do not read this when
- 永続化された設定ファイルの生成・同期・編集処理だけを確認するときは、対象の設定ファイルや doctor 実装を直接読む。
- ModelClass、ReasoningEffort、その他の参照元型の具体的な列挙値だけを確認するときは、その型定義を直接読む。
- 個別機能における設定・パスモデル・標準・構造化文書の利用方法だけを確認するときは、利用元を直接読む。
- oracle や realization の仕様、通常の Markdown 記法、構造化文書を利用しない文書生成を確認するときは、この共通モデル群を読まない。

## hash
- 4c5b20c8577c323ed7c92e402386e4484cc0bb06bdd7bc756378e57a67568e16

# `prompt_builder`

## Summary
- プレースホルダ名と実パス・文字列の対応を表す型定義。プレースホルダ展開時の置換対象を統一して扱うための基礎要素。
- cmoc の agent 向け完全プロンプトを構築する中心ビルダー。summary・goal、共通規則、oracle/realization、レビュー、ルーティング、補助プロンプトなどを決定的な順序で統合し、placeholder の依存関係や競合も処理する。
- エディタ経由で後続 AI エージェントへ渡すユーザー入力ファイルの初期表示文面を構築する定義。入力方法、記入目安、完全プロンプトの差し込み位置、HTML コメントによる非転送部分を扱う。
- oracle・realization、レビュー、conflict 解消、feedback、ファイルアクセス、INDEX.md ルーティングなど、agent prompt を構成する標準群と規則文面の生成部品をまとめる。用途別の標準コレクションや個別標準定義への入口となる。

## Read this when
- プレースホルダ展開に使う型の意味や、文字列と Path を混在させる置換対象の表現を確認したいときは、プレースホルダ型定義を読む。
- agent 向け完全プロンプトの構成、注入順序、placeholder 統合、または oracle/realization・レビュー・routing などの自動有効化条件を変更・調査するときは、完全プロンプトビルダーを読む。
- エディタ経由のプロンプト入力ファイルに表示する初期文面、ユーザー入力と完全プロンプトの差し込み、HTML コメントによる非転送部分を確認・変更するときは、エディタ入力定義を読む。
- cmoc の agent prompt に組み込む標準コレクション、アクセス・routing・feedback 規則、または用途別の標準群の選択関係を調査するときは、parts ディレクトリを読む。

## Do not read this when
- プロンプト本文の生成手順や置換ロジックの詳細だけを知りたい場合は、プレースホルダ型定義ではなく実装側を読む。
- 個別の規則本文や Standard の内容だけを確認したい場合は、完全プロンプトビルダーではなく対応する parts builder または oracle 文書を直接読む。
- Structured Output の契約や、prompt builder 外の agent call 実行処理だけを調査する場合は、完全プロンプトビルダーを読む必要はない。
- エディタ経由の初期文面ではなく完全プロンプト全体の生成規則や、Markdown の一般的なレンダリング処理だけを確認したい場合は、エディタ入力定義を読まない。
- 個別の oracle・realization の仕様・実装・テストや、具体的な標準文面の判定基準だけを確認したい場合は、parts ではなく該当する標準定義・対象ファイルへ直接進む。
- INDEX.md の既存エントリーや Codex CLI の実行・sandbox 規則だけを確認したい場合は、parts を読む必要はない。

## hash
- 3e06725d766ac5483219f1916deb90362344de391122aaa2893f969142124339
