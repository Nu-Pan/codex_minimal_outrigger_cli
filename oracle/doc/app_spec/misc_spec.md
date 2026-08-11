
# cmoc の雑多な仕様

## oracle file と realization file の責務

oracle file は、人間が所有して全責任を負う正本仕様断片とする。agent は oracle file の作成、変更、調査、およびレビューを補助してよいが、realization file から正本仕様を逆算してはならない。

oracle file の下位概念は、次の責務で区別する。

- oracle doc は `{{work-root}}/oracle/doc` に置き、cmoc の要求、判断基準、および責務を自然言語で定義する意味仕様の正本とする。
- oracle src は `{{work-root}}/oracle/src` に置き、人間が所有する正確な実装定義と schema をプログラミング言語または設定形式で管理する。agent 向け文面の責務は `{{cmoc-root}}/oracle/doc/app_spec/prompt_standard.md` に従う。
- oracle test は `{{work-root}}/oracle/test` に置き、プログラミング言語で正本仕様を検査する。

realization file は、oracle file に記述された人間意図を具体化する成果物とする。realization file は AI が編集し、正本仕様を述べる場所にしてはならない。

realization file の下位概念は、次の責務で区別する。

- realization implementation は `{{work-root}}/src` に置き、product の実装と挙動を記述する設定を含む。
- realization test は `{{work-root}}/test` に置き、realization code の外部挙動または制御ロジックを検査する。
- realization ancillary は、実装と test 以外の補助的な realization file とする。

## oracle file を扱う判断基準

- 判断の根拠は関連する oracle file に置く。cmoc 固有契約または oracle file と installed skill が競合する場合は、前者を優先する。
- installed skill の存在または一般的なベストプラクティスだけを、oracle file の意味または作業完了条件の根拠にしてはならない。
- 実装差を許容しない事項と、人間が判断すべき境界を明示する。仕様の隙間を網羅的に埋めるためだけの分類、列挙、または新規 oracle file を追加してはならない。
- 明示仕様の隙間は、関連する oracle file と、アクセス可能な場合の既存実装および test から自然に導ける小さな範囲で実装者が補ってよい。過剰な実装を誘発し得る境界では goal と non-goal を読み取れるようにする。
- realization file の都合、過去の実装、または偶然の挙動だけから正本仕様を導いてはならない。実装上の制約は、仕様の矛盾または実現不能を調べる材料に限って使用してよい。
- 関連する正本仕様断片の整合性、一般方針と個別仕様の優先関係、用語、および検索性を保つ。依頼の対象外である既存仕様の意味を維持する。
- oracle file の作成または変更では、同じ概念の用語と表記を統一し、名前と定義を一致させる。文意または検索性を損なう誤字、脱字、および文法誤りを残さず、同じ意味の記述を重複させない。

## realization file を扱う判断基準

- 関連する oracle file を先に確認し、その明示要求と矛盾しない realization file にする。
- oracle src の定義または prompt 文面を realization file へ正本のように複製しない。同じ情報が必要な場合は、参照、生成、または意味を変えない変換によって正本を一箇所に保つ。
- 現行仕様に必要な implementation、test、設定、および ancillary だけを保つ。旧仕様の分岐、同じ責務の重複、および根拠のない公開面や抽象化を追加しない。
- 新しい実装は実在する責務境界または重複に対応させ、既存の近い責務を同時に整理する。簡潔化によって意味、可読性、失敗時挙動、または必要な検証を損なわない。
- 対象 repository が追跡する手順を配置場所にかかわらず特定し、必要な検証を行う。手順または実行環境が利用できない範囲を検証済みとして扱わない。

## oracle file に対する realization file の適合性

realization apply と realization refactor は、次の基準で追従要否と所見を判断する。

- oracle file の具体的な要求と realization file の具体的な挙動が明確に不整合な場合は、修正対象とする。
- realization file だけから実行不能または明白な致命的バグと説明できる場合は、修正対象とする。
- 修正対象は、根拠となる oracle file と realization file、または致命的な実装箇所を特定できなければならない。
- oracle file に記述がないこと、複数の妥当解、好み、推測、または一般的なベストプラクティスだけを根拠に修正対象を作らない。
- 調査開始時点ですでに解消されている問題を所見として扱わない。
- 修正後も関連する oracle file の明示要求を満たし、realization file の既存挙動を正本仕様へ逆流させない。

## oracle file と realization file の列挙方法

### 分類結果

「oracle file を列挙」または「realization file を列挙」と言った場合、`{{work-root}}` 配下の全 file を拡張子で制限せず glob し、本節の条件で分類した結果と完全に一致させる。
この full glob は結果の契約であり、検証済みの常時対象外 subtree まで物理的に traversal することは要求しない。

列挙上の常時対象外 root は、次の `{{work-root}}` 直下の exact path とする。

- `{{work-root}}/.git`
- `{{work-root}}/.agents`
- `{{work-root}}/.codex`
- `{{work-root}}/.cmoc`
- `{{work-root}}/memo`

各常時対象外 root 自身とその全 descendant は、oracle file と realization file のどちらにも分類しない。
root 直下の exact path だけを対象とし、nested の同名 path を名前だけで対象外にしてはならない。

nested Git working tree の `.git` path は、実際の repository metadata であると確認できた場合に限り、その path 自身と全 descendant を分類対象外とする。
nested Git working tree 本体の file は、repository metadata を除いて通常どおり分類する。

Git ignore 判定の意味は次のとおりとする。

- 候補 path の owning repository は、その path を含む最内側の検証済み Git working tree とする
- owning repository における通常の index-aware な `git check-ignore` と同値に判定する
- root と nested の `.gitignore`、repository-local exclude、および global exclude を有効な ignore source とする
- owning repository で untracked かつ ignore pattern に一致する regular file は分類対象外とする
- owning repository で tracked な regular file は、ignore pattern に一致していても分類対象に含める
- tracked path を ignore 判定へ含める `--no-index` 相当の意味を採用しない
- ignore pattern に一致しない untracked regular file は分類対象に含める

以上の対象外条件と Git ignore 判定を適用した regular file を、次の条件で分類する。

- `{{work-root}}/oracle` ツリー内にあり、ファイル名が `INDEX.md` と `AGENTS.md` のいずれでもない file を oracle file とする
- `{{work-root}}` ツリー内かつ `{{work-root}}/oracle` ツリー外にあり、ファイル名が `INDEX.md` と `AGENTS.md` のいずれでもない file を realization file とする

単純な `git ls-files` の結果だけを列挙結果として使用してはならない。

doctor preprocess と realization refactor の refactor state 同期は、この列挙結果を使用する。
列挙の最適化によって、entry 集合、対象 path の正規化、file 内容の SHA256、または `investigation_required` の意味を変更してはならない。

列挙順、repository context の検出手段、一括判定に使用する具体的な command または API、および call-local cache の内部構造は定義しない。

### traversal と事前 pruning

常時対象外 root は、descendant の traversal 前に pruning する。
nested の `.git` path は、実際の repository metadata であると確認できた場合だけ pruning 境界とする。

存在する root の pruning 境界と nested の `.git` path は、repository metadata の確認または descendant の traversal より前に `lstat` 相当で検証する。
境界の種類ごとの扱いは次のとおりとする。

- directory なら、その descendant を traversal しない
- regular file なら、その path だけを分類対象外とする
- symlink、FIFO、socket、device、またはその他の非通常ファイルなら、追跡も黙認もせず列挙をエラー終了する

regular file の扱いにより、linked worktree の `.git` metadata file を正常に処理できなければならない。
検証済みの pruned directory の descendant は、個別の列挙と非通常ファイル検証のどちらも行わない。

pruning されなかった領域では directory を traversal し、regular file を分類候補とする。
同領域の symlink は dereference せず、symlink 自身の path を owning repository における通常の index-aware な Git ignore 判定の対象とする。
symlink が untracked かつ ignored と確定した場合だけ、その path を分類対象外として列挙を継続する。
tracked、unignored、または ignore 状態を確定できない symlink は、列挙をエラー終了する。
symlink の参照先は `{{work-root}}` 内外のどちらにあっても、traversal、分類、または repository context の検出対象としない。
同領域の FIFO、socket、device、およびその他の非通常ファイルは、追跡せず列挙をエラー終了する。

directory が Git ignore 対象であることだけを理由に pruning してはならない。
`.venv` などの ignored directory も traversal し、その中で owning repository が tracked とする file を列挙結果に保持する。

### Git ignore 判定の性能不変条件

Git ignore 判定は、regular file の分類候補と pruning されなかった領域の symlink の各 path を、owning repository ごとに一括処理する。
判定は本書の分類結果が定める通常の index-aware な意味を維持し、次の性能不変条件を満たす。

- Git subprocess 数を候補 path 数に比例させない
- 同じ repository context と同じ ignore source の検証結果を、1 回の列挙内で再利用する
- repository context と ignore source が同じまま候補 path 数だけが増えた場合、symlink だけが増えた場合を含め、Git subprocess 数と ignore source の検証回数を増やさない
- nested repository ごとに異なる repository context と ignore source を適用する
- 検証結果の再利用は 1 回の列挙内に限定でき、doctor invocation 間の永続 cache を要求しない
- cache を doctor invocation 間で永続化する場合も、設定変更を見落として以前の検証結果を使用してはならない

repository ごとの `git check-ignore --stdin -z` は許容する実現方法の一例であり、必須の内部 API とはしない。

### 回帰検証

分類結果の回帰検証では、full glob による基準結果と最適化後の列挙結果を比較する。
fixture は少なくとも次の境界を扱う。

- exact root の pruning 対象へ descend せず、nested の同名 directory は名前だけで pruning しない
- pruning 境界の symlink、FIFO、socket、および device 相当を拒否する
- linked worktree の regular `.git` file を正常に扱う
- untracked かつ ignored な `.venv/bin/python` symlink を分類対象外として列挙を正常終了する
- ignored directory を traversal し、その中の tracked regular file を保持する
- tracked、unignored、または ignore 状態を確定できない symlink を拒否する
- symlink の参照先が `{{work-root}}` 内外のどちらにあっても、その参照先を traversal しない
- Git ignore に一致しない untracked file を保持する
- outer repository と nested repository に異なる ignore 規則を適用する
- root と nested の `.gitignore`、repository-local exclude、および global exclude を反映する
- regular file の列挙結果、対象 path の正規化、file 内容の SHA256、`investigation_required` の意味、および refactor state の entry 集合を full glob の基準結果と一致させ、symlink 対応による不要な変更を生じさせない

性能回帰は、次の回数を観測して検出する。

- Git subprocess の起動回数
- 一意な ignore source の検証回数
- pruning 対象への traversal 回数

候補 regular file または symlink のいずれかの件数だけを増やした fixture では、Git subprocess の起動回数と ignore source の検証回数が増えてはならない。
path 件数に依存する wall-clock time を自動テストの合否条件にしてはならない。

## `{{work-root}}` に対する仮定

`{{work-root}}` の定義は、`{{cmoc-root}}/oracle/src/oracle/other/path_model.py` の `AgentCallPathContext.work_root` を正本とする。
cmoc による操作対象 worktree である `{{work-root}}` は、次の要件を満たすものと仮定する。

- git で管理されている
- `{{work-root}}/oracle` 配下に断片的な正本情報が記載されている（`{{cmoc-root}}` 配下がそうであるように）
- `{{work-root}}` に固有の作業のノウハウは、Codex CLI が参照可能な追跡対象の文書、設定、script、または skill としてリポジトリ上に用意されている
    - 言い換えれば cmoc が無くても Codex CLI の直接利用でも作業を完遂出来るように `{{work-root}}` がメンテナンスされている事を仮定する
    - `{{work-root}}/oracle` 配下の file 別に `codex exec` session を起動する責任は cmoc が負う
    - 言語、framework、tool 固有の手順を用意する責任は `{{work-root}}` が負い、その配置先を `.agents/skills` に限定しない

## cmoc 実行時のカレントディレクトリ

- cmoc process は、対象 Git repository のいずれかの worktree root をカレントディレクトリとして実行する
- cmoc process の cwd と `AgentCallParameter.agent_call_cwd` は、異なる値を許容する
- cmoc process の cwd が `{{repo-root}}` であっても、run 用 `AgentCallParameter.agent_call_cwd` は `{{run-root}}` とする
- agent call の path context を、cmoc process の cwd だけから決定してはならない

## タイムスタンプのフォーマット

- タイムスタンプ `{{time-stamp}}` はフォーマット `{{year}}-{{month}}-{{day}}_{{hour}}-{{minute}}_{{sec}}_{{msec}}` に従うものとする
- year は 4 ケタゼロ埋めとする
- month/day/hour/minute/sec は 2 ケタゼロ埋めとする
- msec は 9 ケタとする
- timezone はそのマシンのローカルとする

## 「`{{cmoc-managed-branch}}` 上で～」の定義

「`{{cmoc-managed-branch}}` 上で～」といった時、それは以下の集合の和である

- `{{cmoc-managed-branch}}` 作成元 commit から `HEAD` までの間の commit 上で起きたこと
- working tree または staging area で起きていること

また、補足として、

- 削除済みファイルは対象から除外する
- rename は rename 後のパスを対象とする

例えば「`{{cmoc-session-branch}}` 上で変更のあった `{{repo-root}}/oracle` 配下のファイル」と言った時、それは、

- `{{cmoc-session}}` 作成元 commit から `HEAD` までの間の commit 上で変更のあった `{{repo-root}}/oracle` 配下のファイル
- working tree または staging area 上で変更のあった `{{repo-root}}/oracle` 配下のファイル

のことである。
