# `basic.py`

## Summary
- AIコーディングエージェント呼び出し用の論理パラメータを定義するモジュール。モデルクラス、推論 esfuerzo、ファイルアクセスモード、および呼び出し条件を表す列挙型と、完全なプロンプト・Structured Output schema・作業ディレクトリなどを保持する不変の AgentCallParameter データクラスを提供する。ACP builder のパラメータ構築時に利用する基盤的な型定義への入口。

## Read this when
- agent call のモデル種別、推論強度、ファイルアクセス制御、プロンプト、schema、cwd、indexing preflight の設定を確認または変更するとき
- AgentCallParameter を生成・受け渡しする ACP builder の責務や入力項目を調べるとき

## Do not read this when
- 個別 builder の prompt 内容や field 値の決定規則を確認したいときは、該当する builder 実装を直接読む
- ファイルアクセスモードの正本仕様や Codex CLI sandbox との対応を確認したいときは、参照先の oracle 仕様を直接読む
- realization 側で論理モデル名をバックエンド受理可能なモデル名へ解決する処理を確認したいときは、realization src を直接読む

## hash
- 05194369257ffda7cd8be29b2b7d648cec6868897b7f08ed6ddef69de57f554f

# `feedback`

## Summary
- feedback 処理における issue の同一性判定と、既存 issue candidate の現在状態検証に使う Structured Output schema および AgentCallParameter 定義を扱うディレクトリ。normalize_issue 系は観測と候補の重複判定、verify_issue 系は report cut 時点の evidence に基づく verdict 判定の入口であり、feedback issue の生成・候補絞り込み・保存処理そのものではない。

## Read this when
- feedback observation と既存 issue candidate が同一か新規かを判定する出力契約や agent call の prompt・起動条件を確認するとき
- issue candidate の unresolved、resolved、not_actionable、inconclusive 判定に関する schema、prompt、参照制約、起動設定を確認するとき
- feedback verification 処理の構造化出力への適合性や、report cut references の受け渡しを調べるとき

## Do not read this when
- feedback issue の summary、impact、原因、actionability、human action、relation の生成・評価を確認するとき
- 候補の絞り込み、feedback state の読み取り、raw log・過去 session の参照、issue の保存や report cut 処理を確認するとき
- 一般的な JSON Schema、AgentCallParameter、prompt builder の共通仕様だけを確認するとき
- 個別 issue candidate や verification reference の具体的な内容だけを確認するとき

## hash
- 9f5f8f8b67b20e938d57dc4cf812cc620b846b30a7350cf0da31ad2272732ad4

# `indexing`

## Summary
- `cmoc indexing` の INDEX.md エントリー生成 agent call を構築する。対象本文を埋め込んだ prompt と、読み取り専用アクセス、モデル・推論設定、Structured Output schema、実行 cwd などの起動パラメータを定義する。
- `index_entry.json` は生成結果の JSON Schema を定義する。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成で、prompt の構成や agent call の起動パラメータを変更・確認するとき。
- 対象本文を読み取り専用で処理する indexing 用 builder の責務や設定を確認するとき。
- INDEX.md エントリーの出力形式や必須項目を確認・検証するとき。

## Do not read this when
- 既存の INDEX.md のルーティング内容だけを確認したいとき。
- エントリー生成結果の構造や検証形式だけを確認する場合は、`index_entry.json` を直接読むとき。
- INDEX エントリー生成以外の agent call パラメータを調べるときは、各目的に対応する別の builder を直接読む。

## hash
- a5f3fadd4ccbca14ab84f5a8972f846cb92a03fc09d7164171da99b26805f71f

# `oracle`

## Summary
- oracle の edit・investigation・review 各サブディレクトリへ進むためのルーティング入口。各領域の agent call 起動条件、prompt、アクセス境界、モデル設定、indexing、review 用 Structured Output 契約の確認先を案内する。
- edit は oracle 編集用 call の起動パラメータと prompt 構築、未コミット差分の扱い、配下の fork ディレクトリを扱う。
- investigation は oracle 調査用 TUI の起動条件、完全 prompt、読み取り専用アクセス、モデル・推論・作業ディレクトリ設定を扱う。
- review は oracle review の所見列挙・採否・統合と、支持理由・反証理由、および各段階の Structured Output schema を扱う。

## Read this when
- cmoc oracle edit、investigation、review の agent call 構築や起動条件を確認・変更するとき
- oracle 編集・調査・レビューで使う prompt、モデル、推論強度、アクセス境界、作業ディレクトリ、indexing 設定を確認するとき
- review の所見処理や Structured Output の出力契約を確認するとき
- edit 配下の fork に新しいファイルが追加され、その用途を確認するとき

## Do not read this when
- 実際の oracle 編集処理や call 実行制御を確認・変更するとき
- 共通の prompt 構築、パラメータ型、パス解決、Structured Document の一般的な定義だけを確認するとき
- oracle file の編集規約・設計・テスト要件を確認するとき
- review の個別 schema の項目や形式だけを確認したいとき
- 個別ファイルを直接確認できる edit/fork の内容や、oracle review のサブコマンド実装そのものを調べるとき

## hash
- b4e8fa457b96e75fc7dfe4bf7dabc90b40328a8cac4abfff86b189c7b681d7e3

# `quota_probe.py`

## Summary
- Codex CLI の quota 回復確認用 agent call を構築する定義。利用可能性だけを短く確認する prompt と、READONLY・最小モデル・低 reasoning・preflight 無効などの起動パラメータをまとめ、quota probe の呼び出し設定の入口となる。

## Read this when
- quota 回復確認用 agent call の prompt 文面や起動パラメータを変更・確認するとき
- quota availability probe の実行条件、コスト抑制、再帰的 preflight 回避の設定を追跡するとき

## Do not read this when
- quota probe 自体ではなく、通常の agent call の基本型や共通 prompt 構築規則を確認したいとき
- quota 回復確認の呼び出し結果や CLI 実行処理を直接調べるとき

## hash
- 7ea1a12c739aa06c552a5c0fedb97452249d3a392e01a0bb6886904705dec248

# `realization`

## Summary
- `realization apply fork` と `refactor fork` の Agent call 起動定義を扱うディレクトリ。apply では oracle file の差分を realization file へ反映する追従処理、refactor では差分要約およびファイル単位のレビュー・修正処理への入口を提供する。

## Read this when
- `realization apply fork` の追従対象変更、prompt、アクセス権限、作業ディレクトリ、起動パラメータ、完了条件を確認・変更するとき。
- `refactor fork` の差分要約またはファイル単位のレビュー・修正における調査範囲、修正方針、検証条件、アクセス方針を確認するとき。
- 配下の Agent call に対応する Structured Output schema への入口を探すとき。

## Do not read this when
- `realization apply fork` 以外の apply 経路を調べるときは、該当する apply 配下の対象を直接読む。
- 共通 prompt 生成や構造化ドキュメント仕様を調べるときは、`build_complete_prompt` や `struct_doc` の定義を直接読む。
- 個別の realization implementation・test・ancillary、oracle file の変更内容、repository 共通の開発ルールを確認するときは、それぞれの対象を直接読む。
- 差分要約やレビュー・修正の具体的な出力項目・型・形式だけを確認するときは、対応する schema file を直接読む。

## hash
- 4f68157313eef19ad94633dbbb69a517aadb675078df32d5fc0ed0ea663139fd

# `session`

## Summary
- `cmoc session join` における merge conflict marker 解消用エージェント呼び出しを定義するディレクトリ。対象パスの実パス解決、専用 prompt、リポジトリ書き込み権限、最高品質のモデル・推論設定、preflight 無効化を扱う。conflict 解消の実装詳細を確認する入口となる。

## Read this when
- `cmoc session join` の conflict marker 解消用エージェント呼び出しを変更するとき
- conflict 解消対象ファイルのパス解決、prompt の制約、書き込み権限、モデル・推論設定、preflight 設定を確認するとき

## Do not read this when
- 通常の `session join` 処理や merge 操作そのものを変更するとき
- 共通の prompt 生成処理や一般的なエージェント呼び出しパラメータを調べるとき

## hash
- e808a98687d24a24ec6a97a0f2ebfe4fd990848faf3ab2c727915eb56d08aaa3

# `tui`

## Summary
- `cmoc tui` の起動に必要な AgentCallParameter を構築するディレクトリ。ユーザー入力を埋め込んだ完全プロンプトを生成し、リポジトリ書き込み権限、最高品質のモデル設定、起動前の indexing preflight などの TUI 実行条件を定義する。具体的な起動パラメータの組み立てを確認する入口として `launch_tui.py` を読む。

## Read this when
- `cmoc tui` の起動条件、モデル・推論設定、ファイルアクセス権、作業ディレクトリ、preflight 実行設定を確認または変更するとき。
- ユーザーのオリジナルプロンプトを固定ポリシー付きの完全プロンプトへ組み込む処理を確認または変更するとき。

## Do not read this when
- TUI の内部描画や対話操作の実装を確認したいとき。
- 共通の完全プロンプト構築処理そのものを確認したいときは、`complete_prompt` の実装を直接読む。

## hash
- 1993a6da91988c4dde257bb00f4574ee1f48d1524fb014585df2148ebfbf8891
