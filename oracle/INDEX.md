# `doc`

## Summary
- cmoc の正本ドキュメントを、アプリケーション仕様と開発規約に分けて案内するディレクトリ。`app_spec` は CLI の挙動・実行契約・状態・出力などを扱い、`dev_rule` は Python 実装、CLI 配置、環境、テスト、品質検査の規約を扱う。branch・worktree の設計や不採用案の背景も下位項目への入口として提供する。

## Read this when
- cmoc の正本仕様、設計規約、Python 開発規約、テスト規約、開発環境、品質検査の参照先を探すとき
- アプリケーション挙動の仕様と、実装・環境・テストに関する開発規約のどちらを確認すべきか判断するとき
- branch・commit・worktree のモデルや、採用しなかった設計案の背景を調査するとき

## Do not read this when
- 確認対象の個別仕様書、開発環境規約、テスト規約、テスト実行手順が明確なときは、該当する下位文書を直接読む
- 具体的な realization 実装、テスト成果物、保存済み成果物、CLI の個別挙動だけを確認するときは、対応する対象を直接読む

## hash
- 41fbaa4d1346ecb4d7415e0315df31783c0d32c945b131c11744581d928e1092

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
