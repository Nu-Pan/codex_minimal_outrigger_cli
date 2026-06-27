# `apply`

## Summary
- `cmoc apply fork` 向けの AI 呼び出しパラメータ構築を扱う領域。変更差分の人間向け要約、起点ファイルごとの所見列挙、列挙済み所見をもとにした realization file 修正依頼という各段階で、prompt、補助入力、file access mode、model/reasoning、Structured Output schema をどう組み立てるかへの入口になる。
- 実際の fork 適用処理や git・作業ツリー操作ではなく、apply fork の各フェーズで AI に何を読ませ、どの権限で呼び出し、どの構造化出力を期待するかを定義する。

## Read this when
- `cmoc apply fork` の作業レポート用に、raw git diff をカテゴリ別の変更要約へ変換する AI 呼び出しや出力契約を確認したいとき。
- 起点となる oracle file または realization file から関連ファイルを読ませ、realization file の要修正所見を列挙させる調査フェーズの prompt、モデル指定、権限、出力形式を確認または変更したいとき。
- 検出済み所見を AI への修正作業指示へ変換する際の prompt 内容、realization file 書き込み権限、git add/commit 禁止、realization standard 適用条件を確認したいとき。
- apply fork 系で、raw diff、起点パス、所見 JSON などの補助入力が complete prompt と AgentCallParameter にどう接続されるかを追いたいとき。
- apply fork の要約・所見列挙フェーズにおける Structured Output schema の意味的な責務と、その schema を使う呼び出し側の対応関係を確認したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、実行フロー全体、git branch 操作、実際の fork 適用処理、作業ツリー変更処理を調べたいだけのとき。
- 個々の差分検出、差分分類アルゴリズム、ファイル列挙、複数ファイル分の呼び出し集約、結果の適用制御を確認したいとき。
- complete prompt の共通構築規則、Markdown rendering、StructDoc、path model、file access mode、AgentCallParameter などの基礎型や共通定義そのものを調べたいとき。
- 単一ファイルの本文内容、具体的な変更後コード、または realization file の実装修正箇所を直接調べたいだけのとき。
- 一般的な INDEX.md 用エントリーの書き方やルーティング文書全体の規約を確認したいとき。

## hash
- d0ed97b71e987d094ce82f137529135272604cffd96cb0c787bf7cccb0bbd82f

# `indexing`

## Summary
- cmoc の目次情報生成のうち、対象ファイルまたはディレクトリから INDEX.md 用エントリーを作る AI 呼び出し設定と、その structured output の外形を扱う領域。
- 対象パスの解決、読み取り専用プロンプトへの役割・目的・制約・本文埋め込み、モデルや推論負荷、出力検証 schema の指定を確認する入口となる。
- エントリーに書く意味内容の判断そのものではなく、個別対象からエントリーを生成させるための呼び出し条件と返却形の制約を扱う。

## Read this when
- cmoc indexing が個別対象の INDEX.md エントリー生成を AI に依頼する流れや呼び出しパラメータを確認したいとき。
- エントリー生成時に既存 INDEX.md を根拠にさせず、対象本文と必要な関連文書だけを読む制約を調整したいとき。
- 生成結果の検証で、要約、読む条件、読まなくてよい条件を配列文字列として返し、余分な項目を許さない外形を確認したいとき。
- 目次情報生成用のモデル選択、推論負荷、ファイルアクセスモード、structured output schema の指定に関係する実装を変更するとき。

## Do not read this when
- INDEX.md 全体を走査、更新、保存するファイルシステム処理を調べたいとき。
- 生成されたエントリーを markdown として描画する処理や、目次ファイル全体の組み立てを調べたいとき。
- 特定の対象について実際に読むべきかどうか、またはエントリーにどの意味内容を書くべきかを判断したいとき。
- 通常の実装変更やテスト追加で、目次情報生成プロンプト、AI 呼び出し設定、出力 schema に関係しないとき。

## hash
- a7628c344fe8ab13d81cb306fe13865c27f52674f0200efbb0196feca500a2a2

# `review`

## Summary
- `cmoc review oracle` のレビュー担当 AI 呼び出しに使う builder 群をまとめる領域。oracle file から新規所見を列挙し、所見の支持理由・否定理由を追加調査し、提示採否を判定し、既存所見リストを整理する各段階の呼び出し定義を扱う。
- 各段階でレビュー担当 AI に渡すロール、目標、補助文脈、oracle 読み取り前提、モデル区分、推論量、Structured Output 契約との対応を確認する入口になる。

## Read this when
- `cmoc review oracle` の所見列挙、所見検証、採否判定、所見整理で使う AI 呼び出しパラメータを確認または変更したいとき。
- レビュー対象、既知所見、既知の支持理由、既知の否定理由、現状の所見リストを、oracle review 用プロンプトがどのように補助文脈として渡すか確認したいとき。
- oracle file を根拠にしたレビュー結果について、新規所見、新規の支持理由、新規の否定理由、採否判定、整理操作のいずれかの Structured Output 契約を確認したいとき。
- oracle review の各段階で、読み取り専用の oracle アクセス、標準文脈、モデル区分、推論量、応答スキーマ参照がどう接続されるか追いたいとき。

## Do not read this when
- `cmoc review oracle` の CLI 引数解析、サブコマンド配線、実行順序、保存、表示、入出力管理を調べたいとき。
- レビュー対象となる個々の oracle file の正本仕様本文や、oracle file 自体の標準・品質基準を読みたいとき。
- 共通プロンプト部品、構造化文書レンダリング、パス解決、AI 呼び出しパラメータ型そのものの実装を確認したいとき。
- oracle review 以外のレビュー種別や、一般的な JSON Schema 構文だけを調べたいとき。

## hash
- e26067e72d898d32b326c708729c24c0cb480da17a4084bf89f9288d93eb0374

# `session`

## Summary
- AI エージェントへ依頼する session 関連処理の呼び出しパラメータを組み立てる領域。対象パスの解決、対象ファイル一覧、作業範囲、禁止事項、例外的な編集許可を含む complete prompt とモデル設定の確認入口になる。

## Read this when
- session 関連コマンドから AI エージェントへ渡す呼び出しパラメータ、complete prompt、モデル設定を確認または変更したいとき。
- merge conflict marker 解消の対象ファイルが worktree 上の実パスへどう解決され、AI への対象一覧や作業範囲としてどう渡されるかを確認したいとき。
- conflict marker 解消時の作業境界、禁止事項、oracle file の限定的な編集例外を確認または調整したいとき。

## Do not read this when
- session 関連コマンド全体の制御フロー、merge 実行、conflict 検出、状態管理を調べたいとき。
- complete prompt の共通構築、構造化 markdown レンダリング、path model、AgentCallParameter 型そのものを調べたいとき。
- AI 呼び出し後の検証、テスト、CLI 入出力の外部仕様を確認したいとき。

## hash
- befc1a0955fd583c3a081c4e67e6b5e71b4234dfb3b41fece2837fcf6c832c09

# `tui`

## Summary
- 対象ファイル本文から、TUI のパラメータ解決用プロンプト構築と、その判定結果 schema を扱う領域として要約を作ります。既存の `INDEX.md` は読まず、対象ディレクトリ直下の本文だけ確認します。

## Read this when
- TUI で入力された依頼から、AI Agent CLI/TUI 実行時のファイルアクセス権限や参照すべき標準群を選ばせる parameter resolve 処理を確認・変更するとき。
- パラメータ解決担当へ渡すプロンプト、アクセスモード候補、モデル・reasoning・sandbox・Structured Output schema の対応を確認するとき。
- パラメータ解決結果として、権限選択と oracle・realization・review・INDEX.md エントリー作成標準の参照要否をどのような論理情報で返すかを確認するとき。

## Do not read this when
- TUI サブコマンドの起動、エディタ入力、元プロンプトの前処理、または解決結果を実際の起動パラメータへ適用する処理を調べるとき。
- 各ファイルアクセスモードや各標準文書の本文そのものを確認・変更したいとき。
- oracle file や realization file の責務、編集可否、品質基準、または INDEX.md エントリー本文の一般的な書き方だけを確認したいとき。

## hash
- 778e755d0682c8f5994005e35065398602a0b7a42afacc310d4d8a531363ac3a
