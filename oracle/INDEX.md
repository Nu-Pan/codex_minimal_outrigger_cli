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
- oracle source の実装を構成する下位領域への入口。agent call 構築、prompt/policy、設定・パス・文書モデル、feedback 契約など、cmoc の動作を支える正本実装を責務別に辿るための階層。

## Read this when
- oracle の実装全体で責務の分担や調査の開始地点を確認したいとき。
- agent call、prompt/policy、設定・パス・構造化文書、feedback のいずれかに関わる実装を、責務別の下位領域へ切り分けて調べるとき。

## Do not read this when
- 特定の下位領域の具体的な処理や契約だけを確認したいときは、その責務を直接扱う下位対象へ進む。
- 既存の INDEX.md の内容やルーティング結果だけを確認したいとき。

## hash
- b82e6de44f2da399749607fc7140e811d4cf744306f67ae2e14a45622a4b4712
