# `doc`

## Summary
- cmoc の正本ドキュメント群を機能・設計・開発ルールごとに参照する入口。アプリケーション仕様、session／run の branch model、不採用案、Python 開発ルールへの導線を提供する。
- 各下位文書の責務境界と、実装・テスト・CLI 契約・環境構築など個別の確認先を示す。

## Read this when
- cmoc の仕様・設計・開発ルールを横断して、最初に読むべき正本文書を探すとき。
- CLI やアプリケーション挙動、session／run の git 隔離モデル、Python 実装規則、テスト要件・実行手順の参照先を判断するとき。
- 現行設計で採用されなかった代替案と、その不採用理由を調査するとき。

## Do not read this when
- 確認対象の機能、設計要素、開発規則に対応する下位文書が明確で、その文書を直接読むべきとき。
- 具体的な CLI 入出力契約、実装コード、テストコード、外部契約、環境操作手順など、正本文書群の概観を必要としないとき。
- 採用済み workflow の具体的な操作方法や現在の実行結果だけを確認したいときは、該当する仕様・実装・テスト文書へ直接進むとき。

## hash
- 918be1efa91d612e344dfe3027b1018ad6a7e51d4d1fe695a8f0147231889227

# `src`

## Summary
- cmoc の agent call 構築・prompt 構築・補助モデルを実装する Python ソースのルート。AgentCallParameter、モデル種別、推論強度、ファイルアクセスモード、パスコンテキスト、構造化文書レンダリングなどの共通定義を含む。
- 機能別の agent call builder は `oracle` 配下に分かれており、`acp_builder` は agent call の起動パラメータ、`prompt_builder` は完全 prompt と各種 policy、`other` はパス・設定・構造化文書の補助定義を扱う。feedback 用の入力定義も `oracle` 配下にある。

## Read this when
- agent call の共通パラメータ、論理モデル種別、推論強度、ファイルアクセスモード、agent call の cwd や root path の扱いを確認するとき。
- oracle、realization、feedback、indexing、session、TUI などの機能別 agent call builder を調査・変更するときは `oracle/acp_builder` へ進むとき。
- 完全 prompt の組み立て、placeholder の統合、oracle・realization・feedback・routing・file access などの policy を確認するときは `oracle/prompt_builder` へ進むとき。
- AgentCallPathContext、root path の解決、設定、構造化文書の生成・Markdown レンダリングを確認するときは `oracle/other` へ進むとき。
- feedback reporter の入力形式を確認するときは `oracle/feedback` へ進むとき。

## Do not read this when
- Codex CLI などの実際の agent call 実行処理や、抽象的なモデル・推論設定を具体的な CLI 引数へ変換する処理を確認したいとき。
- oracle や realization の意味仕様、正本文書、または実装・テストそのものを確認したいときは、対応する `oracle/doc`、`src`、`test` の対象へ直接進むとき。
- 既存の INDEX.md のルーティング内容だけを確認したいとき。

## hash
- 6e4bed8d8216f30c5d59a99ed73581d248342ba4b3e0fe7457fb4bc97c3049a7
