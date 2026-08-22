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
- 選択された各種ポリシー、補助プロンプト、プレースホルダ定義を統合し、agent call 用の完全な構造化プロンプトを構築する関数を提供する。
- 基礎規定・個別規定・静的／動的追加プロンプト・目的・プレースホルダ定義を所定の順序で配置し、プロンプト内の参照地図も生成する。
- プレースホルダ定義は重複時の値の不一致を検出し、競合があれば例外を発生させる。

## Read this when
- agent call に渡す完全なプロンプトの構成順序や、各ポリシーブロックの включ却条件を変更・確認するとき
- 複数の placeholder 定義を統合する挙動や、同名定義の競合処理を変更・確認するとき
- 新しいポリシーや補助プロンプトを完全プロンプトへ組み込む入口を探すとき

## Do not read this when
- 個別ポリシー本文の内容だけを確認・変更する場合は、対応する oracle/src/oracle/prompt_builder 配下の policy モジュールを直接読む
- プレースホルダの具体的な値やパス文脈の生成だけを確認する場合は、AgentCallPathContext または関連する placeholder 定義の実装を直接読む
- 構造化ドキュメントの基本的な表現や SDHeader／SDTagBlock 自体の仕様を確認する場合は、struct_doc の定義を直接読む

## hash
- 475e2124d320cc803d13e96b67a8c2be64cc6666e1c0f69dcbfa87447b9b2b6c

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
- agent call 向けの各種 prompt policy builder を集約するディレクトリ。oracle・realization の扱い、所見判定、conflict 解消、file access、feedback 報告、INDEX.md ルーティング、oracle 参照など、個別の作業規定を構築するモジュールへの入口である。

## Read this when
- agent call に適用される prompt policy の種類や構築経路を調査するとき
- oracle・realization の作成、レビュー、実装、conflict 解消に関する規定の生成方法を確認または変更するとき
- INDEX.md ルーティング、file access、feedback reporting など共通ポリシーの責務分担を確認するとき

## Do not read this when
- 個別の oracle file、realization file、実装、テストの内容を直接確認したいとき
- Structured Document の項目・型・形式だけを確認したいとき
- prompt policy の利用箇所や生成された prompt 全体を確認する場合で、呼び出し元を直接読む方が適切なとき

## hash
- 1945e3534f1f0bf3ff7377e22b7c8f249b6e32059d7fea5aaae0f44dd4af8940
