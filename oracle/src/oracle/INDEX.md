# `acp_builder`

## Summary
- `oracle/src/oracle/acp_builder` は、oracle 関連の agent call を構築する下位モジュール群への入口。共通の AgentCallParameter 定義を基盤に、feedback、indexing、oracle、quota probe、realization、session、TUI など目的別の prompt・Structured Output・起動条件を分担する。
- agent call の目的別設定、prompt、モデル・推論強度、ファイルアクセス権、作業ディレクトリ、preflight、出力 schema の入口を探すときに読む。

## Read this when
- oracle 用 agent call の構築責務を確認・変更するとき
- feedback、indexing、quota probe、realization、session、TUI など、目的別 agent call の prompt や起動条件の確認先を探すとき
- AgentCallParameter と各用途の Structured Output schema の関係を調べるとき

## Do not read this when
- 共通の AgentCallParameter 型そのものだけを確認したいときは、`basic.py` を直接読む
- 個別 builder の具体的な prompt 内容や field 値の決定規則を確認したいときは、該当する下位対象を直接読む
- agent call の実行制御、oracle file の編集・調査・レビュー処理、realization の実装処理そのものを確認したいときは、対応する実装を直接読む
- Structured Output の具体的な項目や形式だけを確認したいときは、対応する schema file を直接読む

## hash
- 13acc4fa4882260c5f9834607316d5b64371e2da4994d4c71dc823982e262642

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
- cmoc の共通モデルと Markdown 文書生成ヘルパーをまとめたモジュール群。
- Codex CLI・oracle review・並列実行などのリポジトリ設定、root placeholder と agent call 単位のパス解決、構造化文書ノードの保持と GFM レンダリングを扱う。
- 設定モデル、パス境界、構造化 prompt 文書の表現や出力処理を確認する際の入口となる。

## Read this when
- cmoc の設定モデルや既定値、Codex CLI・oracle review の設定項目を確認するとき
- {{repo-root}}、{{work-root}}、{{run-root}}、{{cmoc-root}} の解決や agent call の作業ルート境界を確認するとき
- SDHeader、SDTagBlock、SDCodeBlock、SDPolicy の構造化文書モデルや Markdown レンダリングを確認するとき

## Do not read this when
- Codex CLI の呼び出し処理、prompt builder、oracle review の所見生成など、これらのモデルを利用する側の責務だけを確認したいとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認したいとき
- 参照の対応検査、ポリシーの意味的統合、prompt part の選択を確認したいとき

## hash
- a50c040f76062b8858f56e510a96342ae8409c92debd928ce6af41a1bc14e7fe

# `prompt_builder`

## Summary
- prompt builder の基本型、完全 prompt 構築、エディタ入力、prompt 部品、policy 実装を扱うディレクトリ。agent call 用 prompt の構成や、各 policy・placeholder・入力初期文面の生成処理へ進むための入口。
- `basic.py` は構築時 placeholder map の型定義、`complete_prompt.py` は policy・補助文面・objective・placeholder を統合した完全 prompt の構築、`editor_input.py` はエディタ用初期入力の生成を担当する。
- `parts` は oracle／realization の分類説明部品、`policy` は file access・routing・feedback・findings・conflict resolution など各 policy の構築を担当する。

## Read this when
- agent call 用 prompt の全体構成や、policy・static/dynamic part・objective・placeholder の統合順序を確認または変更するとき。
- prompt 構築時の placeholder map の型、値の許容範囲、同名定義の衝突処理を確認するとき。
- エディタ入力の初期表示文面や、完全 prompt skeleton の Markdown 化・埋め込み処理を確認するとき。
- oracle／realization の分類説明や、各種 agent call policy の構築責務へ進む入口を判断するとき。

## Do not read this when
- 個別 policy の正本文面や適用条件だけを確認したいときは、対応する oracle または app_spec を直接読む。
- 個別ファイルや下位 policy の具体的な挙動を確認したいときは、該当する下位ファイルを直接読む。
- SDHeader・SDTagBlock・FileAccessMode・AgentCallPathContext などの共通型仕様だけを確認したいときは、それぞれの定義元を直接読む。
- INDEX.md のルーティング規則や entry の内容だけを作成・確認したいときは、prompt 構築実装ではなく対象の INDEX.md と routing 規定を読む。

## hash
- a537596f92808d37f7f9fc782dbc052f5b2e4ed74b021c17693b096d5a7bcd62
