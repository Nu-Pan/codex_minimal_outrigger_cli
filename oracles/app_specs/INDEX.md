# `branch_model.md`

## Summary

- `cmoc` における session branch と apply branch の役割分担、および通常 branch との関係をまとめた文書です。
- session 開始時に checkout 中の local branch を session home branch として扱い、session branch は `cmoc/session/<session-id>`、apply branch は `cmoc/apply/<session-id>/<apply-run-id>` という命名規則を定めます。
- default branch を特別扱いしないこと、1 つの session home branch に対して active な session branch は高々 1 つであること、apply は開始時点の oracle snapshot commit を基準に進めることを示します。

## Read this when

- `cmoc session fork` の分岐元や最終的な merge 先をどう扱うか確認したいとき。
- session branch と apply branch の命名規則、用途、ユーザーが編集してよい branch を確認したいとき。
- apply 実行中にどの HEAD を snapshot として固定し、どの変更を取り込まないかを確認したいとき。

## Do not read this when

- branch 以外の共通規約や実装ルールを確認したいときは、`dev_rules` や他の仕様文書を読むべきです。
- 個別サブコマンドの引数や手順だけを確認したいときは、該当するサブコマンド仕様を直接参照すべきです。
- `INDEX.md` の生成や更新ルールだけを確認したいときは、この文書ではなく `indexing.md` を読むべきです。

## hash

- dd1f141e83ae328b95305aa6ab8e08f5431af4188a4d0d5d4ba130b1fb51148d

# `codex_call.md`

## Summary

- `cmoc` から `codex exec` を呼び出すための共通規約をまとめた文書です。
- stdin でプロンプト本文を渡す方法、プロンプトの構成要件、アクセス制限の書き方、モデル指定と出力方法、失敗時の扱いまでを扱います。

## Read this when

- cmoc から `codex exec` を呼び出す方法や、stdin 経由でのプロンプト送信ルールを実装・修正・レビューしたいとき。
- プロンプトの構成、argv に載せてよい情報の制約、`--output-schema` や `--output-last-message` を含む出力規約を確認したいとき。
- sandbox の read-only / workspace-write の選択基準、Model / Reasoning Effort の指定方針、quota 不足時の待機・再開手順を確認したいとき。

## Do not read this when

- `codex exec` 以外の実行手段や、一般的なシェル呼び出し方針だけを確認したいとき。
- `INDEX.md` の生成・更新ルールや、他の仕様ファイルのルーティングだけを確認したいとき。
- この文書の対象外である、他のサブコマンド固有の手順や状態遷移だけを確認したいとき。

## hash

- 87b6e64fd0d0d82f9c0b062206da7ada02803b320ccd8a5468e935dbaabbb9cf

# `console_and_file_log.md`

## Summary

- サブコマンド呼び出しごとのコンソール・ファイル両方への tee 出力、ログ保存先、追跡可能性の要件を定めている。
- ステップ開始通知、Codex CLI 呼び出し通知、経過時間、戻り値、途中経過と作業完了レポートの見分け方を扱う。
- 標準出力に流す時間表示フォーマットを定義している。

## Read this when

- サブコマンド実行時の標準出力とログファイルの出し分け、または tee の実装を確認したいとき。
- `.cmoc/logs/sub_commands/<time-stamp>.log` への保存や、過去の実行を辿れるログ構造を設計・修正したいとき。
- ステップ開始通知や Codex CLI 呼び出し通知、経過時間表示、完了報告の表示形式を実装・調整したいとき。
- 時間表示を `<hour>h <minute>m <sec>.<msec>s` 形式に揃える必要があるとき。

## Do not read this when

- 特定のサブコマンドの引数、状態遷移、業務ロジックだけを確認したいとき。
- branch model、session/apply の手順、エラー処理など、出力規則以外の仕様を調べたいとき。
- README や AGENTS などのリポジトリ運用ルールだけを確認したいとき。

## hash

- 87802561acbe4b063a58543c94ec190bcbebf3ff78dd8ee015a51e071ab05a1b

# `error_handling.md`

## Summary

- cmoc 全体に適用される一般的なエラーハンドリング規則をまとめた参照先。特別な仕様がない限り、処理を中断し、エラーレポートを stdout に出し、エラー終了ステータスコードを返す。特別な記載がある場合はその指示を優先する。

## Read this when

- 処理を中断してエラーとして扱うべきかを判断したい場合
- エラーレポートとして stdout に何を出すかを確認したい場合
- エラー終了時のステータスコードや、特別な記載がある仕様との優先関係を確認したい場合

## Do not read this when

- 各サブコマンドや個別機能の仕様に、独自のエラー処理が明記されている場合
- 通常の成功系フローや出力仕様だけを確認したい場合
- エラーハンドリング以外の設計規則や実装ルールを調べたい場合

## hash

- bfaceea1701755cbe1f24db75ea9044ad4d4ed7dc98edef844bc94e39c3bbdf8

# `indexing.md`

## Summary

- `cmoc` が `<repo-root>` 配下に `INDEX.md` を自動配置・自動更新するための仕様をまとめた文書です。
- 配置対象ディレクトリと、目次作成対象から除外するファイル・ディレクトリの判定ルールを定義しています。
- `INDEX.md` の各目次項目に必要な見出し構成、説明の書き方、参照ハッシュの扱いを定めています。
- 目次情報の生成方法として、Structured Output の JSON スキーマと `codex exec` の使い方を指定しています。
- `INDEX.md` メンテナンスの実行タイミング、処理順序、既存差分の扱い、自動コミット条件を定義しています。

## Read this when

- `<repo-root>` 配下に `INDEX.md` をどこへ配置するか、どのディレクトリを対象にするかを決めたいとき。
- `INDEX.md` に載せるファイル・ディレクトリの選別ルールや除外条件を確認したいとき。
- `INDEX.md` の Summary / Read this when / Do not read this when / hash の記法や生成方法を実装・更新したいとき。
- `INDEX.md` の再生成、差分更新、自動コミット、メンテナンス実行タイミングを実装・レビューしたいとき。

## Do not read this when

- `INDEX.md` の生成・更新ルールそのものではなく、個別のサブコマンド仕様や実装コードを確認したいとき。
- `oracles` 配下の他の仕様断片だけで用が足り、`INDEX.md` のメンテナンス規則を扱わないとき。
- リポジトリの一般的なアプリ機能や業務ロジックを確認していて、`INDEX.md` の配置・検証・再生成に関与しないとき。

## hash

- a6e6af330d3ce5e851bfd29cd85909bf3af4d01cbbb502863e7eedf5a165a175

# `misc_specs.md`

## Summary

- `cmoc` 全体に共通する雑多な基礎仕様をまとめたファイルです。
- 実装ファイルの列挙ルール、`<repo-root>` 探索とカレントディレクトリ変更、`<repo-root>/.cmoc` の扱いを定義します。
- タイムスタンプ形式と、`<cmoc-managed-branch>` 上で何を指すかの定義も含みます。

## Read this when

- `<repo-root>` 配下の実装ファイルを機械的に列挙するルールを確認したいとき
- `<repo-root>` の探索方法や、`<repo-root>/oracles`・`.gitignore`・`.git`・`INDEX.md` の扱いを確認したいとき
- `<repo-root>` を git 管理リポジトリとしてどう仮定するか、また `cmoc` 実行時のカレントディレクトリの扱いを確認したいとき
- `<repo-root>/.cmoc` の追跡対象外ルールや、タイムスタンプ形式、`<cmoc-managed-branch>` の定義を確認したいとき

## Do not read this when

- `cmoc` の具体的なサブコマンドの手順や入出力仕様を探しているとき
- `apply` / `eval-oracles` / `session-fork` など個別機能の詳細仕様を探しているとき
- リポジトリ固有の実装方針やドメイン知識を確認したいとき

## hash

- 396555d1a18571100a3731b268271af191e67faa57b86ac4f1e9e107be9e1f1b

# `oracles.md`

## Summary

- `oracles ファイル` の定義、役割、自動処理上の扱いをまとめた入口です。
- `<repo-root>/oracles` 配下の非 `INDEX.md` ファイルが対象であり、AI は提案できても編集は人間が行う前提を示します。
- Codex CLI が読み書きしてよい範囲と、workspace-write 後に差分がないことを機械的に検査する規則を確認できます。

## Read this when

- `oracles ファイル` の定義を確認したいとき。
- `oracles ファイル` を人間が所有し、AI が編集しない前提を確認したいとき。
- `oracles` 配下のファイルに対する読み書き可否や自動処理規則を確認したいとき。

## Do not read this when

- `INDEX.md` の作成手順やメンテナンス規則だけを確認したいとき。
- `cmoc` のサブコマンド仕様や実装方針を確認したいとき。
- `oracles` 配下の個別仕様ファイルそのものを編集したいとき。

## hash

- 6ca91e5371d86a6fa925f5b9af6d2d3a2407cb43bd76910f1cb9bdc6cf0d4545

# `session_state.md`

## Summary

- `cmoc` ワークフローで発生する fork/join の状態を、セッションごとの JSON ファイルとして永続化するための仕様です。
- `session` と `apply` の 2 つの領域に分けて状態を保持し、初期値と `ready` 遷移時の初期化方針を定めています。
- 保存先は `<repo-root>/.cmoc/sessions/<session-id>.json` です。

## Read this when

- `cmoc` の fork/join に伴うセッション状態をどこにどう永続化するか確認したいとき。
- `<repo-root>/.cmoc/sessions/<session-id>.json` に保存する状態項目や初期値、遷移条件を確認したいとき。
- `session` と `apply` の状態管理を実装・レビューするときに、保持すべき情報を整理したいとき。

## Do not read this when

- `cmoc session` や `cmoc apply` の操作手順そのものだけを確認したいとき。
- `oracles` 全体のルーティング方針や `INDEX.md` 生成ルールだけを確認したいとき。
- このファイルの保存先や永続化スキーマではなく、実装コードやテストコードだけで足りるとき。

## hash

- 555300a24f708c758456656f0bd1fabe6efa1598b83e12a9d5c0453493cd21b6

# `sub_commands`

## Summary

- `cmoc` の個別サブコマンド仕様への入口です。
- `apply`、`session`、`eval-oracles`、`init` の各手順を下位文書へ案内します。
- このディレクトリを起点に、サブコマンドごとの前提条件や状態遷移を素早く辿れるようにします。

## Read this when

- `cmoc` の個別サブコマンドの入口をまとめて確認したいとき。
- `apply`、`session`、`eval-oracles`、`init` のどの仕様断片へ進むべきか整理したいとき。
- `cmoc` のサブコマンドごとの目的、入力条件、実行手順、終了条件を俯瞰したいとき。

## Do not read this when

- 個別のサブコマンド仕様だけを確認したいときは、この INDEX ではなく該当する `apply_*`、`session_*`、`eval_oracles.md`、`init.md` を直接読むべきです。
- 実装コードやテストコードだけで足りる作業では、このディレクトリの案内を読む必要はありません。
- `branch_model`、`codex_call`、ログ、エラーハンドリング、`oracles` 全体の扱いなど、他の共通仕様を確認したいときは、この INDEX ではなく対応する入口文書を読むべきです。

## hash

- 373b169f7013d4e4f5f0a1efe0478f539a29253959ff4851955209161500a566

# `usage.md`

## Summary

- `cmoc` の利用方法をまとめた文書です。
- `cmoc` コマンドの呼び出し前提、初回の `cmoc init`、想定ワークフローを扱います。
- セッション作成から `apply`、`join` までの基本的な操作順を確認するための入口です。

## Read this when

- `cmoc` の基本的な使い方や、最初に何を実行するかを確認したいとき。
- `cmoc init` から `session fork`、`apply fork`、`apply join`、`session join` までの全体の流れを確認したいとき。
- エンドユーザーが `cmoc` を呼び出す前提や、標準的な作業順序を把握したいとき。

## Do not read this when

- 個別サブコマンドの引数、出力形式、内部手順だけを確認したいときは、`sub_commands/INDEX.md` から該当文書へ直接進むべきです。
- 実装コードやテストコードの作業だけで足りるときは、この利用方法の案内を読む必要はありません。
- `cmoc` の共通規約や設計方針だけを確認したいときは、`app_specs/INDEX.md` 配下の別文書を参照すべきです。

## hash

- 8b19f52b9c8b57989c5eb50f80342410ee3e6b38732410730612640b55b7d5bd
