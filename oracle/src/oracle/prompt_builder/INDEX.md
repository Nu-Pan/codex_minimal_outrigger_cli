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
- cmoc の完全な agent prompt を組み立てる中核モジュール。概要・完了条件、共通規定、oracle/realization・レビュー・ファイルアクセスなどの選択的ポリシー、補助 prompt、placeholder 定義を決定論的な順序で統合し、agent call 用の構造化文書列として返す。
- prompt builder の各種ポリシーがどの条件で自動的に有効化されるか、ポリシー統合と placeholder 衝突検出がどのように行われるかを確認するための入口であり、個別の規定本文を読む前に全体の注入経路を把握できる。

## Read this when
- agent call に渡される完全 prompt の構成、注入順序、動的 prompt と静的 prompt の境界を調査・変更するとき
- oracle/realization 関連ポリシーの依存関係や、apply review による自動有効化を確認するとき
- placeholder 定義の統合、同名異値の拒否、path context 由来の定義を調査するとき
- 複数の prompt builder を組み合わせた出力や、feedback reporting が全 agent call に注入される経路を確認するとき

## Do not read this when
- 個別ポリシーの具体的な規則だけを調査・変更する場合は、対応する parts 配下の builder を直接読む
- prompt の出力を利用する CLI や agent 実行側の挙動だけを調査する場合は、その呼び出し元または実行側を直接読む
- INDEX.md の生成規則そのものだけを確認する場合は、index entry policy の定義を直接読む

## hash
- 8b038b59b842695c9e68644d7f56a4acac509bd2f11c986560f056afbdfac039

# `editor_input.py`

## Summary
- エディタ経由で後続の AI エージェントへ渡すユーザー入力ファイルの初期テキストを構築する定義。使い方・記入方針・完全プロンプトのテンプレートを HTML コメント内にまとめる入口であり、プロンプト入力用ファイルの初期内容やコメント除去前の構造化レンダリングを確認したい場合に読む。

## Read this when
- エディタ経由のプロンプト入力ファイルにどの初期案内やテンプレートを注入するかを変更・確認するとき
- 完全プロンプト中のユーザー入力差し込み位置を、初期テキスト生成側から調査するとき

## Do not read this when
- 後続エージェントへ渡す完全プロンプト全体の構築規則を調べるとき
- StructDoc、StructBlock、Markdown レンダリング自体の仕様を調べるとき
- エディタ経由ではないユーザー入力経路や、保存記録としてのプロンプト管理を調べるとき

## hash
- ef8b185c6711e48c549cd12fc63e19d1412a834885495065bc4b0eabef94017f

# `parts`

## Summary
- プロンプト生成で利用する各種 policy 定義・policy group 構成を集約するディレクトリ。oracle／realization の権威関係、レビュー・conflict 解消・editor handoff・feedback 報告、ファイルアクセス制約、INDEX.md ルーティングなど、agent call に適用する規定の構築入口を提供する。個別仕様や実装本体ではなく、prompt builder が用途別の policy collection を組み立てる際に参照する。

## Read this when
- agent call に適用する policy collection や policy group の構成を確認・変更するとき
- oracle／realization の扱い、レビュー、conflict 解消、editor handoff、feedback 報告、ファイルアクセス、INDEX.md ルーティングに関する prompt policy の構成を調査するとき

## Do not read this when
- 個別 policy の具体的な判定規則だけを確認したいときは、対応する policy 定義を直接読む
- oracle file、realization file、または prompt builder の一般構造そのものを確認するとき
- 実際の agent call の実装や対象文書の仕様を直接確認するとき

## hash
- c365bf357287bcfda18460b3e8e0c9fb4bcb52fd8d233b70bfac5f3d37b7e7d8
