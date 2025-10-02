# ** SorFi -> Files assorting program.
# 클래스, 예외처리 등을 추가적으로 활용하여 GUI 프로그래밍
# tk-inter 활용

from tkinter import *
import tkinter.messagebox as msgbox
import tkinter.filedialog as filedialog
import os
import json
import shutil

root = Tk() # root.mainloop() 사이에 작성

root.title("SorFi_Files Assorting Program")
root.iconbitmap('./resource/icon/SorFi_icon_2.ico')
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
        sourceFrame.pack(side="top", fill="x", padx=10, pady=10, ipady=4)

        # 저장경로 입력 Entry
        self.sourcePath = StringVar()
        self.sourcePath.set("")
        path = Entry(sourceFrame, textvariable=self.sourcePath)
        path.pack(side = "left", fill = "x", expand=True, ipady=4, padx=5, pady=10) 

        # 위치 찾아보기 Button
        btn = Button(sourceFrame, text = "찾아보기", width = 10, 
                     command=self.find_dir, font=customFont1)
        btn.pack(side = "right", padx=10, pady=10) 
        
    def find_dir(self): # 폴더검색창
        # print("find dir")
        dirPath = filedialog.askdirectory(initialdir = self.sourcePath.get(), 
                                          title="폴더를 선택해주세요")
        if(dirPath==""): pass
        elif(os.path.isdir(dirPath)):
            self.sourcePath.set(dirPath)
        
class OptionFrame: # 폴더명 생성 방식 옵션
    def __init__(self, int):
        optFrame = LabelFrame(root, text="옵션")
        optFrame.pack(side="top", fill="x", padx=10, pady=10, ipady=5)
        
        # 옵션 변수
        self.optVar = IntVar()
        # 옵션 선택
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
        # 프레임이 달라서 FolderNameFrame 클래스에서 실행
        folderNameFrame.option(self.optVar.get()) 

class FolderNameFrame: # 생성할 폴더명 리스트박스
    # 인터페이스 생성
    def __init__(self, var): 
    # 폴더명 메인 프레임
        self.frame = LabelFrame(root, text="폴더명") 
        self.frame.pack(side="top" ,fill="both", expand=True, padx=10, pady=10, ipady=4)
        
        # 폴더명 작성방식 프레임 -> 내용은 self.option 에서 작성
        self.addFolderFrame = Frame(self.frame) 
        self.addFolderFrame.pack(side="top", fill="x")
        self.option(var)
        
        
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
                             command=lambda : CheckDigitExample(), font=customFont1)
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
            # print("폴더명 직접 입력 방식")
                # 폴더명 Entry (상단-좌)
            self.folderNameEntry = Entry(self.addFolderFrame)
            self.folderNameEntry.pack(side="left", fill="x", expand=True, ipady=4, padx=5, pady=10)
            
            # Enter키 이벤트 바인딩
            self.folderNameEntry.bind("<Return>", self.addFolderName)
            
                # 추가 Button (상단-우)
            folderNameBtn = Button(self.addFolderFrame, text = "추가", width = 10, 
                                   command=self.addFolderName, font=customFont1)
            folderNameBtn.pack(side="right", padx=10, pady=10)
        elif (var == 2):
            # print("자리수 지정해서 폴더명 생성 방식")
                # 폴더명 시작번호 idx
            startNumTxt = Label(self.addFolderFrame, text="시작 위치 : ", font=customFont1)
            startNumTxt.pack(side="left", padx=(5,0), pady=10)
            self.startNum = Entry(self.addFolderFrame, width=5)
            self.startNum.pack(side="left", fill="x", expand=True, ipady=4)
                # 폴더명 끝번호 idx
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
        
    def createFolderNameBtn(self): # 입력받은 idx를 기반으로 폴더명 생성
        
        userPath = sourceFrame.sourcePath.get()
        try:
            start_idx = int(self.startNum.get().strip())
            end_idx = int(self.endNum.get().strip())
            
            # 양의정수가 아니거나 시작인덱스가 클 경우 오류 발생
            if(start_idx <=0 or start_idx > end_idx): 
                raise Exception
        except:
            msgbox.showwarning("잘못된 입력", "\"시작위치\" 혹은 \"끝 위치\"에 올바른 값을 입력해주세요.\n(양의 정수만 입력 가능)")
            
        temp_file = os.listdir(userPath)
        fileList = [file for file in temp_file if os.path.isfile(userPath+"/"+file)]
        folderSet = set()
        for file in fileList:
            folderSet.add(file[start_idx-1:end_idx].replace(" ", "_"))
        for new_folder in folderSet:
            if new_folder not in list(self.folderList.get(0, END)):
                folderNameFrame.folderList.insert(END, new_folder)
        
    def addFolderName(self): # 폴더명 직접 작성하여 추가
        # 항목이 없을때만 추가
        if(self.folderNameEntry.get() not in self.folderList.get(0, END) and self.folderNameEntry.get() != ""):
            self.folderList.insert(END, self.folderNameEntry.get())
        
    def deleteSelections(self): # 폴더명 선택 삭제
        index = list(self.folderList.curselection())
        index.sort(reverse=True)
        for i in index:
            self.folderList.delete(i)
        '''
        인덱스 순서대로 삭제를 하니 두개 이상 선택했을 경우 앞에서 요소가 삭제되어 기존에 
        선택한 인덱스와 삭제할 인덱스가 맞지 않는 상황이 생겨 의도와 다른 요소가 삭제됨
        인덱스 역순으로 정렬해서 삭제 진행하면 문제 없을 것으로 생각됨
        '''
        
    def resetList(self): # 리스트박스 내 폴더명 전체 삭제
        self.folderList.delete(0, END)
        
class CheckDigitExample: # 파일명 입력하여 문자열 자리수 확인
    def __init__(self):
        self.window = Tk()
        self.window.title("SorFi_Check Digit")
        self.window.iconbitmap('./resource/icon/SorFi_icon_2.ico')
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
        # print("파일명 자리수 확인 >>", self.fileName.get())
        for wiget in self.line3.winfo_children():
            wiget.destroy()
        txtList = [x for x in self.fileName.get()]
        result = Label(self.line3, text="  ".join(txtList), font=("Courier New", 10, "bold"))
        result.pack()
        
        index = [format(i,"02") for i in range(1, len(self.fileName.get())+1)]
        resultIdx = Label(self.line3, text=index, font=("Courier New", 10, "bold"))
        resultIdx.pack()
        
class CheckDigitOption: # 문자열 위치 확인 여부
    def __init__(self):
    # 메인 프레임
        self.frame = LabelFrame(root, text="문자열 위치 확인")
        self.frame.pack(side="top", fill="x", padx=10, pady=10, ipady=0)
        # 확인 체크박스
        self.chkVar = IntVar()
        self.chkBox = Checkbutton(self.frame, 
                                  text="해당 문자열 위치 확인",
                                  variable=self.chkVar, 
                                  command=self.chkIdx, 
                                  font=customFont1)
        self.chkBox.pack(side="left", padx=10, pady=10)
        
        self.startIdxVar = IntVar()
        self.startIdxVar.set(1)
        # 비활성화된 옵션 (나중에 다시 정리)
        self.xchkIdxTxt = Label(self.frame, text="시작 위치 : ", state="disabled", font=customFont1)
        self.xstartIdx = Entry(self.frame, width=5, state="disabled")
        self.xchkIdxTxt2 = Label(self.frame, text="번째 자리부터", state="disabled", font=customFont1)
        self.xchkIdxTxt.pack(side="left", padx=(10,0))
        self.xstartIdx.pack(side = "left", ipady=4)
        self.xchkIdxTxt2.pack(side="left")
        
        # 활성화된 옵션
        self.chkIdxTxt = Label(self.frame, text="시작 위치 : ", font=customFont1)
        self.startIdxEntry = Entry(self.frame, width=5, textvariable=self.startIdxVar)
        self.chkIdxTxt2 = Label(self.frame, text="번째 자리부터", font=customFont1)
        

    def chkIdx(self):
        if(self.chkVar.get()==1):
            # print("문자열 위치 확인")
            self.xchkIdxTxt.pack_forget()
            self.xstartIdx.pack_forget()
            self.xchkIdxTxt2.pack_forget()
            
            self.chkIdxTxt.pack(side="left", padx=(10,0))
            self.startIdxEntry.pack(side = "left", ipady=4)
            self.chkIdxTxt2.pack(side="left")
            
        elif(self.chkVar.get()==0):
            # print("문자열 위치 확인 안함")
            self.chkIdxTxt.pack_forget()
            self.startIdxEntry.pack_forget()
            self.chkIdxTxt2.pack_forget()
            
            self.xchkIdxTxt.pack(side="left", padx=(10,0))
            self.xstartIdx.pack(side = "left", ipady=4)
            self.xchkIdxTxt2.pack(side="left")
            
    # 문자열 위치 확인, 시작인덱스 변수에 저장
    def setIdx(self, idx):
        self.startIdxVar.set(idx)
        self.chkIdx()
        
# 설정 저장 및 실행 (SorFi_run에 메서드 작성)
class RunFrame: 
    def __init__(self):
        run_frame = Frame(root)
        run_frame.pack(side="bottom", fill="both", padx=10, pady=10, expand=True)


        run_frame_L = Frame(run_frame)
        run_frame_L.pack(side="left", fill="both", expand=True)
        
        run_frame_LT = Frame(run_frame_L) # 설정저장 및 불러오기 프레임
        run_frame_LT.pack(side="bottom", fill="x", ipady=10)
        # 설정 저장
        btn_save_opt = Button(run_frame_LT, text="설정 저장", font=customFont1,
                              command=self.setSettings, width=10)
        btn_save_opt.pack(side="left", padx=5, pady=0)
        # 설정 불러오기
        btn_read_opt = Button(run_frame_LT, text="설정 불러오기", font=customFont1,
                              command=self.getSettings, width=10)
        btn_read_opt.pack(side="left", padx=5, pady=0)

        # 되돌리기
        run_frame_LB = Frame(run_frame_L) # 되돌리기 프레임
        run_frame_LB.pack(side="bottom", fill="x")
        btn_revert = Button(run_frame_LB, text="되돌리기", width=10, font=customFont1,
                            command=self.undo)
        btn_revert.pack(side="left", padx=5, pady=0)
        
        txt_revert = Label(run_frame_LB, fg="gray", text="※ 되돌리기는 실행 직후에만 가능합니다!!")
        txt_revert.pack(side="left")


        # 실행버튼 프레임
        run_frame_R = Frame(run_frame)
        run_frame_R.pack(side="right", fill="both")
        run_frame_RB = Frame(run_frame_R)
        run_frame_RB.pack(side="right", fill="both", expand=True)
        # 실행
        btn_run = Button(run_frame_RB, text="실 행", width=10, height=2, font=customFont2, background="gray80",
                         command=self.run)
        btn_run.pack(side="bottom", padx=5, pady=10)
        

        
        
        self.userPath = ""
        self.newFolders = list()
        self.fileList = list()
        self.basefiles = list()

    def run(self):
        try:
            startIdx = int(chkDigit.startIdxEntry.get().strip())
        except:
            msgbox.showwarning("잘못된 입력", "\"문자열 위치 확인\" 부분의의 \"시작위치\"에 올바른 값을 입력해주세요.\n(양의 정수만 입력 가능)")
        self.userPath = sourceFrame.sourcePath.get() + "/"
        self.basefolders = [folder for folder in os.listdir(self.userPath) 
                         if os.path.isdir(self.userPath+folder)]
        
        # 이동할 파일
        self.fileList = [file for file in os.listdir(self.userPath) 
                         if os.path.isfile(self.userPath+file)]
        self.basefiles = self.fileList
        
        # 리스트박스 값 가져오기
        self.newFolders = list(folderNameFrame.folderList.get(0, END))
        
        # 폴더 생성
        for folder in self.newFolders:
            # 생성하려는 폴더명이 기존에 없을 경우 폴더 생성
            if not os.path.exists(self.userPath + folder): 
                os.makedirs(self.userPath + folder)
                
            # 문자열 위치 확인 여부
            lowFolder = "".join(folder).lower().strip("_") # 대소문자 관계없이 정리하기 위해서 검사용 임시시 폴더명 변수 생성성

            if chkDigit.chkVar.get()==1:
                for file in self.fileList:
                    if lowFolder in file[startIdx-1:startIdx + len(folder):].lower(): # 길이는 folder로 확인, 문자는 정리된 lowFolder로 비교
                        shutil.move(self.userPath+file, self.userPath+folder+"/"+file)
            elif chkDigit.chkVar.get()==0:
                for file in self.fileList:
                    if lowFolder in file.lower():
                        shutil.move(self.userPath+file, self.userPath+folder+"/"+file)
        
        # 실행 완료 메시지 출력
        msgbox.showinfo("완료", "정리가 완료되었습니다")


    def undo(self):
        for folder in self.newFolders:
            inner_file_list = os.listdir(self.userPath + folder)
            for file in inner_file_list:
                if file in self.basefiles: # 프로그램 실행시 관여한 파일만 되돌리기기
                    shutil.move(self.userPath + folder + "/" + file, self.userPath + file)
            if folder not in self.basefolders: # 기존에도 이미 이던 폴더는 제외하고고
                try:
                    os.removedirs(self.userPath + folder) # 빈 폴더 삭제
                except:
                    print(f"\"{folder}\" 폴더 삭제 싪패")
            
    def getSettings(self):
# json 파일 불러와서 각각의 변수에 set() 진행
        settingFile = filedialog.askopenfilename(initialdir = sourceFrame.sourcePath.get(), title="설정 불러오기",
                                        filetypes=(("JSON", "*.json"), ("all files", "*.*")))
        # print(settingFile)
        with open(settingFile, "r", encoding="UTF-8") as loadFile:
            json_data = json.load(loadFile)
        # print(json.dumps(json_data, indent=4)) # json 파일 내용 출력
        
        sourceFrame.sourcePath.set(json_data["Run_Path"])
        folderNameFrame.folderList.delete(0, END)
        for list_data in json_data["Folder_name_List"]:
            folderNameFrame.folderList.insert(END, list_data)
        chkDigit.chkVar.set(json_data["Digit_Check_opt"])
        # 문자열 확인 시작 인덱스 설정이 안됨
        chkDigit.setIdx(json_data["Digit_Start_idx"])

    def setSettings(self): # 설정 저장하기
        settingFile = filedialog.asksaveasfilename(title="설정 저장",
                                            filetypes=(("JSON", "*.json"), ("all files", "*.*")))
        # settingdir = settingFile[:int(settingFile.rfind('/'))] # 저장될 폴더 경로
        if(settingFile.endswith(".json")): pass
        elif(settingFile==""): pass
        else: settingFile = settingFile + ".json"
        
        json_data = {}
        json_data["Run_Path"] = sourceFrame.sourcePath.get()
        json_data["Folder_name_List"] = folderNameFrame.folderList.get(0, END)
        json_data["Digit_Check_opt"] = chkDigit.chkVar.get()
        json_data["Digit_Start_idx"] = chkDigit.startIdxEntry.get()
        
        # print("설정파일 저장 경로 :", settingFile)
        with open(settingFile, "w", encoding="UTF-8") as saveFile:
            json.dump(json_data, saveFile, indent=4)


"""인터페이스 정의"""
# 파일 경로 프레임 생성
sourceFrame = SourceFrame() 
# print(f"파일 경로 : {sourceFrame.path.get()}")
# 옵션 프레임 생성
optFrame = OptionFrame(1) 
folderNameFrame = FolderNameFrame(optFrame.optVar.get())
# 문자열 자리수 확인 옵션
chkDigit = CheckDigitOption() 
runFrame = RunFrame()


root.mainloop()