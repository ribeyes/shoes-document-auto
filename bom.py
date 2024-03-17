import pandas as pd
import csv
import re
import shutil
import os.path
from config import *

bom_list_all = [] # 엑셀 전체 행 
bom_list = [] # 엑셀 1개의 행에 해당


# 고정된 값
shoes_size_tmp = list(range(225,260,5)) # 사이즈 225~255 int형
shoes_size = list(map(str,shoes_size_tmp))  # 사이즈 225~255 int형을 str형으로

# # 변경 해줘야하는 값들
# shoes_code = 'SN_62' # 신발이름코드
# shoes_color = ['BK'] # 신발 색

# # 채산 사양서의 자재명
# cut_name = [
# '액션02+호인'
# ]

# # 재단물 색. 번호 있으면 색_번호 로 표시
# cut_color = [
# ['BK']
# ]

# # 재단물 소모수량
# cut_consum = [2.5]
# begin_code = [shoes_code,'UP','CUT_GGM'] # 신발이름, 갑피,재단물꼬미,재단물 코드



up_code = [] # 부재료 코드 생성에서 사용할 갑피 코드
# 갑피,재단물꼬미,재단물 코드 생성
for n in begin_code:
    for c in shoes_color:
        for s in shoes_size:
            match n:
                case 'UP':
                    bom_list.append(shoes_code + c + s + '_' + 'UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    
                    if 'CUT_GGM' in begin_code: # 재단물 꼬미가 있는 경우
                        bom_list.append(shoes_code + c + s +'_' + 'CUT_GGM')
                    else: # 재단물 꼬미가 없는 경우
                        bom_list.append(shoes_code + c + s +'_' + 'CUT')
                    
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(1) # 소모수량
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue

                case 'CUT_GGM':
                    bom_list.append(shoes_code + c + s + '_' + 'CUT_GGM')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(shoes_code + c + s +'_' + 'CUT')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(1) # 소모수량
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
                
                case shoes_code:
                    bom_list.append(shoes_code + c + s)
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(shoes_code + c + s +'_' + 'UP')
                    up_code.append(shoes_code + c + s +'_' + 'UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(1) # 소모수량
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue

        bom_list_all.append([]) # 빈 행 추가            
    bom_list_all.append([])   




# 재단물 생산품목 코드 생성
def cut_product(color,size):
    bom_list.append(shoes_code + color + size + '_CUT')
    bom_list.append(''); bom_list.append('')
    bom_list.append(''); bom_list.append('')

# 재단물 소모수량 부분
def cons_cnt(cons):
    bom_list.append(''); bom_list.append('')
    bom_list.append(cons) # 소모수량

# 재단물 코드생성
for cn,cc,con in zip(cut_name,cut_color,cut_consum):
    match cn:
        case '액션02+호인'|'액션02+스티커'|'액션02+스티커+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '액션02+호인':
                        if '오플' in n: # 오플가죽인경우
                            bom_list.append('OPACTION_'+ n[2:] +'_HO')
                        else:
                            bom_list.append('ACTION02_'+ n +'_HO')
                    
                    elif cn == '액션02+스티커':
                        if '오플' in n:
                            bom_list.append('OPACTION_'+ n[2:] +'_HO')
                        else:
                            bom_list.append('ACTION02_'+ n +'_ST')
                    
                    else:
                        if '오플' in n:
                            bom_list.append('OPACTION_'+ n[2:] +'_HO')
                        else:
                            bom_list.append('ACTION02_'+ n +'_ST_HO')
                    
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case '양가죽':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('SHEEP_'+ n)
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case '스프리트'|'스프리트+903B':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '301':
                        bom_list.append('SPLIT_'+ n)
                    else:
                        bom_list.append('SPLIT_'+ n + '_903B')
                        
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case '301'|'301+호인':  # 301원단
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '301':
                        bom_list.append('301'+n)
                    else: 
                        bom_list.append('301'+ n + '_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case '하이포라+중탄6mm20g+호인'|'하이포라+이합지+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '하이포라+중탄6mm20g+호인':
                        bom_list.append('하이포라_'+ n +'_중탄6mm20g_HO')
                    else:
                        bom_list.append('하이포라_2HOPJI_'+ n +'_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case '아크릴보아+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('아크릴보아_'+ n + '_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case '융이지+2mm스펀지NT+호인'|'융이지+2mmSP/NT+호인'|'융이지+K32mm스펀지NT+호인'|'융이지+2mmNT+호인'|\
            '융이지+SP2mmNT+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '융이지+2mm스펀지NT+호인':
                        bom_list.append('CF_LN_'+ n + '_2mmSPGNT_HO')
                    elif cn == '융이지+2mmSP/NT+호인':
                        bom_list.append('CF_LN_'+ n + '_2mmSPGNT_HO')
                    elif cn == '융이지+K32mm스펀지NT+호인':
                        bom_list.append('CF_LN_'+ n + '_K32mmSPGNT_HO')
                    elif cn == '융이지+2mmNT+호인':
                        bom_list.append('CF_LN_'+ n + '_2mmNT_HO')
                    else:
                        bom_list.append('CF_LN_'+ n + '_2mmSP/NT_HO')

                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case '양털보아+메라본20g+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('양털보아_'+ n + '_MB60g_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case 'FG8mm보아+메라본20g+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('BOA_FG8mm'+ n + '_MB60g_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case '903핫핑크+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('903_'+ n + '_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
        
        case '메리메쉬+4mmNT+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('MM_'+ n +'_4mmNT_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '903B'|'903B+호인'|'903B+스티커'|'903B+스티커+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '903B':
                        bom_list.append('903B_'+ n)
                    elif cn == '903B+호인':
                        bom_list.append('903B_'+ n +'_HO')
                    elif cn == '903B+스티커':
                        bom_list.append('903B_'+ n +'_ST')
                    else:
                        bom_list.append('903B_'+ n +'_ST_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '2903B'|'2903B+호인'|'2903B+스티커'|'2903B+스티커+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '2903B':
                        bom_list.append('2903B_'+ n)
                    elif cn == '2903B+호인':
                        bom_list.append('2903B_'+ n +'_HO')
                    elif cn == '2903B+스티커':
                        bom_list.append('2903B_'+ n +'_ST')
                    else:
                        bom_list.append('2903B_'+ n +'_ST_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '샤무드+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('CHAMUDE_'+ n +'_HO')  # 추가되면 수정할 부분!
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '633원단+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('633_'+ n +'_HO')  # 추가되면 수정할 부분!
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '이합지+스티커+호인'|'이합지+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '이합지+스티커+호인':
                        bom_list.append('2HOPJI_WH_ST_HO') # 이합지가 색 없이 있는 경우는 화이트로 취급
                    else:
                        bom_list.append('2HOPJI_WH_HO') # 이합지가 색 없이 있는 경우는 화이트로 취급
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '포리600+스티커+호인':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('FR600'+ n + '_ST_HO')  # 추가되면 수정할 부분!
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '고탄4mmNT+스티커+호인'|'고탄2mmNT+스티커+호인'|'고탄4mmNT+스티커':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '고탄4mmNT+스티커+호인':
                        bom_list.append('GT4mmNT_ST_HO')
                    elif cn == '고탄2mmNT+스티커+호인':
                        bom_list.append('GT2mmNT_ST_HO') 
                    else:
                        bom_list.append('GT4mmNT_ST')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '고탄10mm+스티커'|'고탄8mm+스티커':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '고탄10mm+스티커':
                        bom_list.append('GT10mm_ST')  # 추가되면 수정할 부분!
                    else:
                        bom_list.append('GT8mm_ST')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '핫멜트0.6'|'핫멜트0.6단면'|'핫멜트0.6양면':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if '단면' in cn:
                        bom_list.append('HM0.6_SS')
                    elif '양면' in cn:
                        bom_list.append('HM0.6_BS')
                    else:
                        bom_list.append('HM0.6')  # 추가되면 수정할 부분!
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '핫멜트0.8':  # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('HM0.8')  # 추가되면 수정할 부분!
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '신PU15mm'|'신PU+호인': # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if '신PU15mm' in cn:
                        bom_list.append('NEW_PU15mm_BK') # 현재는 블랙만 있음.
                    else :
                        bom_list.append('NEW_PU_'+ n)
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case 'S보드056'|'S보드2268'|'S보드5368'|'S보드6268'|'S보드223H': # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == 'S보드056': # 추가되면 수정할 부분!
                        bom_list.append('SBD056_FOXPUFF'+s) 
                    elif cn == 'S보드2268':
                        bom_list.append('SBD2268_FOXPUFF'+s)
                    elif cn == 'S보드5368':
                        bom_list.append('SBD5368_FOXPUFF'+s)
                    elif cn == 'S보드6268':
                        bom_list.append('SBD6268_FOXPUFF'+s)
                    else:
                        bom_list.append('SBD223H_FOXPUFF'+s)
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '케미시트1.2': # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('KMST1.2_FOXPUFF'+s) 
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '고급고무80mm': # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('80mm_HC_RB_'+n) 
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '헌팅고무6mm': # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('6mm_HURB_'+n) 
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '하이프렌4mm+스티커+호인'|'하이프렌2mm+스티커+호인': # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '하이프렌4mm+스티커+호인': # 추가되면 수정할 부분!
                        bom_list.append('HF4mm_ST_HO') 
                    else:
                        bom_list.append('HF2mm_ST_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '택션1.6'|'택션1.6+연질3mm+호인'|'택션+연질3mm+호인': # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '택션1.6': # 추가되면 수정할 부분!
                        bom_list.append('TT1.6') 
                    elif cn == '택션1.6+연질3mm+호인':
                        bom_list.append('TT1.6_YJ3mm_HO')
                    else:
                        bom_list.append('TT_YJ3mm_HO')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '연질2mm'|'연질2mm+스티커': # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    if cn == '연질2mm': # 추가되면 수정할 부분!
                        bom_list.append('YJ2mm')
                    else:
                        bom_list.append('YJ2mm_' + n + '_ST')
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case '40mm고무': # 추가되면 수정할 부분!
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append('40mm_RB_'+n) 
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가

        case x: # 일치하는 재단물 이름 없을 경우
            for sc,n in zip(shoes_color,cc):
                for s in shoes_size:
                    cut_product(sc,s)
                    bom_list.append(cn + '_' + n) 
                    cons_cnt(con)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                    continue
            
                bom_list_all.append([]) # 빈 행 추가
                
    bom_list_all.append([]) # 빈 행 추가
# '연질2mm'|'연질2mm+스티커'

# sub_material = ['평끈8mm'] # 부재료 이름
# sub_material_color = [['BK']] # 부재료 색 (화이트,블랙,브론즈,니켈 등)
# sub_consum = [''] # 부재료 소모수량
# 부재료 코드 생성
for sm, submc, subcons in zip(sub_material,sub_material_color, sub_consum):
    match sm:
        case '40mm고무': # 고무 폭40mm
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append('40mm_RB_'+ smc)
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case '300번': # 구멍쇠300번
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append('EY_' + smc + '_300')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case '내경18mm': # 타원형구멍쇠
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append('타원형구멍쇠_내경18mm_'+ smc)
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case '내경15mm'|'내경13mm'|'내경20mm': # 비죠
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    if sm == '내경15mm':
                        bom_list.append('BJ_15mm_'+ smc)
                    elif sm == '내경13mm':
                        bom_list.append('BJ_13mm_'+ smc)
                    else:
                        bom_list.append('BJ_20mm_'+ smc)
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case '내경7mm': # 손톱장식
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append('7mm_NAILDECO_'+ smc)
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case '기장10cm' | '기장15cm' | '기장18cm' | '기장20cm' | '기장25cm': # 쟈크는 사이즈 범위에 따라 길이가 다른 조건 나오면 수정.
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    if sm == '기장10cm': 
                        bom_list.append('ZIP_'+ '10' + '_' + smc )
                    elif sm == '기장15cm': 
                        bom_list.append('ZIP_'+ '15' + '_' + smc )
                    elif sm == '기장18cm': 
                        bom_list.append('ZIP_'+ '18' + '_' + smc )
                    elif sm == '기장20cm': 
                        bom_list.append('ZIP_'+ '20' + '_' + smc )
                    else: 
                        bom_list.append('ZIP_'+ '25' + '_' + smc )
                    
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case '평끈8mm': # 평끈은 사이즈 범위에 따라 길이가 다른 조건 나오면 수정.
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    if int(s) <= 240: 
                        bom_list.append('PSTRING8mm_'+ smc + '90cm')
                    else: 
                        bom_list.append('PSTRING8mm_'+ smc + '95cm')
                    
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case '연질2mm'|'연질2mm+스티커': 
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    if sm == '연질2mm': 
                        bom_list.append('YJ2mm')
                    else:
                        bom_list.append('YJ2mm_ST')
                    
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case '갈매기7mm': 
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    if int(s) <= 230: 
                        bom_list.append('GULL_RB_7mm_'+ smc + '_50cm')
                    elif int(s) <= 240: 
                        bom_list.append('GULL_RB_7mm_'+ smc + '_52cm')
                    elif int(s) <= 250: 
                        bom_list.append('GULL_RB_7mm_'+ smc + '_54cm')
                    else:
                        bom_list.append('GULL_RB_7mm_'+ smc + '_56cm')
                    
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case '통끈': 
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    if int(s) <= 240: # 225-240 120cm
                        bom_list.append('TSTRING_120cm_'+ smc)
                    else: # 240-255 125cm
                        bom_list.append('TSTRING_125cm_'+ smc)
                    
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        
        case x: 
            for sc, smc in zip(shoes_color, submc):
                for s in shoes_size:
                    bom_list.append(shoes_code + sc + s + '_UP')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(sm + '_' + smc)
                    bom_list.append(''); bom_list.append('')
                    bom_list.append(subcons)
                    bom_list_all.append(bom_list) # 전체 행에 추가
                    bom_list = [] # 행 초기화
                
                bom_list_all.append([]) # 빈 행 추가
            bom_list_all.append([]) # 빈 행 추가
        



# insol = 'CI' # 컵인솔 있으면 CI 없으면 I
# insol_mold = '5368' # mold 번호
# insol_color = ['GR'] # 안창 색
# insol_cut = '903B' # 안창 자재명
# insol_prod = 'B' # 안창 제조사명
insol_code = [] # 안창 중복 없는 코드
insol_cut_code = [] # 안창 자재코드
# 안창 코드 생성
# 신발,안창+제조사명까지 코드 생성
for sc,ic in zip(shoes_color,insol_color):
    if insol == '': break # 안창 없는 경우
    for s in shoes_size:
        bom_list.append(shoes_code + sc + s)
        bom_list.append(''); bom_list.append('')
        bom_list.append(''); bom_list.append('')
        if insol == 'CI': # 컵인솔 있는 경우
            match insol_cut:
                case '융이지':
                    cut_tmp = insol_mold + '_' + insol + '_' + ic + s 
                    tmp_code = insol_mold + '_' + insol + '_CF_'+ ic + s + insol_prod
                    bom_list.append(tmp_code)
                    if tmp_code not in insol_code:
                        insol_code.append(tmp_code)
                    if cut_tmp not in insol_cut_code:
                        insol_cut_code.append(cut_tmp)
                
                case '903B':
                    cut_tmp = insol_mold + '_' + insol + '_' + ic + s 
                    tmp_code = insol_mold + '_' + insol + '_903B_'+ ic + s + insol_prod
                    bom_list.append(tmp_code)
                    if tmp_code not in insol_code:
                        insol_code.append(tmp_code)
                    if cut_tmp not in insol_cut_code:
                        insol_cut_code.append(cut_tmp)
                
                case x:
                    cut_tmp = insol_cut + '_' + insol + '_' + ic + s 
                    tmp_code = insol_cut + '_' + insol + '_' + ic + s + insol_prod
                    bom_list.append(tmp_code)
                    if tmp_code not in insol_code:
                        insol_code.append(tmp_code)
                    if cut_tmp not in insol_cut_code:
                        insol_cut_code.append(cut_tmp)

        else: # 컵인솔 없는 경우
            match insol_cut:
                case '2903B+고탄4mmNT+호인':
                    cut_tmp = '2903B_'+ ic +'_GT4mmNT_HO_' + insol + s
                    tmp_code = '2903B_'+ ic +'_GT4mm_HO_' + insol + s + insol_prod
                    bom_list.append(tmp_code)
                    if tmp_code not in insol_code:
                        insol_code.append(tmp_code)
                    
                    insol_cut_code.append(cut_tmp)
                
                case '2903B+라텍스발포3mm+호인':
                    cut_tmp = '2903B_' + ic + '_LATEX_BP3mm_HO_' + insol + s
                    tmp_code = '2903B_' + ic + '_LATEX_BP3mm_HO_' + insol + s + insol_prod
                    bom_list.append(tmp_code)
                    if tmp_code not in insol_code:
                        insol_code.append(tmp_code)
                    
                    insol_cut_code.append(cut_tmp)
                
                case '903B+고탄4mmNT+호인':
                    cut_tmp = '903B_' + ic + '_GT4mmNT_HO_' + insol + s
                    tmp_code = '903B_' + ic + '_GT4mmNT_HO_' + insol + s + insol_prod
                    bom_list.append(tmp_code)
                    if tmp_code not in insol_code:
                        insol_code.append(tmp_code)
                    
                    insol_cut_code.append(cut_tmp)
                
                case '903B':
                    cut_tmp = '903B_'+ ic +'_HO_' + insol + s
                    tmp_code = '903B_' + ic + '_HO_'+ insol + s + insol_prod
                    bom_list.append(tmp_code)
                    if tmp_code not in insol_code:
                        insol_code.append(tmp_code)
                    
                    insol_cut_code.append(cut_tmp)
                
                case x:
                    cut_tmp = insol_cut + '_' + ic + '_' + insol + s
                    tmp_code = insol_cut + '_' + ic + '_' + insol + s + insol_prod
                    bom_list.append(tmp_code)
                    if tmp_code not in insol_code:
                        insol_code.append(tmp_code)
                    
                    insol_cut_code.append(cut_tmp)

        bom_list.append(''); bom_list.append('')
        bom_list.append(1) # 소모수량
        bom_list_all.append(bom_list) # 전체 행에 추가
        bom_list = [] # 행 초기화
        continue

    bom_list_all.append([]) # 빈 행 추가
bom_list_all.append([]) # 빈 행 추가



match insol:
    case 'CI': # 컵인솔 있는 경우
        list_tmp = []
        for ic in insol_code:
            bom_list.append(ic)
            bom_list.append(''); bom_list.append('')
            bom_list.append(''); bom_list.append('')
            bom_list.append(ic[:-1])
            list_tmp.append(ic[:-1])
            bom_list.append(''); bom_list.append('')
            bom_list.append(1) # 소모수량
            if ic[-4:-1] == '255':
                bom_list_all.append(bom_list)
                bom_list_all.append([]) # 빈 행 추가
                bom_list = [] # 행 초기화 
            else:
                bom_list_all.append(bom_list)
                bom_list = [] # 행 초기화 
        bom_list_all.append([]) # 빈 행 추가
        
        for ic,insc in zip(list_tmp,insol_cut_code):
            bom_list.append(ic)
            bom_list.append(''); bom_list.append('')
            bom_list.append(''); bom_list.append('')
            bom_list.append(insc)
            bom_list.append(''); bom_list.append('')
            bom_list.append(1) # 소모수량
            if ic[-3:] == '255':
                bom_list_all.append(bom_list)
                bom_list_all.append([]) # 빈 행 추가
                bom_list = [] # 행 초기화 
            else:
                bom_list_all.append(bom_list)
                bom_list = [] # 행 초기화 
        bom_list_all.append([]) # 빈 행 추가
        
        for ic in list_tmp: 
            bom_list.append(ic)
            bom_list.append(''); bom_list.append('')
            bom_list.append(''); bom_list.append('')
            match insol_cut: # 수정해야할 부분
                case '융이지':
                    bom_list.append('CF_LN_'+ ic[-5:-3])
                case '903B':
                    bom_list.append('903B_'+ ic[-5:-3])
                case '903B+고탄4mmNT+호인':
                    bom_list.append('903B_'+ ic[-5:-3] + '_GT4mmNT_HO')
                case x:
                    bom_list.append(insol_cut + '_' + ic[-5:-3])

            bom_list.append(''); bom_list.append('')
            bom_list.append(insol_consume) # 소모수량
            if ic[-3:] == '255':
                bom_list_all.append(bom_list)
                bom_list_all.append([]) # 빈 행 추가
                bom_list = [] # 행 초기화 
            else:
                bom_list_all.append(bom_list)
                bom_list = [] # 행 초기화 
        bom_list_all.append([]) # 빈 행 추가
    
    
    case 'I': # 컵인솔 없는 경우
        list_tmp = []
        for ic in insol_code:
            bom_list.append(ic)
            bom_list.append(''); bom_list.append('')
            bom_list.append(''); bom_list.append('')
            bom_list.append(ic[:-1])
            list_tmp.append(ic[:-1])
            bom_list.append(''); bom_list.append('')
            bom_list.append(1) # 소모수량
            if ic[-4:-1] == '255':
                bom_list_all.append(bom_list)
                bom_list_all.append([]) # 빈 행 추가
                bom_list = [] # 행 초기화 
            else:
                bom_list_all.append(bom_list)
                bom_list = [] # 행 초기화 
        bom_list_all.append([]) # 빈 행 추가
        
        for ic in list_tmp:
            bom_list.append(ic)
            bom_list.append(''); bom_list.append('')
            bom_list.append(''); bom_list.append('')
            match insol_cut: # 수정해야할 부분
                case '903B':
                    bom_list.append('903B_'+ ic[5:7])
                case '903B+고탄4mmNT+호인':
                    bom_list.append('903B_'+ ic[5:7] + '_GT4mmNT_HO')
                case x:
                    bom_list.append(insol_cut + '_' + ic[-7:-5])
            
            bom_list.append(''); bom_list.append('')
            bom_list.append(insol_consume) # 소모수량
            if ic[-3:] == '255':
                bom_list_all.append(bom_list)
                bom_list_all.append([]) # 빈 행 추가
                bom_list = [] # 행 초기화 
            else:
                bom_list_all.append(bom_list)
                bom_list = [] # 행 초기화 
        bom_list_all.append([]) # 빈 행 추가
        
    

# 아웃솔 코드 생성
# outsol_pu = ['BK'] # 아웃솔(O) 색
# outsol_mold = '5368' # 아웃솔 mold 번호
# bottom_type = '빨래판무늬투명' # 밑창 종류 (ex: 고무족창투명,빨래판무늬레드) 무슨 색인지 작성해야함
# bottom_mold = '' # 밑창 mold 번호 (ex: KI-023은 023으로 입력) 고무족창은 ki 번호가 있지만 빨래판무늬는 없다.
outsol_total_code = [] # 아웃솔 중복 없는 코드
outsol_itself = [] # 자체 아웃솔 중복 없는 코드

for sc,pu in zip(shoes_color,outsol_pu):
    for s in shoes_size:
        bom_list.append(shoes_code + sc + s)
        bom_list.append(''); bom_list.append('')
        bom_list.append(''); bom_list.append('')
        match bottom_type:
            case '': # 아웃솔만 있는 경우
                tmp = outsol_mold + '_O_'+ pu + s
                bom_list.append(tmp)
            
            case '고무판창'|'고무족창':
                tmp = outsol_mold + '_O_'+ pu + s + '_' + bottom_code
                tmp2 = outsol_mold + '_O_'+ pu + s
                bom_list.append(tmp)
                if tmp not in outsol_total_code:
                    outsol_total_code.append(tmp)
                if tmp2 not in outsol_itself:
                    outsol_itself.append(tmp2)
            
            case x:
                tmp = outsol_mold + '_O_'+ pu + s + '_' + bottom_code
                tmp2 = outsol_mold + '_O_'+ pu + s
                bom_list.append(tmp)
                if tmp not in outsol_total_code:
                    outsol_total_code.append(tmp)
                if tmp2 not in outsol_itself:
                    outsol_itself.append(tmp2)
        
        bom_list.append(''); bom_list.append('')
        bom_list.append(1)
        bom_list_all.append(bom_list)
        bom_list = [] # 행 초기화
    bom_list_all.append([]) # 빈 행 추가
bom_list_all.append([]) # 빈 행 추가


for oc,oi in zip(outsol_total_code,outsol_itself):
    bom_list.append(oc)
    bom_list.append(''); bom_list.append('')
    bom_list.append(''); bom_list.append('')
    bom_list.append(oi)
    bom_list.append(''); bom_list.append('')
    bom_list.append(1)
    bom_list_all.append(bom_list)
    bom_list = [] # 행 초기화
    if oi[-3:] == '255':
        bom_list_all.append([]) # 빈 행 추가

bom_list_all.append([]) # 빈 행 추가


bottom_size = 225 
for oc in outsol_total_code:
    bom_list.append(oc)
    bom_list.append(''); bom_list.append('')
    bom_list.append(''); bom_list.append('')
    
    match bottom_type: 
        case '':
            break

        case '고무판창': 
            bom_list.append(bottom_code)
            bottom_size += 5
        
        case '고무족창': 
            if re.match('[0-9]', bottom_code[-3:]) is None: # 색 코드가 3글자인 경우
                bom_list.append('KI' + bottom_code[:-3] + '_' + bottom_code[-3:] + str(bottom_size))
            else: # 색 코드가 2글자인 경우
                bom_list.append('KI' + bottom_code[:-2] + '_' + bottom_code[-2:] + str(bottom_size))
            bottom_size = int(bottom_size) 
            bottom_size += 5

        case x: 
            bom_list.append(bottom_code)
            bottom_size += 5

    bom_list.append(''); bom_list.append('')
    bom_list.append(1)
    bom_list_all.append(bom_list)
    bom_list = [] # 행 초기화
    if bottom_size == 260:
        bottom_size = 225
        bom_list_all.append([]) # 빈 행 추가


df = pd.DataFrame(bom_list_all, columns = ['생산품목코드', '','','','', '소모품목코드', '','', '소모수량'])
df = df.set_index('생산품목코드')
df.to_csv('./bom생성/'+ file_name +'.csv', encoding="euc-kr")



# 품목등록 시트
item_list_all = [] # 품목등록 엑셀 전체 행
item_list = [] # 품목등록 엑셀 1개의 행에 해당
consume_list = [] # BOM의 소모품목코드


# erp 등록된 csv 파일 불러오기
f = open('erp.csv','r', encoding='utf8')
rdr = csv.reader(f)
erp_item_code = [] # erp에 등록된 품목코드

# erp 품목코드를 리스트로 저장
for item in rdr:
    erp_item_code.append(item[0])


# BOM 소모품목코드 저장(중복제거)
for item in bom_list_all:
    if len(item) == 0:
        consume_list.append('')
        if consume_list[-2] == '' and consume_list[-3] == '' :
            consume_list.pop()
        continue
    
    if item[5] not in consume_list:
        consume_list.append(item[5])




# 신발이름
item_list_all.append([shoes_code, shoes_name, '1', '족', '', '1', '', '', '100'])
item_list_all.append([])


i = 1 # 신발이름 앞에 번호
# 신발이름 색상 사이즈 코드생성
for cl in consume_list:
    if cl in erp_item_code: # erp에 등록되어 있으면 제외
        continue
    
    if 'CUT_GGM' in cl or '_CUT' in cl:
        break

    if len(cl) == 0:
        item_list_all.append([])
        i += 1
        continue
      
    if cl[-2:] == 'UP':
        item_list.append(cl[:-3])
        if cl[5:7] in color_korean:
            item_list.append(str(i) + shoes_name + color_korean[cl[5:7]] + cl[-6:-3])
        else:
            item_list.append(str(i) + shoes_name + cl[-6:-3])
        
        item_list.append('1'); item_list.append('족'); item_list.append('')
        item_list.append('1'); item_list.append(''); item_list.append(''); item_list.append('100')
        item_list_all.append(item_list)
        item_list = []
        continue
    

i = 1 # 신발이름 앞에 번호
# 재단물, 부재료, 안창, 아웃솔 코드생성
for cl in consume_list:
    if cl in erp_item_code: # erp에 등록되어 있으면 제외
        continue

    if len(cl) == 0:
        item_list_all.append([])
        if len(item_list_all[-2]) == 0 and len(item_list_all[-3]) == 0:
            item_list_all.pop()
        continue

    if cl[-2:] == 'UP': # 갑피
        item_list.append(cl)
        if cl[5:7] in color_korean:
            item_list.append(str(i) + shoes_name + color_korean[cl[5:7]] + cl[-6:-3] + '갑피')
        else:
            item_list.append(str(i) + shoes_name + cl[-6:-3] + '갑피')
        
        if '255' in cl: 
            i += 1
        
        if i == len(shoes_color) + 1:
            i = 1
        
        item_list.append('1'); item_list.append('족'); item_list.append('')
        item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('200')
        item_list_all.append(item_list)
        item_list = []
        continue
    
    if cl[-7:] == 'CUT_GGM': # 재단물꼬미
        item_list.append(cl)
        if cl[5:7] in color_korean:
            item_list.append(str(i) + shoes_name + color_korean[cl[5:7]] + cl[-11:-8] + '재단물꼬미')
        else:
            item_list.append(str(i) + shoes_name + cl[-11:-8] + '재단물꼬미')
        
        if '255' in cl: 
            i += 1

        if i == len(shoes_color) + 1:
            i = 1
        
        item_list.append('1'); item_list.append('족'); item_list.append('')
        item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('700')
        item_list_all.append(item_list)
        item_list = []
        continue
    
    if cl[-3:] == 'CUT': # 재단물
        item_list.append(cl)
        if cl[5:7] in color_korean:
            item_list.append(str(i) + shoes_name + color_korean[cl[5:7]] + cl[-7:-4] + '재단물')
        else:
            item_list.append(str(i) + shoes_name + cl[-7:-4] + '재단물')
        
        if '255' in cl: 
            i += 1
        
        item_list.append('1'); item_list.append('족'); item_list.append('')
        item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('300')
        item_list_all.append(item_list)
        item_list = []
        continue

    if 'ACTION02' in cl: # 액션02
        item_list.append(cl)
        item_list.append('')
        item_list.append('1'); item_list.append('평'); item_list.append('')
        item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('500')
        item_list_all.append(item_list)
        item_list = []
        continue
    
    if 'SHEEP' in cl: # 양가죽
        item_list.append(cl)
        item_list.append('')
        item_list.append('1'); item_list.append('평'); item_list.append('')
        item_list.append('0'); item_list.append(''); item_list.append(''); item_list.append('')
        item_list_all.append(item_list)
        item_list = []
        continue

    if 'SPLIT' in cl: # 스프리트
        item_list.append(cl)
        item_list.append('')
        item_list.append('1'); item_list.append('평'); item_list.append('')
        item_list.append('0'); item_list.append(''); item_list.append(''); item_list.append('')
        item_list_all.append(item_list)
        item_list = []
        continue

    if '_HO' in cl or '_ST' in cl: # 호인 또는 스티커
        item_list.append(cl)
        item_list.append('')
        item_list.append('1'); item_list.append(''); item_list.append('')
        item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('500')
        item_list_all.append(item_list)
        item_list = []
        continue

    if 'FOXPUFF' in cl: # 빳지심
        item_list.append(cl)
        item_list.append('')
        if 'SBD' in cl: # S보드인 경우
            item_list.append('1'); item_list.append('족'); item_list.append('')
            item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('')
        else: # 케미시트인 경우
            item_list.append('1'); item_list.append(''); item_list.append('')
            item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('300')

        item_list_all.append(item_list)
        item_list = []
        continue

    if '_O_' in cl: # 아웃솔 + (고무족창,고무판창 등)
        if '_DR' in cl or '_WR' in cl or '_WA' in cl or '_RAWRB' in cl:
            item_list.append(cl)
            item_list.append('')
            item_list.append('1'); item_list.append('족'); item_list.append('')
            item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('400')
            item_list_all.append(item_list)
            item_list = []
            continue
        
        else: # 아웃솔만 있는 경우
            item_list.append(cl)
            item_list.append('')
            item_list.append('1'); item_list.append('족'); item_list.append('')
            item_list.append(''); item_list.append(''); item_list.append(''); item_list.append('')
            item_list_all.append(item_list)
            item_list = []
            continue

    if '_CI_' in cl: # 컵인솔+제조사명
        if cl[-1:] == 'A' or cl[-1:] == 'B' or cl[-1:] == 'F' or cl[-1:] == 'Y':
            item_list.append(cl)
            item_list.append('')
            item_list.append('1'); item_list.append('족'); item_list.append('')
            item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('800')
            item_list_all.append(item_list)
            item_list = []
            continue
        
        elif '_CI_CF' in cl or '_CI_903B' in cl or '_CI_ELIM' in cl: # 컵인솔 + *
            item_list.append(cl)
            item_list.append('')
            item_list.append('1'); item_list.append('족'); item_list.append('')
            item_list.append('2'); item_list.append(''); item_list.append(''); item_list.append('600')
            item_list_all.append(item_list)
            item_list = []
            continue
        
        else: # 컵인솔만 있는 경우
            item_list.append(cl)
            item_list.append('')
            item_list.append('1'); item_list.append('족'); item_list.append('')
            item_list.append('0'); item_list.append(''); item_list.append(''); item_list.append('')
            item_list_all.append(item_list)
            item_list = []
            continue
            
    item_list.append(cl)
    item_list.append('')
    item_list.append('1'); item_list.append(''); item_list.append('')
    item_list.append(''); item_list.append(''); item_list.append(''); item_list.append('')
    item_list_all.append(item_list)
    item_list = []

f.close() # 파일 닫기





df = pd.DataFrame(item_list_all, columns = ['품목코드', '품목명','규격구분','규격','', '품목구분', '','', '생산공정'])
df = df.set_index('품목코드')
df.to_csv('./bom생성/'+ file_name +'_품목등록.csv', encoding="euc-kr")



