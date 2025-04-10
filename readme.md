## GOAL

0000 코딩

0020 유튜브

-> 20분 코딩으로 자동 집계

이후 하루에 뭘 얼마나 했는지 그래프, 통계

과거 데이터를 수정하는 것은 가정하지 않음.

## TODO

* 통계페이지 제작
* 일간 소분류간 통계
* 대분류 도입
* 자동 대분류 저장
* 입력페이지에서 소분류 검색
* 일간 통계를 그래프화
* 주간, 월간 통계화
* act 기준 category_1 지정하는 페이지

## python installed

```cmd
# TDD
pip install pytest
# graph
pip install matplotlib
# GUI
pip install PySide6
# formatter
pip install black
pip install isort
```

## setting
```JSON
{
  "editor.defaultFormatter": "ms-python.black-formatter",
  "editor.formatOnSave": true,
  "python.sortImports": true
  "files.trimTrailingWhitespace": true
}
```