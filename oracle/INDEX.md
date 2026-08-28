# `doc`

## Summary
- cmoc の正本文書群への上位入口。アプリケーション仕様、開発ルール、branch model、採用しなかった代替案など、実装・調査時に参照先を振り分ける。
- 利用者向け挙動や実行契約は app_spec、開発・テスト・環境の規則は dev_rule、session/run の git 隔離モデルは branch_model、設計上の不採用案と理由は considered_alternative から確認する。

## Read this when
- cmoc の正本文書を探しており、対象がアプリケーション仕様、開発ルール、branch・worktree モデル、または不採用となった代替案のいずれかに該当するとき
- 複数の文書領域にまたがる仕様・実装・調査の入口を選ぶ必要があるとき

## Do not read this when
- 対象文書の領域が明確で、app_spec、dev_rule、branch_model、considered_alternative のいずれかを直接読めるとき
- 実装ファイル、テスト、または個別仕様の具体的な内容だけを確認したいとき

## hash
- c51320ce58bcd02e3c03008f6ee6f5add39b9c50b3c1b3eecc24cfb4eaf4f229

# `src`

## Summary
- oracle文書を扱うcmocの実装定義をまとめ、agent call構築、prompt生成、設定・パス・構造化文書、feedback入力などの用途別領域への入口を提供する。
- agent callのパラメータ構築やquota probeはacp_builder、promptと適用ポリシーはprompt_builder、設定・パス・構造化文書の基盤はother、feedback報告入力の契約はfeedbackへ進む。

## Read this when
- oracle文書に関するagent callの起動パラメータ、prompt生成、ファイルアクセスやroutingなどの適用ポリシー、Structured Output入力契約を確認・変更するとき。
- oracle実装の設定モデル、agent callのパスコンテキスト、構造化文書レンダリングなど、複数のoracle機能が共有する基盤を調べるとき。

## Do not read this when
- oracleの意味仕様や編集・レビュー規則そのものを確認したいとき。
- realizationの実装・テスト、session join、TUIなど特定の下位機能だけを調べる場合は、対応する下位ディレクトリを直接読むとき。
- 既存のINDEX.mdのルーティング内容だけを確認したいとき。

## hash
- d80ef6dd918331d63242f3561556df451f922fa14ead68396c806059c13145a5
