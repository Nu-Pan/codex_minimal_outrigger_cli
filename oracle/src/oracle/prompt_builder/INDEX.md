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
- cmoc の agent 向け完全プロンプトを構築する中心的なビルダー。summary・goal、共通規則、選択された oracle/realization・レビュー・ルーティング規則、補助プロンプト、placeholder 定義を決定的な順序で統合し、agent call に渡す構造化文書列を生成する。
- 各 Standard の依存関係を自動的に有効化し、placeholder の競合を検出しながら、静的・動的プロンプトと参照先定義を一つの完全な prompt にまとめる。プロンプト構築経路や、利用する規則の組み合わせを変更・調査するときの入口となる。

## Read this when
- agent 向け完全プロンプトの構成、注入順序、選択可能な規則、または placeholder 統合を変更・調査するとき。
- oracle/realization、レビュー、index entry、routing などの規則がどの条件で自動的に有効化されるかを確認するとき。
- 補助 prompt や file access rule を含む最終的な StructDoc/StructBlock 列の生成経路を追うとき。

## Do not read this when
- 個別の規則本文や Standard の内容だけを確認したい場合は、対応する parts builder または oracle 文書を直接読む。
- Structured Output の出力契約や、prompt builder 外の agent call 実行処理だけを調査する場合。

## hash
- d77d0f07473d299ddc1948b151ba1c0b79d502d4b6b18ecb748d7d0548bbcd25

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
- oracle と realization の扱い、レビュー・conflict 解消・feedback 報告・ファイルアクセス・INDEX.md ルーティングなど、cmoc の agent prompt を構成する標準群と規則文面の生成部品をまとめるディレクトリ。用途別の標準コレクション構築と、共通標準・個別定義への入口を提供する。

## Read this when
- cmoc の agent prompt に組み込む標準コレクション、アクセス規則、routing 規則、feedback 規則の構成を変更・レビューするとき
- oracle file と realization file のレビュー、適合性判断、conflict 解消、INDEX.md エントリー生成に適用する prompt 部品を調査するとき
- 個別の標準定義へ進む前に、用途別の標準群の選択関係や共通部品の責務を把握したいとき

## Do not read this when
- 個別の oracle・realization file の仕様や実装、テスト内容を確認したいとき
- 具体的な標準文面の判定基準だけを確認したいときは、標準定義へ直接進む
- INDEX.md の既存エントリーや、Codex CLI の実行・sandbox 規則そのものだけを確認したいとき

## hash
- 5e8d738fcd04e8d625c7652136d94d9299e7fe6f5e89e93c7ef4fa96b4eb6b9d
