# `doc`

## Summary
- cmoc の正本ドキュメントを集約するディレクトリ。アプリケーション仕様、branch・commit・worktree のモデル、採用しなかった設計案、Python 開発規約を扱い、個別仕様や開発手順へ進むための入口となる。

## Read this when
- cmoc のアプリケーション挙動、CLI、agent call、ログ、prompt、run／session lifecycle、サブコマンドの正本仕様を探すとき
- session fork、run の隔離、branch・commit・worktree の関係やライフサイクルを確認するとき
- realization refactor で採用しなかった作業方式・検査方式・状態管理方式の理由を確認するとき
- Python のコーディング規則、CLI 設計、開発環境、テスト規則、テスト実行手順を確認するとき

## Do not read this when
- INDEX.md の生成規則やルーティング方針だけを確認するとき
- 対象が明確な個別仕様、開発環境手順、コーディング規則、CLI 配置方針、テスト規則、テスト実行手順を直接確認できるとき
- realization 実装や realization テスト固有の内容だけを調査するとき
- 現行仕様ではなく、具体的な実装ファイルやテストファイルの内容だけを確認するとき

## hash
- e5ad7a677991c6f41c30ea66e602a2a0e9fe95f3701af1aa2344081a9708a865

# `src`

## Summary
- AIコーディングエージェント呼び出しに関する正本実装をまとめたソースディレクトリ。共通パラメータ構築、設定・パス・規範・構造化文書のモデル化、oracle・realization規範やINDEX.mdルーティング規則のprompt builder処理を下位実装への入口として提供する。

## Read this when
- Agent call のパラメータ構築、設定・パスモデル、規範や構造化文書の処理を調査・変更するとき
- oracle・realization の適合性、ファイルアクセス制約、INDEX.md ルーティング規則を prompt builder へ変換する処理を調査・変更するとき

## Do not read this when
- 個別機能の実際の処理ロジックやテストだけを調べるとき
- 共通 prompt 構築、パス解決、レビュー基準、差分適用、マージ操作など、下位実装が直接の対象であるとき

## hash
- d96bec8652f08ac01841fa2fa974e3154b3c1ffe23e110dfc641b9ceb1e1601f
