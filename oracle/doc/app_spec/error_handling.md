# エラーハンドリング規則

本書は、エラー終了時の handled failure と internal failure の分類、およびスタックトレースの共通契約の正本とする。console と terminal result の出力先、表示順序、および共通 field は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` を正本とする。

## エラー分類

### handled failure

handled failure は、個別仕様または共通仕様が想定済みの失敗として判断可能にしたエラー終了である。少なくとも次の失敗を含む。

- 明示された事前条件への違反
- 既知の conflict
- 既知の state 異常
- 外部 process の既知の失敗
- 上記と同等に、仕様から想定済みと判断できる失敗

### internal failure

internal failure は、仕様で想定済みの失敗へ変換されていない内部障害である。少なくとも次の失敗を含む。

- 未捕捉例外
- 実装上の invariant 違反
- handled failure に分類できない想定外の内部障害

終了コードだけから handled failure と internal failure を分類してはならない。

## handled failure の表示

- その場で処理を中断し、個別仕様が定める state 確定、rollback、report、および後処理を行う
- エラー terminal result には、簡潔な理由、必要な詳細、関連する path、実際に取り得る次の操作、終了コード、および診断用サブコマンドログのフルパスを含める
- 次の操作が 1 つしかない場合は、架空の選択肢を複数提示しない
- stdout と stderr のどちらにも、スタックトレースまたはコールスタックを表示しない
- エラー詳細は、サブコマンドログから診断できる状態にする

## internal failure の表示

- internal failure のスタックトレースをサブコマンドログへ保存する
- スタックトレースを console に表示する場合は stderr に表示し、簡潔なエラー terminal result より前に表示する
- エラー terminal result を、そのサブコマンドの最後の console 出力にする

## エラーとして扱わない結果

個別仕様が正常な処理結果として定義する状態は、internal failure として扱わない。これには、`attention`、`incomplete`、`completed_with_unresolved`、およびレビュー所見が存在する結果を含む。

中断可能サブコマンドのユーザー中断要求は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` に従って正常系として扱う。ユーザー中断要求では、stdout と stderr のどちらにもスタックトレースまたはコールスタックを表示しない。

## 個別仕様との関係

個別仕様がエラー時の state、rollback、report、次の操作、または終了コードを明示する場合は、その指示に従う。個別仕様に特別な記載がない事項には、本書の共通規則を適用する。
