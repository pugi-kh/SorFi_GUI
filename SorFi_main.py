# ** SorFi -> Files assorting program.
# 클래스, 예외처리 등을 추가적으로 활용하여 GUI 프로그래밍
# tk-inter 활용

from tkinter import *

root = Tk() # root.mainloop() 사이에 작성

root.title("SorFi_Files Assorting Program")
root.iconbitmap('./resource/SorFi_icon.ico')
root.geometry("480x640")

"""소스파일 경로 프레임"""
class SourceFrame:
    def __init__(self):
        self.sourceFrame = LabelFrame(root, text="파일 경로")
        self.sourceFrame.pack(fill="x", padx=10, pady=10, ipady=4)

        # 저장경로 입력 Entry
        dest_path = Entry(self.sourceFrame) # 한줄로만 입력하는 텍스트박스 Entry
        dest_path.pack(side = "left", fill = "x", expand=True, ipady=4, padx=5, pady=10) 
        self.dest_path = dest_path # self를 이용하여 클래스에 값 매핑
        # 수평으로 길게 fill, i(nner)pady높이 변경
        # Entry가 좌측으로 정렬되어 가로로 길게 채워지고, 내부에 y축 방향으로 4 높이 여백 생성
        # 외부로 10 여백 생성

        # 위치 찾아보기 Button
        btn_dest_path = Button(self.sourceFrame, text = "찾아보기", width = 10, command=self.find_dir)
        btn_dest_path.pack(side = "right", padx=10, pady=10) 
        # 경로를 입력하는 Entry 우측에 찾아보기 버튼 추가
    def get(self):
        print(self.dest_path.get()) # self로 매핑한 값 사용
    def find_dir(self):
        print("running find_dir")
        
class OptionFrame:
    def __init__(self):
        self.optFrame = LabelFrame(root, text="옵션")
        self.optFrame.pack(fill="x", padx=10, pady=10, ipady=5)
        
        folder_var = IntVar()
        rbt_folder_name1 = Radiobutton(self.optFrame, text="폴더명 직접 입력", 
                                    value=1, variable=folder_var, command=self.folder_options)
        rbt_folder_name1.select()
        rbt_folder_name2 = Radiobutton(self.optFrame, text="자리수를 지정하여 폴더명 생성", 
                                    value=2, variable=folder_var, command=self.folder_options)
        # folder_var.get() 메서드를 사용하면 value값을 반환 -> folder_options 함수 실행
        rbt_folder_name1.pack(side="left", padx=10)
        rbt_folder_name2.pack(side="left", padx=60)
    def folder_options(self):
        print("folder_options")

sourceFrame = SourceFrame()
optFrame = OptionFrame()

root.mainloop()
