from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from schema import AnswerQuestion 
from langchain_core.output_parsers import PydanticToolsParser,JsonOutputToolsParser
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv  import load_dotenv
import datetime

pydantic_parser=PydanticToolsParser(tools=[AnswerQuestion])
load_dotenv()
actor_prompt_template=ChatPromptTemplate.from_messages(
    [
       ( "system",
            """You are expert AI researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After the reflection, **list 1-3 search queries separately** for researching improvements. Do not include them inside the reflection.
""",
       ),
       MessagesPlaceholder(variable_name="messages"),
       ("system", "Answer the user's question above using the required format."),
    ]
).partial(time=lambda:datetime.datetime.now().isoformat(),
          )

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer"
)
llm = ChatOpenAI(model="gpt-4o")

first_responder_prompt_template=first_responder_prompt_template|llm.bind_tools(tools=[AnswerQuestion],tool_choice='AnswerQuestion')|pydantic_parser

response=first_responder_prompt_template.invoke({
    "messages":[HumanMessage("AI Agents taking over content creation"
                             )]
                             })
print(response)