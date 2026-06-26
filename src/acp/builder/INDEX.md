# `apply`

## Summary
- フォーク適用処理で使う AI エージェント呼び出しパラメータ群への入口。変更差分の要約、起点ファイルごとの所見列挙、列挙済み所見に基づく修正依頼について、プロンプト本文、モデル選択、推論量、ファイルアクセス権限、Structured Output schema の接続を組み立てる領域である。
- 差分解析、git 操作、実際のファイル修正を直接担う領域ではなく、下流エージェントへ渡す作業指示と出力契約を構成するための builder 群を収める。

## Read this when
- フォーク適用の各フェーズで、AI エージェントに渡す role、summary、goal、補助プロンプト、標準適用条件、ファイルアクセスモードを確認または変更したいとき。
- 変更差分を人間向けに要約する呼び出し、realization file の要修正点をファイル起点で列挙する呼び出し、列挙済み所見に基づいて修正作業を依頼する呼び出しのどれに進むべきかを判断したいとき。
- フォーク適用の作業レポートやレビュー・修正フェーズで使う Structured Output schema と、エージェント呼び出しパラメータとの対応を確認したいとき。
- raw diff、起点ファイル、所見リストなどの入力データが、どのような補助プロンプトとして埋め込まれ、どの権限でエージェントに渡されるかを追いたいとき。

## Do not read this when
- フォーク適用そのものの git 操作、ブランチ作成・削除、作業ツリーへの反映、複数ファイル処理の制御フローを調べたいとき。
- 実際に差分内容を解析するアルゴリズム、所見を統合・重複排除する処理、修正結果を検証する処理を探しているとき。
- complete prompt の共通構築規則、Markdown レンダリング、パスモデル、ACP の基礎型など、汎用部品の仕様や実装だけを確認したいとき。
- 個別の Structured Output 項目の詳細だけを確認したいときは、該当する schema 本文へ直接進めばよい。

## hash
- 4501a514ca3bce497bd7fa3e18fa6be68d3195b344f93832cb1ac6472b80d71e

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
- oracle file レビュー用の agent 呼び出しパラメータを組み立てる実装群をまとめる領域。新規所見の列挙、所見理由の追加調査、所見採否の判定、所見群の整理といった review oracle の各呼び出し単位を扱う。
- 各呼び出しについて、role、goal、標準 prompt、oracle 読み取り用の file access mode、model class、reasoning effort、Structured Output schema の対応を定義し、oracle file を根拠にした結果だけを返させるための入口になる。

## Read this when
- `cmoc review oracle` の agent 呼び出し内容、prompt、モデル設定、推論量、file access mode、出力 schema の対応を確認または変更したいとき。
- oracle file から新規レビュー所見を列挙する処理や、既知所見との重複回避、所見なしの場合の扱いを追いたいとき。
- 単一のレビュー所見について、oracle file に基づく支持理由と反対理由を追加調査する呼び出しを確認したいとき。
- 支持理由・反対理由を踏まえて、所見を人間へ提示するかどうか判定する処理を確認したいとき。
- 複数の oracle review 所見を、重複・矛盾・過剰な細分化の観点で削除・置換・統合する処理を確認したいとき。
- review oracle 標準や oracle 標準を組み込んだ complete prompt と、各 Structured Output schema の選択関係を確認したいとき。

## Do not read this when
- oracle file そのものの正本仕様内容や、レビュー対象として実際に調査すべき仕様断片を探しているだけのとき。
- oracle file と realization file の基本定義、編集責任、配置ルール、または oracle 標準そのものを確認したいとき。
- レビュー所見の保存、CLI 表示、通知、集計、実行フロー全体、サブコマンド入口処理を確認したいとき。
- oracle file 以外の実装レビューや、通常の realization file レビューの prompt 構築を調べたいとき。
- 汎用的な agent 呼び出しパラメータ、path 解決、Markdown レンダリング、構造化ドキュメント描画などの共通 helper の詳細を調べたいとき。
- Structured Output schema の項目名・型・JSON 形式だけを機械的に確認したいとき。

## hash
- b1d75be495b276bec9fcfd2c669325cd22163e90aeae6b48dfcb7e19be40bdf2

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
