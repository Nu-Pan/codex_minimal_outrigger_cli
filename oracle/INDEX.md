# `doc`

## Summary
- cmoc のアプリケーション仕様と開発規則を分野別にまとめた oracle doc 群。機能仕様、branch/session/run のモデル、不採用案、Python・CLI・テストなどの開発規則へ進む入口。

## Read this when
- cmoc の個別機能や共通アプリケーション仕様の正本文書を探すとき。
- session・run・branch・worktree の境界や運用を確認するとき。
- 採用しなかった設計案とその理由を調べるとき。
- Python 実装、CLI 配置、開発環境、realization test の規則を確認するとき。

## Do not read this when
- 既に対象仕様文書が特定できており、その本文だけを確認すればよいとき。
- 実装ファイルの具体的な処理や個別テストの実装詳細を確認したいとき。
- cmoc 以外の通常の git 運用やリポジトリ固有の実装方針だけを確認したいとき。

## hash
- 2baf3efdc11b9fbc5526ce5f036b07ef8741c2c985c331b70998b2297d0bb980

# `src`

## Summary
- cmoc の oracle src を構成する実行可能な正本仕様・生成部品への入口。ACP builder、設定・共通データ構造、プロンプト builder などを扱い、エージェント呼び出しに必要なパラメータ、prompt、Structured Output schema、実行設定、文書生成関連の定義を確認する起点となる。

## Read this when
- ACP builder の呼び出し条件、パラメータ、prompt、Structured Output schema、実行設定を調査するとき
- cmoc の設定モデル、パス解決、規範データ、StructDoc、Markdown 文書生成の定義を確認するとき
- oracle と realization の境界、標準規則、ファイルアクセスやルーティングに関する実行可能な定義を確認するとき

## Do not read this when
- realization code の実装・テスト、CLI の実行フロー、表示、永続化、実際のファイル編集処理だけを調査するとき
- 個別の Enum、StructDoc、標準文書、Requirement など下位対象の定義だけを確認したいとき
- oracle file の配置・命名に関する上位方針や、対象本文の INDEX.md 要約だけを確認したいとき

## hash
- f460fa8b855ffcc96b1c4218afe5a6fa90492d2811ec93855e192248a0954cf5
