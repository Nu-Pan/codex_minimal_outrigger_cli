# `basic.py`

## Summary
- プレースホルダ名を実パスや文字列へ対応付ける型定義を置く。プロンプト組み立てで、置換対象の名前と置換先を共通の表現で扱いたいときに読む。

## Read this when
- プレースホルダ展開に使う型の意味を確認したいとき。
- 文字列と `Path` を混在させる置換対象の表現を統一したいとき。

## Do not read this when
- プロンプト本文の生成手順や置換ロジックの詳細を知りたいときは、実装側を読む。
- プレースホルダを使わない処理や、別の設定値の表現を確認したいだけのとき。

## hash
- 526fb2d3d3f5fd312f3f1cc48c630d59e91568f38d6ac0d09bc5241792eb1e18

# `complete_prompt.py`

## Summary
- 完全 prompt を構築する中心的な builder です。agent call の path context から placeholder 定義を初期化し、補助 prompt と各種 standard を統合して、最終的な構造化 prompt を返します。
- oracle・realization 関連の規範には依存関係があり、適用する standard に応じて基礎概念や oracle standard を自動的に有効化します。feedback reporting は全 agent call に共通して注入されます。
- 静的 standard、個別 rule、補助 prompt、file access rule、routing rule、summary・goal などの動的 prompt を決められた順序で組み立てるため、prompt の構成や有効化経路を変更・調査するときの入口です。
- 同名 placeholder の異値定義を拒否し、standard collection を合成してから一度だけ構造化文書へ変換することで、定義の衝突と重複出力を管理します。

## Read this when
- 完全 prompt の構築順序や、静的・動的 prompt の注入位置を変更または確認するとき
- oracle、realization、review、conflict resolution、index entry の各 standard がどの条件で連鎖的に有効化されるかを追跡するとき
- placeholder 定義の統合、衝突検出、path context 由来の定義を調査するとき
- standard collection の合成や、file access・routing ルールの注入経路を確認するとき

## Do not read this when
- 個別の standard の文言や責務だけを確認する場合は、対応する standard builder を直接読むとき
- 特定の file access rule、routing rule、oracle・realization rule の詳細だけを確認する場合は、対応する個別 rule を直接読むとき
- prompt の利用側が渡す summary・goal の内容だけを確認する場合は、呼び出し側を直接読むとき

## hash
- 9f962a7ed31696f419b02012bd1d1bb73052907a30d7360e09585eb5ae582872

# `editor_input.py`

## Summary
- エディタ経由で後続 AI エージェントへ渡すユーザー入力ファイルの初期表示文面を構築する定義。入力方法、記入の目安、完全プロンプトのテンプレートを含む初期テキストを生成する。

## Read this when
- エディタ経由のプロンプト入力ファイルに表示する初期文面の構造や内容を確認・変更するとき。
- ユーザー入力と完全プロンプトの差し込み位置、HTML コメントによる非転送部分の扱いを確認するとき。

## Do not read this when
- エディタ経由の初期文面ではなく、完全プロンプト全体の生成規則を確認したいとき。
- Markdown 構造の一般的なレンダリング処理そのものを確認したいとき。

## hash
- ab47b18db214c4c267917f67e838f69065647618f31a1ad2a28d24cbba352aa9

# `parts`

## Summary
- oracle・realization の扱い、各種 review・conflict 解消、feedback 報告、ファイルアクセス、INDEX.md ルーティングなど、agent call 用 prompt 部品の構築定義を集約するディレクトリ。個別の標準定義、共通標準グループ、概念説明、アクセス規則を確認するための入口として機能する。

## Read this when
- agent call 用の prompt 部品全体から、対象の規範・ルーティング・アクセス規則・oracle/realization 説明の構築定義を探すとき
- oracle、realization、oracle review、apply review、conflict 解消、feedback 報告の instruction 構成を確認または変更するとき
- INDEX.md エントリー生成に適用する標準群や、共有 Standard 定義の利用範囲を確認するとき

## Do not read this when
- 特定の oracle file、realization file、test、または INDEX.md の本文や実装内容を調査するときは、対象を直接読む
- 個別標準の具体的な判定要求だけを確認したいときは、対応する standard 定義へ直接進む
- prompt 部品ではなく、リポジトリ固有の実行手順や CLI 実装の挙動を確認するときは、対応する oracle・realization・手順書を読む

## hash
- 3cf8e21213c8b179ceabd3aa91f480c1baa06140f39219a9aed000d1a89fe685
