
# realization 基本情報

## realization files

- realization files とは、oracles files ではない、cmoc の裁量で読み書きして良いファイルの総称である

## realization code

- realization code とは、realization files のうち、実装またはテストのソースコードを指す

## realization implementation

- realization implementation  とは、realization code のうち、実装ファイルを指す
- 純粋なソースコードだけでなく、プロダクトの挙動を記述する設定ファイル類も含めて良い
- e.g. `<work-root>/src/**/*.py`, `<work-root>/src/**/*.json`

## realization test

- realization test とは、realization code のうち、テストのソースコードを指す
- e.g. `<work-root>/test/**/*.py`

## realization ancillary

- realization ancillary とは、realization files のうち、補助的なファイルを指す
- e.g. `<work-root>/.gitignore`, `<work-root>/bin/**/*`
