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
- 選択した規範・補助プロンプト・動的な依頼内容を統合し、agent call 用の完全な構造化 prompt を構築する入口。placeholder 定義を統合し、依存する規範を自動的に有効化したうえで、静的規則・動的 summary/goal・定義情報を決定論的な順序でまとめる。

## Read this when
- agent call に渡す完全 prompt の構成、規範の依存関係、静的 prompt と動的 prompt の注入順序を確認したいとき
- placeholder 定義の統合や同名定義の競合時の扱いを確認したいとき
- oracle、realization、review、routing などの選択オプションがどの補助規則を連動して有効化するかを確認したいとき

## Do not read this when
- 個別の oracle・realization・file access・routing 規則の本文を確認したいだけのときは、それぞれの規則ビルダーまたは正本を直接読む
- prompt の構造化データ型やブロック表現そのものを確認したいだけのときは、StructDoc、StructBlock などの定義を直接読む
- agent call の実行、CLI の利用、または生成済み prompt の具体的な内容だけを確認したいとき

## hash
- 5947a9ed09d7476bd93871b1cee478d031ef383b49b07f9578e7827047e029a7

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
- oracle file と realization file の追従要否・レビュー所見を判断する規範の構築部品。仕様不整合や致命的実装問題のレビュー基準を確認するときの入口。
- session join の conflict marker 解消用 instruction と、関連 oracle file の意味を保つ conflict 解消規範を構築する部品。conflict 解消 prompt の要件を確認するときに読む。
- 全 agent call 共通の human feedback 報告規範を構築する部品。作業外の人間対応へ報告すべき問題の条件や報告後の継続方針を確認するときに読む。
- agent のファイルアクセスモードに応じた読み書き制限、パス境界、oracle/realization file の扱いを構築する部品。アクセス規則やその placeholder の生成を変更・検証するときの入口。
- INDEX.md エントリーの責務、読むべき条件、対象外境界を構造化して生成する部品。ルーティング情報の生成基準や含める情報の範囲を確認するときに読む。
- oracle と realization の定義・役割・分類を、work-root に応じて構築する prompt 部品。基本概念の説明文や root placeholder の生成を変更するときの入口。
- oracle review における fatal・minor の成立条件と根拠の境界を構造化して構築する部品。oracle のレビュー所見を判定・統合する基準を確認するときに読む。
- oracle file を正本仕様として扱うための標準規範を構築する部品。oracle の作成・変更・調査・レビューに適用する要求や仕様間整合性の基準を確認するときの入口。
- realization code に対応する oracle file の path をコメントへ記載する規則を構築する部品。realization 実装時の oracle 参照ルールや path placeholder の生成を確認するときに読む。
- realization file の作成・変更・レビューに適用する標準規範を構築する部品。oracle への適合、最小実装、repository 固有の検証手順を含む instruction の生成元を確認するときの入口。
- INDEX.md から対象本文へ進む routing 規則を構築する prompt 部品。Summary・Read this when・Do not read this when による候補絞り込みや下位 INDEX.md の利用手順を確認するときに読む。

## Read this when
- このディレクトリ内の prompt builder 部品の責務、生成文面、構造化文書、placeholder の変更・調査・レビューを行うとき
- 特定の agent call 向け標準規範や routing・feedback・access rule の構築経路を確認するとき

## Do not read this when
- 個別の oracle 文書、realization 実装、realization test の内容を調査するとき
- prompt builder 部品を組み合わせる呼び出し元や agent call 全体の選択処理を調べるとき
- 既存 INDEX.md のルーティング情報だけを確認・更新するとき
- Structured Output schema の形式や、ファイル名・hash など機械的な識別情報だけを確認するとき

## hash
- 0b99319ef7f10c06868eaa2803459106002521ad633822fa5feebd968ee10b8b
