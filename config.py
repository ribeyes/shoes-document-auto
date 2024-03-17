# 채산 사양서 정보
# 설정 파일은 bom.py 파일과 같은 폴더에 있어야 한다.


# 파일 이름
file_name = '벨로체스판부츠' # 신발이름

# 신발, 재단물 정보
shoes_name = '벨로체스판부츠'
shoes_code = 'BT_33' # 신발이름코드
shoes_color = ['BK','BR','GR','BE','WI'] # 신발색
cut_name = [  # 리스트 개수들이 같아야 한다. 안창은 제외
'스판세무+호인'
,'903B+호인'
,'샤무드+호인'
,'이합지+스티커+호인'
,'301'
,'포리600+스티커+호인'
,'핫멜트0.6양면'
,'케미시트1.2'
,'홍아대 조리중창'
,'융고급+호인'


] # 재단물 이름
cut_color = [ # 액션02의 블랙은 블랙_12 로
    ['BK','BR','GR','BE','WI']
    ,['BK','BK','BK','BK','BK']
    ,['GR','GR','GR','GR','GR']
    ,['','','','','']
    ,['BK','BR','GR','BE','RE']
    ,['','','','','']
    ,['','','','','']
    ,['','','','','']
    ,['','','','','']
    ,['BK','BK','BK','BK','BK']
    
] # 재단물 색. 번호 있으면 색_번호 로 표시
cut_consum = [ 
0.177
,0.069
,0.029
,0.085
,0.008
,0.047
,0.022
,0.028
,1
,0.082


] # 재단물 소모수량
begin_code = [shoes_code,'UP','CUT_GGM'] # 신발이름,갑피,재단물꼬미, 재단물 코드. 꼬미가 없는 경우에는 꼬미 제거

# 색상 코드별 한글 이름
color_korean = {'BK': '블랙', 'BE': '베이지', 'WH': '화이트', 'BR': '브라운', 'WI': '와인', 'GR': '그레이', 'CA': '카멜', 
                'OR': '오렌지', 'PK': '핑크', 'YEW': '옐로우', 'BL': '블루', 'GN': '그린', 'CR': '크림', 'NB': '네이비블루',
                'IV': '아이보리', 'NA': '네이비', 'MO': '모카', 'KK': '카키'}

# 부재료 정보
sub_material = ['기장25cm'] # 부재료 이름
sub_material_color = [ 
    ['BK','BR','GR','BE','BR']
] # 부재료 색. (부재료 개수만큼 리스트를 만든다)
sub_consum = [
    2
] # 부재료 소모수량 (부재료 개수만큼 리스트를 만든다)


# 안창 정보
insol = 'I' # 컵인솔 있으면 CI 없으면 I
insol_mold = '' # mold 번호
insol_color = ['BK','BK','BK','BK','BK'] # 안창 색
insol_cut = '융+메모리폼3MM+메라본20+호인' # 안창 자재명
insol_prod = '' # 안창 제조사 코드 (브루마스 등)
insol_consume = '0.033'


# 아웃솔 정보
outsol_pu = ['BK','BK','BK','BK','BK'] # 아웃솔 색 (신발 색 개수만큼 채워야한다.)
outsol_mold = '053' # 아웃솔 mold 번호 (안창에 넣는 mold 번호와 같다.)
bottom_type = '' # 밑창 종류 (ex: 고무족창, 고무판창) 
bottom_code = '' # 밑창 코드 (ex:WRTM, WARE, DRBR, 023BK -> KI-023고무족창블랙) 
bottom_mold = '' # 밑창 mold 번호 (ex: KI-023은 023으로 입력) 고무족창은 ki 번호가 있지만 빨래판무늬는 없다.