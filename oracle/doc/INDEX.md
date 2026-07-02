# `app_spec`

## Summary
- cmoc のアプリケーション仕様断片を集める領域。CLI 補完、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、セッション状態、run 隔離、サブコマンド、利用手順など、利用者向け挙動と実行基盤の正本仕様断片へ進む入口になる。
- 個別文書は、外部契約、状態永続化、標準入出力、ファイルアクセス制限、agent call 境界、git branch/worktree 操作、自動生成されるルーティング情報など、実装差を避けたい要件ごとに読む先を分けている。

## Read this when
- cmoc の CLI としての外部挙動、実行前後の処理、ログ、エラー、状態、git 操作、agent call 呼び出し境界のいずれかを実装・修正・テストするとき。
- 補完プローブ、通常実行、サブコマンド実行、Codex CLI 起動、Structured Output、retry/resume、並列実行、インデクシング、自動コミットなど、アプリケーション全体の制御仕様を探すとき。
- セッション開始から oracle 改訂、review、apply fork/join、セッション終了までの標準ワークフローや、その途中で記録される状態・ブランチ・ログの関係を確認したいとき。
- 個別仕様に進む前に、対象がサブコマンド固有の話か、横断的な実行基盤の話か、利用手順の話かを切り分けたいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー生成基準だけを確認したいとき。
- パスキーワードやルート種別の体系そのものを確認したいだけのときは、パスモデルを定義する対象へ直接進む。
- 実装モジュール、テスト配置、内部 helper 分割、既存コード構造など、realization code の具体的な作りを調べたいとき。
- agent call の個別 prompt builder や parameter schema の正本実装だけを確認したいときは、該当する builder 側へ直接進む。

## hash
- ada265522c984a91fa106cef035715935bfb9c9c25c0f348cfeab32536576164

# `branch_model.md`

## Summary
- cmoc が通常の local branch から session branch を作り、run ごとに session branch から run branch と linked worktree を分離して扱う git branch / commit / worktree モデルを定義する。
- repository default branch を特別扱いせず、session fork 時点の local branch を session home branch として扱う方針、cmoc-managed branch の命名規則、fork / join commit の用語を確認する入口になる。

## Read this when
- cmoc session fork / join や run 系サブコマンドが、どの branch を作成し、どの branch を分岐元・merge 先として扱うべきかを確認したいとき。
- cmoc-managed branch、session branch、session home branch、run branch、apply / review などのサブコマンド別 branch 名の関係を実装・テストする前。
- run の作業内容を session branch や repo root から隔離するための branch / linked worktree の責務、命名規則、commit 用語を確認したいとき。
- repository default branch、local branch、remote-tracking branch が cmoc 管理対象かどうか、また default branch を特別扱いしないことを確認したいとき。

## Do not read this when
- oracle file と realization file の責務分担、正本仕様断片としての扱い、INDEX.md エントリー作成基準を確認したいだけのとき。
- path キーワードや repo root / run root / work root の一般的な定義を確認したいとき。
- git branch / commit / worktree の cmoc 用語ではなく、CLI 出力形式、設定項目、永続状態、実装品質基準、テスト肥大化抑制の一般方針を調べたいとき。

## hash
- 3548445dc5441fa2e2e774ba8b45d8bdaaf363b110f5e8a3f4704bdac6cdf3af

# `considered_alternative`

## Summary
- cmoc の設計で検討されたが採用されなかった代替案を集めた正本仕様断片群。`cmoc apply` の orchestration 方針、gitignore と permission profile の連携、AI-generated memory/kaizen の自動注入、作業計画レビュー方式などについて、不採用理由と採用済み方針の背景を確認する入口になる。
- 採用済み仕様の詳細そのものではなく、過去に自然に見える設計案を退けた根拠、人間と AI の責務境界、暗黙仕様や状態管理を増やさない判断、トークン消費や文脈分断を避ける設計判断を扱う。

## Read this when
- cmoc に機能や workflow を追加する際、過去に検討された代替案を再採用してよいか判断したいとき。
- `cmoc apply` の実行フロー、所見リストアップ、並列 agent call、作業計画立案、調査対象管理に関する不採用案の背景を確認したいとき。
- git 追跡対象外ファイルを読み書き規則や permission profile の例外として扱う案が採用されていない理由を調べるとき。
- AI-generated kaizen、memory、振り返り結果、失敗分析を後続の Codex CLI 実行へ自動注入する設計を避ける根拠を確認したいとき。
- AI が作業計画を作り、人間がそれをレビューする workflow ではなく、人間が oracle を編集して AI が実装可能性を評価する方式を採る背景を確認したいとき。

## Do not read this when
- 採用済みの CLI 入出力、状態ファイル仕様、テスト期待値、実装手順など、現在の具体仕様を確認したいとき。
- oracle file、realization file、読み書き規則、permission profile などの一般定義や正本仕様そのものを確認したいとき。
- INDEX.md エントリー生成規則や oracle/realization 全体の記述標準を確認したいとき。
- 不採用案の背景ではなく、個別コマンドや補助機能の現在の操作方法だけを知りたいとき。

## hash
- 4a7f9c7172d16b676b7a434588b4b03425de8931194b44cb3281e1ea7425b547

# `dev_rule`

## Summary
- cmoc の開発時に従う横断的な規則群への入口。Python 実装の書き方、CLI 構成と共通処理の配置、開発環境、テスト方針を扱う正本仕様断片をまとめている。
- 個別機能の利用者向け仕様ではなく、realization code を追加・修正・検証するときの共通判断基準を確認するための領域である。

## Read this when
- Python の実装またはテストを追加・変更する前に、型ヒント、import、docstring、コメント、ログ、非公開識別子などの基本的な書き方を確認したいとき。
- CLI 引数解釈、エントリーポイント、サブコマンド本体、複数サブコマンドで使う共通処理の配置方針を判断したいとき。
- 開発環境、Python 仮想環境、pip、依存追加、ファイルエンコード、ファイル名・ディレクトリ名の命名規則を確認したいとき。
- pytest による自動テストを追加・変更し、Codex CLI や LLM の挙動ではなく、決定論的な制御ロジックとして検証してよい範囲を判断したいとき。
- コードレビューや実装修正で、実装・テスト全体に共通する品質基準や責務分離の基準を確認したいとき。

## Do not read this when
- 個別サブコマンドの外部仕様、入出力 schema、保存状態、エラー条件など、利用者に見える機能仕様を確認したいとき。
- path キーワード、oracle file と realization file の関係、正本仕様断片の扱い、INDEX.md 生成基準など、リポジトリ全体の基本概念を確認したいとき。
- 特定の実装ファイル、テストファイル、既存関数のシグネチャ、内部ロジック、現在のテスト期待値を探したいとき。
- Codex CLI や LLM の実際の応答品質、プロンプト品質、生成結果の妥当性を評価したいとき。

## hash
- c1fea811a659d60c1026cb0cff145c59f0af412ed0e06fbdc61402924b088a7f
