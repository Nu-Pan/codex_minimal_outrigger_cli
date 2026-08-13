# `doc`

## Summary
- cmoc の正本文書を集約するドキュメント領域。アプリケーション仕様、branch・commit・worktree のモデル、採用しなかった設計案の検討記録、開発ルールへの入口を提供する。各領域の詳細確認が必要な場合は、対応する下位対象へ進む。

## Read this when
- cmoc の利用者向け挙動や機能間の責務境界を確認するとき
- session・run の分岐、commit、worktree の用語や関係を確認するとき
- realization refactor で不採用となった作業方式や設計案の理由を確認するとき
- Python 実装、CLI 設計、開発環境、テスト要件、テスト実行手順の正本文書を探すとき

## Do not read this when
- 確認対象の仕様本文、開発ルール、検討記録がすでに特定できており、その対象を直接読めばよいとき
- 実装コード、realization file、テスト内容、ログ、実行成果物の詳細を調べるとき
- INDEX.md の生成規則やルーティング情報だけを確認するとき

## hash
- db3b2317d3ce9c74020f6f1d2c764ffefc98c59bace4b5f94fef2a10cbc65c89

# `src`

## Summary
- AI エージェント呼び出しに必要なパラメータ、パスコンテキスト、設定、Structured Markdown、完全 prompt の構築基盤を提供する。
- acp_builder はモデル・推論・ファイルアクセスを含む agent call パラメータと用途別 builder、prompt_builder は共通 prompt と規則部品、other はパス解決・設定・構造化文書・要求モデルを扱う。各用途や共通機能を調査するときの上位入口として、配下の oracle、acp_builder、prompt_builder、other へ進む。

## Read this when
- agent call の共通パラメータ、モデル・推論設定、ファイルアクセスモード、cwd、Structured Output、indexing preflight を確認・変更するとき。
- 用途別の agent call builder、quota probe、oracle・realization・feedback・session・TUI の起動パラメータの配置先を判断するとき。
- 完全 prompt の組み立て、共通規則部品、パス placeholder の解決、設定モデル、構造化 Markdown の生成を調査・変更するとき。

## Do not read this when
- 特定用途の agent call 定義が明確なときは oracle または acp_builder 配下の該当領域を直接読む。
- prompt の共通部品や完全 prompt の構築だけが目的のときは prompt_builder 配下を直接読む。
- パス解決、設定、要求モデル、構造化 Markdown のいずれか一つだけが目的のときは other 配下の該当対象を直接読む。
- agent call の実行処理や対象ファイルの仕様を確認することが目的のときは、それぞれの実行側または仕様側の対象を直接読む。

## hash
- eb4fa8ae9a5cee5e1e2892c3c628f94d8034a17bc4b84e70917022eb576831b3
