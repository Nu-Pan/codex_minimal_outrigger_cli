
# Codex Minimal Outrigger CLI (cmoc) - AGENTS.md

## 基本事項

- このリポジトリでは Codex Minimal Outrigger CLI の開発を行う
- Codex Minimal Outrigger CLI は cmoc と略す

## パス表記

- ファイル・ディレクトリパスの表記に `<cmoc-root>`, `<repo-root>`, `<run-root>`, `<work-root>` を用いる
- 特に `<cmoc-root>` は、このリポジトリのルートディレクトリパスを表す
- これらパスキーワードの説明は `<cmoc-root>/oracle/src/basic/path_model.py` を参照すること

## ルーティング

- `<cmoc-root>` ツリー内の各ディレクトリには `INDEX.md` が存在する
- `INDEX.md` には、同階層のファイル・ディレクトリへのルーティング情報が記載されている
- 作業を始める前に `<cmoc-root>/oracle/INDEX.md` を必ず読むこと
- 作業中、必要に応じて逐次 `INDEX.md` を読んでファイルを探すこと

## ファイルアクセス規則

以下のファイルは閲覧・編集禁止

- `<cmoc-root>/memo`

以下のファイルは編集禁止

- `<cmoc-root>/README.md`
- `<cmoc-root>/AGENTS.md`
- `<cmoc-root>/oracle`

## `<cmoc-root>/oracle`

- cmoc の正本仕様断片は `<cmoc-root>/oracle` 配下のファイルで述べている
- これはあくまで「断片」であり、oracle に記載の無い「隙間」は実装者である AI の裁量で決めて良い
- oracle とそれ以外とが乖離している場合は実装の方を合わせる

## 実装・テスト

- cmoc の実装は `<cmoc-root>/src` に書く
- cmoc の自動テストは `<cmoc-root>/test` に書く
