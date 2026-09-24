# `__init__.py`

## Summary
- oracle src の basic 互換 import 入口を残す理由と、既存の basic.* 参照がなくなり移行が済んだ後に削除できる条件を説明する。

## Read this when
- basic.* 参照を維持する理由や、互換入口を削除できるか判断するとき。

## Do not read this when
- oracle 側の定義や ACP 基本型の内容を調べるときは、それぞれの定義元へ進む。
- 個別の basic.* 参照箇所や移行状況を確認するときは、実際の利用箇所を調べる。

## hash
- 8a9d153c30f1ec0c568fd2702b1580077d56f027401c802ee1cca9b03f7b76bb

# `acp.py`

## Summary
- Oracle 側で定義する `AgentCallParameter` と `FileAccessMode` を再公開し、実行時モジュールにある既存の `basic.acp` 参照を保つ薄い互換層です。ACP 型の定義元ではありません。

## Read this when
- `basic.acp` 経由で公開される型や既存の import 互換性を確認するとき。
- この再公開層がまだ必要か、参照を撤去できるかを調べるとき。

## Do not read this when
- ACP 型の構造やファイルアクセスモードの意味を調べたり変更したりするときは、定義元の `oracle/src/oracle/acp_builder/basic.py` と関連仕様を直接確認してください。
- Codex の実行や preflight の挙動を調べるときは、該当する `src/commons/runtime_codex_*.py` を直接確認してください。このファイルは型を再公開するだけです。

## hash
- 53332796af2860b66db15176a77da24eb3dc94d8c7a9cd5ac7c0976c131ceef3

# `path_model.py`

## Summary
- realization 側の互換層として、正本の path model 実装を複製せずに既存利用側の import と公開 API を保つ。

## Read this when
- 既存コードやテストの import 互換性、この層が公開する API、または互換層の廃止条件を確認するとき。

## Do not read this when
- プレースホルダ解決、Git の root 探索、call-scoped path context の仕様や実装を変更するときは、正本の実装を直接読む。
- 互換 import に関係しない利用側固有の挙動を追うときは、該当する caller を直接読む。

## hash
- f80137559e09b7e85d1b92c22df5d0ef5f82420f970ee0de34e7b4a5a58eabf3

# `struct_doc.py`

## Summary
- 正本の構造化文書型と描画機能を再公開し、既存の呼び出し側との互換性を保つ入口。旧形式の単一要素またはリスト入力を正本の描画関数へ渡す。

## Read this when
- 既存の互換 API を使う箇所を調べるときや、その呼び出し方を維持・移行するとき。
- この互換層を削除できるか、呼び出し側の参照状況を確認するとき。

## Do not read this when
- 構造化文書の型や描画規則を変更するときは、正本の実装を直接読む。
- 作業がこの互換 API やその利用箇所に関係しないときは、対象となる実装や利用箇所から調べる。

## hash
- af43e040dd3486650a983758c3690bb793725619f88150162976d6f590e8b8ac
