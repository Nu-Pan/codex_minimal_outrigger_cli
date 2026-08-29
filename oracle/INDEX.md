# `doc`

## Summary
- cmoc のアプリケーション挙動仕様を分野別に確認する入口。CLI、session・run、feedback、editor input、ログ・エラー、通知などの担当仕様へ案内する。
- session と run を git branch・commit・worktree で隔離するモデルの正本文書へ案内する。分岐、統合、差分検査、管理 branch の境界を扱う。
- 設計・リファクタで不採用となった作業方式や仕様案と、その理由を確認する検討資料群への入口。現行仕様や実装手順の正本ではない。
- cmoc 開発ルールの入口。Python 記述、CLI 責務配置、開発環境、テスト要件、テスト実行手順を各正本文書へ振り分ける。

## Read this when
- 個別アプリケーション機能の挙動仕様、または対応する正本仕様の担当範囲と詳細入口を探すとき。
- session fork、run の branch 分岐・統合、worktree、関連 commit の役割や管理 branch の境界を実装・変更・調査するとき。
- cmoc の設計・リファクタで採用されなかった作業フロー、調査方式、仕様案と不採用理由を比較するとき。
- Python の記述規則、CLI の責務境界、開発環境・依存関係、テスト要件、または既存環境でのテスト実行手順を確認するとき。

## Do not read this when
- 単一のアプリケーション仕様の詳細な挙動だけを確認するときは、対応する仕様書を直接読む。
- branch model の具体的な CLI 入出力契約だけを確認するときは、該当する CLI 仕様を直接読む。
- 現行のアクセス制御・workflow、具体的な realization 実装、CLI 挙動、テスト手順を調べるときは、それぞれの正本文書や realization file を直接読む。
- INDEX.md の生成・更新規則、アプリケーション挙動以外の共通規則、または特定の実装・テスト配置だけを確認するときは、対応する規則文書を直接読む。

## hash
- e1608877c7a51123d8acba6f503bf3f3912e3a95c3d33e7eb73ccf83f572d0b7

# `src`

## Summary
- cmoc の agent call 構築、prompt・policy 生成、Structured Output 定義を扱う oracle 実装領域への入口です。
- agent call の種類別パラメータ、ファイルアクセス規則、oracle・realization の編集・調査・レビュー・適用処理を確認する下位領域へ進みます。
- feedback issue の正規化・検証、INDEX.md エントリー生成、セッション統合、TUI 起動など、agent call の用途別処理を確認できます。
- エディター入力の引き渡し、feedback 入力契約、設定・パス解決・構造化文書レンダリングなど、prompt 構築を支える共通要素も扱います。

## Read this when
- agent call の用途別構成、起動パラメータ、ファイルアクセスモード、Structured Output schema の配置を調査するとき。
- oracle・realization の編集、調査、レビュー、適用や、feedback・indexing・session・TUI に関する agent call の責務を探すとき。
- prompt の共通部品・policy、エディター入力、feedback 入力、設定・パス・構造化文書処理の担当箇所を特定するとき。

## Do not read this when
- 特定の agent call の詳細な prompt 文面、フィールド、既定値、変換規則だけを確認したいときは、該当する下位モジュールを直接読む。
- 正本仕様としての oracle doc や realization の個別実装、一般的な CLI 実行処理、既存 INDEX.md の内容を調査したいときは、この実装領域を入口にしない。

## hash
- 086de132793ef1cf93139bf8a3a7d0715a9032ffb1a1d4f63baaeacaf65d0f20
