# `app_spec`

## Summary
- `app_spec` は cmoc の共通基盤と個別サブコマンドの正本仕様を束ねる入口です。ここでは、補完・ログ・エラー・プロンプト・隔離・実行環境・状態管理の共通断片と、`sub_command/` 配下の個別仕様へ読む先を振り分けます。
- 上位の共通断片は、特定サブコマンドの本文に入る前に前提をそろえるためのものです。`usage` や `sub_command` は利用フローと個別責務の案内であり、実装の詳細は各個別文書へ進みます。
- `external_model_provider.md` は本文が空で、この階層の routing 先としては使いません。実仕様が入った場合のみ対象になります。
- `sub_command/` は `apply` / `session` / `doctor` / `review` / `indexing` / `tui` などの個別コマンド仕様へ分岐する入口です。コマンド単位の実行条件、状態遷移、後処理を確認したいときにここから入ります。

## Read this when
- cmoc の共通前提として、補完・ログ・エラー処理・プロンプト生成・隔離実行・状態永続化のどれを読むべきか判断したいとき。
- `cmoc` 全体の利用手順を確認したいとき、または個別サブコマンドの前に読むべき共通仕様を探したいとき。
- `apply` / `session` / `doctor` / `review` / `indexing` / `tui` のいずれかの個別責務を確認したいときは、`sub_command/` 配下へ進む前提でここを読む。
- `cmoc managed ollama` の可用性、`codex exec` 呼び出し制約、補完時の副作用抑止、`Ctrl+C` 中断の共通規則を確認したいとき。

## Do not read this when
- 特定サブコマンドの入力条件・状態遷移・後始末をすでに知っているなら、この階層ではなく該当する個別文書を直接読む。
- `sub_command/` 配下の個別仕様を直接探しているなら、共通断片ではなくそのサブコマンドの文書へ進む。
- `external_model_provider.md` の本文が空のままなら、この文書単体から判断しようとしない。

## hash
- 59ba53da0cfd052a7b5cde840e88eea68cac528de187eb526db9f171ec85c2bd

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
