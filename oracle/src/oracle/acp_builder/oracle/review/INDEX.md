# `enumerate_finding.json`

## Summary
- 対象 JSON は、レビューで見つかった新規所見を構造化して返すための出力スキーマです。所見ごとに重大度、短い見出し、主な根拠となる oracle file、理由を保持します。

## Read this when
- oracle file のレビュー結果を新規所見として列挙するとき。
- 所見の重大度や根拠ファイル、既知の所見との差分を確認するとき。

## Do not read this when
- レビュー所見を扱わない通常の ACP builder 実装を読むとき。
- INDEX.md のルーティング情報だけを確認するとき。

## hash
- bf1beeb7e863efdb9f38a22902dbccae13ddd76b070e8492eeb4dd1e929aa085

# `enumerate_finding.py`

## Summary
- `cmoc oracle review`で新規所見を列挙するエージェント呼び出しパラメータの正本実装。レビュー対象oracle file、関連所見、レビュー用プロンプト、出力schema、読み取り権限を組み立てる。

## Read this when
- `cmoc oracle review`の新規所見列挙処理を変更・調査するとき
- レビュー対象ファイルや既知の関連所見をプロンプトへ渡す方法を確認するとき
- oracle review用のagent call設定、prompt生成、Structured Output設定を確認するとき

## Do not read this when
- 通常のoracle fileレビュー規則や所見の判定基準だけを確認したいときは、oracle reviewの仕様文書を直接読む
- レビュー対象以外のagent call構築や一般的なprompt生成を変更・調査するときは、該当する実装を直接読む
- CLIの通常のサブコマンド実装やレビュー実行結果だけを確認したいとき

## hash
- edc5bfb01ae723664c191cdd1186d08ae27fb725eefab5b015e27dc416729db7

# `judge_finding.json`

## Summary
- 対象は `verdict` と `reason` を必須とする判定結果用 JSON Schema です。

## Read this when
- 対象の判定結果形式を確認するとき。

## Do not read this when
- 判定対象の所見そのものを確認するとき。

## hash
- a024022fc7378f92b7df63be281522661d57e9b773f1d51db649dbcb5b673512

# `judge_finding.py`

## Summary
- `cmoc oracle review` における、仕様断片レビュー所見の採否判定用 AgentCallParameter を構築する。所見、その妥当性を支持する理由、反対理由をプロンプトへ埋め込み、oracle レビュー規則に従う判定依頼を生成する。

## Read this when
- `cmoc oracle review` の所見採否判定プロンプトを変更・確認するとき
- 判定用エージェント呼び出しのモデル、推論強度、読み取り権限、Structured Output schema の指定を確認するとき

## Do not read this when
- 所見採否判定以外の oracle review 処理を確認したいとき
- 一般的な prompt builder や構造化文書レンダリングの実装を直接確認すべきとき
- 判定結果の Structured Output schema 定義そのものを確認したいとき

## hash
- dc28daf9de56368770161b431e467e106392ac0df06dabcf5495f93c92536b11

# `merge_finding.json`

## Summary
- 対象 JSON Schema は、入力所見リストの重複・矛盾を整理する編集操作を表す。各操作は delete・replace・merge のいずれかで、対象 finding_id と、削除時の null または編集後所見を指定する。

## Read this when
- 所見の重複や矛盾を解消するための編集操作形式を確認するとき。
- finding の重大度、タイトル、根拠 oracle file、整理理由の構造を確認するとき。

## Do not read this when
- 個別の所見内容やレビュー判定の基準だけを確認したいとき。
- この JSON Schema を実装・検証するコードを直接確認したいとき。

## hash
- 0966bfdbee83e16727ad5010f02f8010e46f6ea9121624f7093757678ed500eb

# `merge_finding.py`

## Summary
- `cmoc oracle review` における、oracle file の所見リストを整理する agent call 用パラメータを構築する正本実装。入力所見を埋め込んだレビュー prompt、oracle-only のファイルアクセス制約、Structured Output schema の参照先をまとめる。

## Read this when
- `cmoc oracle review` の所見リストマージ処理を変更・調査するとき。
- 所見の重複・矛盾を解消するための prompt 生成条件、モデル設定、oracle-only 読み取り制約を確認するとき。

## Do not read this when
- 所見リストの編集操作 schema 自体を確認したい場合は、prompt が参照する JSON schema 定義を直接読む。
- `cmoc oracle review` の所見検出・レビュー実行など、所見マージ以外の処理を調査するときは、該当する prompt builder やサブコマンド実装を直接読む。

## hash
- badab8d57d521725a64f57bec1cb4d5898fd4edcddf156bb2e0819cea1a691bd

# `validate_finding_advocate.json`

## Summary
- 対象 JSON は review 用 oracle src で、validate_finding_advocate の入力・出力契約を定義する。

## Read this when
- review finding の advocate 検証処理の入出力契約を確認するとき。

## Do not read this when
- review finding の advocate 検証処理以外を扱うとき。

## hash
- 229fedb31871f51de412eb7dd3a7026bc34829344851b2bc81dc8231b250e296

# `validate_finding_advocate.py`

## Summary
- `cmoc oracle review` がレビュー所見を擁護するためのエージェント呼び出しパラメータを構築する oracle source。所見、既知の賛成理由、反対理由をプロンプトへ組み込み、oracle file を根拠に新規の妥当性理由だけを列挙させる。関連する JSON schema とプロンプト生成処理への入口となる。

## Read this when
- `cmoc oracle review` の所見擁護処理、またはそのエージェント呼び出しパラメータを変更・調査するとき
- 対象所見・既知理由のプロンプト埋め込みや、oracle-only のファイルアクセス制約を確認するとき
- 所見擁護エージェントの出力 schema と生成プロンプトの対応を確認するとき

## Do not read this when
- 所見の妥当性判定そのものや、反対理由の列挙処理を調査するときは、それぞれの専用実装を直接読む
- 一般的なエージェント呼び出し基盤、パス解決、構造化文書レンダリングの仕様だけを調査するとき
- `cmoc oracle review` と無関係なサブコマンドやプロンプト生成処理を調査するとき

## hash
- 8185d38249598e99507ba4d80c4626e7f5f048a7f13f60aae578033885763320

# `validate_finding_challenger.json`

## Summary
- 対象所見が妥当ではない新規理由を返すための JSON Schema を定義している。理由がない場合は空配列を許容する。
- `reasons` は必須かつ追加プロパティを認めないため、出力形式が明確に制約されている。

## Read this when
- 対象所見に対する反証理由の出力形式を確認するとき
- レビュー用 Structured Output の schema を確認するとき

## Do not read this when
- 妥当性の判定基準そのものを確認したいとき
- レビュー処理のプロンプト生成実装を確認したいとき

## hash
- dfeec2f83fac0acf4622e1f9286a65c266d11d3943bcbf685448b58b9ce245bc

# `validate_finding_challenger.py`

## Summary
- `cmoc oracle review` における、レビュー所見が妥当ではない理由を列挙する AI エージェント呼び出しパラメータの正本。所見・既知の賛成理由・反証理由をプロンプトへ渡し、oracle file を根拠とする新規反証理由のみを返す処理の入口。

## Read this when
- `cmoc oracle review` の所見否定理由列挙 prompt を変更・確認するとき
- 反証理由の入力項目、oracle-only のアクセス制約、重複排除や空配列の要求を確認するとき

## Do not read this when
- レビュー所見の判定ロジック自体や Structured Output schema の詳細を確認したいとき
- `cmoc oracle review` の他の prompt やサブコマンド実装を確認したいとき

## hash
- f05dc1f82f71f61e8d4772ef90c47afb26006ae3e76c5b8482dbab29ba324141
