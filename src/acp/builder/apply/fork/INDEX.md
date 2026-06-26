# `change_summary.json`

## Summary
- 差分要約を意味カテゴリごとに整理するための JSON Schema。変更カテゴリごとの人間向け要約と、根拠となる主要な変更パスの集合を表す構造を定義する。

## Read this when
- フォーク適用や変更処理の結果として、変更内容をカテゴリ別の要約として出力・検証する schema を確認したいとき。
- 差分要約に含める情報の粒度、カテゴリ単位のまとまり、主要な変更パスの扱いを確認したいとき。

## Do not read this when
- 実際の差分生成アルゴリズム、フォーク作成手順、ファイル適用処理の制御フローを調べたいとき。
- 個別カテゴリ名の網羅的な一覧や、変更パス抽出の具体的な実装規則を探しているとき。

## hash
- 4148f8f7efb949b4872076b64dcb4bd2792df6d888011903c10501ce6f519987

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向けに、変更要約生成を担当する AI エージェント呼び出しパラメータを構築する実装。
- 未加工の `git diff` 出力を補助プロンプトとして埋め込み、差分を人間向けに Structured Output schema へ要約させるための complete prompt、モデル種別、推論量、読み取り専用アクセス、出力 schema 参照をまとめて返す。
- リポジトリルート解決、prompt parts、ACP の基本型を組み合わせ、変更内容そのものの解析ではなく要約依頼用パラメータ生成に責務を限定している。

## Read this when
- `cmoc apply fork` の作業レポートで、変更要約生成エージェントに渡す role、summary、goal、補助 diff、file access mode を確認または変更したいとき。
- `git diff` の生テキストをどのように prompt に埋め込み、どの AgentCallParameter と schema に接続しているかを追いたいとき。
- apply fork 系の prompt builder のうち、変更差分の要約生成だけに関わる実装入口を探しているとき。

## Do not read this when
- `cmoc apply fork` の実際の git 操作、branch 操作、fork 適用処理、作業ツリー変更処理を調べたいだけのとき。
- 生成された要約 JSON の項目定義や Structured Output schema 自体を確認したいとき。
- complete prompt の共通構築規則、StructDoc の markdown 描画、ACP 型の汎用仕様を調べたいとき。
- 差分内容を解析・整形するロジックを探しているとき。この実装は raw diff を解析せず prompt に渡すだけである。

## hash
- 0753a2b42aa5847606f10680feaa7ea8d9221643539dae78c24c4ac6c8aeb225

# `file_finding_enumeration.json`

## Summary
- 実装調査で見つかった問題点を、根拠位置、正本仕様上の要求、観測された実装、問題理由、修正方針として報告するための構造化出力を定義する。
- 仕様と実装の乖離をレビュー結果として人間に渡す場面で使う、所見リストの出力契約を担う。

## Read this when
- 実装レビューや適合性調査の結果として、明確に修正が必要な所見を返す出力形式を確認したいとき。
- 所見に含めるべき根拠情報、仕様要求、観測結果、理由、修正方針の粒度を確認したいとき。
- レビュー結果の生成側または検証側で、所見リストが空でない根拠位置を持つことを前提にしたいとき。

## Do not read this when
- 単に実装対象の仕様そのものを探しているとき。ここには個別機能の要求ではなく、レビュー所見の報告形式だけがある。
- INDEX.md 用エントリーや一般的なルーティング文書の書き方を確認したいとき。
- 所見を JSON 以外の文章、ログ、CLI 表示としてどう見せるかを確認したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` で、単一の起点ファイルから realization file の要修正点を列挙するための AI 呼び出しパラメータを組み立てる実装。
- 起点パスを実パス化し、リポジトリルート内の関連する oracle file と realization file を読む read-only 調査 prompt を生成して、所見リスト用の構造化出力設定とともに返す。
- ファイル数分呼ばれる重い処理だが、下流への影響が大きいため mainstream model と medium reasoning を選ぶ、という判断もこの対象内で扱う。

## Read this when
- `cmoc apply fork` のファイル単位レビューや所見列挙の prompt 内容、role・summary・goal・標準適用条件を確認したいとき。
- 起点ファイルから関連する oracle file と realization file を読ませる AI 呼び出しパラメータの構築方法を変更したいとき。
- apply review standard、oracle standard、realization standard を有効にした所見リストアップ呼び出しの model class、reasoning effort、file access mode、出力 schema の指定を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体のコマンド制御、ファイル列挙、複数ファイル分の呼び出し集約、または結果の適用処理を調べたいだけのとき。
- 所見リストの構造化出力 schema そのもの、または complete prompt の共通レンダリング処理を変更したいとき。
- パスモデルの定義、実パス解決、リポジトリルート解決の詳細を確認したいとき。

## hash
- aebe9ac6115f9e612efcca42bb3f08ac10dde025487f49775c846e99596a087f

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出済みの所見に対応する修正作業を AI エージェントへ依頼するための呼び出しパラメータを構築する実装。
- 所見リストを JSON コードブロックとしてプロンプトに埋め込み、realization file の修正、realization standard 遵守、git add/commit 禁止などの作業条件を含む complete prompt を生成する。
- モデル種別、推論努力、ファイルアクセスモード、生成済み Markdown prompt をまとめた `AgentCallParameter` を返す入口。

## Read this when
- `cmoc apply fork` が所見対応用エージェントを起動する際の prompt 内容、権限、モデル指定を確認または変更したいとき。
- 所見データをどのように AI への作業指示へ変換しているかを調べたいとき。
- 所見対応作業に含める注意事項、realization file 修正条件、realization standard の適用有無を調整したいとき。
- `AgentCallParameter` の生成ロジックのうち、所見対応フェーズ専用の入力と出力を確認したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、実行フロー全体を調べたいだけのとき。
- 所見そのものを生成・検出するロジックを調べたいとき。
- complete prompt の共通構築処理や Markdown rendering の詳細を調べたいとき。
- path model、file access mode、agent call parameter などの基礎型や共通定義を確認したいだけのとき。

## hash
- 09fc110b1ae3e5680a8bdfa4f8e94fb7691d4d1f271e7484d642f4602f5a5c3b
