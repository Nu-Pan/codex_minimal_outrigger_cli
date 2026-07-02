# `fork`

## Summary
- `cmoc apply fork` で使う AI エージェント呼び出しパラメータと、その出力契約を扱う。差分要約、ファイル単位の所見列挙、所見対応作業の prompt・モデル設定・ファイルアクセス方針・Structured Output schema への入口となる。

## Read this when
- `cmoc apply fork` の作業レポート向け差分要約、実装レビュー所見の列挙、または検出所見への対応 agent call parameter を確認するとき。
- fork 適用後の差分や対象ファイルを AI に渡す prompt、placeholder、readonly/write 権限、model class、reasoning effort、Structured Output schema の指定を確認したいとき。
- 変更要約や所見リストの JSON 出力契約と、それを生成・利用する apply fork 用 oracle src の対応関係をたどりたいとき。

## Do not read this when
- `cmoc apply fork` 全体の CLI 引数解析、git 操作、branch 操作、作業レポート保存、所見統合などの実行フローを調べたいとき。
- apply fork 以外のサブコマンド用 prompt、agent call parameter、出力 schema を探しているとき。
- AgentCallParameter、complete prompt builder、path placeholder 解決、markdown rendering などの共通部品そのものの実装詳細を確認したいとき。

## hash
- bb2f3cefe92fabe1755ef47e94b56af1f6bdcff410e29dd9326d59ae260d56fb
