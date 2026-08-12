# `doc`

## Summary
- cmoc の正本ドキュメント群への入口。アプリケーション仕様、branch・commit・worktree のモデル、採用しなかった設計案の検討記録、開発ルールを扱い、目的に応じた下位文書へ進むためのルーティングを担う。

## Read this when
- cmoc の正本仕様や開発ルールの所在を確認するとき
- CLI・Codex 呼び出し・ログ・feedback・prompt・run／session・通知などのアプリケーション挙動を調べるとき
- session fork、run の隔離、branch・commit・worktree の関係を調べるとき
- 実装配置、開発環境、テスト要件、テスト実行手順を確認するとき
- 現行仕様ではなく、採用しなかった設計案の背景や採否理由を調べるとき

## Do not read this when
- 実装ファイルやテストの具体的な挙動だけを確認する場合
- 読むべき特定の正本文書が既に判明しており、その本文へ直接進める場合
- 単一の CLI サブコマンドの挙動だけを確認し、関連する仕様の分担や境界を調べる必要がない場合
- 現行仕様や実装の直接の参照先が必要で、採用しなかった設計案の背景を確認する必要がない場合

## hash
- e22ea899003707a6f4c3c086a0c09f6d4a98a7be947fe62bdbb0e81390d1eee6

# `src`

## Summary
- cmoc の正本側 Python 実装と構造化定義を集約するディレクトリです。agent call のパラメータ、prompt の構築、設定・パス・構造化文書の共通モデル、feedback 入力契約を扱います。
- agent call の用途別定義を調査するときは、用途別の構築定義へ進みます。設定・パス・構造化文書を調査するときは共通モデルへ、prompt の構成規則を調査するときは prompt 構築定義へ進みます。feedback reporter の入力契約を調査するときは feedback の構造化定義へ進みます。

## Read this when
- cmoc の正本実装における agent call、prompt、設定、パスモデル、構造化文書、feedback 契約の責務範囲を確認するとき
- agent call の起動パラメータや用途別 prompt 定義の入口を特定するとき
- cmoc 共通のモデル選択、推論強度、ファイルアクセス、パス placeholder、構造化 Markdown の定義を調査するとき
- feedback reporter が受け取る問題分類、重要度、影響、根拠、継続状態の契約を確認するとき

## Do not read this when
- 個別の prompt 構築定義、設定モデル、パスモデル、構造化文書、feedback 契約の本文を確認するときは、該当する下位対象を直接読む
- collector による feedback の保存・集約・重複判定や、agent call の実行処理を確認するとき
- realization 実装や realization test の正本内容を確認するとき
- 既存の INDEX.md のルーティング情報だけを確認するとき

## hash
- 9b6635c247d2613c0704e7a079613b2021ce5deed395549579712c3b53bbca1e
