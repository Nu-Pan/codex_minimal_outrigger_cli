# `app_spec`

## Summary
- app_spec 配下は、cmoc アプリケーション全体の利用者向け挙動と実行時規約を述べる oracle doc 群への入口です。CLI 補完、Codex CLI 呼び出し、ログ、エラー処理、INDEX.md インデクシング、セッション状態、run 隔離、プロンプト規範、使用手順、サブコマンド仕様へ読み進むための領域です。
- 個別ファイルは横断規約を扱い、下位ディレクトリはサブコマンド単位の外部挙動や状態遷移を扱うため、cmoc の公開 CLI 挙動と管理状態の仕様を探す起点になります。

## Read this when
- cmoc の CLI としての公開挙動、利用手順、サブコマンドの事前条件・状態遷移・出力・git 操作を、仕様断片から確認したいとき。
- Codex CLI 呼び出し、Structured Output、ログ保存、エラー処理、プロンプト生成、run 隔離、セッション状態、INDEX.md 自動生成など、複数サブコマンドから参照されるアプリケーション横断規約を実装・修正・テストするとき。
- どのサブコマンド仕様または横断仕様を読むべきかを、関心領域から選びたいとき。
- 利用者の標準ワークフローにおける初期化、session fork/join、oracle review、apply fork/join の順序と、branch・worktree・oracle snapshot の関係を確認したいとき。

## Do not read this when
- oracle file と realization file の基本的な責務分担、編集権限、正本仕様断片としての一般原則だけを確認したいとき。
- path keyword や root model の定義そのものだけを確認したいとき。
- 実装ファイルやテストファイルの配置、関数分割、既存 helper、内部コード構造だけを調べたいとき。
- 個別の AgentCallParameter builder が生成する schema やパラメータ内容だけを確認したいとき。
- INDEX.md エントリーの書き方やルーティング文書一般の品質基準だけを確認したいとき。

## hash
- 72b24335934491de32629c1661c20a709615ee5c63e1d9b2d5f0e3db8b0a39da

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
- 採用しなかった設計案とその理由を集めた設計判断メモ群。AI の記憶・kaizen 自動注入、AI 作業計画の人間レビュー、apply 系処理の orchestration など、採用済み仕様だけでは見えにくい non-goal と判断背景を扱う。
- 現行方針を変更する前に、過去に退けた案がどの前提で不採用になったかを確認する入口になる。特に、人間の認知負荷、暗黙仕様化、agent call 間の文脈分断、状態ズレ、重複調査、責務分担の観点から設計案を比較するための領域。

## Read this when
- 採用済み仕様だけではなく、なぜ別案を採らなかったのかという設計判断の背景を確認したいとき。
- AI に継続的な記憶、振り返り、改善案、作業計画を持たせる workflow を追加または再検討しているとき。
- 人間が正本仕様断片を編集し、AI が実装可能性を見て実装を追従させるという責務分担の根拠を確認したいとき。
- apply 系処理で、計画立案の独立工程化、所見リストアップの並列化、所見単位の修正、ダーティフラグ方式などの不採用理由を確認したいとき。
- 新機能や workflow 変更案が、oracle とは別の暗黙仕様、余分な状態管理、文脈分断、人間レビュー負荷を増やさないか判断したいとき。

## Do not read this when
- 採用済み仕様の詳細、CLI の具体的な入出力、状態ファイル仕様、テスト期待値を確認したいだけのとき。
- oracle file、realization file、INDEX、ログ、実行成果物などの一般的な定義や配置を確認したいとき。
- 個別コマンドの現在の操作方法や実装手順を探しており、不採用案の背景を必要としていないとき。
- kaizen、作業計画、apply 系処理などの具体的な不採用判断ではなく、正本仕様断片全体の記述標準やルーティング規則を確認したいとき。

## hash
- 8fa7fb4c53865b798f61c90edc698f9860fb35996919fcfc3e579ea9614e529b

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
