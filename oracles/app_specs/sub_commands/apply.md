# `cmoc apply`

## 概要

- `<repo-root>` の実装を `<repo-root>/oracles` で記述している正本仕様断片に追従させる

## 引数

- 引数なし

## 事前条件

- `<cmoc-branch>` 上に居なければエラー終了とする
- `<repo-root>/oracles` の外の未コミット差分があればエラー終了する

## 実行作業

1. `<repo-root>/.cmoc` が git の追跡対象外であることを保証する
2. `<repo-root>/oracles` 配下の未コミット差分を自動コミット
3. ループ（最大５回）
    1. `oracles` と実装との明確なズレを調査
    2. ズレがなければこの時点でループ終了
    3. `<repo-root>` の実装を `<repo-root>/oracles` に追従させる作業を Codex CLI にやらせる
    4. `<repo-root>/oracles` などの編集禁止ディレクトリに未コミット差分が有る場合はエラー終了
    5. 全ての未コミット差分を git にコミット（コミットメッセージは Codex CLI で適切なものを生成）
    6. ループ先頭に戻る
4. 作業結果をレポートする

## ズレ調査の仕様

- `oracles` ファイルと実装との明確なズレが無いかの調査を Codex CLI に依頼する
- この調査は `oracles` ファイルそれぞれに対して独立に行う (for each)
    - つまり `oracles` ファイルが N 件存在するのであれば `codex exec` を N 回呼び出す
    - `codex exec` で指定したファイルは以外のファイルも、必要にならば読むべきである（指定は「だけ」の意味ではない）
- 調査結果は Structured Output で「ズレのリスト」として受け取る
- Structured Output の schema は以下の通り
    ```json
    {
        "type": "object",
        "additionalProperties": false,
        "required": ["discrepancies"],
        "properties": {
            "discrepancies": {
                "type": "array",
                "description": "oracles と実装との明確なズレのリスト。空配列の場合のみズレなしとみなす。",
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
                            "description": "ズレの根拠となる oracle ファイルの絶対パス。"
                        },
                        "oracle_line_start": {
                            "type": ["integer", "null"],
                            "description": "ズレの根拠となる oracle 記述の開始行。行番号を特定できない場合は null。"
                        },
                        "oracle_line_end": {
                            "type": ["integer", "null"],
                            "description": "ズレの根拠となる oracle 記述の終了行。行番号を特定できない場合は null。"
                        },
                        "implementation_paths": {
                            "type": "array",
                            "description": "ズレに関係する実装・テスト・設定ファイルの絶対パス。未実装などで該当ファイルを特定できない場合は空配列。",
                            "items": {
                                "type": "string"
                            }
                        },
                        "title": {
                            "type": "string",
                            "description": "ズレの短い見出し。"
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
                            "description": "なぜ oracle と実装が明確にズレていると言えるのか。推測や未確認事項は含めない。"
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
- 「ズレのリスト」は全て要修正項目として扱う
- ズレのリストが空の場合のみ「ズレなし」とみなす

## ズレ追従作業の仕様

- 実装の `oracles` への追従作業を Codex CLI に依頼する
- 補足情報として「ズレのリスト」をプロンプトに注入する

## 回数上限でループを抜けた場合

- 正常系とみなして処理を続行する

## 作業レポートの仕様

- レポート執筆は Codex CLI に依頼する
- レポートの内容
    - 作業結果
        - 作業結果の区分を一言で書く
        - 作業区分
            - 完了 : 異常が起きずに最後まで完走出来た場合
            - 未完了 : 回数上限に引っかかった場合
    - ズレ件数の推移
        - ループごとに何件のズレを見つけたかを書く
        - 回数上限に引っかかった場合は、まだズレが残っている可能性を追記する
    - `<cmoc-branch>` 上の全ての変更内容に対する要約
        - この `cmoc apply` で行った作業内容だけの要約ではない（それ以前の作業内容も含めるということ）
        - 変更内容の意味論に基づいたカテゴリ分けを行うこと
- レポート本体は `<repo-root>/.cmoc/reports/apply/<time-stamp>.md` にファイルに保存する
- 作成したレポートのフルパスを標準出力に流す

## サブコマンドの終了コード

- 作業区分（完了・未完了）、エラーの３種類を区別可能であること
