# `doc`

## Summary
- `app_spec` 配下の個別仕様へ進むための入口。CLI の振る舞い、状態、出力、エラー処理など、この配下にある正本仕様断片を読む必要があるときに使う。
- `branch_model.md` は session 用 branch と run 用 branch / worktree の切り分けを定める基礎仕様。分岐元、最終 merge 先、fork / join commit、worktree 名の対応を揃える必要がある変更の入口。
- `considered_alternative` は採用しなかった設計案と不採用理由の集積。現行仕様の詳細ではなく、過去に退けた案を再検討するときの入口。
- `dev_rule` は Python 実装・テストの共通記法と書き方の基準。型ヒント、import、docstring、コメント、ログ、命名など、コード全体の書式方針を確認するときに読む。

## Read this when
- `app_spec` 配下の個別仕様を実装・修正・テストするとき。
- 対象機能の人間向け仕様がこの配下にあるか確認してから本文へ進むべきとき。
- 複数の正本仕様断片のうち、この配下のものを読む必要があるか切り分けたいとき。
- session 作成時の分岐元や最終 merge 先を決める必要があるとき。
- run 実行を session の作業履歴から分離する branch / worktree の扱いを実装・修正したいとき。
- branch 名、fork / join commit 名、worktree 名の命名規則を合わせたいとき。
- cmoc の現行設計に対して、過去に不採用となった代替案を再検討しているとき。
- cmoc apply の作業計画立案、所見リストアップ、並列 agent call、所見単位修正、調査対象管理方式を変更する根拠を探しているとき。
- file access rule 違反を agent call 後の差分検査や別 agent call による回復で扱う案を検討しているとき。
- git 追跡対象外ファイルを読み書き規則や permission profile の例外として扱う案、または .gitignore を permission profile へ変換する案を検討しているとき。
- AI-generated kaizen、memory、振り返り結果、改善案、継続的指示を後続の Codex CLI 実行へ自動注入する状態管理を検討しているとき。
- AI に作業計画を書かせて人間がレビューする workflow と、oracle を人間が編集し AI が実装可能性を評価する方式を比較したいとき。
- Python の実装またはテストを追加・修正し、型ヒント、import、docstring、コメント、ログメッセージ、非公開識別子の書き方を確認したいとき。
- コードレビューや実装修正で、コメントの粒度、日本語コメントと英語ログの使い分け、NOTE を付けるべき補足の扱いを判断したいとき。
- 新しい関数・クラス・モジュールを作る前に、命名、責務、入出力を明確に保ち、過剰な実装を避けるための共通規則を確認したいとき。
- 相対 import、循環参照、TYPE_CHECKING の使い方など、モジュール間参照の書き方を判断したいとき。

## Do not read this when
- この配下ではない別の正本仕様断片を直接確認したいとき。
- 実装ファイルやテストファイルの内容だけを見れば判断できるとき。
- oracle file と realization file の一般原則だけを確認したいとき。
- git の一般的な branch 運用や worktree 機能そのものを学びたいだけで、cmoc 固有の対応関係は不要であるとき。
- session や run の状態保存、エラー処理、表示文言の仕様を確認したいとき。
- 採用済みの詳細仕様、CLI 入出力、状態ファイル仕様、テスト期待値、実装経路を確認したいとき。
- oracle file と realization file の一般的な定義、責務境界、記述標準、INDEX.md エントリー生成規則を確認したいとき。
- Codex CLI 本体の memory 機能、git ignore の一般仕様、permission profile の現在の実装方法など、外部または現行採用仕様の詳細を調べたいとき。
- ファイル分割、重複削減、依存追加、テスト肥大化抑制など、realization file の保守量や構成判断に関する一般原則を確認したいとき。
- 対象コードの具体的な実装場所や既存実装の現在の構造を探したいとき。

## hash
- b0d56948a920266180c666f1be2f0aad58cb0d1bc781923c557b00e3d03f98ca

# `src`

## Summary
- `cmoc` の oracle-side source を束ねる入口。ACP builder 向けの共通型・パス解決・構造化文書レンダリング・プロンプト組み立ての土台を読むためのルーティング先。
- 個別の生成処理は、apply, review, session, tui, indexing の各領域に分かれている。ここでは共通概念と各領域への入口だけを押さえ、詳細仕様は下位へ進む。

## Read this when
- ACP builder 全体の共通仕様や、まずどの下位領域を読むべきかを絞り込みたい。
- agent 呼び出しパラメータ、モデルクラス、ファイルアクセスモード、パス表現の共通ルールを確認したい。
- プロンプト生成の共通部品や、oracle / realization に共通する基本標準の入口を確認したい。
- indexing, apply, review, session, tui のいずれかが扱う入力条件や出力契約の境界を先に把握したい。

## Do not read this when
- 特定のサブ機能の個別仕様だけを見たいときは、対応する下位領域へ直接進む。
- 実装詳細やテストの挙動を確認したいときは、oracle ではなく対応する realization file を読む。
- ACP builder 以外の正本仕様や、別系統のドキュメントを探しているときはここを起点にしない。

## hash
- 12f945f1dde21dad595bf87bbdaee8ab00c12c5738b6043990afb2adf3b346cb
