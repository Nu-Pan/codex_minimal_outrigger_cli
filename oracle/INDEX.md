# `doc`

## Summary
- cmoc のアプリケーション仕様群への入口。CLI 実行、session／run、feedback、Codex 呼び出し、ログ、通知、editor input、文書分類などの個別仕様と、sub_command 配下のサブコマンド仕様へ案内する。
- cmoc の session と run を git branch・commit・worktree で隔離するモデルを定義する正本文書。分岐、統合、run isolation、差分検査などの Git 管理上の関係を確認する入口。
- cmoc の開発規則群への入口。Python コーディング、CLI 設計、開発環境、テスト要件、テスト実行手順を、それぞれの正本文書へ振り分ける。
- cmoc realization refactor などで採用しなかった作業方式と、その不採用理由を記録する検討資料群。現行仕様や実装の根拠ではなく、過去の設計判断と代替案の背景を確認する入口。

## Read this when
- cmoc のアプリケーション挙動に関する正本仕様を探すとき。
- CLI、session／run、feedback、Codex CLI、ログ、通知、editor input、INDEX.md、または個別サブコマンドの仕様入口を判断するとき。
- session fork・run の branch 分岐、commit、worktree、統合、または Git 管理対象の関係を実装・変更・調査するとき。
- Python の記述規則、CLI の責務配置、開発環境、依存関係、テスト要件、または品質検査の実行手順を確認するとき。
- realization refactor の作業フロー、file access policy、.gitignore 連携、AI-generated kaizen、oracle review、または作業計画レビューを採用しなかった理由を確認するとき。

## Do not read this when
- 特定機能や特定サブコマンドの詳細な挙動、field、prompt、schema、出力、または実装責務を確認したいときは、app_spec 配下の該当する個別仕様書や sub_command 配下の仕様書を直接読む。
- branch model の具体的な CLI 入出力契約や workload 固有の report を確認したいときは、対応するアプリケーション仕様を直接読む。
- Python 環境の構築・依存関係・pip 操作、CLI 実装配置、テストの意味要件、またはテスト実行手順を確認したいときは、dev_rule 配下の対応文書を直接読む。
- 現行の実装、realization file、アクセス制御、採用済み仕様、または具体的なテスト内容を確認したいときは、considered_alternative 配下の検討資料ではなく、該当する正本仕様・実装・テストを直接読む。
- アプリケーション仕様、Git 管理モデル、開発規則、または設計判断に関係しない内容を調査するとき。

## hash
- 9be31bd164815089e1f95ff0b781279aba37db221d3172f7ac992738170ad824

# `src`

## Summary
- cmoc の oracle 実装群における上位入口。agent call パラメータ、prompt 構築、用途別の起動・検証定義、設定・パス・構造化文書モデルを下位要素へ振り分ける。
- agent call の呼び出し設定や用途別 builder を調べる場合は acp_builder、prompt の組み立て規則や各種ポリシーを調べる場合は prompt_builder、設定・パス解決・Markdown 構造化文書を調べる場合は other から読み始める。

## Read this when
- oracle の実装全体で、agent call 関連の責務がどの下位要素にあるかを判断するとき。
- 呼び出しパラメータ、prompt 構築、用途別起動処理、設定・パスモデルの調査開始点を決めるとき。

## Do not read this when
- 特定の prompt policy、agent call builder、設定クラス、パス解決処理、または構造化文書モデルだけを確認したい場合は、対応する下位要素を直接読むとき。
- agent call の実行結果の保存・集約や、oracle／realization 本文・INDEX.md 自体の編集方法を調べるとき。

## hash
- 4af0b7fbf24db6d6442d583b4b206d10b4771528c060ff8e984534a8ad377dc5
