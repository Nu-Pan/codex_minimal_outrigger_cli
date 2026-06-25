# `app_spec`

## Summary
- cmoc の公開仕様断片のうち、アプリケーション全体の外部挙動と横断ルールをまとめる領域。CLI 自動補完、Codex CLI 呼び出し、ログ、共通エラー処理、インデクシング、セッション状態、run 隔離、利用手順、サブコマンド仕様への入口を扱う。
- 個別ファイルは正本仕様断片として、利用者に見える CLI 挙動、状態・ログ・ブランチや worktree の扱い、agent call 前後の制御、プロンプト方針など、複数実装領域から参照される仕様判断の起点になる。
- サブコマンド固有の詳細は下位領域に分かれており、この領域は cmoc 全体の挙動を判断するための共通仕様と、どの詳細仕様へ進むべきかを選ぶための入口として位置づけられる。

## Read this when
- cmoc の CLI としての外部挙動、利用手順、サブコマンド単位の状態遷移、stdout・stderr・ログ出力、エラー処理、補完処理、インデクシング、Codex CLI 呼び出し規約を確認したいとき。
- session branch、run branch、worktree、oracle snapshot、apply 状態、ログファイル、Structured Output、retry・resume・quota 待機など、複数機能にまたがる制御や永続状態の仕様を実装・修正・テストするとき。
- 利用者向けコマンドの呼び出し順、初期化から session 開始、oracle 改訂、apply fork/join、session 終了までの標準ワークフローを確認したいとき。
- 個別サブコマンド仕様へ進む前に、共通の run 隔離、ログ、エラー、プロンプト、インデクシング、Codex CLI 呼び出し境界を押さえる必要があるとき。
- INDEX.md 生成や agent call 前処理、CLI 補完プローブ、サブコマンドログなど、通常のサブコマンド実行前後に混ざる横断処理の責務境界を判断したいとき。

## Do not read this when
- oracle file と realization file の基本的な責務分担、編集権限、正本仕様としての位置づけだけを確認したいとき。
- パスキーワードや root model の定義そのものを調べたいときは、パスモデルを定義する仕様または実装を読む。
- 実装ファイルの配置、関数分割、helper 設計、テスト構成など、公開仕様ではなく realization 側のコード構造だけを調べたいとき。
- 特定の AgentCallParameter builder、Structured Output schema、個別ログ JSON の具体的な key など、下位実装や個別 schema の詳細だけを確認したいとき。
- 既に対象のサブコマンド、ログ仕様、補完仕様、インデクシング仕様などが明確に決まっている場合は、この領域全体ではなく該当する本文または下位領域を直接読む。

## hash
- 203dcd4dbed8c750c794f8869bb44ebf7650352260fcd4782431f5828367b2d9

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
- 採用しなかった設計方針とその理由を集めた正本仕様断片群への入口。修正点リストアップ後の独立した作業計画立案、AI-generated kaizen や memory の次回実行への自動注入、AI が作業計画を書いて人間がレビューする workflow を採用しない理由を扱う。
- 採用済み仕様の詳細ではなく、過去に検討済みの non-goal と設計判断の境界を確認するための領域。人間の認知負荷、oracle の正本性、暗黙仕様の発生、AI と人間の責務分担、ループ設計上のトークン消費を判断材料として読む。

## Read this when
- 採用済み機能に新しい計画フェーズ、継続的な AI 記憶、自動注入される改善情報、人間による AI 計画レビューを追加すべきか判断したいとき。
- 実装対象にしない方針や、過去に検討済みの代替案を再提案していないか確認したいとき。
- 人間が oracle を編集し、AI が実装可能性を評価して realization を追従させる責務分担の背景を確認したいとき。
- cmoc のループ設計や作業支援設計で、事前計画、修正点リストアップ、実行結果の振り返り、kaizen、memory、暗黙仕様の扱いが論点になるとき。

## Do not read this when
- 採用済みコマンドの現在の入出力仕様、CLI の具体的挙動、実装手順、テスト仕様を確認したいとき。
- oracle file、realization file、INDEX、ログ、実行成果物の一般的な定義、配置、生成手順を確認したいとき。
- 個別の kaizen 文面、レビュー観点、改善提案の内容だけを設計しており、次回以降の実行コンテキストへの自動注入可否を扱わないとき。
- 作業計画立案フェーズや採用済み workflow の操作方法を実装するための詳細を探しているとき。

## hash
- 791a29b58819b2f1ee47fbe53448957a5f57f5ae77603021ab748952b6c6724c

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
