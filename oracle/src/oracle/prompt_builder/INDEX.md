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
- agent 向けの完全な構造化プロンプトを、基礎規定、選択式ポリシー、追加プロンプト、目的、placeholder 定義の順に構築する。
- パスコンテキスト由来と追加指定の placeholder 定義を統合し、同名で異なる値がある場合はエラーにする。
- 基礎規定と各ポリシーは対応する builder で生成し、指定された場合だけ完全プロンプトへ追加する。
- このファイルは prompt builder 配下で、複数のポリシーや補助要素を agent 呼び出し用の最終構造へ集約する入口である。

## Read this when
- agent 呼び出しへ渡す完全プロンプトの構成順序や、どのポリシーを条件付きで含めるかを確認したいとき
- summary・goal、静的／動的追加プロンプト、placeholder 定義が最終プロンプトへ入る位置を確認したいとき
- placeholder 定義の競合時の扱いや、path_context と追加定義の統合処理を確認したいとき

## Do not read this when
- 特定のポリシー本文や、そのポリシーが生成する文面の詳細を確認したいときは、対応する policy ファイルを直接読む
- SDHeader・SDTagBlock のデータ構造や、FileAccessMode・AgentCallPathContext の定義を確認したいときは、それぞれの定義元を直接読む
- 生成済みプロンプトの解釈・実行や、agent 呼び出しの実行制御を確認したいときは、呼び出し側または実行側の対象を読む

## hash
- b511950f40d2eb2518ddc8d32199ff71bedfeb8caaaa91a3bd10035067bffc27

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
- agent call 向けの各種 prompt policy を構築するモジュール群。ファイルアクセス、oracle・realization、feedback、routing、conflict resolution、editor handoff、所見判定、INDEX.md エントリー生成など、個別の作業規定や文面の生成責務を扱う。特定の policy の内容・構造・変更範囲を確認するときの入口となる。

## Read this when
- agent call に注入する policy の定義や構成を確認・変更するとき
- oracle・realization・feedback・routing・handoff・conflict resolution など、共通または個別の作業規定の生成責務を調査するとき
- INDEX.md エントリー生成や所見判定の規定を確認するとき

## Do not read this when
- 特定の oracle file、realization file、実装コード、テストの具体的な内容を直接確認したいとき
- prompt policy を利用する agent call 全体の構築処理や PlaceholderMap の一般仕様を確認したいとき
- policy とは無関係な CLI 機能やデータモデルを調べるとき

## hash
- ddb6c206bd7d1310882906c201380100c60cef54d62f1175dbb133a0cd15bc48
