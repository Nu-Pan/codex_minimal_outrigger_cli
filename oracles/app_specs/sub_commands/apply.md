# `cmoc apply`

## 概要

- `cmoc apply` は、`<repo-root>` の実装を `<repo-root>/oracles` の正本仕様断片へ近づけるために、Codex CLI による不整合調査・修正ループを実行する
- `cmoc apply` が正常に実行完了したからといって、正本仕様への追従完了が保証されるわけではない（修正ループの実行までが `cmoc apply` の責任範囲である）

## 引数

- 位置引数なし
- オプション引数 `--repeat` (`-r`) を受け取る
- オプション引数 `--full` (`-f`) を受け取る

## 事前条件

- `<cmoc-branch>` 上に居なければエラー終了とする
- `<repo-root>/oracles` の外の未コミット差分があればエラー終了する

## 部分・全体適用モード

- `cmoc apply` は部分適用・全体適用の２つのモードを持つ
- `--full` がついている場合は全体適用モードへ
- `--full` が付いていない場合
    - `<cmoc-branch>` 上で `oracles` ファイル・実装ファイルの削除が有る場合は全体適用モードへ
    - そうでなければ部適用モードへ

## 実行作業

1. `<repo-root>/.cmoc` が git の追跡対象外であることを保証する
2. `<repo-root>/oracles` 配下の未コミット差分を自動コミット
3. 不整合調査・修正ループ（最大 N 回）
    1. 部分・全体適用モードを再評価
    2. `oracles` ファイル・実装ファイルを列挙する
    3. 部分適用モードの場合、 1. で列挙したファイルリストを「`<cmoc-branch>` 上で変更のあった `oracles` ファイル・実装ファイル」に絞り込む
    4. Codex CLI に、`oracles` と実装との明確な不整合をリストアップさせる
    5. Codex CLI に、不整合リストを整理させる
    6. 整理された不整合リストが空であれば、追加修正対象が検出されなかったものとしてループを終了する
    7. 整理された不整合リストに対する修正作業を Codex CLI に依頼する
    8. `<repo-root>/oracles` などの編集禁止ディレクトリに未コミット差分が有る場合はエラー終了
    9. 全ての未コミット差分を git にコミット（コミットメッセージは Codex CLI で適切なものを生成）
    10. ループ先頭に戻る
4. 作業結果と判断材料をレポートする

## `cmoc apply` の責務境界

- `cmoc apply` の責務は、指定された最大回数の範囲で、不整合調査・修正ループを実行し、その結果を人間が判断できる形でレポートすることである
- `cmoc apply` は、`<repo-root>/oracles` と実装の間に不整合が残っていないことを保証しない
- `cmoc apply` は、Codex CLI の調査結果に含まれた不整合を要修正項目として扱うが、Codex CLI が全ての不整合を発見することは保証しない
- ループが回数上限に達した場合も、コマンド実行としては正常系として扱う
- 回数上限到達後にさらに `cmoc apply` を再実行するか、`cmoc eval-oracles` や人手レビューを行うか、作業を打ち切るかは人間が判断する

## 不整合修正ループの反復回数の決め方

- サブコマンドの引数 `--repeat`, `-r` で不整合修正ループの反復回数を受け取る
- デフォルト値は 5 とする

## 不整合リストアップの仕様

- `oracles` ファイルと実装との明確な不整合が無いかの調査を Codex CLI に依頼する
- 調査対象として `oracles` ファイルと実装ファイルを列挙するが、
- この調査は「`oracles` ファイルそれぞれ」「実装ファイルそれぞれ」に対して独立に行う (for each)
    - つまり `oracles` ファイルが N 件と実装ファイルが M 件存在するのであれば `codex exec` を N + M 回呼び出す
    - `codex exec` で指定したファイルは以外のファイルも、必要にならば読むべきである（指定は「だけ」の意味ではない）
- 調査結果は Structured Output で「不整合のリスト」として受け取る
- Structured Output の schema は以下の通り
    ```json
    {
        "type": "object",
        "additionalProperties": false,
        "required": ["discrepancies"],
        "properties": {
            "discrepancies": {
                "type": "array",
                "description": "oracles と実装との明確な不整合のリスト。空配列の場合のみ不整合なしとみなす。",
                "items": {
                    "type": "object",
                    "additionalProperties": false,
                    "required": [
                        "oracle_path",
                        "oracle_line_start",
                        "oracle_line_end",
                        "implementation_paths",
                        "title",
                        "oracle_requirement",
                        "observed_implementation",
                        "reason",
                        "suggested_fix"
                    ],
                    "properties": {
                        "oracle_path": {
                            "type": "string",
                            "description": "不整合の根拠となる oracle ファイルの絶対パス。"
                        },
                        "oracle_line_start": {
                            "type": ["integer", "null"],
                            "description": "不整合の根拠となる oracle 記述の開始行。行番号を特定できない場合は null。"
                        },
                        "oracle_line_end": {
                            "type": ["integer", "null"],
                            "description": "不整合の根拠となる oracle 記述の終了行。行番号を特定できない場合は null。"
                        },
                        "implementation_paths": {
                            "type": "array",
                            "description": "不整合に関係する実装・テスト・設定ファイルの絶対パス。未実装などで該当ファイルを特定できない場合は空配列。",
                            "items": {
                                "type": "string"
                            }
                        },
                        "title": {
                            "type": "string",
                            "description": "不整合の短い見出し。"
                        },
                        "oracle_requirement": {
                            "type": "string",
                            "description": "oracle が要求している仕様。"
                        },
                        "observed_implementation": {
                            "type": "string",
                            "description": "調査時点の実装が実際にどうなっているか。"
                        },
                        "reason": {
                            "type": "string",
                            "description": "なぜ oracle と実装が明確に不整合していると言えるのか。推測や未確認事項は含めない。"
                        },
                        "suggested_fix": {
                            "type": "string",
                            "description": "実装を oracle に追従させるための修正方針。"
                        }
                    }
                }
            }
        }
    }
    ```

## 不整合リスト整理の仕様

- ファイルごとに個別に列挙された不整合リストを１つに連結する
- 連結した不整合リストが、１つのリストとしてまとまりのあるものになるように整理する作業を Codex CLI に依頼する
- e.g.
    - 内容に重複のある不整合は１つにマージする
    - 相互に矛盾する修正方針を矛盾しないように修正する
- 「整理された不整合リスト」上の項目は、全て要修正項目として扱う
- 「整理された不整合リスト」が空の場合のみ「検出された不整合なし」と扱う
    - これは「この調査結果においては」という但し書きが付くが、不整合の完全解消は `cmoc apply` の目的ではないので、これでよい
- Structured Output の schema
    - 「不整合リストアップ」用の schema をそのまま流用する

## 不整合追従作業の仕様

- 出された不整合を解消するための修正作業を Codex CLI に依頼する
- この修正作業は、不整合点１つにつき１回 Codex CLI を起動する
- 補足情報として不整合点の情報をプロンプトに注入する
- Codex CLI に依頼する作業は不整合の修正そのものを目的とし、実装が `oracles` へ完全に追従したことの保証は求めない

## 回数上限でループを抜けた場合

- エラーとみはみなさず、作業結果の区分「未収束」として処理を続行する

## 作業レポートの仕様

- レポート執筆は Codex CLI に依頼する
- レポートの内容
    - 作業結果
        - 作業結果の区分を一言で書く
            - 収束 : 「検出された不整合リストが空」によりループを終了した場合
            - 未収束 : 「回数上限に達した」によりループを終了した場合
    - 不整合件数の推移
        - ループごとに何件の不整合を見つけたかを書く
        - 「未収束」の場合は、まだ不整合が残っている可能性を追記する
    - `<cmoc-branch>` 上の全ての変更内容に対する要約
        - この `cmoc apply` で行った作業内容だけの要約ではない（それ以前の作業内容も含めるということ）
        - 変更内容の意味論に基づいたカテゴリ分けを行うこと
- レポート本体は `<repo-root>/.cmoc/reports/apply/<time-stamp>.md` にファイルに保存する
- 作成したレポートのフルパスを標準出力に流す

## サブコマンドの終了コード

- 収束・未収束・エラーの３種類を区別可能であること
