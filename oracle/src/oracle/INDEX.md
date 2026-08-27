# `acp_builder`

## Summary
- ACP builder の共通データモデルと、各 cmoc 機能で使用する Codex CLI agent call の prompt・起動パラメータ構築をまとめた領域です。
- feedback、indexing、oracle、realization、session、tui、quota probe の agent call 定義と、Structured Output を使う処理の出力契約を扱います。
- 共通の呼び出しパラメータや列挙型を確認する場合は `basic.py`、機能別の起動定義を確認する場合は各下位ディレクトリへ進みます。

## Read this when
- agent call のモデルクラス、推論強度、ファイルアクセスモード、prompt、cwd、Structured Output schema、indexing preflight の共通契約を確認・変更するとき
- cmoc の feedback、indexing、oracle、realization、session join、tui、quota probe が構築する agent call の prompt や起動条件を調査するとき
- 特定機能の agent call 定義を探すときに、feedback、indexing、oracle、realization、session、tui の下位ディレクトリを入口として参照するとき

## Do not read this when
- Codex CLI の実際の実行処理やバックエンドモデル名への変換規則を確認したいとき
- agent call が利用する oracle file、realization file、feedback state、既存 INDEX.md の内容を確認したいとき
- prompt 生成や構造化文書の共通実装、パス解決、ファイルアクセス policy の正本を直接確認すれば足りるとき

## hash
- 485c046c046220f2f516614fdcd565ed4c259683cea1d2e1abd30154c9453185

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
- cmoc の設定モデル、パス表記・ルート解決、構造化文書の Markdown レンダリングを扱う補助モジュール群。設定値や既定値、agent call のパス境界、文書要素の整形規則を確認する際の入口となる。

## Read this when
- cmoc の設定項目、Codex CLI 設定、oracle review のループ上限、設定値の JSON/TOML 表現を確認するとき
- agent call の cwd から work root・repository root を導出する規則や、ルートプレースホルダー付きパスの解決・変換を確認するとき
- 構造化された見出し、参照可能な cmoc ブロック、コードブロック、規定文を Markdown へレンダリングする挙動を確認するとき

## Do not read this when
- Codex CLI の実際の呼び出し処理や CLI 実装の責務を確認するとき
- oracle review のレビュー処理や所見生成ロジックそのものを確認するとき
- 設定ファイルの保存内容・人手による調整結果だけを確認するとき
- 具体的な正本仕様や生成文書の内容を確認する必要があり、別の仕様・呼び出し元を直接読むべきとき

## hash
- 6125a10678c23ca628f6b05330ed05e7e19dcdfdc72e272f7ec6c54533ce00a1

# `prompt_builder`

## Summary
- プロンプト生成に関する共通定義をまとめるディレクトリ。完全 prompt の構築、エディタ入力文面の生成、oracle／realization の基本説明、各種 policy の構築を扱う。個別のプロンプト規定や構築経路を調査する際の入口となる。

## Read this when
- agent call に渡す完全 prompt の構成や placeholder 統合を確認するとき。
- エディタへ注入するプロンプト初期文面の生成を確認するとき。
- oracle／realization の基本説明、または prompt policy の構築箇所を特定するとき。
- 個別の policy や prompt 部品へ進む前に、全体の構成要素と責務分担を把握するとき。

## Do not read this when
- 実際の oracle file・realization file の意味仕様や実装を確認するとき。
- プロンプトを利用する agent call の呼び出し側の責務を調べるとき。
- 構造化文書のデータ構造や Markdown レンダリング自体を確認するときは、対応する共通モジュールを直接読む。
- 個別 policy の具体的な規定だけを確認するときは、policy ディレクトリ内の該当モジュールを直接読む。

## hash
- 7ba366ab6721c6e4c8fa9b54c7372a2b84b33eb05348b2335430190fc8e5127b
