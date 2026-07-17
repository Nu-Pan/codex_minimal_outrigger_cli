# `doc`

## Summary
- cmoc の oracle 文書群への入口。アプリケーション仕様、branch/session/run モデル、設計上の不採用案、開発規則を扱い、各詳細文書へルーティングする。

## Read this when
- cmoc の利用者向け挙動、CLI フロー、状態遷移、エラー処理、ログ、補完、モデルサービス、プロンプト生成を確認するとき。
- session・run と branch・worktree の境界を確認するとき。
- 採用しなかった設計案の背景や理由を調査するとき。
- Python 開発環境、CLI 設計・配置、テスト方針などの開発規則を確認するとき。

## Do not read this when
- 個別 realization file の実装詳細を確認したいとき。
- 通常の git 運用や cmoc と無関係なリポジトリ方針を確認したいとき。
- 個別機能の詳細仕様を直接確認できる対象文書が分かっているとき。

## hash
- 9bb2d1e094d7c704ba3812e524a6c8b96aa2568d555ca697268bf2fefdd3cd76

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
