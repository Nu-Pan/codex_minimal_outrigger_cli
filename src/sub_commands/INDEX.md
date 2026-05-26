# `__init__.py`

## Summary

- `src/sub_commands/__init__.py` は `src.sub_commands` パッケージを宣言するだけの最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src.sub_commands` が Python パッケージとして宣言されていることを確認したいとき。
- `src/sub_commands` ディレクトリ全体の入口を把握したいとき。
- パッケージレベルのルーティング文書を作成・更新したいとき。

## Do not read this when

- 個別のサブコマンド実装や実行フローを確認したいときは、`src/sub_commands/init.py` などの具体的なモジュールを読む。
- `cmoc init`、`cmoc apply`、`cmoc eval-oracles`、`cmoc session join` などの挙動そのものを調べたいとき。
- `commons` 配下の共通処理やテスト仕様だけを確認したいとき。

## hash

- ea4df02b820eba1ca77dfb1b2227c81dbff61cd7c4c2bf4d26d891369b57fa77

# `apply.py`

## Summary

- `src/sub_commands/apply.py` は `cmoc apply` の本体で、session branch 上での前提検証、apply worktree の作成、oracle と実装の不整合調査、修正適用、commit、report 出力までをまとめています。
- Structured Output schema の定義と検証、調査用 prompt の生成、要修正点リストの整理・改善、実装のみから見つかった問題の取り扱いも含みます。
- INDEX.md 維持、編集禁止領域の検査、apply state の更新、終了コードの決定など、`cmoc apply` の周辺制御もこのモジュールに集約されています。

## Read this when

- `cmoc apply` の起動条件、前提検証、処理順、終了コード、report 出力を確認したいとき。
- oracle / 実装ファイルの調査対象選定、部分適用と全体適用の切り替え、要修正点リストの整理ロジックを追いたいとき。
- Structured Output schema、調査用 prompt、要修正点の検証、apply report の必須内容を変更したいとき。
- apply run における `.cmoc` の追跡対象外保証、INDEX.md の維持、編集禁止領域チェックを実装・修正したいとき。
- session state の `apply.state` 更新や、apply worktree / apply branch の作成・削除条件を確認したいとき。

## Do not read this when

- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` など、apply 以外のサブコマンド仕様だけを確認したいとき。
- `cmoc apply` の実装ではなく、`INDEX.md` の一般的な生成ルールや `oracles` 全体の扱いだけを確認したいとき。
- ユーザー向けの使い方全体や、具体的な操作手順の概要だけをざっくり把握したいとき。
- `cmoc apply` の中でも、調査・修正ループや report 生成ではなく、branch や session の運用仕様だけを見たいとき。

## hash

- 9a4021718e6b6b211d234857c7080531c6c626eb114c061d5808f81047bf11dd

# `eval-oracles.py`

## Summary

- `cmoc eval-oracles` の実装本体で、`--full` とブランチ状態に応じた部分評価・全体評価の切り替え、oracle ファイル列挙、Codex CLI による評価実行、レポート保存までをまとめている。
- Structured Output schema の検証、評価用 prompt の組み立て、問題点集約、Markdown レポート生成の処理も含む。
- `.cmoc` の ignore 保証や INDEX.md メンテナンスなど、評価前後の周辺処理も扱う。

## Read this when

- `cmoc eval-oracles` の実装フローや `--full` の扱いを確認したいとき。
- 評価対象 oracle の選択、部分評価と全体評価の分岐、deleted oracle 検知の条件を確認したいとき。
- Codex CLI に渡す評価プロンプト、Structured Output schema、レポート生成の仕様を確認したいとき。
- `cmoc eval-oracles` の失敗時レポートや出力先 `.cmoc/reports/eval-oracles` の挙動を確認したいとき。

## Do not read this when

- `cmoc apply`、`cmoc init`、`cmoc session fork`、`cmoc session join` など、`cmoc eval-oracles` 以外のサブコマンド実装を調べたいとき。
- `oracles` 配下の個別仕様断片そのものを読みたいときは、この実装ファイルではなく対応する oracle 文書を読むべきとき。
- コマンドの設計ルール、評価基準、開発環境ルールだけを確認したいとき。
- 純粋なテスト実装や別モジュールの共通処理を追いたいとき。

## hash

- 8dbd4e4386d66f709cb2524ea2100c941f9589fc671a717f70adb1be1447879c

# `init.py`

## Summary

- `cmoc init` の本体処理を実装している。
- 直接呼び出し時は共通 runner に委譲し、`.cmoc` の ignore 保証と初期化差分の commit を 2 ステップで進める。
- 処理結果として `committed initialization changes` または `no initialization changes` を表示し、最後に処理時間を報告する。

## Read this when

- `cmoc init` の実際の処理順や、`repo_root` 未指定時の共通 runner 委譲を確認したいとき。
- `.cmoc` を git 追跡対象外にする保証処理と、初期化差分の commit 判定の実装を確認したいとき。
- 実行結果メッセージと timing report の出力条件を確認したいとき。

## Do not read this when

- `cmoc init` の仕様そのものではなく、他のサブコマンドの実装を確認したいとき。
- `.cmoc` の ignore 判定や tracked 解除の詳細ルールだけを仕様書側で確認したいとき。
- `cmoc session fork` / `cmoc session join` / `cmoc apply` / `cmoc eval-oracles` など、別コマンドの処理を見たいとき。

## hash

- 766eb4ef5567a176766be2bb55dbc8f955c55af92c1ddc3f64043c1be4bda4ee

# `session_abandon.py`

## Summary

- `src/sub_commands/session_abandon.py` は `cmoc session abandon` の本体処理を実装するモジュールです。
- 現在 checkout している session branch を検証し、session state と apply state を確認したうえで、home branch へ切り替えて session を abandoned として記録し、session branch を削除します。
- 直接呼び出し時の共通 runner 委譲、`.cmoc` の非追跡保証、cleanup 失敗時の復元処理も含みます。

## Read this when

- `cmoc session abandon` の実装・修正・レビューを行いたいとき。
- 現在の session branch を merge せずに破棄する前提条件、state 検証、`git switch`、`git branch -D` の流れを確認したいとき。
- cleanup 失敗時の state 復元や、session branch / session state の整合性確認を追いたいとき。

## Do not read this when

- `cmoc session join` や `cmoc session fork` など、他の session サブコマンドの挙動だけを確認したいとき。
- `cmoc apply abandon` を含む apply 側の破棄手順だけを確認したいとき。
- `src/commons` の共通基盤や `INDEX.md` 生成ロジックだけを確認したいとき。

## hash

- e76c36a188ae7ebd5d36f7f92b74c8061219f8f98d8f6352dc0fb764abb50db1

# `session_fork.py`

## Summary

- `cmoc session fork` の実装本体で、現在 checkout している local branch を session home branch として session branch を作成し、session state を保存します。
- detached HEAD、remote-tracking branch、commit hash、cmoc 管理 branch、未コミット差分、既存 active session などの事前条件チェックを行います。
- `.cmoc` の追跡対象外保証、session branch 作成の最大 10 回リトライ、作成結果と home branch の標準出力表示までを扱います。

## Read this when

- cmoc session fork の挙動やエラー条件を実装・修正・レビューしたいとき。
- session home branch の決め方、session branch の命名規則、session state の初期保存処理を確認したいとき。
- detached HEAD や remote-tracking branch からの起動、未コミット差分、既存 active session の扱いを追いたいとき。
- `.cmoc` の ignore 保証や、session branch 作成失敗時の再試行ロジックを確認したいとき。

## Do not read this when

- cmoc session join、cmoc session abandon、cmoc apply など別サブコマンドの流れだけを確認したいとき。
- cmoc 全体の branch model の概要だけを確認したいときは、`oracles/app_specs/branch_model.md` を読むべきです。
- session state のスキーマや初期値だけを確認したいときは、`oracles/app_specs/session_state.md` を直接読むべきです。
- 実装コードではなく、`cmoc session fork` の正本仕様断片だけを確認したいとき。

## hash

- 79cffa7ff3de334560cef693809731381cea09af27d8772c2f144bfa632c01b0

# `session_join.py`

## Summary

- `src/sub_commands/session_join.py` は `cmoc session join` の実装本体で、現在の session branch を session state に記録された home branch へ `git merge --no-ff` する処理をまとめています。
- 現在 branch、session state、apply state、home branch、未コミット差分などの前提条件を検証し、home branch へ switch してから merge します。
- merge 失敗時は Codex CLI に conflict marker の解消を依頼し、成功後は session state を joined に更新し、安全なら session branch を削除します。

## Read this when

- `cmoc session join` の実行条件、session state の検証、標準出力・エラー出力の挙動を確認したいとき。
- `git switch` から `git merge --no-ff`、conflict 解消、merge commit 作成、session branch 削除までの流れを追いたいとき。
- merge 開始後に手動解消が必要になった場合の案内文や、conflict 対応の実装を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc apply`、`cmoc eval-oracles` など、他サブコマンドの実装や手順だけを確認したいとき。
- `src/commons` の共通基盤や `INDEX.md` 生成ロジックだけを確認したいとき。
- `cmoc session fork` の開始処理や session 管理の別フェーズだけを確認したいとき。

## hash

- 14595336ef117e01c9897b727971c2fc3f77a5571bce4576ea8e3a53faf47177
