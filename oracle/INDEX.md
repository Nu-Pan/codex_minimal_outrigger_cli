# `doc`

## Summary
- cmoc の正本文書を、アプリケーション仕様（app_spec）、開発ルール（dev_rule）、branch・commit・worktree のモデル、採用しなかった代替案の検討資料（considered_alternative）に分類して案内するディレクトリ。CLI の挙動・ライフサイクル、実装・テスト・環境の規約、設計判断の背景を確認する際の入口となる。

## Read this when
- cmoc の正本仕様・開発規約・設計背景を横断して探すとき
- CLI の挙動、branch／worktree のモデル、Python 開発環境、テスト要件や実行手順の参照先を選ぶとき
- 現行設計の背景や不採用となった代替案を調査するとき

## Do not read this when
- 確認対象の仕様・開発ルール・検討資料が既に特定できており、該当する下位ディレクトリや文書を直接読めるとき
- 個別の実装ファイル、具体的なテスト結果、既存 report や生成物だけを調査するとき

## hash
- f407bd0f93ae6eb2c1029707de3b6b3ca415108975e58ecdf1eea860451d8a58

# `src`

## Summary
- cmoc の正本モデルと agent call 構築定義を扱うソース群への入口。agent call パラメータ、quota probe、prompt 構築、path context・root placeholder、設定、構造化 Markdown 文書、feedback reporter 入力スキーマを提供する。
- 用途別に `acp_builder`、`prompt_builder`、`other`、`feedback` へ分かれ、呼び出し契約、完全 prompt と policy、共通モデル、問題報告入力契約の確認先となる。

## Read this when
- agent call のモデル・reasoning effort・ファイルアクセス・cwd などの共通パラメータや quota availability probe を調査または変更するとき。
- 完全 prompt の構造、policy の組み込み、placeholder 定義、agent 向け入力文面を調査または変更するとき。
- root path と worktree の解決、cmoc 設定、構造化 Markdown ノード、feedback reporter の入力契約を確認するとき。
- 用途別の定義や構築処理の所在を特定し、`acp_builder`、`prompt_builder`、`other`、`feedback` の下位要素へ進む必要があるとき.

## Do not read this when
- 既存の INDEX.md のルーティング情報だけを確認したいとき。
- Codex CLI のバックエンド固有実装、通常の realization・session・TUI 実行処理、collector の保存・集約処理を直接確認したいとき。
- 個別の issue、レビュー所見、または realization の具体的な変更内容だけを調査したいときは、対応する下位定義や実装を直接読む。

## hash
- 55fbe5233c3f29be57323a6b1d2332b48a440e3b53bc2a98edae4dd517d352d0
