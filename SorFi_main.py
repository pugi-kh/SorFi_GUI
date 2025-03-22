# ** SorFi -> Files assorting program.
# 클래스, 예외처리 등을 추가적으로 활용하여 GUI 프로그래밍
# tk-inter 활용

from tkinter import *
import tkinter.messagebox as msgbox
import os
import shutil
from SorFi_run import *

root = Tk() # root.mainloop() 사이에 작성

root.title("SorFi_Files Assorting Program")
root.iconbitmap('./resource/SorFi_icon_2.ico')
appWidth = 480
appHeight = 640
widthPosition = (root.winfo_screenwidth()/2) - (appWidth/2)
heightPosition = (root.winfo_screenheight()/2) - (appHeight/2)
root.geometry(f"{appWidth}x{appHeight}+{int(widthPosition)}+{int(heightPosition)}")

customFont1 = ("", 10)
customFont2 = ("", 14, "bold")


class SourceFrame: # 동작할 폴더 경로 입력 프레임
    def __init__(self):
        sourceFrame = LabelFrame(root, text="파일 경로")
        sourceFrame.pack(fill="x", padx=10, pady=10, ipady=4)

        # 저장경로 입력 Entry
        sourceEntry = StringVar()
        sourceEntry.set("C:\\")
        self.path = Entry(sourceFrame, textvariable=sourceEntry) # 한줄로만 입력하는 텍스트박스 Entry
        self.path.pack(side = "left", fill = "x", expand=True, ipady=4, padx=5, pady=10) 
        # 수평으로 길게 fill, i(nner)pady높이 변경
        # Entry가 좌측으로 정렬되어 가로로 길게 채워지고, 내부에 y축 방향으로 4 높이 여백 생성
        # 외부로 10 여백 생성

        # 위치 찾아보기 Button
        btn = Button(sourceFrame, text = "찾아보기", width = 10, command=self.find_dir, font=customFont1)
        btn.pack(side = "right", padx=10, pady=10) 
        # 경로를 입력하는 Entry 우측에 찾아보기 버튼 추가
        
    def find_dir(self):
        print("find dir")
        
class OptionFrame: # 폴더명 생성 방식 옵션
    def __init__(self, int):
        optFrame = LabelFrame(root, text="옵션")
        optFrame.pack(fill="x", padx=10, pady=10, ipady=5)
        
        self.optVar = IntVar()
        optButton1 = Radiobutton(optFrame, text="폴더명 직접 입력", 
                                    value=1, variable=self.optVar, 
                                    command=self.folderOptions, 
                                    font=customFont1)
        optButton2 = Radiobutton(optFrame, text="자리수를 지정하여 폴더명 생성", 
                                    value=2, variable=self.optVar, 
                                    command=self.folderOptions, 
                                    font=customFont1)
        if(int==1):
            optButton1.select()
        elif(int==2):
            optButton2.select()
            
        # optVar.get() 메서드를 사용하면 value값을 반환 -> folderOptions 함수 실행
        optButton1.pack(side="left", padx=10)
        optButton2.pack(side="left", padx=(50,0))
        
    def folderOptions(self):
        print("< 폴더명 생성 옵션 변경 >") 
        folderNameFrame.option(self.optVar.get()) # 프레임이 달라서 FolderNameFrame 클래스에서 실행

class FolderNameFrame: # 생성할 폴더명 리스트박스
    # 인터페이스 생성
    def __init__(self, var): 
    # 폴더명 메인 프레임
        self.frame = LabelFrame(root, text="폴더명") 
        self.frame.pack(fill="both", expand=True, padx=10, pady=10, ipady=4)
        
        # 폴더명 작성방식 프레임 -> 내용은 self.option 에서 작성
        self.addFolderFrame = Frame(self.frame) 
        self.addFolderFrame.pack(side="top", fill="x")
        self.option(1)
        
        
        # 폴더 리스트 프레임(하단) -> 리스트박스, 스크롤바, 선택삭제 버튼
        self.listFrame = Frame(self.frame) # 리스트 프레임 생성
        self.listFrame.pack(fill="both", expand=True)
        
            # 폴더 리스트박스 프레임(하단-좌)
        self.listFrame_L = Frame(self.listFrame)
        self.listFrame_L.pack(side="left", expand=True , fill="both", padx=5, pady=5)
            # 스크롤바, 리스트박스 만들기
        scrollbar = Scrollbar(self.listFrame_L) # 스크롤바 생성
        scrollbar.pack(side = "right", fill = "y") # 스크롤바 우측으로 밀고 Y축에 맞게 늘리기
            # list_frame_L 안에 만들고, 크기 등 설정 후 yscrollcommand=scrollbar.set 를 통해 스크롤바 연동
        self.folderList = Listbox(self.listFrame_L, selectmode="extended", yscrollcommand=scrollbar.set, font=customFont1)
        self.folderList.pack(side="bottom", fill="both", expand=True)
        scrollbar.config(command = self.folderList.yview) # 스크롤바에도 리스트박스 연결
        
        # 폴더 리스트박스 선택삭제 프레임(하단-우)
        self.listFrame_R = Frame(self.listFrame) # 우측 리스트 프레임 생성
        self.listFrame_R.pack(side="right", fill="both")
            # 선택삭제 버튼
        deleteBtn = Button(self.listFrame_R, text="선택삭제", width=10, 
                           command=self.deleteSelections, font=customFont1)
        deleteBtn.pack(side="top", padx=10, pady=5)
            # 자리수 확인 버튼
        chkDigitBtn = Button(self.listFrame_R, text="자리수 확인", width=10, 
                             command=lambda : CheckDigit(), font=customFont1)
        chkDigitBtn.pack(side="top", padx=10, pady=5)
            # 리스트 초기화 버튼
        resetBtn = Button(self.listFrame_R, text="목록 초기화", width=10, 
                          command=self.resetList, font=customFont1)
        resetBtn.pack(side="bottom", padx=10, pady=5)
        
        # 설명 (폴더명 메인 프레임 하단)
        explanation = Label(self.frame, fg="gray", 
                            text="※ 파일명이 폴더명을 포함하고 있는 경우 해당 폴더로 이동")
        explanation.pack(side="left", padx=5)
        
    # functions
    def option(self, var): # 폴더명 작성 방식에 따른 gui 구성
        for wiget in self.addFolderFrame.winfo_children():
            wiget.destroy()
        if (var == 1):
            print("폴더명 직접 입력 방식")
                # 폴더명 Entry (상단-좌)
            self.folderNameEntry = Entry(self.addFolderFrame)
            self.folderNameEntry.pack(side="left", fill="x", expand=True, ipady=4, padx=5, pady=10)
                # 추가 Button (상단-우)
            folderNameBtn = Button(self.addFolderFrame, text = "추가", width = 10, 
                                   command=self.addFolderName, font=customFont1)
            folderNameBtn.pack(side="right", padx=10, pady=10)
            
        elif (var == 2):
            print("자리수 지정해서 폴더명 생성 방식")
                # 폴더명 Entry (상단-좌)
            startNumTxt = Label(self.addFolderFrame, text="시작 위치 : ", font=customFont1)
            startNumTxt.pack(side="left", padx=(5,0), pady=10)
            self.startNum = Entry(self.addFolderFrame, width=5)
            self.startNum.pack(side="left", fill="x", expand=True, ipady=4)
            
            endNumTxt = Label(self.addFolderFrame, text="끝 위치 : ", font=customFont1)
            endNumTxt.pack(side="left", padx=(5,0), pady=10)
            self.endNum = Entry(self.addFolderFrame, width=5)
            self.endNum.pack(side="left", fill="x", expand=True, ipady=4, padx=5, pady=10)
            
                # Entry 기본값 설정
            self.startNum.insert(0, "1")
            self.endNum.insert(0, "1")
            
                # 추가 Button (상단-우)
            folderNameBtn = Button(self.addFolderFrame, text = "생성", width = 10, 
                                   command=self.createFolderNameBtn, font=customFont1)
            folderNameBtn.pack(side="right", padx=10, pady=10)
        
    def createFolderNameBtn(self): # 입력받은 번호를 idx번호로 변경
        try:
            start_idx = int(self.startNum.get())
            end_idx = int(self.endNum.get())
            if(start_idx <=0 or end_idx <=0 or start_idx > end_idx): # 양의정수가 아니거나 시작인덱스가 클 경우 오류 발생
                raise Exception
            self.createFolderName(start_idx, end_idx)
        except:
            msgbox.showwarning("잘못된 입력", "\"시작위치\" 혹은 \"끝 위치\"에 올바른 값을 입력해주세요.\n(양의 정수만 입력 가능)")
            
    def createFolderName(self, sIdx, eIdx): # idx번호를 기반으로 폴더명 추출 실행
        print(f"파일명에서 추출 >> 시작 idx : {sIdx}, 끝 idx : {eIdx}")
        
    def addFolderName(self): # 폴더명 직접 작성하여 추가
        print("add folder name >> ", self.folderNameEntry.get())
        # 항목이 없을때만 추가
        if(self.folderNameEntry.get() not in self.folderList.get(0, END) and self.folderNameEntry.get() != ""):
            self.folderList.insert(END, self.folderNameEntry.get())
        
    def deleteSelections(self): # 폴더명 선택 삭제
        index = self.folderList.curselection()
        for i in index:
            print(self.folderList.delete(i))
        
    def resetList(self): # 리스트박스 내 폴더명 전체 삭제
        self.folderList.delete(0, END)
        
class CheckDigit: # 파일명 입력하여 문자열 자리수 확인
    def __init__(self):
        self.window = Tk()
        self.window.title("SorFi_Check Digit")
        self.window.iconbitmap('./resource/SorFi_icon_2.ico')
        self.appWidth = 640
        self.appHeight = 180
        self.widthPosition = (self.window.winfo_screenwidth()/2) - (self.appWidth/2)
        self.heightPosition = (self.window.winfo_screenheight()/2) - (self.appHeight/2)
        self.window.geometry(f"+{int(self.widthPosition)}+{int(self.heightPosition)}")
        
        line1 = Frame(self.window)
        line1.pack(side="top", fill="both", padx=10, pady=(10,0))
        txt = Label(line1, text="파일명 붙여넣기")
        txt.pack(side="left", padx=5)
        line2 = Frame(self.window)
        line2.pack(side="top", fill="both", padx=10, pady=0)
        self.fileName = Entry(line2, width=40)
        self.fileName.pack(side = "left", fill = "x", expand=True, ipady=4, padx=5, pady=(0, 10)) 
        
        enter = Button(line2, text="확인", width=10, command=self.check)
        enter.pack(side="right", padx=10, pady=(0, 10))
        
        self.line3 = LabelFrame(self.window, text="")
        self.line3.pack(fill="both", padx=15, pady=(0, 10))
        
        
        self.window.mainloop()
        
    def check(self):
        print(self.fileName.get())
        for wiget in self.line3.winfo_children():
            wiget.destroy()
        txtList = [x for x in self.fileName.get()]
        result = Label(self.line3, text="  ".join(txtList), font=("Courier New", 10, "bold"))
        result.pack()
        
        index = [format(i,"02") for i in range(1, len(self.fileName.get())+1)]
        print(index)
        resultIdx = Label(self.line3, text=index, font=("Courier New", 10, "bold"))
        resultIdx.pack()
        
class CheckDigitOption: # 문자열 위치 확인 여부
    def __init__(self):
    # 메인 프레임
        self.frame = LabelFrame(root, text="문자열 위치 확인")
        self.frame.pack(side="bottom", fill="x", padx=10, pady=10, ipady=5)
        # 확인 체크박스
        self.chkVar = IntVar()
        self.chkBox = Checkbutton(self.frame, 
                                  text="해당 문자열 위치 확인",
                                  variable=self.chkVar, 
                                  command=self.chkIdx, 
                                  font=customFont1)
        self.chkBox.pack(side="left", padx=10, pady=10)
            
       
        # 비활성화된 옵션 (나중에 다시 정리)
        self.xchkIdxTxt = Label(self.frame, text="시작 위치 : ", state="disabled", font=customFont1)
        self.xstartIdx = Entry(self.frame, width=5, state="disabled")
        self.xchkIdxTxt2 = Label(self.frame, text="번째 자리부터", state="disabled", font=customFont1)
        self.xchkIdxTxt.pack(side="left", padx=(10,0))
        self.xstartIdx.pack(side = "left", ipady=4)
        self.xchkIdxTxt2.pack(side="left")
        
        self.chkIdxTxt = Label(self.frame, text="시작 위치 : ", font=customFont1)
        self.startIdx = Entry(self.frame, width=5)
        self.chkIdxTxt2 = Label(self.frame, text="번째 자리부터", font=customFont1)
        

    def chkIdx(self):
        if(self.chkVar.get()==1):
            print("문자열 위치 확인")
            self.xchkIdxTxt.pack_forget()
            self.xstartIdx.pack_forget()
            self.xchkIdxTxt2.pack_forget()
            
            self.chkIdxTxt.pack(side="left", padx=(10,0))
            self.startIdx.pack(side = "left", ipady=4)
            self.chkIdxTxt2.pack(side="left")
            
        elif(self.chkVar.get()==0):
            print("문자열 위치 확인 안함")
            self.chkIdxTxt.pack_forget()
            self.startIdx.pack_forget()
            self.chkIdxTxt2.pack_forget()
            
            self.xchkIdxTxt.pack(side="left", padx=(10,0))
            self.xstartIdx.pack(side = "left", ipady=4)
            self.xchkIdxTxt2.pack(side="left")
        
class RunFrame: # 설정 저장 및 실행 (SorFi_run에 메서드 작성)
    run_frame = Frame(root)
    run_frame.pack(side="bottom", fill="x", padx=10, pady=10, expand=True)


    run_frame_L = Frame(run_frame)
    run_frame_L.pack(side="left", fill="both")
    
    run_frame_L2 = Frame(run_frame_L) # 설정저장 및 불러오기 프레임
    run_frame_L2.pack(side="left", fill="both")
    # 설정 저장
    btn_save_opt = Button(run_frame_L2, text="설정 저장", font=customFont1)
    btn_save_opt.pack(side="bottom", padx=5, pady=10, fill="both")
    # 설정 불러오기
    btn_read_opt = Button(run_frame_L2, text="설정 불러오기", font=customFont1)
    btn_read_opt.pack(side="bottom", padx=5, pady=0, fill="both")

    # 되돌리기
    run_frame_L3 = Frame(run_frame_L) # 되돌리기 프레임
    run_frame_L3.pack(side="left", fill="both", expand=True)
    btn_revert = Button(run_frame_L3, text="되돌리기", width=10, font=customFont1)
    btn_revert.pack(side="bottom", padx=5, pady=10, fill="both")


    # 실행버튼 프레임
    run_frame_R = Frame(run_frame)
    run_frame_R.pack(side="right", fill="both", expand=True)
    # 실행
    btn_run = Button(run_frame_R, text="실행", width=10, height=2, font=customFont2, background="gray80")
    btn_run.pack(side="right", padx=5, pady=10)


sourceFrame = SourceFrame() # 파일 경로 프레임 생성
print(f"파일 경로 : {sourceFrame.path.get()}")
optFrame = OptionFrame(1) # 옵션 프레임 생성
folderNameFrame = FolderNameFrame(optFrame.optVar.get())
chkDigit = CheckDigitOption() # 문자열 자리수 확인 옵션

root.mainloop()
