# shoes-document-auto
신발제조 문서 자동화 작업

# 총 3개의 파일이 필요
ERP 엑셀 파일, bom.py, config.py 

1. ERP 엑셀 파일
   ERP에 등록된 코드들이 정리되어 있는 엑셀 파일.
   
2. bom.py
   BOM과 품목등록 csv 파일을 생성해주는 파이썬 프로그램. config에 입력된 값들을 활용해서 csv 파일을 생성.
   
3. config.py
   채산서에 있는 재단물, 신발 색 등을 작성
   

# 실행시 참고사항
위 3개의 파일은 같은 경로에 위치한 상태에서 실행. bom에서 경로 수정 가능.
깃허브에는 bom과 config 파일만 업로드할 예정.
