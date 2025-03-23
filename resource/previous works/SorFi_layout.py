# ** SorFi -> Files assorting program.
# 클래스, 예외처리 등을 추가적으로 활용하여 GUI 프로그래밍
# tk-inter 활용

'''
project) SorFi_파일들을 정리하는 프로그램

[사용자 시나리오]
1. 사용자는 정리할 파일들이 있는 최상위 폴더의 경로를 지정한다.
2. 어떤 기준으로 파일을 정리할 것인지 선택한다.
    2-1. 파일명을 앞에서부터 자리수를 선택해 해당하는 자리의 문자열을 폴더명으로 지정.
        (ex. 1~4번째 자리가 ABCD인 파일들이 있으면 ABCD폴더 생성.)
    2-2. 폴더명을 직접 입력
    2-3. 자리수와 상관없이 진행할 것인지 자리수일치해야 정리할 것인지 선택
3. 2번까지 완료되면 리스트박스에 폴더명들이 생성됨.
4. 정리시작 버튼을 누르면 어떤 기준으로 어떻게 정리할 것인지 한번 알림창으로 다시 설명 후 확인 or 취소 버튼 생성
5. 알림창에서 확인을 누르면 파일 이동 작업 시작.
6. 되돌리기 버튼을 눌러 이동한 파일들을 다시 되돌리고, 만들었던 폴더는 삭제한다.
7. 작업을 저장할 수 있게 만들어 "해당 위치에서 동일한 이름의 폴더를 생성해 파일을 정리"하는 루틴을 등록할 수 있도록 함.
8. X를 눌러서 프로그램 종료

[기능 명세]
1. 폴더 경로 지정 : 정리할 파일들이 있는 폴더의 경로 입력
2. 폴더명 생성 방식 : "파일명 자리수 입력" 혹은 "직접 작성" 라디오버튼을 통해 인터페이스 변경
3. 파일명 자리수 입력 : 예시로 하나의 파일을 불러와 몇번째 자리인지 한눈에 보이도록
4. 폴더명 직접 작성 : 리스트 박스에 폴더 이름 추가
5. 자리 일치 여부 : 해당 문자열이 위치한 자리도 동일해야 작업을 진행할 것인지 선택 (Default : yes)
6. 작업 진행 여부 확인 : 작업 진행 버튼 클릭시 작업에 대한 설명을 명세한 알림창 팝업
7. 루틴 저장 : 1 ~ 5까지의 작업을 저장해 추후에 불러왔을 때 바로 실행만 할 수 있도록
8. 루틴 실행 : 루틴이 실행파일로 저장되어 실행시 프로그램은 동일하게 켜지는데 선택해야 될 옵션들이 미리 저장해놓은 값들로 지정되어 있는 상태.
9. 루틴 불러오기 : 프로그램을 기본으로 켰는데 루틴을 불러오면 저장된 옵션들이 적용.
'''

from tkinter import *
# from tkinter import font

root = Tk() # root.mainloop() 사이에 작성

root.title("SorFi_Files Assorting Program")
root.iconbitmap('./resource/SorFi_icon.ico')
root.geometry("480x640")
# root.resizable(False, False) # x(너비), y(높이) 값 수정 가능 여부 (창 크기 변경 불가)

# # 기본 폰트 설정 --> 모르게따아아
# font_path = "./Font/Pretendard-Regular.ttf"
# font_size = 20

# custom_font = font.Font(family="Pretendard-Regular", size = font_size)


"""소스파일 경로 프레임"""
source_frame = LabelFrame(root, text="파일 경로")
source_frame.pack(fill="x", padx=10, pady=10, ipady=4)

# 저장경로 입력 Entry
txt_dest_path = Entry(source_frame) # 한줄로만 입력하는 텍스트박스 Entry
txt_dest_path.pack(side = "left", fill = "x", expand=True, ipady=4, padx=5, pady=10) 
# 수평으로 길게 fill, i(nner)pady높이 변경
# Entry가 좌측으로 정렬되어 가로로 길게 채워지고, 내부에 y축 방향으로 4 높이 여백 생성
# 외부로 10 여백 생성

# 위치 찾아보기 Button
btn_dest_path = Button(source_frame, text = "찾아보기", width = 10)
btn_dest_path.pack(side = "right", padx=10, pady=10) 
# 경로를 입력하는 Entry 우측에 찾아보기 버튼 추가


"""옵션 프레임"""
opt_frame = LabelFrame(root, text="옵션")
opt_frame.pack(fill="x", padx=10, pady=10, ipady=5)

# 폴더명 옵션 command
# 프레임 삭제하고 새로 만들기
def folder_options():
    for widget in fol_opt_frame.winfo_children(): # 프레임 내부 위젯 삭제
        widget.destroy()
    if(folder_var.get() == 1) : 
        fol_write_frame(fol_opt_frame)
    elif(folder_var.get() == 2) : 
        fol_count_frame(fol_opt_frame)
    return

# 폴더명 생성옵션1        
def fol_write_frame(fol_opt_frame):
    """폴더명"""
    folder_name_frame = LabelFrame(fol_opt_frame, text="폴더명")
    folder_name_frame.pack(fill="both", expand=True, padx=10, pady=10, ipady=4)
    
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
    list_frame.pack(fill="both", expand=True)
    
    
    # 좌측 리스트 프레임 생성 (리스트 박스)
    list_frame_L = Frame(list_frame)
    list_frame_L.pack(side="left", expand=True , fill="both", padx=5, pady=5) # 리스트박스의 좌우 여백이 남아서 좌우 여백 제거

    # 스크롤바, 리스트박스 만들기
    scrollbar = Scrollbar(list_frame_L) # 스크롤바 생성
    scrollbar.pack(side = "right", fill = "y") # 스크롤바 우측으로 밀고 Y축에 맞게 늘리기
    # list_frame_L 안에 만들고, 크기 등 설정 후 yscrollcommand=scrollbar.set 를 통해 스크롤바 연동
    list_file = Listbox(list_frame_L, selectmode="extended", yscrollcommand=scrollbar.set)
    list_file.pack(side="bottom", fill="both", expand=True)
    scrollbar.config(command = list_file.yview) # 스크롤바에도 리스트박스 연결
    
    
    
    # 우측 리스트 프레임 생성 (선택삭제 버튼)
    list_frame_R = Frame(list_frame) # 우측 리스트 프레임 생성
    list_frame_R.pack(side="right", fill="both")
    
    btn_delete = Button(list_frame_R, text="선택삭제", width=10)
    btn_delete.pack(side="top", padx=10, pady=5)
    
    txt_explanation = Label(folder_name_frame, fg="gray", text="※ 파일명이 폴더명을 포함하고 있는 경우 해당 폴더로 이동")
    txt_explanation.pack(side="left", padx=5)
    
    
    # 자리 확인 옵션
    pos_option(fol_opt_frame)
    
    return

# 폴더명 생성옵션2
def fol_count_frame(fol_opt_frame):
    """폴더명 프레임"""
    folder_name_frame = LabelFrame(fol_opt_frame, text="폴더명")
    folder_name_frame.pack(fill="x", padx=10, pady=10, ipady=4)
    """자리수 일치여부"""
    return

# 자리수 일치여부 확인할 것인지
pos_var = IntVar()
def pos_option(pos_option_frame) :
    pos_option_frame = LabelFrame(fol_opt_frame, text="문자열 위치 확인")
    pos_option_frame.pack(side="bottom", fill="x", padx=10, pady=10, ipady=5)
    
    # 문자열 확인위치 들어갈 프레임
    pos_option_frame_R = Frame(pos_option_frame)
    pos_option_frame_R.pack(side="right", fill="both")

    def chk_pos_opt():
        if(pos_var == 1):
            test = Label(pos_option_frame_R, text="disabled")
            test.pack()
        elif(pos_var == 2):
            test = Label(pos_option_frame_R, text="normal")
            test.pack()
        
    # 시작위치 활/비활
    # 선택에 따라 동작 수행
    rbt_pos_option1 = Radiobutton(pos_option_frame, text="확인 안함", 
                                value=1, variable=pos_var, command=chk_pos_opt)
    rbt_pos_option2 = Radiobutton(pos_option_frame, text="해당 문자열 위치 확인", 
                                value=2, variable=pos_var, command=chk_pos_opt)
    rbt_pos_option2.select()
    rbt_pos_option1.pack(side="left", padx=10)
    rbt_pos_option2.pack(side="left", padx=0)
    return



"""폴더명 생성기준 선택"""
folder_var = IntVar()
rbt_folder_name1 = Radiobutton(opt_frame, text="폴더명 직접 입력", 
                               value=1, variable=folder_var, command=folder_options)
rbt_folder_name1.select()
rbt_folder_name2 = Radiobutton(opt_frame, text="자리수를 지정하여 폴더명 생성", 
                               value=2, variable=folder_var, command=folder_options)
# folder_var.get() 메서드를 사용하면 value값을 반환 -> folder_options 함수 실행
rbt_folder_name1.pack(side="left", padx=10)
rbt_folder_name2.pack(side="left", padx=60)


# 옵션 프레임의 선택 결과에 따라 하위 요소 실행
fol_opt_frame = Frame(root)
fol_opt_frame.pack(fill="both", expand=True)
fol_write_frame(fol_opt_frame) # 우선 기본값으로 fol_write_frame 실행


"""실행 프레임"""
run_frame = Frame(root)
run_frame.pack(side="bottom", fill="x", padx=10, pady=10)


run_frame_L = Frame(run_frame)
run_frame_L.pack(side="left", fill="both")
run_frame_L2 = Frame(run_frame_L)
run_frame_L2.pack(side="bottom", fill="both")
# 설정 저장
btn_save_opt = Button(run_frame_L2, text="설정 저장", width=10)
btn_save_opt.pack(side="left", padx=5, pady=10)
# 설정 불러오기
btn_read_opt = Button(run_frame_L2, text="설정 불러오기", width=12)
btn_read_opt.pack(side="left", padx=5, pady=10)

# 되돌리기
btn_revert = Button(run_frame_L2, text="되돌리기", width=10)
btn_revert.pack(side="right", padx=5, pady=10)
txt_space = Label(run_frame_L2, text = "            ")
txt_space.pack(side="right")



run_frame_R = Frame(run_frame)
run_frame_R.pack(side="right", fill="both")
# 실행
btn_run = Button(run_frame_R, text="실행", width=15, height=3)
btn_run.pack(side="right", padx=5, pady=10)
# # 되돌리기
# btn_revert = Button(run_frame_R, text="되돌리기", width=10)
# btn_revert.pack(side="right", padx=5, pady=10)

root.mainloop()