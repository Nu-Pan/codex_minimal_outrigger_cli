# `oracle`

## Summary
- agent call ごとの起動 parameter と固有 prompt を組み立て、呼び出しによっては Structured Output の契約も与える実装群。
- 共通 prompt と policy の合成に加え、path、文書参照、構造化 Markdown、設定を扱う共通モデルを提供する。
- editor input handoff のガイドと本文、および handoff や feedback observation に関わる入出力契約も含む。

## Read this when
- cmoc が agent call に渡す prompt、アクセス境界、起動 parameter の構成箇所を横断して追跡・変更するとき。
- 共通 prompt 部品と個別 call の組み合わせ方や、path・文書参照・設定モデルの分担を調べるとき。

## Do not read this when
- 単一の agent call の動作や結果契約だけを調べるときは、全体ではなく該当機能の構築処理と schema から読む。
- handoff の本文・ガイドや MCP 入出力だけを扱うときは、その担当実装へ直接進む。
- 人間意図やコマンドの意味仕様を確認するときは、実装ではなく対応する oracle doc を読む。

## hash
- c4b22e1920be566579dc3ca207f5c6e13efc7a19750c4c37d485b84f1827956b
