# `app_spec`

## Summary
- `app_spec` 配下の個別仕様を読むための入口。CLI の振る舞い、状態、出力、エラー処理などのうち、この配下にある正本仕様断片へ進む必要があるときに使う。

## Read this when
- この配下の個別仕様を実装・修正・テストするとき。
- 対象機能の人間向け仕様がこの配下にあるか確認してから本文へ進むべきとき。
- 複数の正本仕様断片のうち、この配下のものを読む必要があるか切り分けたいとき。

## Do not read this when
- この配下ではない別の正本仕様断片を直接確認したいとき。
- 実装ファイルやテストファイルの内容だけを見れば判断できるとき。
- oracle file と realization file の一般原則だけを確認したいとき。

## hash
- c82fb3ef7d1cfebe970227c130ed8814a68e92d1f2b07949ec671969d35f0281

# `branch_model.md`

## Summary
- cmoc が session 用 branch と run 用 branch / worktree をどう切り分けるかを定める基礎仕様。`session fork` でどの local branch を session の home とみなすか、各 merge commit が何を結ぶか、run ごとの隔離先の命名と役割を確認したいときに読む。
- branch 名・commit 名・worktree 名の対応関係を揃える必要がある変更の入口。サブコマンド固有名を決める前提として、共通の抽象概念と具体名への落とし込みを確認するために読む。

## Read this when
- session 作成時の分岐元や最終 merge 先を決める必要がある。
- run 実行を session の作業履歴から分離する branch / worktree の扱いを実装・修正したい。
- branch 名、fork / join commit 名、worktree 名の命名規則を合わせたい。

## Do not read this when
- 個別サブコマンドの実処理や引数仕様だけを確認したい。
- git の一般的な branch 運用や worktree 機能そのものを学びたいだけで、cmoc 固有の対応関係は不要である。
- session や run の状態保存、エラー処理、表示文言の仕様を確認したい。

## hash
- 641e02b2de87442586902c10daa64b10afe5459c2e7f4dc361d085a419c25eb7

# `considered_alternative`

## Summary
- cmoc で採用しなかった設計案と、その不採用理由を集めた設計判断メモ群。apply orchestration、file access rule 違反の事後検査、gitignore と permission profile の変換、AI-generated memory/kaizen の自動注入、AI 作業計画の人間レビュー方式について、再検討時の入口になる。
- 採用済み仕様そのものではなく、過去に検討して退けた案の背景、避けるべき理由、設計判断の境界を確認するための領域。

## Read this when
- cmoc の現行設計に対して、過去に不採用となった代替案を再検討しているとき。
- cmoc apply の作業計画立案、所見リストアップ、並列 agent call、所見単位修正、調査対象管理方式を変更する根拠を探しているとき。
- file access rule 違反を agent call 後の差分検査や別 agent call による回復で扱う案を検討しているとき。
- git 追跡対象外ファイルを読み書き規則や permission profile の例外として扱う案、または .gitignore を permission profile へ変換する案を検討しているとき。
- AI-generated kaizen、memory、振り返り結果、改善案、継続的指示を後続の Codex CLI 実行へ自動注入する状態管理を検討しているとき。
- AI に作業計画を書かせて人間がレビューする workflow と、oracle を人間が編集し AI が実装可能性を評価する方式を比較したいとき。

## Do not read this when
- 採用済みの詳細仕様、CLI 入出力、状態ファイル仕様、テスト期待値、実装経路を確認したいとき。
- oracle file と realization file の一般的な定義、責務境界、記述標準、INDEX.md エントリー生成規則を確認したいとき。
- Codex CLI 本体の memory 機能、git ignore の一般仕様、permission profile の現在の実装方法など、外部または現行採用仕様の詳細を調べたいとき。
- 不採用案の背景ではなく、個別コマンドの操作方法、現在の workflow の具体的挙動、または実装・テスト対象を探しているとき。

## hash
- 7767be4a4c27a93b3358c7b521d7f73444e4557bc421c8899dca1dcddd2e6e29

# `dev_rule`

## Summary
- Python 実装・テストを書くときの共通コーディング規則をまとめる入口。型ヒント、import、docstring、コメント、ログ、非公開識別子など、実装差を避けたい書き方の基準を確認する。
- CLI の構成や共通処理の配置ではなく、コード全体に共通する記法・記述方針を確認したいときに読む。

## Read this when
- Python の実装またはテストを追加・修正し、型ヒント、import、docstring、コメント、ログメッセージ、非公開識別子の書き方を確認したいとき。
- コードレビューや実装修正で、コメントの粒度、日本語コメントと英語ログの使い分け、NOTE を付けるべき補足の扱いを判断したいとき。
- 新しい関数・クラス・モジュールを作る前に、命名、責務、入出力を明確に保ち、過剰な実装を避けるための共通規則を確認したいとき。
- 相対 import、循環参照、TYPE_CHECKING の使い方など、モジュール間参照の書き方を判断したいとき。

## Do not read this when
- CLI の具体的なコマンド仕様、出力 schema、保存状態、エラー条件など、利用者に見える個別機能の正本仕様を確認したいとき。
- oracle file と realization file の役割、正本仕様断片の扱い、仕様と実装の関係など、リポジトリ全体の仕様管理原則を確認したいとき。
- ファイル分割、重複削減、依存追加、テスト肥大化抑制など、realization file の保守量や構成判断に関する一般原則を確認したいとき。
- 対象コードの具体的な実装場所や既存実装の現在の構造を探したいとき。

## hash
- bfbb73fd94dd2b748b8d08b8cd6c2d64351a217ea93d72282d9411013623a388
