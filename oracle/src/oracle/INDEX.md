# `acp_builder`

## Summary
- Agent Call Parameter の呼び出し種別、ファイルアクセスモード、完全な prompt、Structured Output schema のパス、cwd、indexing preflight 実行有無を一つの不変データクラスに集約する。
- 論理的なファイルアクセスモードの列挙と、agent call 設定を保持するデータ構造を確認するための入口。

## Read this when
- agent call のパラメータ構造や、呼び出し種別・アクセスモード・prompt・schema・cwd・preflight 設定を確認するとき。
- 一つの agent call に設定される実行条件をデータクラスへどう集約するか確認するとき。

## Do not read this when
- 各ファイルアクセスモードの意味や Codex CLI sandbox との対応を確認したいとき。
- Agent Call Parameter の生成・利用箇所、個別 builder の実装、または実際の agent call 実行処理を確認したいとき。

## hash
- fb841e28c737a19013bf348b27d23aa0b19b92de54f151628f1972a8ce76a438

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- 日本語技術文書のルーティングエントリーを、対象ディレクトリ内の構造化文書・設定モデル・パスモデルの責務に基づいて整理します。

## Read this when
- cmoc の設定集約、パスコンテキストやプレースホルダ解決、構造化文書の Markdown レンダリングを調査・変更するとき。
- これらの実装対象のどれを入口にすべきか、またはディレクトリ内の関連モジュールの責務の境界を確認したいとき。

## Do not read this when
- 個別モジュールのフィールド定義、既定値、具体的な変換規則を確認したいときは、ルーティング情報ではなく該当ファイルを直接読むべきです。
- agent call の生成規則や index エントリー生成処理そのもの、または一般的な CLI 機能を調査するときは、別の仕様・実装対象を直接読むべきです。

## hash
- 01da7b21d4a4bb34d4188332c0c76f0719fcce78b2fcb31d8220c81697804620

# `prompt_builder`

## Summary
- agent call 用の完全な prompt を組み立てる共通部品群の入口。placeholder 型、prompt 統合、エディタ初期入力、oracle／realization 概念、policy builder 群を扱う。

## Read this when
- agent call の prompt 構築や統合順序、placeholder の扱いを確認・変更するとき。
- ファイルアクセス、routing、oracle／realization、feedback、所見判定などの prompt policy の構築責務を調べるとき。
- エディタ入力の初期文面や、oracle／realization の基本概念を prompt に組み込む処理を確認するとき。

## Do not read this when
- 個別 policy の意味仕様、個別 oracle 文書、実装、テストの詳細を確認したいときは、該当する対象を直接読む。
- 生成済み prompt の実行規則や Codex CLI のサンドボックス設定を確認するとき。
- プロンプト構築と無関係な CLI 挙動や、具体的なテンプレート展開処理だけを調べるとき。

## hash
- 4fe76be06ff59f6b839bd4d43df7fc387e89ff60efb8d9875e67538bb21ff65c
