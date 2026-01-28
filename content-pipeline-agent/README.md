# CREWAI : CONTENT PIPELINE AGENT

##  Flows 사용
- Flow는 여러 개의 method를 가진 class
- decorator들을 사용하여 언제 method 를 실행할지 정하거나 event를 감지할 수 있음
- method가 끝나면 그 event를 감지해 다른 method를 실행할 수 있음
- router를 실행하거나, and, or 같은 조건문을 쓸수 있음
- or_ : 여러 개의 function을 listen 할 수 있는데, 그 중 하나가 끝나면 코드가 실행 됨
- and_ : or_ 와 동일하나 모두 끝나야만 코드가 실행 됨
- 프로그램의 흐름을 제어할 수 있게 해줌