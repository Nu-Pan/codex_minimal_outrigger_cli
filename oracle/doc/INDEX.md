# `app_spec`

## Summary
- cmoc のアプリ仕様断片を集めた入口。CLI の実行条件、前処理、補完、ログ、エラー、状態、プロンプト基盤など、個別サブコマンドの挙動を決める前に読むべき正本をここから選ぶ。
- 個別機能の本文へ進むための案内であり、利用手順の全体像だけを知りたいときは上位の usage を先に読む。

## Read this when
- cmoc の挙動を仕様レベルで実装・変更するとき。
- 個別サブコマンドや共通基盤のどの正本を読むべきか判断したいとき。
- CLI の前処理、補完、エラー処理、ログ、状態管理、実行隔離、プロンプト規範のような横断的な仕様を確認したいとき。

## Do not read this when
- どのコマンドをどの順で使うかだけを知りたいときは usage を読む。
- すでに読むべき個別仕様が分かっているときは、この入口ではなく該当文書を直接読む。
- 実装ファイルやテストの詳細だけを追いたいときは、ここではなく realization 側を見る。

## hash
- 5cf8a7e83f5763faf9230f5d8f7eaaabca60cd76ba602a6f4805d15e51c6d2a7

# `branch_model.md`

## Summary
- cmoc が session と run の境界をどう切るかを定める。どの branch や worktree が誰の作業領域か、session fork/join と各サブコマンドの run fork/join を扱う文脈で読む。

## Read this when
- session の開始・終了で branch の生成や merge の扱いを決めたいとき
- apply や review などの run がどの branch と worktree を使うか確認したいとき
- cmoc 管理対象の branch 名や commit 名の責務境界を確認したいとき

## Do not read this when
- 個別サブコマンドの入出力や実行手順だけを知りたいとき
- branch 名や worktree 名の具体的な生成規則ではなく、内部実装の詳細を詰めたいとき
- cmoc 以外の通常の git 運用やリポジトリ本流の方針だけを確認したいとき

## hash
- e48fc3d9371ee9b4c447d06cdcb12a96f006afa581263ea87bd285118a7a60ed

# `considered_alternative`

## Summary
- `cmoc` の採用しなかった設計案と、その不採用理由を集めた文書群への入口。`apply` 系の進め方、事後検査の位置づけ、権限例外の扱い、永続記憶の可否、作業計画レビューの責務分担など、実装方針の分岐点を確認するときに読む。

## Read this when
- `cmoc` の実行フローや状態管理で、採用案ではなく却下案の背景を確認したいとき。
- `apply` の段取り、調査の並べ方、復旧方針、計画レビュー、記憶の引き継ぎ方など、設計判断の根拠を比較したいとき。
- 権限プロファイルや事後検査の扱いについて、なぜ別案を採らなかったかを確認したいとき。

## Do not read this when
- 現在採用している `cmoc` の具体的な CLI 手順、出力形式、保存先、テスト期待値だけを確認したいとき。
- 個別機能の実装手順や現行仕様そのものを探していて、不採用案の背景は不要なとき。
- `oracle` と `realization` の一般定義や記述標準だけを確認したいとき。

## hash
- cad9fc4f61a6f59d4a593a1ed5039859c760c986de217d8b353dbe12520073a0

# `dev_rule`

## Summary
- `coding_rule.md` は Python 実装全体の書き方を定める正本。命名、型ヒント、import、docstring、コメント、非公開識別子の扱いを確認したいときに読む。
- `design_rule.md` は cmoc の CLI 構成と共通モジュール配置の方針を定める。エントリーポイント、サブコマンド本体、`src/commons` に置く共有処理の境界を決めたいときに読む。
- `development_environment.md` はこのリポジトリを作業する環境条件と Python/venv の運用ルールを案内する。実行環境、仮想環境、依存追加、ファイル命名や UTF-8 BOM なしの制約を確認したいときに読む。
- `test_rule.md` は pytest を使う cmoc のテスト実装方針を案内する入口。決定論的な制御ロジックの検証、Real Codex CLI を含む経路での cmoc managed ollama 利用、Fake Codex CLI の位置づけを確認したいときに読む。

## Read this when
- Python の新規実装や修正を行うとき。
- 既存コードの命名、型ヒント、docstring、コメントの統一方針を確認したいとき。
- 循環参照の回避や相対 import の使い方を判断したいとき。
- `src/main.py` と各サブコマンド実装の責務分担を決めたいとき。
- サブコマンド間で共有する処理をどこに置くか判断したいとき。
- CLI の実装配置方針を確認したいとき。
- このリポジトリをローカルで開く前提条件や Codex CLI の実行環境を確認したいとき。
- Python 3.12.3 以上、仮想環境の場所、`pip` の実行方法など、開発時の環境運用ルールを確認したいとき。
- 新しい依存を `pyproject.toml` に追加して仮想環境へ入れる手順を確認したいとき。
- ファイル名の付け方や UTF-8 BOM なし運用の制約を確認したいとき。
- cmoc の決定論的な制御ロジックを pytest で検証したいとき。
- Real Codex CLI 呼び出しを含む経路で、prompt 渡し、出力保存、schema 指定、profile 生成など cmoc が責任を持つ結合動作を確認したいとき。
- テストの実行環境を `tmp_path` 配下に構築する必要があるとき。
- Real Codex CLI 呼び出しのテストで cmoc managed ollama を使うべきか、Fake Codex CLI で十分かを判断したいとき。

## Do not read this when
- このファイルの内容をそのまま実装に写すだけで足りるとき。
- 個別モジュールの業務ロジックや CLI 挙動を確認したいとき。
- 他言語の実装規約やプロジェクト固有の入出力仕様を調べたいとき。
- Python の文法、型ヒント、docstring、コメントの書き方を確認したいとき。
- テストの目的や配置方針を確認したいとき。
- CLI の挙動や出力内容そのものの正本仕様を確認したいとき。
- 個別の機能仕様、コマンド仕様、実装方針を知りたいとき。
- 既存の `INDEX.md` のルーティングだけを更新したいとき。
- README だけで足りる一般的な利用方法を知りたいとき。
- LLM の回答品質や Codex CLI に依頼した仕事の意味的な成功を検証したいだけのとき。
- Codex CLI 自体、外部 provider、有料クラウド backend の正しさや安定性を保証したいとき。
- テスト配置やライフサイクルの正本が cmoc managed ollama そのものにあると分かっているとき。

## hash
- 27140fd9b30f01a50314ec912654fb571d956951778e3596d606e86a1416efb2
