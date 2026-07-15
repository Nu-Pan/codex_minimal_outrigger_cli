# `oracle`

## Summary
- ACP builder の agent call パラメータ型、prompt builder の構成・依存注入、設定モデル、ルートパス解決、規範文書と構造化 markdown の共通 oracle src をまとめる領域。各サブディレクトリの仕様・実装へ進むための入口。

## Read this when
- agent call のモデル・推論強度・ファイルアクセス・Structured Output・作業ディレクトリの論理型を確認するとき。
- prompt の組み立て、standard の依存関係、プレースホルダ、ファイルアクセス規則や routing rule の注入を調査するとき。
- cmoc 設定のモデル・ループ回数・JSON 保存方針、ルートパスプレースホルダの解決、構造化 markdown の検査・レンダリングを確認するとき。
- 個別の実装や設定を読む前に、acp_builder、prompt_builder、other のどの共通基盤へ進むべきか判断するとき。

## Do not read this when
- 個別サブコマンドの実行フロー、CLI 入出力、ファイル探索や生成物の保存処理を調査するとき。
- 個別の oracle file・realization file の具体的な仕様や実装を確認するとき。
- 下位ディレクトリの責務が明確で、agent call パラメータ、prompt 構築、設定・パス・構造化文書の共通基盤を確認する必要がないとき。

## hash
- e778f3022e0ed9e076a012f28b041ea5e9eeabd6ea940e77b7e284b3b41236b0
