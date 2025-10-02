from tkinter import *

def fol_write_frame(fol_opt_frame):
    """폴더명"""
    folder_name_frame = LabelFrame(fol_opt_frame, text="폴더명")
    folder_name_frame.pack(fill="x", padx=10, pady=10, ipady=4)
    
    """폴더명/폴더명 추가"""
    add_folder_frame = Frame(folder_name_frame)
    add_folder_frame.pack(side="top", fill="x")
    
    # 폴더명 Entry, 추가 Button
    txt_folder_name = Entry(add_folder_frame)
    txt_folder_name.pack(side="left", fill="x", expand=True, ipady=4, padx=5, pady=10)
    
    btn_folder_name = Button(add_folder_frame, text = "추가", width = 10)
    btn_folder_name.pack(side="right", padx=10, pady=10)
    
    """폴더명/폴더명 리스트"""
    list_frame = Frame(folder_name_frame) # 리스트 프레임 생성
    list_frame.pack(fill="both")
    
    
    # 좌측 리스트 프레임 생성 (리스트 박스)
    list_frame_L = Frame(list_frame)
    list_frame_L.pack(side="left", expand=True , fill="both", padx=5, pady=5) # 리스트박스의 좌우 여백이 남아서 좌우 여백 제거

    # 스크롤바, 리스트박스 만들기
    scrollbar = Scrollbar(list_frame_L) # 스크롤바 생성
    scrollbar.pack(side = "right", fill = "y") # 스크롤바 우측으로 밀고 Y축에 맞게 늘리기
    # list_frame_L 안에 만들고, 크기 등 설정 후 yscrollcommand=scrollbar.set 를 통해 스크롤바 연동
    list_file = Listbox(list_frame_L, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
    list_file.pack(side="bottom", fill="both", expand=True)
    scrollbar.config(command = list_file.yview) # 스크롤바에도 리스트박스 연결
    
    
    
    # 우측 리스트 프레임 생성 (선택삭제 버튼)
    list_frame_R = Frame(list_frame) # 우측 리스트 프레임 생성
    list_frame_R.pack(side="right", fill="both")
    
    btn_delete = Button(list_frame_R, text="선택삭제", width=10)
    btn_delete.pack(side="bottom", padx=10, pady=10)
    
    
    """자리수 일치여부"""
    pos_option_frame = LabelFrame(fol_opt_frame, text="문자열 자리 일치 여부")
    pos_option_frame.pack(fill="x", padx=10, pady=10, ipady=4)
    
    

    
    """자리수 확인 위치""" # 자리수 일치여부 확인시
    
    
    
    
def fol_count_frame(fol_opt_frame):
    """폴더명 프레임"""
    folder_name_frame = LabelFrame(fol_opt_frame, text="폴더명")
    folder_name_frame.pack(fill="x", padx=10, pady=10, ipady=4)
    """자리수 일치여부"""