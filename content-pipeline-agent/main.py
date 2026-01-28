from crewai.flow.flow import Flow, listen, start, router, and_, or_
import os
import shutil
from pydantic import BaseModel

os.environ["LANGCHAIN_TRACING_V2"] = "false"

class MyFirstFlowState(BaseModel):
    user_id: int = 1
    is_admin: bool = False

class MyFirstFlow(Flow[MyFirstFlowState]):
    @start()
    def first(self):
        print(self.state.user_id)
        print('hHello')
    
    @listen(first)
    def second(self):
        self.state.user_id = 3
        print('world')
    
    @listen(first)
    def third(self):
        print('!')
    
    @listen(and_(second, third))
    def final(self):        
        print(':)')

    @router(final)
    def route(self):
        if self.state.is_admin:
            return "even"
        else:
            return "odd"

    @listen('even')
    def handle_even(self):
        print("even")

    @listen('odd')
    def handle_odd(self):
        print("eidd")


flow = MyFirstFlow()

# 저장된 경로 임시 저장
temp_file_path = flow.plot()
temp_folder_path = os.path.dirname(temp_file_path)

# 2. 타겟 폴더 (내 소스 코드가 있는 현재 위치)
current_working_dir = os.path.dirname(os.path.abspath(__file__))

# 3. 임시 폴더 안의 파일들만 골라서 복사 (기존 파일 유지)
for filename in os.listdir(temp_folder_path):
    source_file = os.path.join(temp_folder_path, filename)
    target_file = os.path.join(current_working_dir, filename)
    
    # 파일인 경우에만 복사 (폴더 내의 하위 폴더까지 필요하다면 shutil.copy2 사용)
    if os.path.isfile(source_file):
        shutil.copy2(source_file, target_file)

flow.kickoff()




    