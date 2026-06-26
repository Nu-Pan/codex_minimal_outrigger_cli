# `apply`

## Summary
- fork 適用後のレビュー・修正サイクルにおける AI 呼び出しの組み立てを扱う領域。差分要約、oracle と realization の乖離や要修正点の列挙、列挙済み所見への対応依頼について、prompt 構成、モデル指定、reasoning effort、file access mode、structured output 契約への接続を確認する入口となる。

## Read this when
- fork 適用後の変更内容を、人間向けにカテゴリ単位で要約する AI 呼び出しや出力契約を確認・変更したいとき。
- oracle と realization の不一致や要修正点を、根拠位置、要求、観測実装、問題理由、修正方針つきで列挙する調査呼び出しを確認したいとき。
- 列挙された所見を AI エージェントへ渡して realization file を修正させるための prompt、権限、モデル、reasoning effort を確認・調整したいとき。
- apply fork 系の要約、レビュー、所見対応で使われる structured output schema と prompt builder の対応関係を追いたいとき。

## Do not read this when
- fork の生成、適用、ブランチ操作、差分取得、サブコマンド引数解析など、apply fork 全体の実行制御だけを調べたいとき。
- oracle standard、realization standard、apply review standard の本文や判定基準そのものを確認したいとき。
- complete prompt の共通組み立て、markdown レンダリング、パス解決、AgentCallParameter 型定義など、汎用 helper の内部実装を調べたいとき。
- 個々の実際の差分内容や変更ファイル本文を直接レビューしたいだけのとき。

## hash
- 7d15e626ff06c8cfe06f9b663e68ee93a15528a94fe0b1f5af7bfe54dc9359c6

# `indexing`

## Summary
- 個別対象のルーティング情報を生成するための実装領域であり、生成結果に求める構造の定義と、AI へ渡す呼び出し条件の組み立てを扱う。
- 目次エントリー生成で使うプロンプト、読み取り専用前提、対象本文の埋め込み、Structured Output の保存先、モデル設定、出力検証の形を確認する入口になる。

## Read this when
- 目次エントリー生成処理で、対象パスと対象内容から AI 呼び出し条件がどのように作られるかを調べたいとき。
- 生成される目次エントリーが満たすべき構造や、検証で要求される意味領域を確認したいとき。
- ルーティング文書作成担当向けの役割、目的、生成規則、対象本文がプロンプトへどう反映されるかを追いたいとき。

## Do not read this when
- 目次生成全体の対象探索、既存目次の読み書き、CLI サブコマンドの実行フローを調べたいときは、より上位の実装を読む。
- 共通のプロンプト部品、Markdown レンダリング、パスモデル、AI 呼び出しパラメータ型そのものの仕様を調べたいときは、それぞれの共通モジュールを読む。
- 特定対象に対して実際に生成済みのルーティング本文や、文章品質の一般基準だけを確認したいときは、その対象や基準を定義する文書を読む。

## hash
- ca765591b805b214160cde03dc54ac63f77ae131dbef192a715972a8779c37fc

# `review`

## Summary
- `cmoc review oracle` の各レビュー段階について、AI 呼び出しへ渡すロール、ゴール、補助入力、標準文書、モデル設定、ファイルアクセス方針、Structured Output schema 参照を組み立てる実装をまとめる領域。
- レビュー対象の oracle file から新規所見を列挙する段階、所見の擁護・反証理由を列挙する段階、人間へ提示するかを判定する段階、複数所見を整理・統合する段階の入口になる。
- レビュー用サブタスクのプロンプト構成と、各段階が期待する構造化出力契約との対応を追うための実装群である。

## Read this when
- `cmoc review oracle` の oracle file レビューで、各サブタスクに渡す AI 呼び出しパラメータの設計や変更箇所を調べたいとき。
- 新規所見列挙、所見の擁護理由列挙、反証理由列挙、人間提示の採否判定、所見リストの整理・統合のうち、どの段階の実装を読むべきか切り分けたいとき。
- 既知所見、既知理由、対象所見、所見リストなどの補助入力が、レビュー用プロンプトや構造化出力 schema 参照へどう接続されるか確認したいとき。
- レビュー各段階で参照される標準文書、読み書き制限、モデル設定、出力 schema と、呼び出し側実装の対応関係を確認したいとき。

## Do not read this when
- oracle file そのものの正本仕様内容、oracle と realization の基本概念、またはレビュー標準文書の本文を理解したいとき。
- CLI 引数解析、レビュー結果の保存・表示・通知、返却された編集操作の適用など、レビュー用 AI 呼び出し後の処理を調べたいとき。
- 個別の oracle file を探索して、仕様矛盾・表記揺れ・命名問題などを実際に判定するロジックを探しているとき。
- Structured Output schema の一般的な設計方法や JSON Schema 検証ライブラリの使い方だけを確認したいとき。

## hash
- a92724761f55a78661605824c31c83b317af9bd3293db6e2f9365e7bd25ec0cf

# `session`

## Summary
- `cmoc session join` の merge conflict marker 解消フェーズで、AI エージェントへ渡す `AgentCallParameter` を組み立てる領域。
- conflict 対象パスを作業ルート基準の実パスへ解決し、解消対象一覧、編集範囲、禁止事項、oracle file 例外を含む完了用プロンプトを生成する。
- 呼び出しパラメータには mainstream モデル、中程度 reasoning、realization write のファイルアクセスモード、生成済み markdown prompt、編集対象パス集合を設定する。

## Read this when
- `cmoc session join` の conflict marker 解消作業で、AI 呼び出しに渡す role、goal、file access rule、対象ファイル一覧を確認または変更したいとき。
- merge conflict marker 解消時に、oracle file の編集を例外的に許可する条件や、git add / git commit を禁止する制約を確認したいとき。
- conflict 対象パスの解決方法、プロンプトへの対象ファイル一覧の埋め込み方、`AgentCallParameter` の構成を追いたいとき。

## Do not read this when
- 通常の `cmoc session join` の join 処理全体、branch 操作、merge 実行、conflict 検出の流れを調べたいだけのとき。
- merge conflict marker の実際の解消アルゴリズムや、対象ファイル本文をどう編集するかを調べたいとき。
- 汎用的なプロンプト構築部品、markdown rendering、パスモデルの詳細仕様を調べたいとき。

## hash
- aa43cebd3069435c14a04dbca1b16b569c7e77a75e9026c8c76d83d13eb90374

# `tui`

## Summary
- AI Agent CLI/TUI の実行前パラメータ解決に関する実装と検証構造を扱う領域。元プロンプトからファイルアクセスモード、標準文書群の参照要否、モデル種別、推論強度、出力先を決めるためのエージェント呼び出し内容と、その結果を検証する構造を確認する入口になる。

## Read this when
- TUI で入力された元プロンプトを、実行前のモデル・推論強度・ファイルアクセス権限・structured output 保存先へ変換する処理を調査・変更するとき。
- オリジナルプロンプトから、oracle と realization の基本事項、各種標準、レビュー適用、INDEX.md エントリー生成に関する標準を読む必要があるかどうかを機械的に判定する仕様を確認するとき。
- パラメータ解決結果に含めるファイルアクセスモードの候補、標準プロンプト群の有効化範囲、判定理由の必須性を確認するとき。
- TUI/CLI のパラメータ解決結果を structured output として検証するための形、必須項目、許容される権限分類を確認するとき。

## Do not read this when
- 各標準文書そのものの要求内容、oracle file や realization file の定義、レビュー適用や INDEX.md エントリー生成の具体手順を確認したいとき。ここは参照要否や結果形式を扱う入口であり、標準本文の代替ではない。
- 実際のファイルアクセスモードごとの規則文、リポジトリルートや作業ルートの解決規則、共通のプロンプト組み立て処理や markdown レンダリングの詳細だけを調べたいとき。
- TUI の画面操作、入力編集、サブコマンド起動フロー、現在の UI 表示挙動を調べたいとき。ここは実行前パラメータ選定とその検証構造に範囲が限られる。

## hash
- ba373163b40d00ce5e87506dde390b172fd3ec20f6b1f97001f7700615eba88b
