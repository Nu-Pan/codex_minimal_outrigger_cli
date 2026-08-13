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
- AI エージェント呼び出しのパラメータ構築、完全 prompt の生成、Structured Markdown、パス・設定・規範モデルをまとめる実装群のルート。
- 用途別の agent call 定義は `acp_builder`、prompt の合成と入力処理は `prompt_builder`、feedback 入力契約は `feedback`、共有設定・パス・構造化文書モデルは `other` へ進む入口。
- 呼び出し条件やモデル・推論設定・ファイルアクセスモード・cwd・Structured Output の構築全体を確認するときに読む対象。

## Read this when
- AI エージェント呼び出しの共通パラメータ、モデルクラス、推論強度、ファイルアクセスモード、cwd、indexing preflight を調査・変更するとき。
- 用途別 agent call の起動定義や Structured Output schema の配置先を判断するとき。
- 複数の prompt 規範、routing 規則、placeholder、ファイルアクセス規則を完全 prompt へ統合する処理を調査するとき。
- agent call のパスコンテキスト、cmoc 設定、Structured Markdown の構造モデルを確認するとき。

## Do not read this when
- 特定用途の agent call 定義が明らかな場合は、`acp_builder` 配下の該当用途へ直接進むとき。
- prompt の個別規範や editor 入力処理だけを確認する場合は、`prompt_builder` 配下の該当実装へ直接進むとき。
- feedback の入力契約だけを調査する場合は、`feedback` 配下の schema を直接読むとき。
- 設定・パス・構造化文書の個別仕様だけを確認する場合は、`other` 配下の該当モデルへ直接進むとき。

## hash
- 88a3612c571892cfa0a6b9df05a7391f4f7070c662fa41df9c36e9e2daa87227
