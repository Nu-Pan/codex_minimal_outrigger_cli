# `doc`

## Summary
- `oracle/doc` は、cmoc のアプリケーション仕様と開発規則を集約し、CLI・状態管理・agent call・feedback・通知・branch/worktree 運用、Python 実装・環境・テストの正本文書へ進むための上位入口を提供する。採用しなかった設計案は `considered_alternative` から参照できる。
- アプリケーション挙動や共通契約は `app_spec`、branch・commit・worktree の隔離モデルは `app_spec/branch_model.md`、開発・環境・実装配置・テスト規則は `app_spec/dev_rule` へ進む。

## Read this when
- cmoc のアプリケーション仕様、開発規則、branch/worktree 運用、または採用しなかった設計案の参照先を選ぶとき
- CLI、状態管理、agent call、feedback、通知、Python 実装、開発環境、テストなど、下位の正本文書へルーティングするとき
- 複数の仕様領域にまたがる責務境界を確認し、個別仕様へ進む前の上位構造を把握するとき

## Do not read this when
- 特定の機能・サブコマンド・実装・テスト・環境手順が明確で、対応する下位文書を直接確認できるとき
- 採用しなかった代替案の詳細だけを調べる場合に、該当する `considered_alternative` の資料へ直接進めるとき
- `oracle/doc` 配下の仕様・開発規則と無関係なコードや文書を扱うとき

## hash
- 948ace7319b4de94ca69186997add50fcffea5b2b028a55ab4e7df77ef5f9014

# `src`

## Summary
- `oracle/src/oracle` は、cmoc が利用する oracle 側の Python 実装と Structured Output 定義の中核領域です。agent call パラメータ、feedback 入力、設定・パス・構造化文書、prompt 構築を扱い、詳細な責務ごとに `acp_builder`、`feedback`、`other`、`prompt_builder` へ分かれています。

## Read this when
- oracle 側の実装コードや Structured Output 定義の全体像を調査・変更するとき
- agent call の構築、feedback 入力、cmoc 設定・パス解決・構造化文書、prompt 構築の入口を探すとき
- 下位責務がまだ特定できず、適切な下位ディレクトリへのルーティングが必要なとき

## Do not read this when
- 人間が所有する oracle の意味仕様そのものを確認するとき
- cmoc の realization 実装、CLI 実行処理、テストの具体的な挙動を直接確認すれば足りるとき
- 特定の責務が明らかな場合は、この階層ではなく `acp_builder`、`feedback`、`other`、`prompt_builder` の該当ディレクトリを直接読むとき

## hash
- c3539dffe2759740eaf86ab7d54eb9e9666e534fa07f51d4e354463bac04c80a
