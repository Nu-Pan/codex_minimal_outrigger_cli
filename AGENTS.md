
# Codex Minimal Outrigger CLI (cmoc) - AGENTS.md

## 基本事項

- このリポジトリでは Codex Minimal Outrigger CLI の開発を行う
- Codex Minimal Outrigger CLI は cmoc と略す

## パス表記

- ファイル・ディレクトリパスの表記に `<cmoc-root>`, `<work-root>`, `<run-root>` を用いる
- 特に `<cmoc-root>` は、このリポジトリのルートディレクトリパスを表す
- これらパスキーワードの説明は `<cmoc-root>/oracles/docs/path_model.md` を参照すること

## ファイルアクセス規則

以下のファイルは AI 閲覧・編集禁止

- `<cmoc-root>/memo`

以下のファイルは AI 編集禁止

- `<cmoc-root>/README.md`
- `<cmoc-root>/AGENTS.md`
- `<cmoc-root>/oracles`

## `<cmoc-root>/oracles`

- cmoc の正本仕様断片は `<cmoc-root>/oracles` 配下のファイルで述べている
- これはあくまで「断片」であり、 `oracles` に記載の無い「隙間」は実装者である AI の裁量で決めて良い
- `oracles` とそれ以外とがている場合は実装の方を合わせる

## ルーティング

- `<cmoc-root>/oracles` 配下の各ディレクトリには `INDEX.md` が存在する
- `INDEX.md` には、同階層のファイル・ディレクトリへのルーティング情報が記載されている
- `<cmoc-root>/oracles` 配下の正本仕様を調べる際は、 `INDEX.md` のルーティング情報を手がかりに、最低限必要なファイルだけを読むこと
- 作業を始める前に `<cmoc-root>/oracles/INDEX.md` を必ず読むこと

## 実装・テスト

- cmoc の実装は `<cmoc-root>/src` に書く
- cmoc の自動テストは `<cmoc-root>/tests` に書く
