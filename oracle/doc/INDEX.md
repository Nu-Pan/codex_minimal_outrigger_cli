# `app_spec`

## Summary
- cmoc アプリケーション全体の正本仕様断片を集める領域。CLI 補完、Codex CLI 呼び出し、ログ、共通エラー処理、インデクシング、横断的な雑則、プロンプト、run 隔離、セッション状態、サブコマンド仕様、利用手順への入口になる。
- 個別実装の構造ではなく、外部挙動、状態管理、ファイル生成、agent call、出力、作業隔離など、複数機能にまたがる仕様判断を始めるためのルーティング対象。

## Read this when
- cmoc の CLI 外部挙動、サブコマンド単位の状態遷移、利用者向け出力、ログ、エラー処理、補完処理のいずれかに関わる仕様を探すとき。
- Codex CLI を呼び出す agent call、プロンプト引き渡し、Structured Output、retry・resume、profile やファイルアクセス制限の仕様を確認したいとき。
- INDEX.md の自動生成、ハッシュ更新、自動コミット、目次生成 agent call、または明示インデクシングの仕様を調べたいとき。
- セッション状態、run ごとの branch・worktree 隔離、apply や fork/join の前提となる状態保存・作業反映モデルを確認したいとき。
- cmoc の標準的な利用順序、初期化からセッション開始、oracle 改訂、apply、セッション終了までの流れを確認したいとき。
- タイムスタンプ、実装ファイル列挙、作業用状態領域、カレントディレクトリ、管理ブランチ上の変更範囲など、複数機能から参照される横断的な前提を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー作成基準そのものだけを確認したいとき。
- パスキーワードやルート種別の定義そのものを確認したいときは、パスモデルを扱う対象を読む。
- 実装モジュール、テスト、helper 分割、依存追加、補助スクリプトなど、realization 側の現在構造だけを調べたいとき。
- 特定サブコマンドの詳細仕様を読む対象が既に分かっているときは、そのサブコマンド固有の仕様へ直接進む。
- 既に単一の仕様断片が対象として決まっており、その本文から実装・テスト判断を行うだけのとき。

## hash
- 887cd112cf0385ee1bd76eb6f3b0ebaf443233baa15a85a6c123a4d140a0fd80

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
