# `cmoc`

## Summary
- 仮想環境の Python 実行可否を確認し、利用可能なら cmoc の Python CLI を起動するユーザー向けシェルラッパー。仮想環境が未セットアップまたは実行不能な場合は、セットアップ手順と呼び出し元情報を含むエラーを表示する。シェル入口や cmoc の起動障害を調査するときの対象。

## Read this when
- cmoc コマンドの起動経路、仮想環境 Python の検査、起動前エラー表示を確認・変更するとき。

## Do not read this when
- Python CLI 本体のコマンド処理や業務ロジックを確認したいとき。起動後の実装は src 側の対象を直接読む。

## hash
- 04095773b91ee2508a5f4590dd91dda76e82fbff45b3c7de61133ca2f0b92ff4
