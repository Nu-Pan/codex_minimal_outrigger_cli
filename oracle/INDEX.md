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
- oracle/src は、cmoc の oracle 実装を構成する Python パッケージのルートである。agent call の論理パラメータ、prompt の組み立て、Structured Output schema、設定・パス・構造化文書のモデル、feedback 入力契約を扱う。
- acp_builder は用途別の agent call パラメータを構築する。session、tui、feedback、indexing、oracle review、oracle edit/investigation、realization apply/refactor の各処理へ進む入口である。
- prompt_builder は共通 prompt と構成部品を組み立てる。アクセス規則、oracle・realization 規則、routing、index entry、feedback、conflict resolution の標準文面を確認するときに進む。
- other は agent call と prompt 構築で共有する設定、パス、構造化文書、標準規約のモデルを提供する。個別の共通型や変換処理を確認するときに進む。
- feedback は feedback reporter の入力契約を定義する。feedback issue の正規化・検証用 agent call と、reporter input schema を確認するときに進む。

## Read this when
- oracle/src 配下の複数領域にまたがる agent call、prompt、schema、共有モデル、feedback 契約の関係を調査・変更するとき。
- 対象領域が acp_builder、prompt_builder、other、feedback のどれに属するかを判断し、下位ディレクトリへの調査入口を選ぶとき。
- oracle 実装パッケージ全体の責務分担や、用途別 agent call 定義と共通 prompt・共有モデルの接続を確認するとき。

## Do not read this when
- 特定の agent call の prompt と起動パラメータだけを確認する場合は、該当する acp_builder 配下へ直接進む。
- 共通 prompt の単一部品だけを確認する場合は、該当する prompt_builder 配下へ直接進む。
- 設定・パス・構造化文書など単一の共有モデルだけを確認する場合は、other 配下へ直接進む。
- feedback reporter の入力項目や feedback issue の個別処理だけを確認する場合は、feedback 配下へ直接進む。
- agent call の実行、CLI バックエンド、状態保存、realization 実装を調べる場合は、oracle/src ではなく対応する実行側・状態管理側・realization 側を読む。

## hash
- ba7cc3c09f9432b620a9b11fc5c53e6c175c832286072434b3d297087582c822
