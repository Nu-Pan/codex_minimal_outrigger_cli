# `__init__.py`

## Summary
- 固定 Node 推論 worker と依存資材を Python パッケージに含めるためのパッケージ入口を示す。

## Read this when
- 固定 worker 資材のパッケージ上の所属や入口の役割を確認するとき。

## Do not read this when
- 推論処理の内容や入出力を変更するときは、worker の実装を直接読む。
- 依存バージョンや配布対象の設定を変更するときは、依存定義・lock またはパッケージ設定を直接読む。

## hash
- a8c8e522b95b500173ab5204688aee834c890e914b00eca31c963e319b35ff50

# `package-lock.json`

## Summary
- document search worker の npm 依存関係を固定し、node-llama-cpp を含む依存ツリーの解決バージョンとプラットフォーム別の任意パッケージを記録する。

## Read this when
- worker の依存関係やインストール結果の再現性を確認・変更するとき。
- 依存パッケージの脆弱性や、OS・CPU ごとのネイティブパッケージの解決状況を調べるとき。

## Do not read this when
- worker の入力形式や埋め込み・再ランキング処理を理解または変更するときは、worker の実装を読む。
- 直接依存や Node.js の実行要件の宣言だけを確認・変更するときは、package.json を読む。

## hash
- 7486ee5717110a8e2d7b7ef955f72070b75ce88a5a9718d9f96d66434848efa3

# `package.json`

## Summary
- 文書検索 worker 用 Node.js package の実行環境要件と直接依存を宣言する。
- Python 側がこの package 宣言を資材として配置・照合するため、worker の Node.js 要件や依存関係を確認するときの入口となる。

## Read this when
- 文書検索 worker の Node.js 実行環境要件や直接依存を確認・変更するとき。
- Python 側で配布・照合される worker package metadata の範囲を確認するとき。

## Do not read this when
- chunking、embedding、reranking、入出力など worker の処理を調べるときは、worker の実装を読む。
- 資材の準備、実行時検査、子 process の起動を調べるときは、Python 側の setup/runtime 実装を読む。
- npm の推移依存や platform 別の解決内容を調べるときは、依存 lock を読む。
- 初期採用する Node.js や node-llama-cpp の識別値の正本を確認するときは、それらを所有する正本資料を読む。

## hash
- 96c15818c1ef628e2eac60d3c44dc739df55233fd7dc719a29def6333b5810ed

# `worker.mjs`

## Summary
- Python が渡した許可済み本文を、Node.js と node-llama-cpp で処理する文書検索 worker。
- tokenizer に基づく分割、文書・query の embedding、候補の rerank と、それぞれの出力検査を担う。
- 要求の振り分け、親 process の生存確認、モデル資源の解放、JSON 出力を扱う。

## Read this when
- 文書分割の token 上限、overlap、原文中の位置対応を変更するとき。
- embedding の入力条件、context 上限、ベクトルの検査や返却を変更するとき。
- rerank の評価入力、raw score の取得・検査、worker の要求 protocol や親 process の監視を変更するとき。

## Do not read this when
- 検索対象の認可・列挙・本文読取、索引同期・保存、cache、検索結果の組み立てを変更するときは、Python 側の検索処理を参照する。
- worker の起動、要求組み立て、資材の identity 検査、取消・終了猶予を変更するときは、Python 側の worker 管理を参照する。
- モデル資材の正本情報や検索設定の定義を変更するときは、それらを所有する仕様・定義を直接参照する。

## hash
- 6edf144e08ef999d0d70c6faea0a44288be834db4be83a2dd7b539d7acb4392e
