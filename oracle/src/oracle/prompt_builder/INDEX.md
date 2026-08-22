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
- agent 向けの完全な prompt を構築する関数。固定・動的 prompt、各種 policy、placeholder 定義を所定の順序で統合し、構造化された prompt として返す。
- oracle・realization・routing・index entry などの policy を指定条件に応じて追加する。placeholder は重複定義の値を照合し、異なる値があればエラーにする。
- prompt 冒頭に基礎規定と目的への参照を配置し、末尾に統合済み placeholder 定義を配置する。下位の policy builder や prompt 構築仕様を確認する際の入口となる。

## Read this when
- 完全な agent prompt の構築順序、構成要素、挿入位置を確認したいとき
- oracle・realization・routing・index entry などの policy を prompt に含める条件を確認したいとき
- 複数の placeholder 定義を統合する際の競合検出とエラー条件を確認したいとき
- agent call 用の静的 prompt、動的 prompt、構造化タグの組み立て方を変更または調査したいとき

## Do not read this when
- 個別 policy の本文や生成ロジックだけを確認したいとき
- placeholder の実際の値や path context の定義だけを確認したいとき
- prompt 構築ではなく、oracle・realization 自体の仕様や実装を直接調査するとき

## hash
- 2380f011c762e728bc3b85fd4b3e37973b312b133517abbc70a5fad032c64c5c

# `editor_input.py`

## Summary
- 対象ファイルは、エディタ経由で後続 AI エージェントへ渡すユーザー入力ファイルの初期表示文面を構築する関数を定義する。使い方・記入上の目安・完全プロンプトのテンプレートを HTML コメント内にまとめ、入力本文が所定のプレースホルダーへ注入される前提を扱う。

## Read this when
- エディタ経由のプロンプト入力ファイルに表示する初期文面の構成や、ユーザーへの記入案内、テンプレート埋め込みの挙動を確認・変更するとき。
- 初期テキストに含める構造化見出し・タグブロックの組み立てと、HTML コメントとしてのレンダリング範囲を確認するとき。

## Do not read this when
- エディタ入力の初期文面ではなく、完全プロンプト全体の生成規則や別経路のプロンプト入力処理を確認するときは、それぞれの担当実装・仕様を直接読む。
- 構造化ドキュメント要素の定義や Markdown レンダリング仕様そのものを確認したい場合は、インポート元の構造化ドキュメント実装を読む。

## hash
- 801c5e31f4bbfc2b036f94ce9ef77536f12136fe02cba369a4f477b5b6150d35

# `parts`

## Summary
- oracle と realization の基本概念を prompt-builder の説明文として構築する部品。両者の役割、正本関係、下位分類、分類条件をまとめ、call-scoped context の work-root を各パス説明へ埋め込む。
- uncategorised file の分類対象として、特定ディレクトリ・ファイル名・git ignore・実際の git metadata に基づく規則を説明文へ含める。対象ディレクトリ内で oracle/realization の分類ルール全体へ進む入口となる。

## Read this when
- oracle file と realization file の責務境界、編集主体、正本関係を確認するとき
- oracle doc・oracle src・oracle test、または realization code・realization implementation・realization test・realization ancillary の分類を確認するとき
- work-root を使った oracle/realization の配置場所や分類条件を確認するとき
- uncategorised file のパス、ファイル名、git ignore、git repository metadata による分類規則を確認するとき
- work-root の call-scoped context から説明文用プレースホルダーへ値を渡す処理を変更・調査するとき

## Do not read this when
- 個別の oracle 文書・実装・テストの内容そのものを確認したいとき
- realization の具体的な実装責務やテスト実行方法だけを確認したいとき
- INDEX.md や AGENTS.md 自体の分類対象外規則だけを確認したいとき

## hash
- 81e086274e3b84b3f847a1b3cf05f5016357bec748a19d77d50bcb84cafb0189

# `policy`

## Summary
- prompt_builder/policy 配下の各 policy 定義ファイルについて、担う規定の種類、確認・変更時の入口、関連対象との責務境界を示す INDEX.md 用ルーティング情報。
- conflict_resolution.py は session join の merge conflict 解消方針、feedback_reporting.py は全 agent call 共通の人間向け feedback 報告方針、file_access.py はファイルアクセス制限、index_entry.py は INDEX.md エントリー生成規定を扱う。
- oracle.py・realization.py および各 findings 系は、それぞれ oracle／realization の扱いと適合性所見の判定基準を扱う。realization_oracle_reference.py は realization code から oracle file を参照する規定、routing.py は INDEX.md による探索規定を扱う。

## Read this when
- agent call に適用される policy の内容や生成方法を確認・変更するとき
- oracle file、realization file、INDEX.md、ファイルアクセス、feedback 報告、conflict resolution に関する共通規定の入口を探すとき
- 個別 policy の要求・禁止・許可事項や、関連する prompt builder との責務境界を調査するとき

## Do not read this when
- 個別の oracle file、realization file、実装ファイル、テストの具体的な内容を確認したいとき
- policy の利用箇所や生成された prompt 全体を確認したいときは、呼び出し元または prompt 生成側を直接読むとき
- Structured Output の項目・型・形式だけを確認したいとき

## hash
- 70d8707891b1e6066df967fa1d150f7c7f36ce08a4d9737463404bb5fd25e922
