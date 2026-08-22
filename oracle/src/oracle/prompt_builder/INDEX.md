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
- agent 向け完全 prompt の構築入口。基礎規定、条件付きポリシー、caller の追加 prompt、セッション目的、placeholder 定義を指定順に SDHeader・SDTagBlock のリストへまとめる。
- build_complete_prompt は、path_context 由来の placeholder を基盤に追加定義を統合し、同名 placeholder の異値定義を ValueError で拒否する。各種 policy の採用可否を boolean 引数で制御する。

## Read this when
- 完全 prompt の全体構造、各セクションの配置順、policy の条件付き追加を確認するとき
- build_complete_prompt の引数、prompt builder の統合入口、caller 追加 prompt の挿入位置を調査・変更するとき
- placeholder 定義の統合規則や衝突時のエラー処理を確認するとき

## Do not read this when
- 個別の policy prompt の内容や生成処理だけを確認したいときは、対応する policy モジュールを直接読む
- AgentCallPathContext の placeholder 定義やパス計算の仕様だけを確認したいときは、path_model の定義元を直接読む
- SDHeader・SDTagBlock のデータ構造や生成仕様だけを確認したいときは、struct_doc の定義元を直接読む
- この関数を利用する具体的な CLI や agent call の動作だけを確認したいときは、呼び出し側を直接読む

## hash
- 6790fdc03aa542ade23668d74f5ea332d99102361dd47bd451e4bb9d9d40bfba

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
- agent call 向けの各種 policy prompt builder 定義をまとめるディレクトリ。ファイルアクセス、oracle／realization、所見判定、feedback 報告、conflict resolution、routing、INDEX.md エントリー生成など、個別の指示文を構築する責務を扱う。対象領域の policy prompt の内容や生成方法を確認・変更するときの入口であり、具体的な oracle／realization 本文や prompt の利用箇所を調べる場合は各下位対象へ進む。

## Read this when
- agent call に適用される policy prompt の構成や生成責務を確認・変更するとき
- ファイルアクセス、oracle／realization、所見、feedback 報告、conflict resolution、routing、INDEX.md エントリー生成のいずれかの規定を調べるとき

## Do not read this when
- 個別の oracle file や realization file の具体的な仕様・実装を確認するとき
- policy の利用箇所や agent call 全体の prompt 構成だけを確認したいとき
- Structured Output の出力項目や形式だけを確認したいとき

## hash
- 51c5288034015c98d3cbd5502dc3449becfa40e43b365e62321ab6fb27f31fc3
