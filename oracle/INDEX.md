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
- oracle の実装ソースを集約する領域。AI エージェント呼び出しの論理パラメータ、モデル・推論強度・ファイルアクセス、cwd と indexing preflight、リポジトリ設定、root placeholder を含むパス解決、Standard と構造化文書、完全 prompt の構築、feedback reporter 入力契約を扱う。用途別の agent call 定義や oracle review など、より具体的な実装領域へ進む前の入口として機能する。

## Read this when
- 共通の agent call パラメータ、モデル選択、推論強度、ファイルアクセス制約、Structured Output、indexing preflight の実装を調べるとき。
- agent call の cwd を起点とした work root・repository root・run root の解決や、prompt 内の root placeholder の扱いを確認するとき。
- Standard の合成、構造化文書の Markdown 化、placeholder を含む完全 prompt の構築規則を確認するとき。
- feedback reporter が受け取る問題分類、影響、原因の確度、根拠、継続状態を確認するとき。
- 共通実装ではなく、用途固有の acp builder、prompt の Standard、feedback 処理、oracle review へ進むべきかを判断するとき。

## Do not read this when
- 特定の用途に固有な agent call の起動定義や Structured Output の内容が対象で、用途別の実装を直接確認できるとき。
- Codex CLI の実行処理、realization 側の個別仕様、collector による feedback の保存・集約だけを調べるとき。
- oracle の共通モデルや prompt 構築を利用しない機能の実装詳細だけを確認するとき。

## hash
- 53c3dbb84061e18a276869bb584969d192572d52a3d494907143a867cc197c20
