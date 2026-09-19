# `oracle`

## Summary
- cmoc の oracle source 群を構成する実装・設定・Structured Output schema の入口。agent call 用 prompt、アクセス方針、サブコマンド別の起動パラメータ、feedback 処理、入力 handoff、共有データモデルを扱う。
- `acp_builder` は各サブコマンドや内部処理について、prompt 本文・ファイルアクセスモード・実行 cwd・schema・indexing 条件をまとめた AgentCallParameter を構築する。
- `prompt_builder` は複数のポリシーと共通の oracle/realization 説明を組み合わせ、agent に渡す完全 prompt を生成する。
- `other` は path 解決、構造化文書、設定、ドキュメント参照など、prompt と agent call builder が共有する基盤モデルを提供する。
- `editor_input_handoff` と `feedback` は、それぞれ editor 引き渡し入力の schema・本文生成、および feedback observation の入力 schema を定義する。

## Read this when
- cmoc が agent を呼び出す際の prompt、アクセス境界、cwd、Structured Output schema、indexing 条件を変更・調査するとき
- 新しいサブコマンドまたは内部 agent call の起動パラメータ構築箇所を探すとき
- 共通 prompt の構成要素や oracle/realization、routing、file access などの policy 組み合わせを確認するとき
- editor input handoff や feedback reporting の入力形式・本文生成を確認するとき
- path、構造化文書、設定、ドキュメント参照の共有モデルが必要なとき

## Do not read this when
- oracle の人間向け意味仕様やサブコマンドの詳細要件を確認したいときは、まず `oracle/doc` の該当仕様を読むべきとき
- 実際の製品挙動を実装・検証する realization code や realization test の変更箇所を直接探しているとき
- 単一の agent call の呼び出し結果や実行制御だけを調べる場合で、対応する `src` 側の利用箇所を直接読む方が適切なとき
- INDEX 生成以外の目的で、対象配下の個別ファイルの詳細実装だけを確認したいとき

## hash
- 5814398d8b64ce54dd97128d902a9d1fe50d2d5c651cfc9a80577b306c4c66d3
