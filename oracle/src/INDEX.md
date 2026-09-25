# `oracle`

## Summary
- Agent call に渡す構造化 prompt を組み立て、共通方針と各 call の目的・範囲・文脈を組み合わせる。
- 編集・調査・競合解消・インデクシング・feedback issue 処理などの agent call の起動情報と structured output 定義を構成する。
- 共有するアクセスモード、パス文脈、設定、文書参照、構造化文書のモデルと処理を含む。
- editor input handoff のガイドと本文、および feedback observation の入力定義を扱う。

## Read this when
- agent call に渡す共通規定や個別の prompt がどこで組み立てられるか調べるとき。
- 共有モデルやパス・アクセス設定、構造化文書や参照の扱いを追うとき。
- editor input handoff や feedback observation・issue 処理の構築を調べるとき。

## Do not read this when
- 要求や意味仕様の確認だけが目的で、コード上の組み立てを追う必要がないときは、意図を定める正本文書から読む。
- 個別コマンドの実行順序、入出力、外部状態の扱いが論点なら、それらを制御する実行処理から読む。
- 対象が単一の agent call や共有モデルに限られる場合は、該当する下位項目から確認を始める。

## hash
- 4994862d7b7d2fbf7116d33bd86736c61a90c2fe71674d563a46e61cdfd0f14f
