# エラーハンドリング規則

本書は、エラー終了時の handled failure と internal failure の分類、およびスタックトレースの共通契約の正本とする。console と terminal result の出力先、表示順序、および共通 field は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「コンソール・ファイル、ログ出力規則」を正本とする。

## エラー分類

handled failure／internal failure は、エラー終了の性質による分類であり、回復待ちの対象かどうかとは別に判断する。Codex CLI の回復待ちの可否と終了条件は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「`codex exec` が失敗した場合」を正本とし、エラー終了へ移る場合に本節の基準で分類する。

### handled failure

handled failure は、個別仕様または共通仕様から、想定済みの失敗と判断できるエラー終了である。少なくとも次の失敗を含む。

- 明示された事前条件への違反
- 既知の conflict
- 既知の state 異常
- 外部 process の既知の失敗

### internal failure

internal failure は、仕様で想定済みの失敗へ変換されていない内部障害である。少なくとも次の失敗を含む。

- 未捕捉例外
- 実装上の invariant 違反
- primary report を保存できず、最外側の非対話末端サブコマンドの完了契約を確定できない障害

終了コードだけから handled failure と internal failure を分類してはならない。

## エラー終了の確定

cmoc は、handled failure と internal failure のどちらの場合も、個別仕様が定める state 確定、rollback、および後処理を行う。handled failure では、その場で本命処理を中断して、これらの終了処理へ移る。

最外側の非対話末端サブコマンドでは、エラーまでに確定した作業内容とエラー終端結果を、個別仕様が定める primary report に保存する。その後、`error` の terminal result とサブコマンド終了イベントを確定する。

primary report 自体を保存できない場合は、元の失敗結果に代えて report 保存基盤の internal failure を確定する。この場合、保存を確認できない report の役割または path は表示しない。

## handled failure の表示

- エラー terminal result には、簡潔な理由、必要な詳細、関連する path、実際に取り得る次の操作、終了コード、および診断用サブコマンドログのフルパスを含める
- 次の操作が 1 つしかない場合は、架空の選択肢を複数提示しない
- stdout と stderr のどちらにも、スタックトレースまたはコールスタックを表示しない
- エラー詳細は、サブコマンドログから診断できる状態にする

## internal failure の表示

- internal failure のスタックトレースをサブコマンドログへ保存する
- スタックトレースを console に表示する場合は stderr に表示し、簡潔なエラー terminal result より前に表示する

## エラーとして扱わない結果

個別仕様が正常な処理結果として定義する状態は、internal failure として扱わない。これには、`attention`、`incomplete`、および `completed_with_unresolved` を含む。

中断可能サブコマンドのユーザー中断要求は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「サブコマンドのユーザー中断」に従って正常系として扱う。ユーザー中断要求では、stdout と stderr のどちらにもスタックトレースまたはコールスタックを表示しない。

## 個別仕様との関係

個別仕様がエラー時の state、rollback、report、次の操作、または終了コードを明示する場合は、その指示に従う。個別仕様に特別な記載がない事項には、本書の共通規則を適用する。
