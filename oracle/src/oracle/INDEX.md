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
- `cmoc_config.py` は、リポジトリ単位で変化する cmoc 設定のデータモデルと既定値を定義する。Codex CLI のモデル・provider-local 設定・推論 effort、AI 呼び出しの最大並列数、ファイルアクセス違反時のリカバリ試行回数、`cmoc oracle review` の各ループ上限、JSON/TOML 相当の値構造と JSON 永続化方針を確認する入口である。
- `path_model.py` は、cmoc のルートパス placeholder と agent call のパスコンテキストを定義し、placeholder と実パスの相互変換、Git worktree からの cmoc・repository・work・run root の解決を提供する。agent call の cwd から導出される root や、相対パス表記の解決規則を確認する入口である。
- `struct_doc.py` は、構造化された文書ノードを Markdown にレンダリングするためのクラスと処理を提供する。見出し深度、参照可能な `<cmoc_block>`、`<cmoc_ref>` を含む文書構造、コードフェンス、空行、インデント、バッククォートを含む本文の扱いを確認する入口である。

## Read this when
- cmoc の設定項目、Codex CLI のモデル指定・provider-local 設定・推論 effort、並列数、アクセス違反時のリカバリ回数を追加・変更・確認するとき
- `cmoc oracle review` の所見列挙・マージ・検証ループの上限や設定構造を確認するとき
- 設定値の JSON 永続化、Enum 値の保存、既定の設定構成を確認するとき
- `{{cmoc-root}}`、`{{repo-root}}`、`{{work-root}}`、`{{run-root}}` の意味や解決規則を確認するとき
- agent call の cwd から worktree root と repository root を導出する処理、または call-scoped path context を変更するとき
- root placeholder を含むパスと絶対パスの相互変換、相対パスの入力制約を確認するとき
- 構造化文書ノードの型や子要素、見出し深度、Markdown レンダリングの基本挙動を確認するとき
- `<cmoc_block>` の生成、コードブロックの fence、空行の圧縮、インデント解除、バッククォートを含む本文のレンダリングを変更・確認するとき

## Do not read this when
- Codex CLI の呼び出し処理や個別 CLI コマンドの責務を確認したいときは、呼び出し側の実装を直接読むべきである
- `cmoc oracle review` のレビュー実行、所見生成、マージや検証のロジックを確認したいときは、その処理の実装を直接読むべきである
- 設定ファイルの実際の保存内容や、人間が行った設定調整の結果だけを確認したいときは、生成された設定ファイルを読むべきである
- 特定の CLI 機能が path model をどう利用するかを確認したいときは、その機能の実装や仕様を直接読むべきである
- パス解決の正本モデルではなく、Markdown レンダリングを利用する上位機能の挙動だけを確認したいときは、その上位機能を直接読むべきである
- cmoc ブロックの探索・展開やプロンプト生成など、Markdown レンダリング後の処理を確認したいときは、後段の実装を直接読むべきである
- 正本仕様やテスト条件だけを確認したいときは、対応する仕様書またはテストを直接読むべきである

## hash
- 4e982a98c8dd00b036282bc7703ac8f729d415995cf1f053539584aed353a7ae

# `prompt_builder`

## Summary
- プロンプト構築関連の型定義、完全プロンプト生成、エディタ入力初期文面、oracle／realization 説明文、共通 policy 定義を扱うディレクトリ。agent call の prompt 構成や policy の組み込み、入力テンプレート、分類規則、文書ルーティング方針を調査・変更する際の入口になる。

## Read this when
- agent call に渡す prompt の構成や policy の組み込みを調査・変更するとき
- プレースホルダ表現、エディタ入力テンプレート、oracle／realization の分類説明、共通 policy のいずれかを扱うとき
- prompt builder 配下で、対象の責務を担うモジュールや policy 定義への入口を特定したいとき

## Do not read this when
- 具体的な oracle file や realization file の仕様・実装挙動を直接確認することが目的のとき
- 通常の CLI 実装、テスト、文書作成など、prompt builder の構築規則に関係しない作業のとき
- 完全プロンプトの利用側や個別 agent の作業内容だけを調査するとき

## hash
- 419427df979099bbddbcd4e7d915f5aa4dc1863d73a936997e237be040527381
