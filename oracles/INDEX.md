# `app_specs`

## Summary

- cmoc のアプリケーション実行時仕様をまとめる正本仕様断片ディレクトリです。
- Codex CLI 呼び出し、プロンプト構成、サンドボックス指定、Model / Reasoning Effort、Structured Output、ログ保存、リトライ、自然言語の扱いなどの横断仕様を含みます。
- `comconfig.json` と `CMOConfig` の設定、サブコマンド実行中の stdout 進捗表示、`codex exec` 呼び出し表示、完了時の時間レポート、共通エラーハンドリング、終了ステータスを扱います。
- `<repo-root>` の発見、oracle ファイル列挙、実装ファイル列挙、`.cmoc` の git 追跡対象外保証、タイムスタンプ形式、`<cmoc-branch>` 上での変更範囲などの補助仕様を含みます。
- `<repo-root>` 配下に自動配置・自動メンテナンスされる `INDEX.md` の対象、除外規則、フォーマット、Structured Output による目次生成、処理順序、実行タイミングを定義します。
- `sub_commands` 配下を通じて `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の各個別仕様へルーティングします。
- cmoc 利用者向けに、PATH 設定、初期化、作業用ブランチ作成、oracle 評価、実装反映、マージまでの全体ワークフローも案内します。

## Read this when

- cmoc のアプリケーション実行時仕様について、どの個別仕様ファイルやサブディレクトリを読むべきか判断したいとき。
- Codex CLI 連携、`codex exec` の呼び出し方法、プロンプト構成、サンドボックス指定、Model / Reasoning Effort、Structured Output、ログ保存、リトライ方針、使用言語を調べたいとき。
- `comconfig.json` や `CMOConfig` による設定ファイルの生成、補完、過剰パラメータ削除、プロパティ公開の仕様を確認したいとき。
- サブコマンド実行中の stdout 進捗表示、`codex exec` 呼び出し情報の表示、完了時の経過時間レポートを実装または確認したいとき。
- 個別仕様に明記がない場合の共通エラーハンドリング、エラーレポート項目、終了ステータスの扱いを確認したいとき。
- cmoc 実行時の `<repo-root>` 探索、カレントディレクトリ変更、oracle ファイル列挙、実装ファイル列挙、`.cmoc` の git 追跡対象外保証、タイムスタンプ生成、`<cmoc-branch>` 上での変更範囲を調べたいとき。
- `<repo-root>` 配下へ自動配置される `INDEX.md` の対象ディレクトリ、除外規則、目次情報フォーマット、ハッシュ不一致時の再生成、Codex CLI への目次生成依頼を実装または確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の個別仕様への入口を探しているとき。
- cmoc のエンドユーザーが PATH 設定、初期化、作業用ブランチ作成、oracle 評価、実装反映、マージをどの順番で行うか把握したいとき。

## Do not read this when

- cmoc 自体の Python コーディング規約、設計規約、テスト規約、開発環境など、開発者向けルールだけを調べたいとき。
- `<cmoc-root>/README.md`、`AGENTS.md`、`oracles`、`memo` などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- cmoc の実装コードやテストコードの具体的な配置、ファイル構造、実装パターンだけを調べたいとき。
- 対象がアプリケーション実行時仕様ではなく、内部の開発方針やローカル開発環境設定に限られるとき。
- Codex CLI や git の一般的な使い方だけを調べており、cmoc 固有の実行時仕様が不要なとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` のうち、読むべき個別サブコマンド仕様ファイルが既に明確で、このディレクトリ全体のルーティング情報が不要なとき。
- 特定の実装不具合やテスト失敗の原因をコード上で直接調査したいだけで、正本仕様断片へのルーティング判断が不要なとき。

## hash

- 54ac5142fd0e6f415011fd405077c54047a8bc00f3c83a09742f07e870f9d5b8

# `considered_alternatives`

## Summary

- `cmoc` で採用しなかった設計案や運用案をまとめたルーティング用ディレクトリです。
- `cmoc apply` の事前計画分離を見送った理由、AI-generated な memory を次回実行へ自動注入しない理由、作業計画レビュー方式を採らなかった理由を扱います。
- `oracles` を単一の明示的な正本仕様として保ち、暗黙の改善案や計画レイヤーを増やさない方針の背景を整理しています。

## Read this when

- `cmoc apply` の設計で、修正点リストの後に別途作業計画を立てるべきか迷っているとき。
- AI の振り返り結果や改善案を次回以降の実行に自動反映する運用の是非を検討したいとき。
- 作業計画レビューを採用せず、人間が `oracles` を書いて AI が追従する役割分担の背景を確認したいとき。

## Do not read this when

- `cmoc` の具体的な実装コードやテストコードの場所を知りたいとき。
- 各サブコマンドの入出力仕様や操作手順だけを確認したいとき。
- `INDEX.md` の生成規則やメンテナンス方法そのものを調べたいとき。

## hash

- bcf28dba25d16038c99f7ffd3f93fe14a061e8da2ff82b110c1a24034e62c0e3

# `dev_rules`

## Summary

- `oracles/dev_rules` は、cmoc 自体の開発ルールをまとめた正本仕様断片ディレクトリです。
- Python のコーディング規約、CLI と共通処理の設計方針、開発環境、テスト実装規約への入口を提供します。
- `src` 配下の実装方針と `tests` 配下の自動テスト方針を、開発者向けに整理しています。
- cmoc のユーザー向け実行時仕様ではなく、実装作業時の判断基準を扱います。

## Read this when

- cmoc 自体の `src` 配下を実装・修正するとき。
- CLI エントリーポイント、サブコマンド、共通処理の配置や設計方針を確認したいとき。
- pytest を使った自動テストの追加・修正方針や、Fake Codex CLI を用いるテスト可否を確認したいとき。
- Python バージョン、`.venv`、pip、文字コードなどの開発環境ルールを確認したいとき。
- ユーザー向け CLI 仕様ではなく、開発者向けのコーディング・設計・テスト・環境ルールを調べたいとき。

## Do not read this when

- cmoc のユーザー向け CLI 仕様、サブコマンドの詳細挙動、出力形式を調べたいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` などの個別実行時仕様を知りたいとき。
- `README.md`、`AGENTS.md`、`oracles` の運用ルールや編集可否だけを確認したいとき。
- cmoc を使って別リポジトリを開発する際の `<repo-root>` 側の仕様を探しているとき。

## hash

- c272b46afbdb4d329f081fb1eec693b2ae8e369b7ec3ae82c8415d2023da34bb
