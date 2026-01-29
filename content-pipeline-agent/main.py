import stat
from crewai.flow.flow import Flow, listen, start, router, and_, or_
import os
import shutil
from pydantic import BaseModel

os.environ["LANGCHAIN_TRACING_V2"] = "false"

class ContentPipelineState(BaseModel):
    # Inputs
    content_type: str = ""
    topic: str = ""

    # Internal
    max_length: int = 0

class ContentPipelineFlow(Flow[ContentPipelineState]):
    @start()
    def init_content_pipeline(self):
        if self.state.content_type not in ["tweet", "blog", "linkedin"]:
            raise ValueError("The content type is wrong")
        if self.state.topic == "":
            raise ValueError("The topic can't be blank")
    
        if self.state.content_type == "tweet":
            self.state.max_length = 150
        elif self.state.content_type == "blog":
            self.state.max_length = 800
        elif self.state.content_type == "linkedin":
            self.state.max_length = 500

    @listen(init_content_pipeline)
    def conduct_research(self):
        print("Researching...")
        return True

    @router(conduct_research)
    def router(self):
        content_type = self.state.content_type

        if content_type == "blog":
            return "make_blog"
        elif content_type == "tweet":
            return "make_tweet"
        else:
            return "make_linkedin_post"

    @listen("make_blog")
    def handle_make_blog(self):
        print("Making blog post...")        

    @listen("make_tweet")
    def handle_make_tweet(self):
        print("Making tweet post...")        

    @listen("make_linkedin_post")
    def handle_make_linkedin_post(self):
        print("Making linkedin post...")

    @listen(handle_make_blog)
    def check_seo(self):
        print("Checking Blog SEO")

    @listen(or_(handle_make_tweet, handle_make_linkedin_post))
    def check_virality(self):
        print("Checking Virality...")

    @listen(or_(check_seo, check_virality))
    def finalize_content(self):
        print("Finalizing content")



flow = ContentPipelineFlow()

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

# flow.kickoff(
#     inputs={
#         "content_type": "tweet",
#         "topic": "AI Dog Traing"
#     },
# )    


    