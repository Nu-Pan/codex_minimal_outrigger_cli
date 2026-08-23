# `edit`

## Summary
- `cmoc oracle edit` 用の agent call 起動パラメータ実装と、その配下の空ディレクトリを案内する入口。
- `fork` は現時点では本文ファイルを持たない空ディレクトリで、追加された内容を確認する必要がある場合に対象とする。
- `launch_exec.py` は本命編集 call と仕様削減 call の prompt、モデル品質、ファイル境界、indexing、作業ディレクトリを構築する。

## Read this when
- `cmoc oracle edit` の agent call 起動条件、prompt、編集対象境界、モデル設定、indexing 設定を変更・確認するとき。
- oracle 編集処理で本命 call と仕様削減 call の間の情報連携や未コミット差分の扱いを確認するとき。
- `fork` にファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- 実際の oracle 編集処理や call 実行制御を確認・変更する場合は、対応する実行側実装を直接読む。
- 一般的な prompt 構築や Structured Document の Markdown 化を確認する場合は、対応する prompt・文書定義を直接読む。
- oracle file の編集規約・設計・テスト要件を確認する場合は、関連する oracle 規定ファイルを直接読む。
- `fork` 配下の具体的なファイルを直接確認できる場合は、空ディレクトリの案内を読む必要はない。

## hash
- 424fda64b6ee693cb75567d6485f43177f9a58fb8f83c7787a69beefa3dbec17

# `investigation`

## Summary
- oracle investigation 用の TUI 起動条件と、ユーザーの調査指示を含む完全 prompt の構築入口。
- oracle 限定の読み取り専用アクセス、固定モデル・推論設定、リポジトリルートの作業ディレクトリ、indexing preflight など、調査起動時の設定を扱う。

## Read this when
- oracle investigation の TUI 起動条件を確認・変更するとき
- oracle file 調査用 prompt の分類、routing、アクセスモード、ユーザー指示の埋め込み方を確認するとき
- 調査用起動のモデル、推論 effort、作業ディレクトリ、indexing preflight 設定を確認するとき

## Do not read this when
- 共通の完全 prompt 構築規則を確認するときは build_complete_prompt の定義を直接読む
- 起動パラメータの型や列挙値の意味を確認するときは oracle.acp_builder.basic の定義を直接読む
- パスコンテキストの解決規則を確認するときは oracle.other.path_model の定義を直接読む

## hash
- 0d20e4c2cf68adecb5894b6dc8b89874a9c4a9a7ba6a38fcb17ed257561372cf

# `review`

## Summary
- oracle review の所見処理に関する agent call 定義と Structured Output schema をまとめたディレクトリ。新規所見の列挙、所見の採否判定、重複・矛盾の統合、妥当性を支持する理由と反証理由の列挙を扱う。
- Python 定義は各 review 段階の prompt、dynamic input、oracle 専用読み取り、モデル・推論強度、Structured Output schema、indexing preflight などの起動条件を構築する。
- JSON Schema は各段階の出力契約を定義し、所見情報、採否判定、編集操作、支持・反証理由の形式を確認する入口になる。

## Read this when
- oracle review の所見列挙から採否判定、統合までの処理構成を確認するとき
- 所見に対する妥当性の支持理由または反証理由を生成する agent call の prompt と起動条件を確認・変更するとき
- review 用 Structured Output の出力契約や、所見の削除・置換・統合操作を確認するとき

## Do not read this when
- oracle review 以外の agent call 構築や、共通 prompt 構築・一般的なパス解決だけを調べるとき
- 個別 schema の項目や形式だけを確認したい場合は、対象の JSON Schema を直接読むとき
- 所見の根拠となる oracle file や oracle review 全体のサブコマンド実装そのものを調べるとき

## hash
- 17ad539febc0fea048d9869ccf65fce0f6d5ec3814523c0e85e044b9ecc5df46
