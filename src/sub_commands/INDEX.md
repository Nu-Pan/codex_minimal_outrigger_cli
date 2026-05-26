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

- `cmoc apply` の本体処理をまとめた実装ファイルです。
- session state の検証、apply worktree の作成、oracle スナップショットの固定、調査・修正ループ、report 保存までを扱います。
- 要修正点リストの Structured Output schema、調査対象ファイルの選定、Codex CLI への調査・修正依頼、commit 作成、レポート整形の処理が含まれます。

## Read this when

- `cmoc apply` の本体処理、状態遷移、worktree 作成、レポート生成を実装・修正・レビューしたいとき。
- `apply.state` の `ready` / `running` / `completed` / `error` の扱いと、session state の更新条件を確認したいとき。
- oracle ファイルと実装ファイルを対象にした不整合調査、要修正点リストの Structured Output、改善ループの仕様を確認したいとき。
- `--full` と部分適用モードの対象ファイル選定、禁止パス検査、commit 単位の追従処理を確認したいとき。

## Do not read this when

- `cmoc apply abandon` の破棄手順だけを確認したいときは、このファイルではなく `src/sub_commands/apply_abandon.py` を読むべきです。
- `cmoc apply join` のマージ手順や後始末だけを確認したいときは、このファイルではなく `src/sub_commands/apply_join.py` を読むべきです。
- `cmoc session fork` / `cmoc session join` / `cmoc session abandon` の挙動だけを確認したいときは、このファイルは対象外です。
- 不整合調査ではなく、共通の `INDEX.md` 生成ルールや `oracles` 全体の扱いだけを確認したいときは、このファイルを読む必要はありません。

## hash

- 593121872b2169893602b5847823d6f971f764b082a577f7e5302ddf607eb0eb

# `apply_abandon.py`

## Summary

- `src/sub_commands/apply_abandon.py` は `cmoc apply abandon` の本体処理を定義するモジュールです。
- 現在の branch と session state を検証し、未 join の apply run に対応する apply branch と apply worktree を強制削除します。
- 破棄後は `session.state` の `apply.state` を `ready` に戻し、必要な warning と timing を標準出力へ出します。

## Read this when

- `cmoc apply abandon` の本体実装、事前条件、cleanup 手順を確認したいとき。
- 現在の session に紐づく未 join の apply run を破棄する処理や、`apply.state` を `ready` に戻す流れを追いたいとき。
- apply branch と apply worktree の削除条件、warning の出し方、状態復元の挙動を実装・修正・レビューしたいとき。
- `_cmoc_root` や session state の読み書き、apply abandon の出力内容と timing report を確認したいとき。

## Do not read this when

- `cmoc apply fork` の要修正点整理や調査フローだけを確認したいとき。
- `cmoc apply join` の merge 処理や後始末だけを確認したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` など、apply 以外のサブコマンドを確認したいとき。
- `cmoc apply abandon` の仕様本文だけを見たいときは、実装ではなく `oracles/app_specs/sub_commands/apply_abandon.md` を読むべきです。

## hash

- f281e41a0379d679b803e6f9de24858ea2e0481bd210a02b9ea043cc3b1d1d5f

# `apply_join.py`

## Summary

- `cmoc apply join` の本体処理を定義する Python モジュールです。
- 完了済みの apply branch を session branch へ `git merge --no-ff` し、その後の state 更新と後始末までを扱います。
- 直接呼び出し時の共通 runner 委譲、想定外の差分検出、`--force-resolve` による強制解決、merge conflict 時の報告を実装しています。

## Read this when

- `cmoc apply join` の実装・修正・レビューを行いたいとき。
- `<cmoc-apply-branch>` を `<cmoc-session-branch>` に取り込む前提条件、実行順序、状態更新の流れを確認したいとき。
- 想定外の差分の検出、通常モードと `--force-resolve` の分岐、merge conflict 時のエラー処理を追いたいとき。
- merge 後の `apply.state` の更新や、apply branch / apply worktree の削除条件を確認したいとき。

## Do not read this when

- `cmoc apply fork` の要修正点抽出や調査・修正ループだけを確認したいときは、このモジュールではなく `src/sub_commands/apply.py` や対応する正本仕様を読むべきです。
- `cmoc session join` / `cmoc session abandon` など、session 側の開始・終了・破棄だけを確認したいときは、このモジュールは適しません。
- 一般的な `git merge` の解説だけで足りるときや、`INDEX.md` の生成ルールそのものだけを確認したいときは、この実装ファイルを読む必要はありません。

## hash

- 7c04012e7755967e6fa8bfcbf9abfd130391b5e7dad6f7b0fb10bd06314df94d

# `eval-oracles.py`

## Summary

- `cmoc eval-oracles` コマンド本体の実装をまとめた Python モジュールです。
- `oracles` 配下の評価対象を列挙し、現在ブランチと `--full` に応じて部分評価または全体評価を選びます。
- 評価前に `.cmoc` の ignore 保証と `INDEX.md` のメンテナンスを行い、`codex exec` で各 oracle を個別に評価します。
- 各評価結果の Structured Output を検証し、最終的に Markdown レポートまたはエラーレポートを `.cmoc/reports/eval-oracles` に保存します。
- レポート生成、issue 集約、番号付け、参照ファイル一覧化、失敗時の代替レポート作成までを含む、`cmoc eval-oracles` の中核処理です。

## Read this when

- `cmoc eval-oracles` の実装・修正・テスト・レビューを行いたいとき。
- 部分評価・全体評価の切り替え条件、`--full` の扱い、現在ブランチ判定、セッション開始コミット参照の流れを確認したいとき。
- 評価前に `.cmoc` の非追跡保証を行う処理や、`INDEX.md` を先にメンテナンスする順序を確認したいとき。
- oracle ファイルの列挙、変更差分による部分評価の絞り込み、`codex exec` に渡す評価プロンプトと Structured Output 検証の実装を見たいとき。
- 評価結果の Markdown レポート生成、エラーレポート生成、集計結果の出力や保存先を確認したいとき。
- 評価に使う補助関数や、JSON パース・バリデーション・レポート書式の内部仕様を確認したいとき。

## Do not read this when

- `cmoc apply`、`cmoc session`、`cmoc init` など他のサブコマンドの実装だけを確認したいとき。
- `cmoc eval-oracles` の仕様本文やルーティングだけを確認したいときは、`oracles/app_specs/sub_commands/eval_oracles.md` を読むべきで、この実装ファイルを読む必要はありません。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、このファイルではなく `oracles/app_specs/indexing.md` を読むべきです。
- `cmoc` の共通仕様や `oracles` 全体の入口だけを確認したいときは、この実装ファイルではなく各 `INDEX.md` を読むべきです。

## hash

- 97b1f78d613417748f0aec0d08c887ff3ced9c3d6738b316eff9e858aafd7726

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

- `cmoc session abandon` は、現在の `<cmoc-session-branch>` を merge せずに破棄するための仕様です。
- session を完了させる `cmoc session join` とは異なり、成果物を本流に取り込まず、`session.joined_at` を更新しないまま branch を削除します。
- 実行条件、破棄してよいもの・してはいけないもの、実行手順、`session.state` の遷移をまとめています。

## Read this when

- 現在の `<cmoc-session-branch>` を `<cmoc-session-home-branch>` に merge せず破棄したいとき。
- `session.state`、`apply.state`、未コミット差分、home branch の存在など、破棄前の前提条件を確認したいとき。
- `cmoc session abandon` の実装、修正、テスト、レビューを行いたいとき。

## Do not read this when

- `cmoc session fork` の開始条件や session branch 作成手順だけを確認したいとき。
- `cmoc session join` の merge 完了手順や conflict 解消の流れだけを確認したいとき。
- `cmoc apply abandon` など、apply run の破棄仕様だけを確認したいとき。

## hash

- 72cdd1b905f55411908bf6de1f27d57c0c9589833089fb2185e38e184b78206a

# `session_fork.py`

## Summary

- `src/sub_commands/session_fork.py` は `cmoc session fork` の実装本体です。
- 現在 checkout している local branch を session home branch として、その HEAD から session branch を作成し、session state を保存します。
- 事前条件チェック、`.cmoc` の ignore 保証、session branch 作成のリトライ、作成結果と home branch の標準出力表示までを扱います。

## Read this when

- `cmoc session fork` の実装・修正・レビューを行いたいとき。
- 新しい session branch の作成条件や checkout 手順を確認したいとき。
- session home branch の決め方、session metadata の保存先、ブランチ命名規則を確認したいとき。
- detached HEAD、remote-tracking branch、未コミット差分、既存 active session、`cmoc` 管理 branch の扱いを確認したいとき。
- .cmoc の追跡対象外保証や、session branch 作成失敗時の最大 10 回リトライ処理を確認したいとき。

## Do not read this when

- `cmoc session join`、`cmoc session abandon`、`cmoc apply` など、別サブコマンドの挙動だけを確認したいとき。
- `cmoc` 全体の branch model の概要だけを確認したいとき。
- session state のスキーマや初期値だけを確認したいとき。
- 実装コードではなく、`cmoc session fork` の正本仕様断片だけを確認したいとき。

## hash

- 4f3b2291933f066fdb59a552059dbea15716aa00a0e66e4a7bef8bea08a52a2b

# `session_join.py`

## Summary

- `src/sub_commands/session_join.py` は `cmoc session join` の本体実装です。
- 現在の session branch を session state に記録された home branch に `git merge --no-ff` し、`session.state` を `joined` に更新して、必要なら session branch を削除します。
- 事前条件検証、`.cmoc` の非追跡保証、`git switch`、merge conflict 時の Codex CLI 依頼、手動解消案内、unmerged path / conflict marker の検査も含みます。

## Read this when

- `cmoc session join` の実装・修正・レビューで、事前条件と実行順を確認したいとき。
- session branch / home branch の特定、`session.state` と `apply.state` の検証、`git show-ref` による local branch 存在確認を追いたいとき。
- merge conflict 発生時の prompt 生成、Codex CLI への解消依頼、`git add` / `git commit` 禁止、merge commit 作成までの流れを確認したいとき。
- `git branch -d` による削除可否判定や、削除できなかった場合の warning 出力を確認したいとき。
- 手動解消が必要になったときに stderr へ出る案内文や、`.cmoc` 編集禁止の扱いを見たいとき。

## Do not read this when

- `cmoc session fork` や `cmoc session abandon` の開始・破棄フローだけを確認したいとき。
- `cmoc apply` 系の要修正点整理や apply branch/worktree の運用だけを確認したいとき。
- `cmoc init` や `cmoc eval-oracles` など、別サブコマンドの実装だけを見たいとき。
- `cmoc session join` の正本仕様そのものを確認したいときは、実装ではなく `oracles/app_specs/sub_commands/session_join.md` を読むべきです。

## hash

- bcdefe8883ac556357fbedc04f396dc14831026057c83c0ed3d70c5d0a5c2782
