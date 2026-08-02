# `file_access_rule.py`

## Summary
- ファイルアクセスモードに応じた、AI エージェント向けの読み書き禁止規則を構築する。リポジトリ外、管理対象ディレクトリ、AGENTS.md・INDEX.md・memo、oracle file・realization file などのアクセス制約をモード別に組み立てる。
- ファイルアクセス規則の文面とプレースホルダー定義を生成する責務を持つ。アクセス権限の実行環境設定そのものではなく、プロンプトに使用する規則文面の入口である。

## Read this when
- AI エージェントのファイル読み書き規則を変更・確認するとき
- FileAccessMode ごとの oracle file・realization file のアクセス制約や、パスプレースホルダーの生成を調べるとき
- リポジトリ外アクセスや .git・.agents・.codex・.cmoc・memo への制約文面を調べるとき

## Do not read this when
- 特定のサブコマンドや機能の実装責務を調べるとき
- Codex CLI の sandbox 設定や実行権限の正本仕様を調べるときは、対応する oracle 文書を先に確認する
- INDEX.md の生成・更新処理そのものを調べるとき

## hash
- 16cc4569cb6d50750e5f0012d24a558b04cf8ffd01192ef3e51498a4e005b8f9

# `index_entry_standard.py`

## Summary
- INDEX.md エントリーが満たすべき規範文書を生成する。対象の責務、内容に基づくルーティング、機械的情報を含めない方針を定義する。

## Read this when
- INDEX.md のエントリーを新規作成・更新するとき
- 対象を読むべき条件、対象の責務、他対象との境界を判断するとき
- エントリーに含める情報の粒度や、対象内容に基づく根拠を確認するとき

## Do not read this when
- INDEX.md エントリー以外のプロンプト生成規範を確認するとき
- 対象ファイル固有の実装内容や、一般的な StructDoc の構造を確認するときは、対応する実装・定義を直接読む

## hash
- 942b23384c6e0468b807b626d94ad638b8898badc3a7dd37cd5cb0a8f771ddce

# `oracle_and_realization_basic.py`

## Summary
- oracle と realization file の定義・役割・下位概念を構築する prompt builder の一部。oracle file を人間所有の正本仕様断片、realization file をその具体化として整理し、doc・src・test・implementation・ancillary の分類と配置を説明する。

## Read this when
- oracle file と realization file の定義や責務境界を prompt に組み込む処理を変更するとき
- oracle、realization の分類・配置・正本性に関する説明文の生成元を確認するとき

## Do not read this when
- 個別の oracle 文書や realization 実装の内容を確認したいとき
- prompt builder 全体の構成や別の prompt part の仕様だけを調べるとき

## hash
- 46cac8d7867434199021d72041b4b1b9eea45f91fbb845ee3e177089d3dde021

# `realization_oracle_reference_rule.py`

## Summary
- realization code から、対応する oracle file のパスをコメントへ記載するための規則を構築する。パス文脈から `work-root` の定義を取得し、プレースホルダー置換用マップと構造化ドキュメントを返す。

## Read this when
- realization code のコメントに oracle file path を参照させる規則を変更・利用するとき。
- `work-root` のプレースホルダー定義や、対応する構造化ドキュメントの生成方法を確認するとき。

## Do not read this when
- oracle file の一般的な定義やパス文脈全体の仕様だけを確認したいとき。
- realization code の具体的なコメント記述や、別の prompt builder 規則を直接変更するとき。

## hash
- f891c0131b0da1ad3836613b719a1e733c79ea7a2882935ee545126fc5457f3f

# `routing_rule.py`

## Summary
- INDEX.md を使って必要な本文へ進むためのルーティング規則を構築する関数を定義する。call-scoped context から work-root の定義を取得し、INDEX.md の扱い・読み進め方・判断基準を含む構造化文書とプレースホルダ map を返す。

## Read this when
- INDEX.md の役割、読み進め方、対象本文へ進む判断基準を変更・確認するとき
- routing rule の構造化文書生成や work-root プレースホルダの扱いを変更するとき

## Do not read this when
- INDEX.md の個別エントリー内容や対象ファイルの責務を確認したいとき
- ルーティング規則以外の prompt builder 部品を変更・調査するとき

## hash
- bd6e9b76921aaddbccba9336ae77740768a301b4cc6026b3083008a25e525d14
