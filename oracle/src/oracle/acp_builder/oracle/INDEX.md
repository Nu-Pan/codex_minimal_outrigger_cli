# `edit`

## Summary
- oracle 編集用の agent call 起動定義を扱うディレクトリです。現時点では `launch_exec.py` が、`cmoc oracle edit` の本命処理および仕様削減処理に使う `codex exec` の prompt、アクセスモード、モデル・推論設定、作業ディレクトリ、indexing 実行有無を定めています。

## Read this when
- `cmoc oracle edit` の本命 agent call または仕様削減 agent call の起動条件・パラメータを確認または変更するとき。
- oracle 編集用 prompt の構築や、仕様削減時の参照境界を確認するとき。

## Do not read this when
- oracle file の編集内容や仕様そのものを確認したいとき。
- agent call の一般的なパラメータ定義だけを確認したいとき。

## hash
- fe0644b6cf6c750287f22e4e609cec477640c3ac296f58ed85d61afb88a455e2

# `investigation`

## Summary
- `cmoc oracle investigation` 用の TUI 起動パラメータを構築する関数を定義する。ユーザー指示を完全プロンプトへ組み込み、oracle 調査向けの読み取り専用範囲、リポジトリルート起点、固定モデル、最大推論強度、インデックス事前処理などを設定する。

## Read this when
- `cmoc oracle investigation` の TUI 起動パラメータや、oracle 調査エージェントへユーザー指示を渡す経路を確認・変更するとき。

## Do not read this when
- oracle 調査プロンプトの一般仕様を確認するときは、完全プロンプトを構築する定義元を直接読む。
- TUI 起動以外の prompt builder、パス解決、構造化文書レンダリングの仕様を確認するときは、それぞれの定義元を直接読む。

## hash
- d993e860d3bfabef8ec188919fce28012f89dd458e85f1714606d4bdb8160b59

# `review`

## Summary
- oracle review の所見列挙・採否判定・妥当性検証・統合に関する Structured Output schema と agent call 定義をまとめたディレクトリ。各処理の入力所見や理由、oracle 読み取り権限、prompt、モデル設定、出力形式の確認入口を提供する。

## Read this when
- oracle review の所見生成、妥当性検証、採否判定、重複・矛盾の統合に関する入出力契約や agent call 起動条件を確認するとき。

## Do not read this when
- oracle review の対象仕様や実装そのものを調査するとき。
- 共通の agent call パラメータ構築、prompt 生成、パス・アクセス制御を確認するとき。
- 個別の Structured Output schema の項目・型・形式だけを確認するときは、該当する schema ファイルを直接読む。

## hash
- 15535e3aef699edfec925d68b48ce20214acdc660ed7d69b623d34a331776a35
