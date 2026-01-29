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
    score: int = 0

    # Content
    blog_post: str = ""
    tweet_post: str = ""
    linkedin_post: str = ""

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
    def conduct_research_router(self):
        content_type = self.state.content_type

        if content_type == "blog":
            return "make_blog"
        elif content_type == "tweet":
            return "make_tweet"
        else:
            return "make_linkedin"

    @listen(or_("make_blog", "remake_blog"))
    def handle_make_blog(self):
        # 이 내부에서 blog post가 이전에 만들어진 적이 있는지 확인 후 예전 것을 AI에 보여주며 그걸 개선해 달라고 요청
        # 이전에 생성된 적이 없다면 그냥 생성 요청
        print("Making blog post...")        

    @listen(or_("make_tweet", "remake_tweet"))
    def handle_make_tweet(self):
        # 이 내부에서 tweet post가 이전에 만들어진 적이 있는지 확인 후 예전 것을 AI에 보여주며 그걸 개선해 달라고 요청
        # 이전에 생성된 적이 없다면 그냥 생성 요청
        print("Making tweet post...")        

    @listen(or_("make_linkedin", "remake_linkedin"))
    def handle_make_linkedin(self):
        # 이 내부에서 linkedin post가 이전에 만들어진 적이 있는지 확인 후 예전 것을 AI에 보여주며 그걸 개선해 달라고 요청
        # 이전에 생성된 적이 없다면 그냥 생성 요청
        print("Making linkedin post...")

    @listen(handle_make_blog)
    def check_seo(self):
        print("Checking Blog SEO")

    @listen(or_(handle_make_tweet, handle_make_linkedin))
    def check_virality(self):
        print("Checking Virality...")

    @router(or_(check_seo, check_virality))
    def score_router(self):
        content_type = self.state.content_type
        score = self.state.score

        if  score>= 8:
            return "check_passed"
        else:
            if content_type == "blog":
                return "remake_blog"
            elif content_type == "linkedin":
                return "remake_linkedin"
            else:
                return "remake_tweet"

    @listen("check_passed")
    def finalize_content(self):
        print("Finalizing content")



flow = ContentPipelineFlow()

# flow.kickoff(
#     inputs={
#         "content_type": "tweet",
#         "topic": "AI Dog Traing"
#     },
# )    

# 저장된 경로 임시 저장
temp_file_path = flow.plot()
temp_folder_path = os.path.dirname(temp_file_path)

# 타겟 폴더 (내 소스 코드가 있는 현재 위치)
current_working_dir = os.path.dirname(os.path.abspath(__file__))

# 임시 폴더 안의 파일들만 골라서 복사 (기존 파일 유지)
for filename in os.listdir(temp_folder_path):
    source_file = os.path.join(temp_folder_path, filename)
    target_file = os.path.join(current_working_dir, filename)
    
    # 파일인 경우에만 복사 (폴더 내의 하위 폴더까지 필요하다면 shutil.copy2 사용)
    if os.path.isfile(source_file):
        shutil.copy2(source_file, target_file)




    