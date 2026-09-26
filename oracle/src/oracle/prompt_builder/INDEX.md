# `basic.py`

## Summary
- プロンプト構築関数間で共有する、プレースホルダ名と文字列またはパスの置換値との対応型を定義する。置換マップの型を確認する入口であり、プロンプトの組み立てや規定文面は各 builder が担う。

## Read this when
- プロンプト構築関数が受け渡す置換マップのキーや値の型を確認・変更するとき。

## Do not read this when
- 完成プロンプトの構成や有効化条件を調べるときは、プロンプト全体を組み立てる実装を読む。
- 特定のポリシーやプロンプト部品の文面を調べるときは、その内容を構築する実装を読む。

## hash
- f8a558f24e4b59e54e49e1729d4c10dfd1b596dc0b1531a5b8e9a8e2f9a6194a

# `complete_prompt.py`

## Summary
- 選択された規定と呼び出し固有の入力を組み合わせ、構造化された agent 向け prompt を構築する共通部品です。
- prompt の構成順と placeholder 定義の統合を担い、個々の規定文や呼び出し固有の目的を定義する箇所への入口になります。

## Read this when
- agent 向け prompt 全体の構成、規定の選択や配置、入力の組み込み方を調べる・変更する場合。
- 複数の prompt 部品から渡される placeholder 定義の統合方法を確認する場合。

## Do not read this when
- 特定の規定文の内容だけを調べる・変更する場合は、その規定を構築する部品へ進んでください。
- 特定の agent 呼び出しの task や scope だけを調べる・変更する場合は、その呼び出し元へ進んでください。

## hash
- e0b2967c10fae513822686200792fabc7a6e5cf20107541e3bd72e265488307f

# `editor_input.py`

## Summary
- エディタ起動前に表示する、人間向けの短い案内文を返す。案内の正確な文面はこの構築定義が担い、依頼本文には含めない。

## Read this when
- エディタ起動前に人間へ表示する案内の文面や、その表示内容を変更・確認するとき。

## Do not read this when
- editor input のライフサイクルや確定手順を調べるときは、その手順を定める仕様から確認する。
- 完全 prompt の構築や handoff のガイド・target の処理を調べるときは、それぞれを担う prompt builder または handoff の仕様から確認する。

## hash
- ed6c215c953dd93134584d847eb261a0d68073e57ead7513cab2ee4cded3e815

# `merge_conflict_resolution.py`

## Summary
- run join（feedback の自動 join を含む）と session join で共用する、競合解消 agent 向け prompt を構築する。両側の commit の参照入力、統合作業の目的と範囲、共通規定をまとめる。
- 呼び出し元固有の追加文面と、作業中 worktree の文脈・アクセス範囲・文書検索範囲を共通構築に反映する。

## Read this when
- run join と session join に共通して渡す競合解消 prompt の内容や構成を変更・追跡するとき。
- merge 前の両 commit をどう prompt に渡すか、また agent に進行中の競合状態をどう調査させるかを確認するとき。

## Do not read this when
- 競合の判断基準、編集上の責務、検証や報告の方針そのものを変更するときは、その方針を定義する対象を直接読む。
- run または session の個別の編集範囲、固有の追加入力、起動パラメータを変更するときは、該当する呼び出し元やコマンド仕様を直接読む。
- 完全 prompt の共通組み立てや、個別ポリシーの文面を変更するときは、それぞれの構築定義を直接読む。

## hash
- fd29d8f94e915805cabb59e4b7d00e08b4169dd958103d6bdda3ce9585052006

# `parts`

## Summary
- 完全 prompt に含める基本説明を組み立て、oracle・realization・uncategorised file の役割と分類の枠組みを示す。

## Read this when
- agent 向け prompt の基本説明について、これらのファイル区分の役割や境界を変更するとき。

## Do not read this when
- ファイル区分の正本仕様を変更・確認するときは、該当する意味仕様や列挙仕様から確認する。
- 完全 prompt の構成や各説明の有効化条件を変更するときは、prompt 全体の組み立てを担う対象から確認する。
- oracle file または realization file を扱う手順を変更するときは、それぞれの扱い方を定める個別の方針から確認する。

## hash
- 4df4f3bd63df35298afcf98f2050c29c802e660f0337f00edbdf0113fc0c4074

# `policy`

## Summary
- agent call に組み込む規定文面を、話題ごとの builder として構築する。参照 routing、file access、oracle・realization の扱い、適合性所見、競合解消、feedback 報告、editor input handoff を担う。
- 各 builder は prompt の構造化要素と必要な placeholder 定義を返す。個別の規定を選択して完全 prompt に組み込む制御は、上位の prompt 構築側が担う。

## Read this when
- 複数の規定文面にまたがる変更や、この規定群の責務の境界を調べるとき。
- agent call に渡す規定の文面や、path context・file access mode・検索範囲に応じた構築内容を変更するとき。

## Do not read this when
- 単一の規定文面だけを調べる場合は、その規定を構築する箇所から読み始める。
- 規定の選択・有効化・完全 prompt 内の配置や結合方法を変更するときは、完全 prompt の構築側を直接確認する。正本仕様の意味を確認・改訂するときは、該当分野の oracle doc を直接確認する。

## hash
- 8635dc811502a790cae45f75d4490212ee3ad9029551a6daf9d1e8e089ca1a6d
