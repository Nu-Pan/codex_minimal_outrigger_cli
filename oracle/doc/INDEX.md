# `app_spec`

## Summary
- cmoc の app_spec 群をまとめる入口。サブコマンド全体の使い方、事前検証、実行分離、セッションや apply の状態管理、補完、エラー、ログ、中断など、利用者向け挙動の正本断片を探すときにここから入る。
- 個別機能の仕様を読む前に、どの下位文書へ進むべきかを判断するためのルーティング層。全体像を知りたい場合はこの階層を起点にし、詳細は各テーマ別の文書へ進む。

## Read this when
- cmoc の利用手順全体や、どの機能仕様を先に読むべきかを判断したいとき。
- CLI の起動前検証、サブコマンド実行、セッション状態、apply 状態、補完、ログ、エラー、中断のいずれかを仕様として確認したいとき。
- 個別文書の責務境界を見て、該当する正本断片へ直接進みたいとき。

## Do not read this when
- 特定の機能の詳細だけを知りたいなら、この階層ではなく該当テーマの下位文書を直接読む。
- 実装の細部やコードの変更点だけを追いたいなら、先に対象実装へ進む。
- 利用手順の全体像ではなく、単一サブコマンドの入力や出力だけを確認したいとき。

## hash
- adc758507a6715b0a08a18eb7b9c399a398b0297081282041b3e39edfee2d87d

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
- `coding_rule.md`: Python 実装全体の書き方の正本。命名、型ヒント、import、docstring、コメント、非公開識別子の扱いを確認するときに読む。
- `design_rule.md`: cmoc の CLI 構成と共有モジュール配置の方針。エントリーポイント、サブコマンド本体、共有処理の置き場を決めるときに読む。
- `development_environment.md`: この環境で作業するときの前提と開発手順の入口。環境確認、命名基準、自己開発用の検証手順を探すときに読む。
- `test_rule.md`: 自己開発時の検証手順と cmoc managed Ollama の管理・配置・設定注入の入口。テスト実装や検証方針を決めるときに読む.

## Read this when
- Python の書き方や命名規約を確認したいときは `coding_rule.md` を読む。
- CLI の責務分担や共有処理の配置方針を決めたいときは `design_rule.md` を読む。
- 開発環境の前提や自己開発の検証手順を確認したいときは `development_environment.md` を読む。
- テスト実装、検証手順、managed Ollama の扱いを確認したいときは `test_rule.md` を読む.

## Do not read this when
- Python の書き方だけを知りたいときに `design_rule.md` や `test_rule.md` を読む必要はない。
- CLI の実装配置や共有処理の置き場だけを判断したいときに `coding_rule.md` を読む必要はない。
- 個別機能の正本仕様や業務ロジックを探したいときは、これらの案内文書ではなく該当する仕様断片を読む。
- 既に目的の手順や規約を把握していて、別の具体的な本文だけが必要なときは、この階層の案内を再読しない。

## hash
- 50b3bbc7816dd04b966a375da7a31b984231ef2f62b1d2ecba3a6defbe9dcb2a
